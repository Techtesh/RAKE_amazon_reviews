import json
import math
import requests
import uvicorn
import shutil
from bs4 import BeautifulSoup as bs
from rake_nltk import Rake
from nltk import tokenize
from operator import itemgetter
from nltk.corpus import stopwords
from fastapi import FastAPI, File, UploadFile
from typing import Optional
from pydantic import BaseModel
app = FastAPI()
class Item(BaseModel):
    Url: str
    Details: Optional[str] = None
    reviews: Optional[str] = None
    Features: Optional[str] = None
    
def check_sent(word, sentences):
    final = [all([w in x for w in word]) for x in sentences]
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

def json_to_text(json_file="src/example.json", txt_file="src/cache.txt"):
    f = open(json_file)
    raw_data = json.load(f)
    # print(raw_data[0].keys())
    with open(txt_file, "w", encoding="utf-8") as cf:
        for i, data_line in enumerate(raw_data[0]["reviews"]):
            if data_line["Verification"] == "Verified Purchase":
                cf.write(data_line["ReviewTitle"])
                cf.write("\n")

def try_rake(txt_file="src/cache.txt"):
    raw_data = open(txt_file, "r", encoding="utf-8").read().lower()
    total_sentences = tokenize.sent_tokenize(raw_data)
    total_sent_len = len(total_sentences)
    total_words = raw_data.split()
    total_word_length = len(total_words)
    tf_score = {}
    # calculating TF score
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y / int(total_word_length)) for x, y in tf_score.items())
    idf_score = {}
    # calculating IDF score
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1
    # calculate TF*IDF
    idf_score.update((x, math.log(int(total_sent_len) / y)) for x, y in idf_score.items())
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    return sorted(tf_idf_score.items(), key=itemgetter(1), reverse=True)

@app.get("/")
def return_home():
    return {"goto ": "/docs"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open("src/temp.json","wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    json_to_text(json_file="src/temp.json")
    vals = try_rake()[:10]
    op =[]
    for i,val in enumerate(vals):
        op.insert(i,val[0])
    return {"easy_review": op}

stop_words = set(stopwords.words('english'))
additional_stop_words = {'I', 'Very', 'Excellent', '&', 'Amazon','stars','-'}
stop_words = stop_words.union(additional_stop_words)
rake = Rake()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000,reload=True)
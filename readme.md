How to use this project 
1) ensure you have python v3.7.7 or higher
2) ensure youre in a venv
then run 
pip install 0r requirements.txt
uvicorn rake:app --reload 
navigate to localhost:8000/docs and use the api endpoint for uploadfile give it a correct json file with amazon page data and it will give you top 10 keywords from the review section 

TODOs:
rn it only accepts json add endpoints for (i) raw text (ii)csv
add custom filters for "Verified reviews" ,"star ratings","helpful-ness",etc.
add ability to auto genetrate the json file given an amazon url
extend this to other websites as well
write the ops side to host it on aws/azure/gcp/linode 

PS: this project is open for feature and pull requests 

- Your average barely alive dev
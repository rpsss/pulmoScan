First you have to install all the packages, you have two options : 

- You can install the packages one by one using the requirements.txt
- You can create a new conda env with the following command line : 
    conda env vreate -f environnements.yaml

Next, you have to train the model. You just have to execute all the notebook named image_classiffication

To start the application you have to open two terminals.

In the first one you have to write this : 
cd app/backend/
uvicorn api:app --reload

In the second terminal, you have to write this :
cd app/frontend/
streamlit run Home_page.py 

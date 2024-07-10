First you have to install all the packages, you have two options : 

- You can install the packages one by one using the requirements.txt
- You can create a new conda env with the following command line : 
    conda env create -f environnement.yaml

Next, you have to train the model. You just have to execute all the notebook named image_classiffication

To start the application you have to open a terminal and write this :

cd app/
docker build -t pulmoapp .
docker run -p 8000:8000 -p 8501:8501 pulmoapp
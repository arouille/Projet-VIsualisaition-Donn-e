from flask import Flask, render_template, request
import base64
from io import BytesIO
from flask import Flask
from matplotlib.figure import Figure
import numpy as np
import pandas
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
import os


app = Flask(__name__)

@app.route('/')

def index():
  app.config["CACHE_TYPE"] = "null"
  return render_template('index.html')
 

@app.route('/resultat',methods = ['GET'])
def resultat():
 app.config["CACHE_TYPE"] = "null"

 # Generate the figure *without using pyplot*.
 result=request.args
 a = float(result['longueur'])
 b = float(result['largeur'])

 iris=pandas.read_csv("iris.csv")
 x=iris.loc[:,"petal_length"]
 y=iris.loc[:,"petal_width"]
 lab=iris.loc[:,"species"]
 fig = plt.figure(figsize=(8,4))
 plt.scatter(x=a, y=b, c='black')
 setosa = plt.scatter(x[lab==0],y[lab==0],c='blue')
 versicolor = plt.scatter(x[lab==1],y[lab==1],c='orange')
 virginica = plt.scatter(x[lab==2],y[lab==2],c='red')
 plt.legend([setosa, versicolor, virginica], ['setosa', 'versicolor', 'virginica'])
 plt.xlabel("Longueur")
 plt.ylabel("Largeur")
 plt.grid()
 plt.savefig("static/graph.jpg")
 
 
 iris = datasets.load_iris()
 features = iris.data
 target = iris.target

 randomforest = RandomForestClassifier(random_state=0)
 model = randomforest.fit(features, target)

 observation = [[ 0, 0, a, b]]
 prediction = model.predict(observation)
 
 if prediction ==0:
    titre="Setosa"
    Description="C'est une plante vivace provenant d'une large gamme à travers la mer Arctique, le Canada, la Russie, l Asie du Nord-Est et le Japon. La plante a de hautes tiges ramifiées, des feuilles vert moyen et des fleurs violettes, bleu-violet, bleu-violet, bleues et lavande."
    image = "setosa.jpg"

 elif prediction ==1:
    titre="Versicolor"
    Description="L'iris versicolore est une espèce d'iris indigène de l'Amérique du Nord. Elle est commune en milieu humide comme dans les marais et aux rivages des cours d'eau. La fleur est grande, bleu-violet, rayée de jaune."
    image = "versicolor.jpg"

 elif prediction==2:
    titre="Virginica"
    Description="L'Iris virginica, au nom commun d'iris de Virginie, est une espèce de plante à fleurs vivace, originaire de l'est de l'Amérique du Nord. La couleur des pétales et des sépales peut varier du violet foncé au blanc rosé. Les sépales ont une touche de jaune à jaune-orange à la crête."
    image = "virginica.jpg"
 
 return render_template("resultat.html",titre=titre,Description=Description,image=image)
  


app.run(debug=True)

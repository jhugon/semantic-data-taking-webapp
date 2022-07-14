from flask import Flask
from flask import request
from flask import render_template
from db import DBInterface, RDFS
import urllib

app = Flask(__name__)
db = DBInterface("car-example.ttl")

@app.route("/")
def main():
    return render_template("main.html",db=db,urllib=urllib)

@app.route("/features")
def features():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    return render_template("features.html",feature=feature,featureName=featureName,featureURLEncoded=featureURLEncoded,urllib=urllib)

@app.route("/tableview")
def tableview():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    props, headings = db.getColumnHeadings(feature)
    stim_times, data = db.getData(feature)
    print(featureName,headings)
    print(stim_times)
    print(data)
    return render_template("tableview.html",featureName=featureName,featureURLEncoded=featureURLEncoded,headings=headings,stim_times=stim_times,data=data,zip=zip)

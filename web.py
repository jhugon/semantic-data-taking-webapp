from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from db import DBInterface, RDFS
import urllib
from datetime import datetime

app = Flask(__name__)
db = DBInterface("car-example.ttl")

USER="http://data-webapp.hugonlabs.com/test1/users/jhugon"

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

@app.route("/enterdata")
def enterdata():
    feature = request.args["feature"]
    status = None
    try:
        status = request.args["status"]
    except KeyError:
        pass
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    props, headings = db.getColumnHeadings(feature)
    propheadings = list(zip([str(prop) for prop in props],headings))
    return render_template("enterdata.html",featureName=featureName,feature=str(feature),propheadings=propheadings,status=status)

@app.route("/form/adddata",methods=["post"])
def form_adddata():
    form = dict(request.form)
    feature = form.pop("feature")
    db.enterData(feature,datetime.now().astimezone().replace(microsecond=0).isoformat(),USER,"",form)
    return redirect(url_for("enterdata")+"?feature="+feature+"&"+"status=success")

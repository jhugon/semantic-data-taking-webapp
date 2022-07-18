from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from db import DBInterface, DataValidationError, GetSubjectError, QUDT
import urllib
from datetime import datetime

app = Flask(__name__)
db = DBInterface()

USER="http://data-webapp.hugonlabs.com/test1/users/jhugon"

@app.route("/")
def main():
    status = None
    try:
        status = request.args["status"]
    except KeyError:
        pass
    reason = None
    try:
        reason = request.args["reason"]
    except KeyError:
        pass
    return render_template("main.html",db=db,urllib=urllib,status=status,reason=reason)

@app.route("/feature")
def features():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    return render_template("feature.html",feature=feature,featureName=featureName,featureURLEncoded=featureURLEncoded,urllib=urllib)

@app.route("/addproperty")
def addproperty():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    status = None
    try:
        status = request.args["status"]
    except KeyError:
        pass
    reason = None
    try:
        reason = request.args["reason"]
    except KeyError:
        pass
    return render_template("addproperty.html",feature=feature,featureName=featureName,featureURLEncoded=featureURLEncoded,urllib=urllib,quantity_kind_list=db.get_quantity_kind_list(),status=status,reason=reason)

@app.route("/selectpropertyunit")
def selectpropertyunit():
    feature = request.args["feature"]
    propname = request.args["propname"]
    comment = request.args["comment"]
    quantityKind = request.args["quantitykind"]
    quantityKindLabel = db.getLabel(quantityKind)
    featureName = db.getLabel(feature)
    units = db.get_units_for_quantity_kind(quantityKind)
    return render_template("selectpropertyunit.html",feature=feature,featureName=featureName,propname=propname,comment=comment,quantityKind=quantityKind,quantityKindLabel=quantityKindLabel,units=units)


@app.route("/tableview")
def tableview():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    props, headings = db.getColumnHeadings(feature)
    stim_times, data = db.getData(feature)
    return render_template("tableview.html",featureName=featureName,featureURLEncoded=featureURLEncoded,headings=headings,stim_times=stim_times,data=data,zip=zip)

@app.route("/enterdata")
def enterdata():
    feature = request.args["feature"]
    status = None
    try:
        status = request.args["status"]
    except KeyError:
        pass
    reason = None
    try:
        reason = request.args["reason"]
    except KeyError:
        pass
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    props, headings = db.getColumnHeadings(feature)
    propheadings = list(zip([str(prop) for prop in props],headings))
    return render_template("enterdata.html",featureName=featureName,feature=str(feature),propheadings=propheadings,status=status,reason=reason)

@app.route("/form/addfeature",methods=["post"])
def form_addfeature():
    featurename = request.form["featurename"]
    comment = request.form["comment"]
    try:
        db.addNewFeature(featurename,comment)
    except Exception as e:
        return redirect(url_for("main")+"?status=error&reason="+str(e))
    return redirect(url_for("main")+"?status=success")

@app.route("/form/addproperty",methods=["post"])
def form_addproperty():
    feature = request.form["feature"]
    propname = request.form["propname"]
    comment = request.form["comment"]
    quantityKind = request.form["quantitykind"]
    unit = request.form["unit"]
    try:
        db.addNewObservableProperty(propname,comment,feature,quantityKind,unit)
    except Exception as e:
        return redirect(url_for("addproperty")+"?feature="+feature+"&"+"status=error&reason="+str(e))
    return redirect(url_for("addproperty")+"?feature="+feature+"&"+"status=success")

@app.route("/form/adddata",methods=["post"])
def form_adddata():
    form = dict(request.form)
    feature = form.pop("feature")
    try:
        db.enterData(feature,datetime.now().astimezone().replace(microsecond=0).isoformat(),USER,"",form)
    except DataValidationError as e:
        return redirect(url_for("enterdata")+"?feature="+feature+"&"+"status=error&reason="+str(e))
    return redirect(url_for("enterdata")+"?feature="+feature+"&"+"status=success")

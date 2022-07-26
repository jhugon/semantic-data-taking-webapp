from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from db import DBInterface, DataValidationError, GetSubjectError, user_prefix, QUDT
import urllib
from datetime import datetime
import os.path
import logging

logging.basicConfig(level=logging.DEBUG)

from flask_login import LoginManager, current_user
from flask_simple_login import (
    auth,
    User,
    login_required,
)

app = Flask(__name__)

#### Configuration ###################

app.config["DB_STORE_PATH"] = "web-db-store.bdb"
app.config["LOGIN_USER_FILE_PATH"] = "userfile.txt"
#app.config["SERVER_NAME"] = "localhost" # doesn't seem to work with my proxy settings

app.config["SECRET_KEY"] = b"dummy"
app.config["SESSION_PROTECTION"] = "strong"
for key in sorted(app.config.keys()):
    if "SECRET" not in key:
        app.logger.info("{:30} = {}".format(key,app.config[key]))

#######################################

db = DBInterface(app.config["DB_STORE_PATH"])

app.register_blueprint(auth)
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

## Modify User to have a uri
@login_manager.user_loader
def load_user(user_id):
    u = User(user_id)
    u.uri = os.path.join(user_prefix,user_id)
    return u


@app.route("/")
@login_required
def index():
    app.logger.debug(request.headers)
    app.logger.debug(request.host)
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
    return render_template("index.html",db=db,urllib=urllib,status=status,reason=reason)

@app.route("/feature")
@login_required
def features():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    return render_template("feature.html",feature=feature,featureName=featureName,featureURLEncoded=featureURLEncoded,urllib=urllib)

@app.route("/addproperty")
@login_required
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
@login_required
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
@login_required
def tableview():
    feature = request.args["feature"]
    featureName = db.getLabel(feature)
    featureURLEncoded = urllib.parse.quote(feature, safe="")
    props, headings = db.getColumnHeadings(feature)
    stim_times, data = db.getData(feature)
    return render_template("tableview.html",featureName=featureName,featureURLEncoded=featureURLEncoded,headings=headings,stim_times=stim_times,data=data,zip=zip)

@app.route("/enterdata")
@login_required
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
@login_required
def form_addfeature():
    featurename = request.form["featurename"]
    comment = request.form["comment"]
    try:
        db.addNewFeature(featurename,comment)
    except Exception as e:
        return redirect(url_for("index")+"?status=error&reason="+str(e))
    return redirect(url_for("index")+"?status=success")

@app.route("/form/addproperty",methods=["post"])
@login_required
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
@login_required
def form_adddata():
    form = dict(request.form)
    feature = form.pop("feature")
    user_uri = current_user.uri
    try:
        db.enterData(feature,datetime.now().astimezone().replace(microsecond=0).isoformat(),user_uri,"",form)
    except DataValidationError as e:
        return redirect(url_for("enterdata")+"?feature="+feature+"&"+"status=error&reason="+str(e))
    return redirect(url_for("enterdata")+"?feature="+feature+"&"+"status=success")

if __name__ == "__main__":
    app.run()

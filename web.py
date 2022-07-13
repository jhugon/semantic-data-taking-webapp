from flask import Flask
from flask import render_template
from db import DBInterface

app = Flask(__name__)
db = DBInterface("car-example.ttl")

@app.route("/")
def main():
    return render_template("main.html",db=db)

@app.route("/features/<featureName>")
def features(featureName):
    return render_template("features.html",featureName=featureName)

@app.route("/features/<featureName>/tableview")
def tableview(featureName):
    props, headings = db.getColumnHeadings(featureName)
    return render_template("tableview.html",db=db,featureName=featureName,headings=headings)

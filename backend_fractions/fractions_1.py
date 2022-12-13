from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
app = Flask(__name__)

CORS(app)
#multiplying

app.config["SECRET_KEY"]="ibhbds8gs"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///fractions.sqlite3'


db=SQLAlchemy(app)

class familys(db.Model):  #name of table
    id=db.Column(db.Integer,primary_key=True)
    family=db.Column(db.String(200))

class images(db.Model):  #name of table
    id=db.Column(db.Integer,primary_key=True)
    img=db.Column(db.String(2000))
    family_id=db.Column(db.Integer)

class myFractions(db.Model):  #name of table
    id=db.Column(db.Integer,primary_key=True)
    counter=db.Column(db.Integer)
    denomintor=db.Column(db.Integer)
    family_id=db.Column(db.String(200))
    name=db.Column(db.String(200))
    name2=db.Column(db.String(200))
    img_id=db.Column(db.Integer)
    is_int=db.Column(db.Integer)


db.create_all()

@app.route('/all',methods=["GET","POST"])
def index():
    dataFamilys=familys.query.all()
    arrayFamilys=[]
    for family in dataFamilys:
        a1=family.__dict__
        # the family name = Hebrew.. what can i do? 
        arrayFamilys.append({"id":a1["id"],"family":a1["family"]})
    dataImages=images.query.all()
    arrayImages=[]
    for image in dataImages:
        a1=image.__dict__
        arrayImages.append({"id":a1["id"],"img":a1["img"],"family_id":a1["family_id"]})
    dataFractions=myFractions.query.all()
    arrayFractions=[]
    for fraction in dataFractions:
        a1=fraction.__dict__
        arrayFractions.append({"id":a1["id"],"counter":a1["counter"],"denomintor":a1["denomintor"],"family_id":a1["family_id"],"name":a1["name"],"name2":a1["name2"],"img_id":a1["img_id"],"is_int":a1["is_int"]})
    
    return({"arrayFamilys":arrayFamilys,"arrayImages":arrayImages,"arrayFractions":arrayFractions,"random":None})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int(os.environ.get('PORT',5001)))
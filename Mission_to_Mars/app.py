from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

#create an instance for Flask
app=Flask(__name__)

#set up Mongo connection 
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo= PyMongo(app)

@app.route("/")
def index():

    mars_dic=mongo.db.mars_dic.find_one()
    return render_template("index.html",mars=mars_dic)


@app.route("/scrape")
def scrape():

    mars_dic=mongo.db.mars_dic
    mars_data=scrape_mars.scrape()
    mars_dic.update({},mars_data,upsert=True)
    return redirect("/",code=302)

if __name__=="__main__":
    app.run(debug=True)
    
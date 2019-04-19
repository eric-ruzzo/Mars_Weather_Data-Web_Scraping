from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Setup connection to mongodb using Pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.insert_one()

    # Return template and data
    return render_template("index.html", mars=mars_info)


# Create route
@app.route("/scrape")
def scrape():

    # Run scrape_info function from scrape_mars
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)










#@app.route("/scrape")



#if __name__=="__main__":
#    scrape()
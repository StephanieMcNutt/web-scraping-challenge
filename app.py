from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    #Find one record of data from the mongo database
    mars_scraped = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars_scraped=mars_scraped)

@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_scraped = scrape.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_scraped, upsert=True)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
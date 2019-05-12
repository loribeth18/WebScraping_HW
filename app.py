from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdb")

# Initialize PyMongo to work with MongoDBs
# conn = 'mongodb://localhost:27017/marsdb'
# client = pymongo.MongoClient(conn)

# Define database and collection

# db = mongo.marsdb
#collection = mongo.db.marsdb.items

@app.route('/')
def index():
    surfing = mongo.db.items.find_one()
    return render_template('index.html', surfing=surfing)


@app.route('/scrape')
def scrape():
    data = scrape_mars2.scrape()
    mongo.db.items.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)




if __name__ == "__main__":
    app.run(debug=True)

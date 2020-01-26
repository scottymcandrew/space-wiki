import os

import pymongo
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'space_definitions'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/space')
def get_definitions():
    # Grab the latest 5 definitions for display on the main page. Filter to only print ones marked as top (most votes)
    coll = mongo.db.definitions.find({'top_definition': True}).sort("date", pymongo.DESCENDING).limit(5)
    return render_template('space.html',
                           definitions=coll)


@app.route('/add_vote/<def_id>', methods=['POST'])
def add_vote(def_id):
    definitions = mongo.db.definitions
    definitions.update_one({'_id': ObjectId(def_id)},
                           {
                               '$inc': {'votes': 1}
                           })
    return redirect(url_for('get_definitions'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

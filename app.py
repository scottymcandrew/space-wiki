import os
import datetime
import pymongo
from flask import Flask, flash, render_template, redirect, request, url_for, request
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
    # **************************************************
    # ***** NEED TO ADD LOGIC TO CHECK TOP DEFINITION!!!
    # **************************************************
    definitions.update_one({'_id': ObjectId(def_id)},
                           {
                               '$inc': {'votes': 1}
                           })
    return redirect(url_for('get_definitions'))


@app.route('/add_definition')
def add_definition():
    return render_template('add_definition.html')


@app.route('/insert_definition', methods=['POST'])
def insert_definition():
    definitions = mongo.db.definitions
    # Take data from HTML form
    data = request.form.to_dict()
    # Add in the current date / time and initialise vote count
    data['date'] = datetime.datetime.now()
    data['votes'] = 1
    # Check MongoDB Database if definition exists. If unique, sets 'top_definition' to True
    query = {'definition_name': data['definition_name']}
    cursor = definitions.find(query)
    # Need to use count() function of cursor to get the length
    cursor_length = cursor.count()
    # If no matches were found for the same definition name, it will be the top definition
    if cursor_length == 0:
        data['top_definition'] = True
        # flash('Congratulations, you are as smart as Spock, this is the first definition!')
    else:
        data['top_definition'] = False
        # flash('Uh oh, you were not the first to add this definition, try to get some votes!')
    definitions.insert_one(data)
    return redirect(url_for('get_definitions'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

import os
import datetime
import pymongo
from flask import Flask, session, flash, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'space_definitions'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = 'supersecretk3y'

mongo = PyMongo(app)


@app.route('/')
@app.route('/space')
def get_definitions():
    # Grab the latest 10 definitions for display on the main page. Filter to only print ones marked as top (most votes)
    coll = mongo.db.definitions.find({'top_definition': True}).sort("date", pymongo.DESCENDING).limit(10)
    return render_template('space.html',
                           definitions=coll)


@app.route('/add_vote/<def_id>', methods=['POST'])
def add_vote(def_id):
    definitions = mongo.db.definitions
    definitions.update_one({'_id': ObjectId(def_id)},
                           {
                               '$inc': {'votes': 1}
                           })
    # Get definition entry
    definition_dict = definitions.find_one({'_id': ObjectId(def_id)})
    # Check MongoDB Database if definition exists in more than one record
    query = {'definition_name': definition_dict['definition_name']}
    cursor = definitions.find(query)
    # Get the cursor count
    if cursor.count() > 1:
        # Get the definition_name
        definition_dict_name = definition_dict['definition_name']
        # Get the current top definition
        current_top = definitions.find_one({'$and':
            [
                {'top_definition': True},
                {'definition_name': definition_dict_name}
            ]
        })
        # Get the entry with the most votes after this vote. If there is a tie, oldest definition wins
        cursor_top = definitions.find({'definition_name': definition_dict_name}).sort(
            [('votes', -1), ('date', 1)]).limit(1)
        # Convert cursor to dict. Whilst using a for loop it will only be a single entry due to limit(1) above
        calculated_top = {}
        for c in cursor_top:
            calculated_top = c
        # If the entry voted on is different to the current top, set new top definition
        if current_top['_id'] != calculated_top['_id']:
            definitions.update_one({'_id': current_top['_id']},
                                   {'$set':
                                       {
                                           'top_definition': False
                                       }})
            definitions.update_one({'_id': calculated_top['_id']},
                                   {'$set':
                                       {
                                           'top_definition': True
                                       }})

    flash('Thank you for voting!')
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
        flash('Congratulations, you are as smart as Spock, this is the first definition!')
    else:
        data['top_definition'] = False
        flash('Uh oh, you were not the first to add this definition, try to get some votes!')
    definitions.insert_one(data)
    return redirect(url_for('get_definitions'))


@app.route('/edit_definition/<def_id>')
def edit_definition(def_id):
    definition = mongo.db.definitions.find_one({"_id": ObjectId(def_id)})
    return render_template('edit_definition.html', definition=definition)


@app.route('/update_definition', methods=['POST'])
def update_definition():
    definitions = mongo.db.definitions
    # Take data from HTML form
    data = request.form.to_dict()
    definitions.update_one({'_id': ObjectId(data['def_id'])},
                           {'$set': {
                               'definition': data['definition'],
                               'editor': data['editor'],
                               'updated_when': datetime.datetime.now()
                           }})
    flash('Your edit has been accepted!')
    return redirect(url_for('get_definitions'))


@app.route('/delete_definition/<def_id>', methods=['POST'])
def delete_definition(def_id):
    definitions = mongo.db.definitions
    definitions.delete_one({'_id': ObjectId(def_id)})
    flash('I hope you meant to delete that!')
    return redirect(url_for('get_definitions'))


@app.route('/search', methods=['POST'])
def search_definitions():
    definitions = mongo.db.definitions
    data = request.form.to_dict()
    # A dictionary is returned above, place the value into variable
    search_text = data['definition_search']
    # For the below search syntax to work, the MongoDB collection needs to have text indexes set for both keys
    # this allows for case-insensitive searching - https://docs.mongodb.com/manual/core/index-text/#create-text-index
    # The single search will look in both definitions and definition names
    return render_template('search_results.html',
                           definition_name_hits=definitions.find({"$text": {"$search": search_text}}))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

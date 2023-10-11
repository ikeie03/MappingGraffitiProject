from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from logic import get_x_coordinate, get_y_coordinate
import os
from gridfs import GridFS

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder="templates", # where flask looks for templates
    static_folder="static" # where flask looks for static JS, CSS files
)

client = MongoClient('mongodb://localhost:27017')
graffiti_db = client.get_database('graffiti')
images_collection = graffiti_db['images']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/map')
def map():
     #extract coordinates from mongodb database
     all_markers = list(images_collection.find())
     coordinates = [(marker['x_coordinate'], marker['y_coordinate']) for marker in all_markers]
     artists = [marker['artist'] for marker in all_markers]

     # render the map with the markers added
     return render_template('map.html', coordinates=coordinates, artists=artists)

@app.route('/upload')
def upload():
     return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
     artist = request.form['artist']
     description = request.form['description']
     file = request.files['file']
     target = os.path.join(APP_ROOT, 'images/')
     if not os.path.isdir(target):
          os.mkdir(target)
     
     filename = file.filename
     destination = "/".join([target, filename])
     file.save(destination)

     x_coordinate = get_x_coordinate(destination)
     y_coordinate = get_y_coordinate(destination)
     images_collection.insert_one({'artist': artist,
                                   'description': description,
                                   'x_coordinate': x_coordinate,
                                   'y_coordinate': y_coordinate,
                                   'image': filename})
     
     return render_template("index.html") 
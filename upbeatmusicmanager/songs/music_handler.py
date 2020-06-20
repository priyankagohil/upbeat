#songs/music_handler.py

import os
from flask import url_for,current_app

def add_music(music_upload,title):

    filename = music_upload.filename
    filepath = os.path.join(current_app.root_path,'static\music',filename)

    music_upload.save(filepath)

    return filename

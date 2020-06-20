# core/views.py

from flask import render_template,request,Blueprint
from upbeatmusicmanager.models import Music

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    songs = Music.query.order_by(Music.title.asc()).paginate(page=page, per_page=10)

    return render_template('index.html')

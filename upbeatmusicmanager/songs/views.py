# blog_posts/views.py
import os
from flask import render_template,url_for,flash,request,redirect,Blueprint, current_app
from flask_login import current_user,login_required
from upbeatmusicmanager import db
from upbeatmusicmanager.models import Music
from upbeatmusicmanager.songs.forms import MusicForm, SearchForm
from werkzeug.utils import secure_filename
import flask_whooshalchemy as wa
from whoosh.analysis import StemmingAnalyzer



songs = Blueprint('songs',__name__)

######################################################
# songs > blog_posts  # album > author.username
# song > blog_post    # singer > date
# s > post            #   > text
#####################################################


# CREATE
@songs.route('/upload',methods=['GET','POST'])
@login_required
def upload_song():
    form = MusicForm()

    if form.validate_on_submit():
        file_name = form.upload.data.filename
        file_path = os.path.join(current_app.root_path, 'static\music',
                    file_name)
        form.upload.data.save(file_path)

        song = Music(title=form.title.data,
                    album=form.album.data,
                    singer=form.singer.data,
                    song=file_name,
                    user_id=current_user.id )
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('core.index'))

    return render_template('upload.html',form=form)


# songs (VIEW)
@songs.route('/<int:song_id>')
def song(song_id):
    song = Music.query.get_or_404(song_id)
    return render_template('song.html',title=song.title,
                            album=song.album,
                            singer=song.singer,
                            song=song )


#DELETE
@songs.route('/<int:song_id>/delete',methods=['GET','POST'])
@login_required
def delete_song(song_id):

    song = Music.query.get_or_404(song_id)
    if song.user != current_user:
        abort(403)

    db.session.delete(song)
    db.session.commit()

    return redirect(url_for('core.index'))


#SEARCH
@songs.route('/search', methods=['GET', 'POST'])
@login_required
def search_song():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        query = request.args.get(form.search.data)
        results = Music.query.whoosh_search(query).all()
        return render_template('search.html', songs=results, form=form)
    return render_template('search.html', form = form)

@songs.route('/search/<query>', methods=['GET', 'POST'])
@login_required
def search_results(query):
    form = SearchForm()
    results = Music.query.whoosh_search(query).all()
    return render_template('search.html', songs=results, form=form)

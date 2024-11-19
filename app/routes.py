from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from . import db
from .models import Person

UPLOAD_FOLDER = 'app/static/uploads'

def configure_routes(app):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if request.method == 'POST':
            name = request.form['name']
            photo = request.files['photo']
            document = request.files['document']

            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo.filename))
            document_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(document.filename))
            photo.save(photo_path)
            document.save(document_path)

            new_person = Person(name=name, photo=photo.filename, document=document.filename)
            db.session.add(new_person)
            db.session.commit()

            return redirect(url_for('index'))

        persons = Person.query.all()
        return render_template('index.html', persons=persons)

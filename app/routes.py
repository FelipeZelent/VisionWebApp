from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import requests  # Para enviar arquivos para as VMs remotas
from . import db
from .models import Person

# URLs das máquinas virtuais
VM_WINDOWS_URL = 'http://191.232.250.221:5000/upload'
VM_LINUX_URL = 'http://191.232.255.242:5000/upload'

def configure_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            name = request.form['name']
            photo = request.files['photo']
            document = request.files['document']

            # Salvar a foto na VM Windows
            photo_files = {'file': (secure_filename(photo.filename), photo.stream, photo.mimetype)}
            photo_response = requests.post(VM_WINDOWS_URL, files=photo_files)
            if photo_response.status_code != 200:
                return f"Erro ao enviar foto para a VM Windows: {photo_response.text}", 500
            
            # Salvar o documento na VM Linux
            document_files = {'file': (secure_filename(document.filename), document.stream, document.mimetype)}
            document_response = requests.post(VM_LINUX_URL, files=document_files)
            if document_response.status_code != 200:
                return f"Erro ao enviar documento para a VM Linux: {document_response.text}", 500

            # Adicionar os dados no banco de dados
            new_person = Person(
                name=name,
                photo=photo.filename,
                document=document.filename
            )
            db.session.add(new_person)
            db.session.commit()

            return redirect(url_for('index'))

        persons = Person.query.all()
        return render_template('index.html', persons=persons)

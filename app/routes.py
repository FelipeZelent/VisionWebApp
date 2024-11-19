from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import requests  # Para enviar arquivos para as VMs remotas e o Serviço Cognitivo
from . import db
from .models import Person

# URLs das máquinas virtuais
VM_WINDOWS_URL = 'http://191.232.250.221:5000/upload'
VM_LINUX_URL = 'http://191.232.255.242:5000/upload'

# Configuração do Serviço Cognitivo
COGNITIVE_ENDPOINT = "https://brazilsouth.api.cognitive.microsoft.com/"
COGNITIVE_KEY = "28f4d2be23214b75a36985ff80474373"

def analyze_image(image_path):
    analyze_url = f"{COGNITIVE_ENDPOINT}vision/v3.2/analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": COGNITIVE_KEY,
        "Content-Type": "application/octet-stream"
    }
    params = {"visualFeatures": "Description"} 

    with open(image_path, "rb") as image_file:
        response = requests.post(analyze_url, headers=headers, params=params, data=image_file)
        response.raise_for_status()
        return response.json()

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            name = request.form['name']
            photo = request.files['photo']
            document = request.files['document']

            # Salvar a foto na VM Windows
            try:
                photo_files = {'file': (secure_filename(photo.filename), photo.stream, photo.mimetype)}
                photo_response = requests.post(VM_WINDOWS_URL, files=photo_files)
                photo_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return f"Erro ao enviar foto para a VM Windows: {str(e)}", 500
            
            # Salvar o documento na VM Linux
            try:
                document_files = {'file': (secure_filename(document.filename), document.stream, document.mimetype)}
                document_response = requests.post(VM_LINUX_URL, files=document_files)
                document_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return f"Erro ao enviar documento para a VM Linux: {str(e)}", 500

            # Realizar a análise da imagem usando o Serviço Cognitivo
            try:
                photo_path = os.path.join('app/static/uploads', secure_filename(photo.filename))
                photo.save(photo_path)  # Salva temporariamente no servidor
                analysis_result = analyze_image(photo_path)
                description = analysis_result.get("description", {}).get("captions", [{}])[0].get("text", "Nenhuma descrição encontrada.")
            except Exception as e:
                description = f"Erro na análise da imagem: {str(e)}"

            # Adicionar os dados no banco de dados
            new_person = Person(
                name=name,
                photo=photo.filename,
                document=document.filename,
                description=description  # Salva a descrição no banco
            )
            db.session.add(new_person)
            db.session.commit()

            return redirect(url_for('index'))

        persons = Person.query.all()
        return render_template('index.html', persons=persons)

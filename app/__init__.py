from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mssql+pyodbc://adminflask:Admin@123456@sqlserver-rm1142282365.database.windows.net:1433/VisionWebApp?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        return "Conexão com o banco de dados configurada!"

    with app.app_context():
        db.create_all()

    return app
    
    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)
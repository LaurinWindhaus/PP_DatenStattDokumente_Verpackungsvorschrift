from flask import Flask
from core.database import init_db
from api import document_api, image_api

init_db()

app = Flask(__name__, static_url_path='/dsd/static')


app.register_blueprint(document_api.app)
app.register_blueprint(image_api.app)

if __name__ == "__main__":
    app.run(debug=True)
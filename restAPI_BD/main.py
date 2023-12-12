from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:02112001@localhost/rest_api_db'
db.init_app(app)


swagger_url = '/swagger'
api_url = '/static/swagger.yaml'
swagger_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url
)
app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)
app.register_blueprint(request_api.get_blueprint())


if __name__ == '__main__':
    app.run(debug=True)
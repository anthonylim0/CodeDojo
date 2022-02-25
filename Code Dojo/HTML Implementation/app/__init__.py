from flask import Flask
from app.middleware import PrefixMiddleware

application = Flask(__name__)

application.wsgi_app = PrefixMiddleware(application.wsgi_app, voc=False)


from app import routes
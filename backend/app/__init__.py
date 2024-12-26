from flask import Flask
from app.routes import nlp, integration, template_generator, test
from app.utils.config import configure_app, initialize_firebase
from app.routes.settings import settings_bp

def create_app():
    app = Flask(__name__)
    configure_app(app)

    # Initialize Firebase
    initialize_firebase()

    # Register blueprints
    app.register_blueprint(nlp.bp)
    app.register_blueprint(integration.bp)
    app.register_blueprint(template_generator.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(settings_bp)

    @app.route("/")
    def index():
        return "Welcome to the Intelligent Business Template API"

    return app
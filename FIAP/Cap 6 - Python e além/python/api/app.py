from flask import Flask
from .routes import bp as api_bp

def create_app():
    """Factory para criar a aplicação Flask."""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

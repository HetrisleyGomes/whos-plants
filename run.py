from flask import Flask
from src.main.routes.routes import main_bp

app = Flask(__name__, template_folder="src/main/templates", static_folder="src/main/statics")
app.config['SECRET_KEY'] = 'chave_secreta'

if __name__ == "__main__":
    app.register_blueprint(main_bp)
    app.run(host="0.0.0.0", port=3000, debug=True)

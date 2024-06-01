from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_migrate import Migrate

from core.config import Config


# regiser extensions
db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
bootstrap = Bootstrap5()
migrate = Migrate()


def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config)

    # initialize extensions
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

    # error handling in blueprints didnt work as expected hence handled here

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    # # Register error handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, server_error)

    # # register blueprints
    from core.auth.views import auth as AuthBlueprint
    from core.main.views import main as MainBlueprint
    from core.users.views import users as UsersBlueprint
    from core.blog.views import blog as BlogBlueprint

    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(MainBlueprint)
    app.register_blueprint(UsersBlueprint)
    app.register_blueprint(BlogBlueprint)

    return app

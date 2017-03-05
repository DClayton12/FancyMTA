import logging

from flask import current_app, Flask, redirect, url_for

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    if config_overrides:
        app.config.update(config_overrides)

    with app.app_context():
        model = get_model()
        model.init_app(app)

    from .crud import crud
    app.register_blueprint(crud, url_prefix='/fancy-mta')

    # Default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'datastore':
        from . import model_datastore
        model = model_datastore
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please specify datastore, cloudsql, or mongodb")

    return model

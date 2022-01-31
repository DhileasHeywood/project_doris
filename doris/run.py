import os
from flask import Flask, redirect, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev"
        #ELASTICSEARCH_URL = "http://localhost:9200/"
        #DATABASE= Something goes here, but I'm not sure what yet.
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import application
    app.register_blueprint(application.bp)

    return app


app = create_app()


@app.route('/')
def index():
    return redirect(url_for('application.index'))


if __name__ == "__main__":
    app.run()

import os
from flask import Flask
import db


def create_app(test_config=None):
    # 创建、编译app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'my-easy-pic-bed.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    db.init_app(app)

    return app

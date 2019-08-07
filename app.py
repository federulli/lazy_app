from flask import Flask
import os
from flask_graphql import GraphQLView
from tasks import celery_app, test_task
from models import S, create_tables
from schemas import schema

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = f'redis://{REDIS_HOST}:6379'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{REDIS_HOST}:6379'


app.debug = True

celery_app.conf.update(app.config)


@app.route('/')
def hello():
    test_task.delay()
    return 'Hello World! I have been seen'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    S.remove()


if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_graphql import GraphQLView

from models import S
from schemas import schema

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'


app.debug = True

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

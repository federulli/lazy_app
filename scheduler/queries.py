import os
from gql import gql, Client as gql_client
from gql.transport.requests import RequestsHTTPTransport


HOST = os.environ.get('LAZY_APP_HOST', 'backend')
PORT = os.environ.get('LAZY_APP_PORT', '5000')


client = gql_client(
    transport=RequestsHTTPTransport(
            url=f'http://{HOST}:{PORT}/graphql',
            use_json=True
        ),
    fetch_schema_from_transport=True,
)

SEARCH_MOVIES_MUTATION = gql("""mutation {searchMovies{msg}}""")
SEARCH_EPISODES_MUTATION = gql("""mutation {searchChapters{msg}}""")
DELETE_COMPLETED_TORRENTS_MUTATION = gql("""mutation {deleteCompleted{msg}}""")
RELOAD_CHAPTER_COUNT_MUTATION = gql("""mutation {reloadChapterCount{msg}}""")
DELETE_ALL_TORRENTS_MUTATION = gql("""mutation {deleteAllTorrents{msg}}""")
import json
import os

import pulsar
import sad_libraries.redis as sad_redis
import sad_libraries.tmdb as sad_tmdb
from flask import (
    Blueprint, render_template, request, current_app as app, redirect
)

import sad_ui.constants as sad_constants

bp = Blueprint('app', __name__, url_prefix='/')


@bp.route('/')
def index():
    search_keys = sad_redis.get_from_cache(key=sad_constants.SAD_SEARCH_KEYS)
    search_results = sad_redis.get_from_cache(key=sad_constants.SAD_RESULTS)
    tmdb_config = sad_tmdb.get_config()
    return render_template('app/list.html', search_keys=search_keys, search_results=search_results,
                           tmdb_config=tmdb_config)


@bp.route('/health')
def health():
    required_configs = ['TMDB_API_ACCESS_TOKEN', 'PULSAR_SERVER', 'PULSAR_SEARCH_TOPIC', 'PULSAR_DESTROY_TOPIC']
    for config in required_configs:
        try:
            os.environ[config]  # Raises an exception if the config is not set
        except KeyError as e:
            app.logger.error(f"Config '{config}' is not set")
            raise e
    version = os.getenv('VERSION')
    return render_template('app/health.html', version=version)


@bp.route('/request-search')
def request_search():
    search_key = request.args.get('search_key', default=None, type=str)
    app.logger.debug(f"Received search request for '{search_key}'")
    # Create a Pulsar client
    client = pulsar.Client(f'pulsar://{os.environ["PULSAR_SERVER"]}')

    # Create a producer on the topic 'plex-search'
    producer = client.create_producer(os.environ['PULSAR_SEARCH_TOPIC'])

    # Create a message
    message = [search_key]
    message_json = json.dumps(message).encode('utf-8')

    # Send the message
    producer.send(message_json)

    # Close the producer and client to free up resources
    producer.close()
    client.close()
    return "OK"


@bp.route('/request_delete')
def request_delete():
    delete_key = request.args.get('delete_key', default=None, type=str)
    app.logger.info(f"Received delete request for '{delete_key}'")
    # Create a Pulsar client
    client = pulsar.Client(f'pulsar://{os.environ["PULSAR_SERVER"]}')

    # Create a producer on the topic 'plex-search'
    producer = client.create_producer(os.environ['PULSAR_DESTROY_TOPIC'])

    # Create a message
    message = {"plexKey": delete_key}
    message_json = json.dumps(message).encode('utf-8')

    # Send the message
    producer.send(message_json)
    app.logger.info(f"Sent delete request for '{delete_key}'")

    # Close the producer and client to free up resources
    producer.close()
    client.close()
    return "OK"

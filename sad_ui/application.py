from flask import (
    Blueprint, render_template
)
import sad_libraries.redis as sad_redis
import sad_ui.constants as sad_constants
import sad_libraries.tmdb as sad_tmdb
import logging

bp = Blueprint('app', __name__, url_prefix='/')


@bp.route('/')
def index():
    search_keys = sad_redis.get_from_cache(key=sad_constants.SAD_SEARCH_KEYS)
    search_results = sad_redis.get_from_cache(key=sad_constants.SAD_RESULTS)
    tmdb_config = sad_tmdb.get_config()
    return render_template('app/list.html', search_keys=search_keys, search_results=search_results, tmdb_config=tmdb_config)

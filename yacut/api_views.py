from flask import jsonify, request

from http import HTTPStatus

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

SHORT_NOT_FOUND = 'Указанный id не найден'
NO_BODY = 'Отсутствует тело запроса'
EMPTY_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(NO_BODY)
    if not data.get('url'):
        raise InvalidAPIUsage(EMPTY_FIELD)
    try:
        return jsonify(
            URLMap.create(data['url'], data.get('custom_id'), True).to_dict()
        ), HTTPStatus.CREATED
    except (URLMap.ObjectCreateError, URLMap.ShortGenerateError) as exc:
        raise InvalidAPIUsage(str(exc))


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
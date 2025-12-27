from flask import jsonify, request

from . import app
from .error_handlers import CreateLinkException, InvalidAPIUsage
from .models import URLMap
from .utils import create_short_link


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({
            'message': 'Отсутствует тело запроса'
        }), 400

    if not data:
        return jsonify({
            'message': 'Отсутствует тело запроса'
        }), 400

    try:
        result = create_short_link(data)
        return jsonify(result), 201
    except CreateLinkException as error:
        return jsonify({
            'message': str(error)
        }), 400


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=url_map.original), 200
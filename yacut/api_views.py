import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage

from settings import STRING_LENGTH
from utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if not short_id:
        data['custom_id'] = get_unique_short_id()
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    if len(data['custom_id']) > STRING_LENGTH:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    if not re.match(r'^[A-Za-z0-9]+$', data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)

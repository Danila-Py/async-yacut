import random
from re import match

from . import db
from .constants import (
    ALLOWED_AUTO_CHARS, ALLOWED_USER_CHARS,
    AUTO_LINK_LENGJT, SHORT_MAX_LEN
)
from .error_handlers import CreateLinkException
from .models import URLMap


def get_unique_short_id():
    short_link = ''.join(
        random.choice(ALLOWED_AUTO_CHARS) for i in range(AUTO_LINK_LENGJT)
    )
    if URLMap.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link


def validation_data(data):
    if data is None:
        raise CreateLinkException('Отсутствует тело запроса')
    if 'url' not in data:
        raise CreateLinkException('\"url\" является обязательным полем!')
    short_id = data.get('custom_id')
    if not short_id:
        data['custom_id'] = get_unique_short_id()
    elif URLMap.query.filter_by(short=short_id).first():
        raise CreateLinkException(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    elif not match(
        ALLOWED_USER_CHARS, short_id
    ) or len(short_id) > SHORT_MAX_LEN:
        raise CreateLinkException(
            'Указано недопустимое имя для короткой ссылки'
        )
    return data


def create_short_link(data):
    validation_data(data)
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return url_map.to_dict()
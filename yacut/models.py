from datetime import datetime
from re import search
import random

from flask import url_for

from . import db

from .constants import (
    ALLOWED_AUTO_CHARS,
    ORIGINAL_LINK_LENGJT,
    SHORT_URL_VIEW,
    URL_MAX_LEN,
    SHORT_MAX_LEN,
    RESERVED_SHORTS,
    REGEX,
    ADD_TRIES,
    AUTO_LINK_LENGJT
)


LONG_URL = 'Слишком длинная ссылка!'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_GENERATE_ERROR = 'Не удалось подобрать уникальный id. Попыток - {}'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_LENGJT), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LEN), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    class ObjectCreateError(Exception):
        """Класс исключений, возникающих при создании записи."""

    class ShortGenerateError(Exception):
        """Класс исключений, возникающих при генерации короткого id."""

    @staticmethod
    def generate_short():
        for _ in range(ADD_TRIES):
            short = ''.join(random.choices(
                ALLOWED_AUTO_CHARS,
                k=AUTO_LINK_LENGJT
            ))
            if URLMap.get(short) is None:
                return short
        raise URLMap.ShortGenerateError(SHORT_GENERATE_ERROR.format(ADD_TRIES))

    def create(original, short=None, not_validated=False):
        if not_validated and len(original) > URL_MAX_LEN:
            raise URLMap.ObjectCreateError(LONG_URL)
        if not short:
            short = URLMap.generate_short()
        else:
            if (not_validated and len(short) > SHORT_MAX_LEN
                    or not search(REGEX, short)):
                raise URLMap.ObjectCreateError(INVALID_SHORT)
            if URLMap.get(short) or short in RESERVED_SHORTS:
                raise URLMap.ObjectCreateError(SHORT_EXISTS)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    def get_short_url(self):
        return url_for(SHORT_URL_VIEW, custom_id=self.short, _external=True)

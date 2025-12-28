from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError
)

from .constants import (
    SHORT_MAX_LEN,
    ORIGINAL_LINK_LENGJT,
    REGEX,
    RESERVED_SHORTS
)

from .models import URLMap

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class YacutForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(max=ORIGINAL_LINK_LENGJT)
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(max=SHORT_MAX_LEN),
            Optional(),
            Regexp(REGEX, message=INVALID_SHORT)
        )
    )
    submit = SubmitField('Добавить')

    def validate_custom_id(form, custom_id):
        if (custom_id and URLMap.get(custom_id.data)
                or custom_id.data in RESERVED_SHORTS):
            raise ValidationError(SHORT_EXISTS)


class FileUploadForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
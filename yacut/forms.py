from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import SHORT_MAX_LEN, ORIGINAL_LINK_LENGJT


class YacutForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=ORIGINAL_LINK_LENGJT)
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=SHORT_MAX_LEN), Optional()]
    )
    submit = SubmitField('Добавить')


class FileUploadForm(FlaskForm):
    """Форма для страницы загрузки файлов."""
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
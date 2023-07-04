from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import STRING_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(max=256), Optional()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=STRING_LENGTH), Optional(),
            Regexp(r'^[A-Za-z0-9]+$', message='Недопустимые символы')]
    )
    submit = SubmitField('Создать')

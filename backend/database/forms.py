from backend.config.config import *
from backend.database.models import User

class MonopolyAccountForm(FlaskForm):
    email = StringField('Электронная почта Monopoly', validators=[DataRequired()])
    password = PasswordField('Пароль Monopoly', validators=[DataRequired()])
    proxy = StringField('Прокси')
    submit = SubmitField('Сохранить')

class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    register_submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Этот никнейм уже зарегистрирован.')

class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    login_submit = SubmitField('Войти')
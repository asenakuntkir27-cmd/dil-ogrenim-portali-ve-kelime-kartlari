from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from app import db
import sqlalchemy as sa

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('E-Posta', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Şifre Tekrar', validators=[
        DataRequired(), EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen farklı bir tane seçin.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir tane seçin.')

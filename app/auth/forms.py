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

    def validate_password(self, password):
        val = password.data
        errors = []
        if len(val) < 6:
            errors.append("en az 6 karakter uzunluğunda olmalı")
        if not any(char.isupper() for char in val):
            errors.append("en az bir büyük harf (A-Z) içermeli")
        if not any(char.isdigit() for char in val):
            errors.append("en az bir rakam (0-9) içermeli")
            
        if errors:
            raise ValidationError(
                'Siber Güvenlik Politikası Uyarısı: Belirlediğiniz şifre güvenlik standartlarını karşılamıyor. '
                'Şifreniz ' + ' ve '.join(errors) + 'dir. Güvenliğiniz için lütfen kurallara uygun, tahmin edilmesi güç bir şifre seçiniz.'
            )

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen farklı bir tane seçin.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir tane seçin.')

class EditProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('E-Posta', validators=[DataRequired(), Email(), Length(max=120)])
    submit_profile = SubmitField('Değişiklikleri Kaydet')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen farklı bir tane seçin.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.scalar(sa.select(User).where(User.email == email.data))
            if user is not None:
                raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir tane seçin.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mevcut Şifre', validators=[DataRequired()])
    new_password = PasswordField('Yeni Şifre', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Yeni Şifre Tekrar', validators=[
        DataRequired(), EqualTo('new_password', message='Yeni şifreler eşleşmiyor.')
    ])
    submit_password = SubmitField('Şifreyi Güncelle')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-Posta Adresi', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Sıfırlama Bağlantısı Gönder')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Yeni Şifre', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Yeni Şifre Tekrar', validators=[
        DataRequired(), EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Şifreyi Sıfırla')

class ChangeEmailRequestForm(FlaskForm):
    new_email = StringField('Yeni E-Posta Adresi', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Mevcut Şifre', validators=[DataRequired()])
    submit = SubmitField('Değişiklik Bağlantısı Gönder')

    def validate_new_email(self, new_email):
        user = db.session.scalar(sa.select(User).where(User.email == new_email.data))
        if user is not None:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir tane seçin.')

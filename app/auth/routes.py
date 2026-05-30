from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except Exception:
        return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        
        # Giriş yapıldığında kullanıcının streak durumunu tetikle
        user.record_activity(0)
        db.session.commit()
        
        # Ensure user has the decks for the current learning language
        lang_code = session.get('learning_language', 'en')
        from app.seeds import seed_language_decks_for_user
        seed_language_decks_for_user(user, lang_code)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Giriş Yap', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Seed the default language (English) decks for the newly registered user
        from app.seeds import seed_language_decks_for_user
        seed_language_decks_for_user(user, 'en')

        flash('Tebrikler, başarıyla kayıt oldunuz! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Kayıt Ol', form=form)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            return render_template('auth/reset_password_requested.html', reset_url=reset_url, email=user.email, title='Bağlantı Oluşturuldu')
        else:
            flash('Bu e-posta adresine kayıtlı bir kullanıcı bulunamadı.', 'danger')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password_request.html', title='Şifre Sıfırlama Talebi', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    email = verify_reset_token(token)
    if not email:
        flash('Şifre sıfırlama bağlantısı geçersiz veya süresi dolmuş.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = db.session.scalar(sa.select(User).where(User.email == email))
    if not user:
        flash('Kullanıcı bulunamadı.', 'danger')
        return redirect(url_for('auth.login'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Şifreyi Sıfırla', form=form)

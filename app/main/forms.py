from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class DeckForm(FlaskForm):
    name = StringField('Deste Adı', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Açıklama (İsteğe Bağlı)')
    submit = SubmitField('Deste Oluştur')

class CardForm(FlaskForm):
    word = StringField('Kelime (Ön Yüz)', validators=[DataRequired(), Length(min=1, max=128)])
    meaning = StringField('Anlamı (Arka Yüz)', validators=[DataRequired(), Length(min=1, max=256)])
    example_sentence = TextAreaField('Örnek Cümle (İsteğe Bağlı)')
    submit = SubmitField('Kart Ekle')

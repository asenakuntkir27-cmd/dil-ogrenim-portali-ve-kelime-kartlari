from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main import main
from app.main.forms import DeckForm, CardForm
from app.models import Deck, Card

@main.route('/')
@main.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('main/index.html', title='Ana Sayfa')
    
    # Kullanıcı giriş yaptıysa kendi destelerini sayfalayarak getir
    page = request.args.get('page', 1, type=int)
    query = sa.select(Deck).where(Deck.user_id == current_user.id).order_by(Deck.created_at.desc())
    pagination = db.paginate(query, page=page, per_page=10, error_out=False)
    
    return render_template('main/index.html', title='Destelerim', decks=pagination.items, pagination=pagination)

@main.route('/deck/new', methods=['GET', 'POST'])
@login_required
def create_deck():
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(name=form.name.data, description=form.description.data, user=current_user)
        db.session.add(deck)
        db.session.commit()
        flash('Yeni deste başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.index'))
    return render_template('main/create_deck.html', title='Yeni Deste Oluştur', form=form)

@main.route('/deck/<int:deck_id>')
@login_required
def deck_detail(deck_id):
    deck = db.session.get(Deck, deck_id)
    if deck is None or deck.user_id != current_user.id:
        abort(404)
    
    cards = db.session.scalars(
        sa.select(Card).where(Card.deck_id == deck.id)
    ).all()
    
    return render_template('main/deck_detail.html', title=deck.name, deck=deck, cards=cards)

@main.route('/deck/<int:deck_id>/card/new', methods=['GET', 'POST'])
@login_required
def create_card(deck_id):
    deck = db.session.get(Deck, deck_id)
    # Başkasının destesine kart eklenmesini engelle
    if deck is None or deck.user_id != current_user.id:
        abort(404)
        
    form = CardForm()
    if form.validate_on_submit():
        card = Card(
            word=form.word.data,
            meaning=form.meaning.data,
            example_sentence=form.example_sentence.data,
            deck=deck
        )
        db.session.add(card)
        db.session.commit()
        flash('Yeni kelime kartı eklendi!', 'success')
        return redirect(url_for('main.deck_detail', deck_id=deck.id))
        
    return render_template('main/create_card.html', title='Yeni Kart Ekle', form=form, deck=deck)

@main.route('/deck/<int:deck_id>/study')
@login_required
def study_deck(deck_id):
    deck = db.session.get(Deck, deck_id)
    if deck is None or deck.user_id != current_user.id:
        abort(404)
        
    cards = db.session.scalars(
        sa.select(Card).where(Card.deck_id == deck.id)
    ).all()
    
    if not cards:
        flash('Bu destede çalışılacak kart bulunmuyor. Lütfen önce kart ekleyin.', 'warning')
        return redirect(url_for('main.deck_detail', deck_id=deck.id))
        
    return render_template('main/study.html', title=f'{deck.name} - Çalış', deck=deck, cards=cards)


@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

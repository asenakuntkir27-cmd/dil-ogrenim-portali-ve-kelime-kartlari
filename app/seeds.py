import sqlalchemy as sa
from sqlalchemy.exc import OperationalError, ProgrammingError
from app import db
from app.models import User, Deck, Card, CurriculumUnit
from app.vocabulary_data import VOCABULARY_DATA

LANG_NAMES = {
    'en': 'İngilizce',
    'de': 'Almanca',
    'es': 'İspanyolca',
    'fr': 'Fransızca',
    'it': 'İtalyanca'
}

def seed_language_decks_for_user(user, lang_code):
    if lang_code not in VOCABULARY_DATA and lang_code != 'en':
        return False

    lang_name = LANG_NAMES.get(lang_code, lang_code)
    seeded_any = False
    try:
        if lang_code == 'en':
            from app.a1_alphabetical_data import A1_ALPHABETICAL_DECKS
            
            # 1. Eski gün tabanlı veya geçici tüm kelime paketlerini temizle (delete old English decks, but keep idioms)
            existing_en_decks = db.session.scalars(
                sa.select(Deck).where(
                    Deck.user_id == user.id,
                    Deck.name.like("İngilizce - %"),
                    Deck.name != "İngilizce - Popüler İngilizce Kalıplar ve Deyimler"
                )
            ).all()
            for d in existing_en_decks:
                db.session.delete(d)
            db.session.flush()

            # 2. Alfabetik desteleri oluştur ve kelimeleri örnek cümleleri/çevirileriyle aktar
            for deck_key, cards_list in A1_ALPHABETICAL_DECKS.items():
                deck_name = f"{lang_name} - {deck_key}"
                
                # Check duplicate (redundancy check)
                deck = db.session.scalar(
                    sa.select(Deck).where(Deck.user_id == user.id, Deck.name == deck_name)
                )
                if not deck:
                    deck = Deck(
                        name=deck_name,
                        description=f"A1 Seviyesi İngilizce kelimeleri ve örnek cümleleri ({deck_key}).",
                        user=user
                    )
                    db.session.add(deck)
                    db.session.flush()
                
                for card_info in cards_list:
                    card_exists = db.session.scalar(
                        sa.select(Card).where(Card.deck_id == deck.id, Card.word == card_info["word"])
                    )
                    if not card_exists:
                        card = Card(
                            word=card_info["word"],
                            meaning=card_info["meaning"],
                            example_sentence=card_info["example_sentence"],
                            deck=deck
                        )
                        db.session.add(card)
                        seeded_any = True

            # 3. İngilizce Kalıplar ve Deyimler destesini kontrol et ve oluştur/güncelle
            idioms_category = 'Popüler İngilizce Kalıplar ve Deyimler'
            idioms_deck_name = f"{lang_name} - {idioms_category}"
            idioms_deck = db.session.scalar(
                sa.select(Deck).where(Deck.user_id == user.id, Deck.name == idioms_deck_name)
            )
            if not idioms_deck:
                idioms_deck = Deck(
                    name=idioms_deck_name,
                    description=f"{lang_name} dilinde {idioms_category} konusuna ait en sık kullanılan kelimeler ve örnek cümleleri.",
                    user=user
                )
                db.session.add(idioms_deck)
                db.session.flush()
            idioms_cards = VOCABULARY_DATA['en'].get(idioms_category, [])
            for card_info in idioms_cards:
                card_exists = db.session.scalar(
                    sa.select(Card).where(Card.deck_id == idioms_deck.id, Card.word == card_info["word"])
                )
                if not card_exists:
                    card = Card(
                        word=card_info["word"],
                        meaning=card_info["meaning"],
                        example_sentence=card_info["example_sentence"],
                        deck=idioms_deck
                    )
                    db.session.add(card)
                    seeded_any = True
        else:
            lang_data = VOCABULARY_DATA[lang_code]
            for category, cards_list in lang_data.items():
                deck_name = f"{lang_name} - {category}"
                
                # Check if this deck already exists for this user
                deck = db.session.scalar(
                    sa.select(Deck).where(Deck.user_id == user.id, Deck.name == deck_name)
                )
                if not deck:
                    # Create deck
                    deck = Deck(
                        name=deck_name,
                        description=f"{lang_name} dilinde {category} konusuna ait en sık kullanılan kelimeler ve örnek cümleleri.",
                        user=user
                    )
                    db.session.add(deck)
                    db.session.flush() # To get deck.id
                
                # Add cards if they do not already exist in the deck
                for card_info in cards_list:
                    card_exists = db.session.scalar(
                        sa.select(Card).where(Card.deck_id == deck.id, Card.word == card_info["word"])
                    )
                    if not card_exists:
                        card = Card(
                            word=card_info["word"],
                            meaning=card_info["meaning"],
                            example_sentence=card_info["example_sentence"],
                            deck=deck
                        )
                        db.session.add(card)
                        seeded_any = True
            
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding {lang_name} decks for user {user.username}: {e}")
    return False

def seed_curriculum_for_user(user):
    from app.curriculum_data import A1_CURRICULUM
    seeded_any = False
    try:
        for unit in A1_CURRICULUM:
            deck_name = f"A1 Kursu - Unit {unit['unit_number']}: {unit['title']}"
            
            # Check if this deck already exists for this user
            deck = db.session.scalar(
                sa.select(Deck).where(Deck.user_id == user.id, Deck.name == deck_name)
            )
            if not deck:
                # Create deck
                deck = Deck(
                    name=deck_name,
                    description=f"A1 İngilizce Kursu Ünite {unit['unit_number']} kelimeleri: {unit['words_description']}",
                    user=user
                )
                db.session.add(deck)
                db.session.flush() # To get deck.id
            
            # Add cards
            for card_info in unit["words"]:
                card_exists = db.session.scalar(
                    sa.select(Card).where(Card.deck_id == deck.id, Card.word == card_info["word"])
                )
                if not card_exists:
                    card = Card(
                        word=card_info["word"],
                        meaning=card_info["meaning"],
                        example_sentence="",
                        deck=deck
                    )
                    db.session.add(card)
                    seeded_any = True
        if seeded_any:
            db.session.commit()
            return True
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding curriculum decks for user {user.username}: {e}")
    return False

def seed_curriculum_units():
    from app.curriculum_data import A1_CURRICULUM
    
    try:
        # Delete existing to prevent overlaps
        db.session.execute(sa.delete(CurriculumUnit))
        
        for unit in A1_CURRICULUM:
            db_unit = CurriculumUnit(
                unit_number=unit["unit_number"],
                title=unit["title"],
                grammar_topic=unit["grammar_topic"],
                grammar_explanation=unit["grammar_explanation"],
                words_description=unit["words_description"]
            )
            db.session.add(db_unit)
        db.session.commit()
        print("Successfully seeded CurriculumUnit table with 12 units.")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding curriculum units: {e}")
    return False

def seed_db():
    try:
        # First seed the static curriculum units
        seed_curriculum_units()

        # Check if database is empty by checking if any User exists
        user_exists = db.session.scalar(sa.select(User.id).limit(1))
        if user_exists is None:
            # Seed default user
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush() # To get admin.id

            # Seed all language decks for admin
            for code in LANG_NAMES.keys():
                seed_language_decks_for_user(admin, code)
            
            # Seed curriculum for admin
            seed_curriculum_for_user(admin)
            
            print("Database successfully seeded with default user 'admin' and all language decks.")
            return True
        else:
            print("Database already has users. Backfilling missing language decks for all users...")
            users = db.session.scalars(sa.select(User)).all()
            seeded_count = 0
            for u in users:
                for code in LANG_NAMES.keys():
                    if seed_language_decks_for_user(u, code):
                        seeded_count += 1
                if seed_curriculum_for_user(u):
                    seeded_count += 1
            if seeded_count > 0:
                print(f"Successfully seeded/backfilled decks for {seeded_count} user combinations.")
            else:
                print("All existing users already have all language/curriculum decks.")
            return True
    except (OperationalError, ProgrammingError) as e:
        db.session.rollback()
        print(f"Skipping database seeding because tables do not exist yet: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error during database seeding: {e}")
    return False

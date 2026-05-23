import sqlalchemy as sa
from sqlalchemy.exc import OperationalError, ProgrammingError
from app import db
from app.models import User, Deck, Card

def seed_db():
    try:
        # Check if database is empty by checking if any User exists
        user_exists = db.session.scalar(sa.select(User.id).limit(1))
        if user_exists is None:
            # Seed default user
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush() # To get admin.id

            # Seed default deck
            deck = Deck(
                name='A1-A2 Seviyesi Yaygın Kelimeler',
                description='Temel İngilizce seviyesinde (A1-A2) en sık kullanılan 20 kelime ve anlamları.',
                user=admin
            )
            db.session.add(deck)
            db.session.flush() # To get deck.id

            # Seed 20 cards
            cards_data = [
                {"word": "Apple", "meaning": "Elma", "example_sentence": "I eat a red apple every morning."},
                {"word": "Book", "meaning": "Kitap", "example_sentence": "She is reading an interesting book."},
                {"word": "Cat", "meaning": "Kedi", "example_sentence": "The cat is sleeping on the sofa."},
                {"word": "Dog", "meaning": "Köpek", "example_sentence": "He walks his dog in the park."},
                {"word": "House", "meaning": "Ev", "example_sentence": "They live in a beautiful house."},
                {"word": "Water", "meaning": "Su", "example_sentence": "Please give me a glass of water."},
                {"word": "School", "meaning": "Okul", "example_sentence": "Children go to school to learn."},
                {"word": "Teacher", "meaning": "Öğretmen", "example_sentence": "Our English teacher is very helpful."},
                {"word": "Student", "meaning": "Öğrenci", "example_sentence": "The student is studying for the exam."},
                {"word": "Family", "meaning": "Aile", "example_sentence": "I love spending time with my family."},
                {"word": "Friend", "meaning": "Arkadaş", "example_sentence": "He is my best friend from childhood."},
                {"word": "Happy", "meaning": "Mutlu", "example_sentence": "We are very happy to see you."},
                {"word": "Time", "meaning": "Zaman", "example_sentence": "What time does the movie start?"},
                {"word": "Food", "meaning": "Yemek", "example_sentence": "Turkish food is famous worldwide."},
                {"word": "Car", "meaning": "Araba", "example_sentence": "They bought a new electric car."},
                {"word": "Sun", "meaning": "Güneş", "example_sentence": "The sun rises in the east."},
                {"word": "Morning", "meaning": "Sabah", "example_sentence": "Good morning! How are you?"},
                {"word": "Night", "meaning": "Gece", "example_sentence": "The stars look beautiful tonight."},
                {"word": "Day", "meaning": "Gün", "example_sentence": "It is a sunny day today."},
                {"word": "City", "meaning": "Şehir", "example_sentence": "Istanbul is a very large city."}
            ]

            for card_info in cards_data:
                card = Card(
                    word=card_info["word"],
                    meaning=card_info["meaning"],
                    example_sentence=card_info["example_sentence"],
                    deck=deck
                )
                db.session.add(card)
            
            db.session.commit()
            print("Database successfully seeded with default user 'admin' and 'A1-A2 Seviyesi Yaygin Kelimeler' deck.")
            return True
        else:
            print("Database already has users, skipping seeding.")
    except (OperationalError, ProgrammingError) as e:
        db.session.rollback()
        print(f"Skipping database seeding because tables do not exist yet: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error during database seeding: {e}")
    return False

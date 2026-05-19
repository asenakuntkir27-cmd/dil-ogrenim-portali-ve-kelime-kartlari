# Dil Öğrenim Portalı ve Kelime Kartları - AI Günlüğü

Bu belge, proje geliştirme sürecinde AI asistanı ile yapılan oturumların, alınan kararların ve kaydedilen ilerlemenin bir günlüğüdür.

---

## Oturum 1: Proje İskeleti Kurulumu
**Tarih:** 16 Mayıs 2026

### Hedef
Flask 3.x kullanılarak, Application Factory pattern ve Blueprint mimarisine sahip temiz bir proje iskeleti kurmak.

### Yapılanlar
- **Gereksinimler:** `requirements.txt` dosyası oluşturuldu. İçerisinde Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF ve python-dotenv paketleri tanımlandı.
- **Konfigürasyon:** Çevresel değişkenler için şablon (`.env.example`) ve uygulama ayarlarını yönetecek yapı (`config.py`) oluşturuldu. Geliştirme sunucusunu başlatmak için `run.py` hazırlandı.
- **Uygulama Mimarisi (Application Factory):** `app/__init__.py` içerisinde `create_app` fonksiyonu oluşturularak uygulamanın factory pattern ile ayağa kalkması sağlandı.
- **Blueprint Yapısı:** Rotaları mantıksal olarak ayırmak için `main` (ana sayfalar) ve `auth` (kimlik doğrulama) isimli iki temel Blueprint'in dizinleri (`app/main/`, `app/auth/`) ve `__init__.py` iskelet dosyaları oluşturuldu. Factory içerisinde kayıt işlemleri tanımlandı.
- **Git ve Dizin Hazırlığı:** Model modülü (`models.py`) ve Test paketi (`tests/__init__.py`) taslak olarak eklendi. `templates`, `static` ve `migrations` klasörlerinin Git tarafından takip edilmesi için `.gitkeep` dosyaları yerleştirildi. `.gitignore` dosyasının halihazırda `.env` dosyasını yoksaydığı teyit edildi.

### Sonraki Adımlar
- Geliştirme ortamının (Virtual Environment) kurulması ve paketlerin indirilmesi.
- Veritabanı modellerinin (Kullanıcı, Kelime Kartları vb.) oluşturulması.
- Blueprint'ler içerisine ilgili rotaların ve şablonların entegrasyonu.

---

## Oturum 2: Veritabanı Modellerinin Tasarlanması
**Tarih:** 19 Mayıs 2026

### Hedef
SQLAlchemy 2.x stiline (Mapped, mapped_column) uygun olarak Kullanıcı (User), Kelime Destesi (Deck) ve Kelime Kartı (Card) modellerini tasarlamak ve aralarındaki ilişkileri kurmak.

### Yapılanlar
- **Veritabanı İlklendirmesi:** `app/__init__.py` dosyası güncellenerek `db = SQLAlchemy()` nesnesi oluşturuldu ve factory içerisinde (`db.init_app(app)`) uygulamaya dahil edildi. Modellerin sistem tarafından algılanabilmesi için uygun import satırı eklendi.
- **Kullanıcı Modeli (User):** `username`, `email`, `password_hash` ve `created_at` alanları tanımlandı. Parola güvenliği için `werkzeug.security` aracılığıyla `set_password` ve `check_password` metotları oluşturuldu.
- **Deste ve Kart Modelleri:** Kullanıcıların sahip olacağı desteleri (`Deck`) ve destelerin içindeki kelime kartlarını (`Card`) yönetecek modeller tanımlandı.
- **İlişkiler:** User-Deck ve Deck-Card arasında modern SQLAlchemy `relationship` özellikleri kullanılarak bire-çok (One-to-Many) ilişkiler kuruldu. `cascade` işlemleri eklendi.
- **Test ve Konsol İşlemleri:** Tüm modellerin konsolda anlaşılır bir biçimde gösterilmesi için `__repr__` metotları tanımlandı.

### Sonraki Adımlar
- İlk veritabanı migrasyonlarının (`flask db init`, `flask db migrate`) çalıştırılması ve veritabanı dosyasının yaratılması.
- Giriş, kayıt veya anasayfa için Blueprint rotalarının ve şablonlarının oluşturulması.

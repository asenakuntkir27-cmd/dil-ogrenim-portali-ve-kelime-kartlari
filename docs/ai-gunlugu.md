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

---

## Oturum 3: Veritabanı Kurulumu ve Migrasyon Yönetimi
**Tarih:** 19 Mayıs 2026

### Hedef
Sanal ortamın (virtual environment) ayarlanması ve `Flask-Migrate` komutları (`db init`, `db migrate`, `db upgrade`) kullanılarak ilk veritabanı şemasının ayağa kaldırılması.

### Karşılaşılan Sorunlar ve Çözümleri
- **PowerShell ExecutionPolicy Engeli:** Sanal ortamı `activate` scripti üzerinden aktifleştirmeye çalışırken Windows Execution Policy kısıtlamasına takıldık. Bu engeli aşmak için scriptleri çalıştırmak yerine, komutları doğrudan sanal ortamın içindeki çalıştırılabilir dosyalar (executable) üzerinden (örneğin `.\venv\Scripts\flask.exe`) güvenli bir sandbox mantığıyla yürüttük.
- **Eksik Paket Kurulumu:** Projenin bağımlılıklarının (`requirements.txt`) sanal ortam içerisine kurulmadığı tespit edildi. Bu eksiklik `.\venv\Scripts\python.exe -m pip install` yöntemiyle paketler yüklenerek giderildi.
- **.env Dosyası Eksikliği:** Flask'ın `FLASK_APP` gibi konfigürasyonları bulabilmesi için gereken `.env` dosyasının olmadığını fark ettik. `.env.example` dosyasının bir kopyası alınarak eksiklik tamamlandı.
- **Flask-Migrate Entegrasyon Eksikliği:** `flask db` komutlarının çalışmamasının temel sebebi olarak, `app/__init__.py` içerisinde `Migrate(app, db)` tanımlamasının yapılmadığı görüldü. Gerekli kütüphane eklendi ve sistem başlatıldı.

### Yapılanlar
- Tespit edilen sorunların tamamı izole ortamda düzeltildikten sonra `migrations` klasörü temizlenerek sıfırdan oluşturuldu.
- `flask db init` komutuyla Alembic ve Flask-Migrate altyapısı başarıyla kuruldu.
- `flask db migrate -m "initial schema"` komutu çalıştırılarak `User`, `Deck` ve `Card` tabloları için migrasyon dosyası oluşturuldu.
- `flask db upgrade` komutuyla tablo şemaları SQLite (`app.db`) veritabanına sorunsuz şekilde yansıtıldı.

### Sonraki Adımlar
- Blueprint rotalarının (Auth ve Main) detaylandırılarak kullanıcı arayüzü ile bağlanması.
- Uygulamanın temel testlerinin gerçekleştirilmesi.

---

## Oturum 4: Kimlik Doğrulama (Auth) Sisteminin Kurulması
**Tarih:** 21 Mayıs 2026

### Hedef
Kullanıcı kayıt (register), giriş (login) ve çıkış (logout) işlemlerini Flask-Login ve WTForms standartlarına uygun şekilde yönetecek bir `auth` Blueprint yapısının inşa edilmesi.

### Yapılanlar
- **Model ve Konfigürasyon:** 
  - `app/models.py` içerisindeki `User` modeline `flask_login` kütüphanesinden `UserMixin` sınıfı entegre edildi.
  - Oturum yönetimini sağlamak için `load_user` fonksiyonu (`@login_manager.user_loader`) eklendi.
  - `app/__init__.py` dosyasına `LoginManager` dahil edildi ve yetkisiz erişimleri engellemek için `login_view = 'auth.login'` ayarı yapıldı.
- **Form Sınıflarının Oluşturulması (WTForms):** 
  - `app/auth/forms.py` dosyası oluşturuldu. 
  - `LoginForm` (Kullanıcı Adı, Şifre, Beni Hatırla) ve `RegistrationForm` (Kullanıcı Adı, E-Posta, Şifre, Şifre Tekrar) sınıfları kodlandı.
  - Kayıt formuna, aynı kullanıcı adı veya e-postanın kullanılıp kullanılmadığını veritabanından denetleyen özel validatörler (`validate_username`, `validate_email`) eklendi.
- **Rotaların (Routes) Tasarlanması:** 
  - `app/auth/routes.py` dosyası oluşturularak `/login`, `/register` ve `/logout` fonksiyonları yazıldı.
  - Şifre doğrulama işlemlerinde model içerisinde daha önce yazılmış olan `set_password` ve `check_password` metotları kullanıldı.
  - Oluşturulan rotalar `app/auth/__init__.py` içerisine import edilerek Blueprint aktif hale getirildi.
- **HTML Şablonlarının (Templates) Eklenmesi:** 
  - Ana iskelet yapısını tutan ve menü (navigasyon) çubuğunu barındıran `app/templates/base.html` oluşturuldu.
  - WTForms bileşenlerini ve hata mesajlarını (validation errors, flash messages) ekrana yansıtan `login.html` ve `register.html` sayfaları oluşturuldu.
  - Yönlendirme (redirect) hatalarını önlemek adına `app/main` Blueprint'i içerisinde basit bir ana sayfa (`/index`) rotası ve `index.html` şablonu eklendi.

### Sonraki Adımlar
- Kelime Destesi (Deck) ve Kelime Kartı (Card) yönetim arayüzlerinin (CRUD işlemleri) kodlanması.
- Uygulama genelindeki HTML/CSS arayüzünün (UI) modern bir tasarımla (Tailwind/Bootstrap vb.) iyileştirilmesi.

---

## Oturum 5: Deste ve Kart Yönetimi ile Debugging (Hata Ayıklama) Süreci
**Tarih:** 21 Mayıs 2026

### Hedef
Kullanıcıların kendi kelime destelerini ve kelime kartlarını oluşturup yönetebileceği sayfaların, rotaların ve formların (CRUD işlemleri) geliştirilmesi ile geliştirme esnasında karşılaşılan hataların çözülmesi.

### Karşılaşılan Sorunlar ve Çözümleri
- **500 Internal Server Error (Kayıt Formu):** Kullanıcı kayıt formunu gönderdiğinde Flask'ın 500 hatası verdiği tespit edildi. Hataya, WTForms'un `Email()` doğrulayıcısının çalışması için gereken `email-validator` kütüphanesinin eksikliğinin neden olduğu anlaşıldı. Bu kütüphane sanal ortama yüklenerek ve `requirements.txt` dosyasına eklenerek sorun çözüldü.
- **Şablon Çakışması ve Önbellek (Cache) Sorunu:** Kullanıcı giriş yaptıktan sonra ana sayfada oluşturulan destelerin listelenmediği ve yeni deste butonunun çıkmadığı fark edildi. Bunun sebebi, `app/templates/index.html` olarak oluşturulan geçici ve eski ana sayfa dosyası ile Blueprint yapısına uygun oluşturulması gereken `app/templates/main/index.html` dosyalarının çakışması ve tarayıcının eskisini render etmesiydi.
  - *Çözüm:* Kök dizindeki eski `index.html` dosyası sol dosya panelinden manuel olarak temizlendi. `app/main/routes.py` rotalarındaki render hedefleri `main/index.html` olarak güncellendi. Değişikliklerin algılanması için dışarıdan PowerShell sunucusu yeniden başlatıldı (reset) ve sorun giderildi.

### Yapılanlar
- **Formlar (app/main/forms.py):** Deste ekleme işlemleri için `DeckForm` ve desteye kart ekleme işlemleri için `CardForm` yapıları WTForms ile tasarlandı.
- **Güvenli Rotalar (app/main/routes.py):** Destelerin listelendiği `/`, yeni deste oluşturulan `/deck/new`, deste detayının gösterildiği `/deck/<id>` ve desteye kart eklenen `/deck/<id>/card/new` rotaları oluşturuldu. Tüm rotalar `@login_required` ile korundu ve URL üzerinden başkasının destesine kart eklenmesini önlemek için `current_user` doğrulaması eklendi.
- **Şablonlar (Templates):** `app/templates/main/` dizini altına `create_deck.html`, `deck_detail.html` ve `create_card.html` dosyaları eklendi. Ana sayfa `index.html` ise giriş yapan kullanıcıya kendi destelerini listeleyecek ve "Yeni Deste Oluştur" butonu sunacak şekilde yeniden yapılandırıldı.

### Sonraki Adımlar
- Arayüzün modern bir CSS framework'ü (Tailwind CSS, Bootstrap vb.) ile giydirilmesi ve mobil uyumlu hale getirilmesi.
- Eklenen kelime kartları üzerinde çalışma/test yapma (Flashcard Quiz) modülünün geliştirilmesi.

---

## Oturum 6: Arayüz Modernizasyonu, Flashcard Quiz (Çalışma) Modülü ve Testler
**Tarih:** 22 Mayıs 2026

### Hedef
Arayüzü Tailwind CSS kullanarak premium, modern ve mobil uyumlu bir tasarımla giydirmek; kullanıcıların destelerdeki kelimeleri interaktif şekilde çalışabilmesi için kart çevirme animasyonlu (flip card) bir Quiz (Çalışma) modülü geliştirmek ve sistemi testlerle doğrulamak.

### Yapılanlar
- **Tasarım Sistemi ve Arayüz Giydirme:**
  - `templates/base.html` güncellenerek Tailwind CSS, Google Fonts (Outfit) ve FontAwesome ikonları entegre edildi.
  - Giriş (`login.html`), kayıt (`register.html`), deste listeleme (`index.html`), deste detayı (`deck_detail.html`) ve form sayfaları (`create_deck.html`, `create_card.html`) modern Tailwind bileşenleri ve özel koyu/mor renk paletiyle estetik bir tasarıma kavuşturuldu.
  - Kart tasarımlarına yumuşak gölgeler, hover geçişleri ve mikro animasyonlar eklendi.
- **Çalışma/Quiz Modülü Geliştirilmesi:**
  - Deste detay sayfasında bir "Çalışmaya Başla" butonu konumlandırıldı.
  - `/deck/<deck_id>/study` rotası (`study.html`) oluşturularak, kullanıcının kartları tek tek görebileceği bir interaktif çalışma alanı tasarlandı.
  - CSS 3D Transforms (`preserve-3d`, `rotateY`, `backface-visibility`) kullanılarak tıklama ile tetiklenen gerçekçi bir kart çevirme (flip) animasyonu entegre edildi (ön yüzde yabancı kelime, arka yüzde anlamı ve örnek cümle).
  - Kullanıcıya her kart için "Öğrendim" ve "Tekrar Et" seçenekleri sunularak çalışma sonunda başarı istatistiği gösteren bir sonuç paneli ve yeniden başlatma butonu eklendi.
- **Testler ve Doğrulama:**
  - `tests/test_study.py` dosyası altında giriş gereksinimleri, boş deste yönlendirmesi ve kartlı destelerin başarılı şekilde yüklenmesini test eden bir `unittest` yapısı kuruldu. Tüm testler başarıyla çalıştırıldı ve onaylandı.

### Sonraki Adımlar
- Sistem canlıya alınabilir veya ek dil öğrenim özellikleri (örn. kelime eşleştirme oyunları) eklenebilir.

---

## Oturum 7: Sitenin Adının ve Renk Paletinin Özelleştirilmesi
**Tarih:** 22 Mayıs 2026

### Hedef
Kullanıcının isteği üzerine sitenin ismini **LingoRose** olarak güncellemek ve renk temasını pembe, mor, gri ve siyah tonlarına uyarlamak.

### Yapılanlar
- **İsim Güncellemesi (LingoRose):** 
  - `templates/base.html` ve `templates/main/index.html` dosyalarındaki tüm `LingoDeck` isim referansları, başlıklar ve telif hakkı ibareleri `LingoRose` olarak güncellendi.
- **Renk Teması Özelleştirmeleri:**
  - Tüm sayfa şablonlarındaki (`base.html`, `login.html`, `register.html`, `index.html`, `deck_detail.html`, `create_deck.html`, `create_card.html`, `study.html`) violet (menekşe) ve indigo (çivit) ağırlıklı Tailwind CSS renk sınıfları; pembe (`pink`), fuşya (`fuchsia`) ve mor (`purple`/`violet`) tonları ile değiştirildi.
  - Arka planlar ve form girişleri gri (`zinc-900`/`zinc-950`) ve siyah tonlarında korunarak estetik bir uyum sağlandı.
- **Doğrulama:**
  - Değişikliklerin ardından tüm şablon yapısı ve çalışma sayfası testleri (`unittest`) yeniden çalıştırılarak doğrulandı.

### Sonraki Adımlar
- Yeni görsel tasarımı canlı olarak incelemek.

---

## Oturum 8: Hata Yönetimi ve Sayfalama (Pagination) Desteği
**Tarih:** 22 Mayıs 2026

### Hedef
Uygulamada eksik olan 404 ve 500 özel hata sayfalarını (templates ve error handlers) eklemek; ana sayfada (dashboard) listelenen kullanıcı destelerini Flask-SQLAlchemy `db.paginate` özelliği ile 10 kayıt limitiyle sayfalamak.

### Yapılanlar
- **Özel Hata Sayfaları (Error Handlers):**
  - `app/main/routes.py` dosyasına blueprint seviyesinde `@main.app_errorhandler(404)` ve `@main.app_errorhandler(500)` hata yönetim rotaları eklendi.
  - `app/templates/errors/404.html` (Sayfa Bulunamadı) şablonu, pembe-mor gradyan temalı, animasyonlu üzgün yüz ikonu ve geri dönüş butonuyla tasarlandı.
  - `app/templates/errors/500.html` (Sunucu Hatası) şablonu, parlayan uyarı ikonu ile tasarlandı.
- **Veritabanı Sayfalama (Pagination):**
  - `app/main/routes.py` dosyasındaki `index()` rotası güncellenerek `db.paginate` ile kullanıcının desteleri 10 limitli sayfalandı.
  - `app/templates/main/index.html` dosyasına sayfalama durumunu gösteren bilgi metni ve LingoRose tasarım diline uygun (önceki, sonraki, sayfa numaraları) şık sayfalama kontrol butonları entegre edildi.
- **Testler ve Doğrulama:**
  - `tests/test_errors_and_pagination.py` adında yeni bir otomatik test dosyası yazıldı. Testlerde, geçersiz rotaların 404 dönüp özel sayfayı yüklediği ve 12 adet deste eklendiğinde sayfalama sisteminin (page 1'de 10 adet, page 2'de 2 adet) sorunsuz çalıştığı doğrulandı.
  - Tüm test paketleri (`discover -s tests`) çalıştırılarak 5 testin tamamının başarıyla geçtiği onaylandı.

### Sonraki Adımlar
- Projenin yayına alınması veya ek modüllerin entegrasyonu.

---

## Oturum 9: Docker Entegrasyonu
**Tarih:** 22 Mayıs 2026

### Hedef
Uygulamayı canlıda (production) çalıştırmak üzere Docker entegrasyonu kurmak; Gunicorn WSGI sunucusu ve PostgreSQL 15 veritabanı ile konteynerize edilmiş çoklu-konteyner orkestrasyon altyapısı hazırlamak.

### Yapılanlar
- **Gereksinimler:** `requirements.txt` dosyasına `gunicorn` ve `psycopg2-binary` paketleri eklenerek Docker içindeki web konteynerinin üretim WSGI sunucusuna ve PostgreSQL veritabanına bağlanması sağlandı.
- **Dockerfile:** `python:3.11-slim` tabanlı, optimize edilmiş bir Dockerfile oluşturuldu. Konteyner başlangıcında `flask db upgrade` çalıştırılarak yeni şema göçlerinin uygulanması ve ardından `gunicorn` ile uygulamanın sunulması sağlandı.
- **docker-compose.yml:** Web ve PostgreSQL servisleri tanımlandı. PostgreSQL servisi için `healthcheck` eklenerek web servisinin veritabanı hazır olana kadar beklemesini sağlayan `condition: service_healthy` orkestrasyonu kuruldu. Kalıcı veri depolaması için `postgres_data` volume entegrasyonu yapıldı.
- **.dockerignore:** `venv/`, `__pycache__/`, yerel SQLite `app.db` gibi gereksiz veya yerel geliştirme dosyalarının Docker derleme sürecine dahil edilip imaj boyutunu büyütmesi engellendi.
- **Doğrulama:** `docker compose config` komutuyla Docker Compose sözdizimi doğrulandı. Ayrıca yerel test paketleri (`python -m unittest discover -s tests`) yeniden çalıştırılarak bağımlılıkların eklenmesinin yerel sisteme herhangi bir yan etki yapmadığı, tüm 5 testin başarıyla geçtiği doğrulandı.

### Sonraki Adımlar
- Docker konteynerlerini yayına almak.

---

## Oturum 10: Çoklu Dil Desteği, 1500 Kelimelik Hazır Paketler, Eşleştirme Oyunu ve Karşılama Paneli (Kapanış ve Cilalama)
**Tarih:** 23 Mayıs 2026

### Hedef
Kullanıcı deneyimini en üst seviyeye çıkarmak için 5 dilli başlangıç veri seti (seeding) kurmak, dinamik dil filtrelemesi eklemek, Mini Kelime Eşleştirme Oyunu geliştirmek ve ana sayfayı profesyonel bir "Karşılama Paneli" mimarisine geçirmek.

### Yapılanlar
- **Çoklu Dil Altyapısı ve 1500 Kelimelik Paketler:**
  - `app/vocabulary_data.py` modülü altında İngilizce, Almanca, İspanyolca, Fransızca ve İtalyanca dillerinde, 15 temel kategoride, her kategoride 20'şer kelime barındıran toplam 1500 kelimelik hazır kelime seti tanımlandı.
  - `app/seeds.py` güncellenerek kayıt (`register`) ve giriş (`login`) anlarında veya `flask seed` komutuyla tüm dillerin/aktif dilin destelerinin kullanıcı hesabına otomatik kopyalanması sağlandı.
- **Dil Filtreleme ve Kilitlenme Hatası Giderimi:**
  - Üst menüden dil değiştirilmesine rağmen ana sayfada hep İtalyanca destelerinin gelmesi hatası analiz edildi. Hataya, index rotasında dile göre filtreleme yapılmamasının sebep olduğu tespit edildi.
  - `app/main/routes.py` index sorgusuna oturumdaki aktif dil adına göre filtre eklendi (`Deck.name.like(f"{lang_name} - %")`).
  - Özel oluşturulan destelerin isminin başına aktif dil adı otomatik eklendi ve Jinja şablonlarında (`index.html`, `deck_detail.html`, `study.html`, `create_card.html`) bu öneklerin temizlenerek (`replace(current_language['name'] + ' - ', '')`) kullanıcılara gösterilmesi sağlandı.
- **Mini Kelime Eşleştirme Oyunu (Matching Game):**
  - `/deck/<deck_id>/game` rotasında çalışan, Tailwind CSS ile tasarlanmış mobil uyumlu interaktif bir oyun geliştirildi.
  - Kartlar (en fazla 8 kelime = 16 kutu) 4x4 gridde karıştırılarak gösterildi. Doğru eşleşmede yeşil yanıp kaybolma, yanlış eşleşmede kırmızı yanıp shake (titreşim) animasyonu entegre edildi.
  - Oyun tamamlandığında `canvas-confetti` kütüphanesiyle konfeti efekti ve tebrik ekranı eklendi.
- **Dashboard Karşılama Paneli (Karşılama & Modüler Yapı):**
  - Sekmeli yapı kaldırılarak yerine modern bir "Karşılama Paneli" kuruldu. En üstte kurumsal karşılama yazısı ve altında parlayan iki ana modül kutusu ("Kelime Destelerim" ve "Eğitim Oyunları") yerleştirildi.
  - Kullanıcı "Eğitim Oyunları" modülüne tıkladığında alt akış olarak Kelime Eşleştirme Oyunu kartı ve ona tıklayınca da hızlı oyun başlatma deste listesi listelenecek şekilde çok katmanlı dinamik bir akış kuruldu.
  - `sessionStorage` yardımıyla kullanıcının son seçtiği modül ve oyun alt akış durumları oturum hafızasında saklanarak sayfa geçişlerinde durum kaybı engellendi.
- **Testlerin Güncellenmesi:**
  - `tests/test_study.py` ve `tests/test_errors_and_pagination.py` dosyaları yeni dil filtreleme ve oyun rotalarına göre güncellenerek toplam test sayısı 15'e çıkarıldı. Tüm testler başarıyla geçmiştir.

### Sonraki Adımlar
- Hocaya teslim dokümanlarını hazırlamak ve projeyi sunmak.

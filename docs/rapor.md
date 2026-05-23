# LingoRose Dil Öğrenim Portali ve Kelime Kartları Proje Raporu

---

## 1. Projenin Amacı ve Genel Özeti

Yabancı bir dil öğreniminde en büyük zorluklardan biri, yeni öğrenilen kelimelerin hafızada kalıcı hale getirilmesidir. Klasik ezberleme yöntemleri, öğreniciyi aktif bir süreç içerisine dahil etmediğinden verimsiz kalmaktadır. **LingoRose**, bu problemi çözmek amacıyla geliştirilmiş etkileşimli, çok dilli ve oyunlaştırılmış bir web tabanlı dil öğrenim portalidir.

Uygulamanın temel amacı; kullanıcıların kendi çalışma alanlarını özelleştirerek kelime desteleri (decks) oluşturabilmesi, bu destelere diledikleri kelimeleri, anlamlarını ve örnek cümlelerini ekleyebilmesinin yanı sıra sistemde hazır sunulan zengin dil paketlerinden faydalanabilmesidir. LingoRose; **İngilizce, Almanca, İspanyolca, Fransızca ve İtalyanca** olmak üzere 5 farklı dili desteklemektedir. Sistem ilk kurulumda veya kullanıcı kayıt/giriş anlarında otomatik olarak her dil için 15 farklı kategoride (Sayılar, Hayvanlar, Renkler vb.) en az 20'şer adet kelimeden oluşan **toplam 1500 kartlık devasa bir başlangıç verisini (seed data)** kullanıcılara tanımlamaktadır.

Öğrenme sürecini pekiştirmek için iki ana çalışma modülü sunulmaktadır:
1. **3D Kart Çevirme (Quiz) Modülü:** Kullanıcılar premium bir 3D çevirme animasyonuyla kartın ön yüzündeki yabancı kelimeyi görüp anlamını tahmin etmeye çalışmakta, ardından karta tıklayarak arka yüzündeki anlamını ve örnek cümlesini görüntülemektedir. Çalışma sonunda "Öğrendim" veya "Tekrar Et" butonlarıyla başarı skoru ölçülmektedir.
2. **Kelime Eşleştirme Oyunu (Matching Game):** Kullanıcıların o anki aktif dillerine ait destedeki kelimelerin yabancı halleri ile Türkçe anlamlarını 4x4 dinamik bir grid üzerinde eşleştirdikleri süreye dayalı interaktif bir mini oyundur. Eşleşen kartlar yeşil yanarak kaybolmakta, yanlış eşleşmeler kırmızı yanıp titremekte (shake animasyonu) ve oyun sonunda konfeti animasyonlu şık bir tebrik paneli çıkmaktadır.

Sistem, modern bir koyu tema (dark mode) üzerine kurulu, pembe ve mor gradyanlarla desteklenen estetik bir tasarım dili sunmakta; hem masaüstü hem de mobil cihazlarda kusursuz bir kullanıcı deneyimi (UX) hedeflemektedir.

---

## 2. Mimari Yapı ve Klasör Düzeni

Uygulama, Python dilinin popüler mikro-framework'ü **Flask 3.x** üzerine inşa edilmiştir. Ölçeklenebilirlik, bakım kolaylığı ve test edilebilirliği artırmak amacıyla **Application Factory Pattern** ve **Blueprint** mimarileri kullanılmıştır. Veri tabanı katmanında modern **SQLAlchemy 2.0 ORM** standartları benimsenmiştir.

### Klasör Yapısı

Aşağıdaki şemada uygulamanın genel klasör ve dosya organizasyonu gösterilmiştir:

```text
dil-ogrenim-portali-ve-kelime-kartlari/
│
├── app/                           # Uygulama Çekirdeği
│   ├── auth/                      # Kimlik Doğrulama Modülü (Blueprint)
│   │   ├── __init__.py
│   │   ├── forms.py               # Login ve Register Form Sınıfları
│   │   └── routes.py              # Auth Rotaları (/login, /register, /logout)
│   │
│   ├── main/                      # Temel İşlevler Modülü (Blueprint)
│   │   ├── __init__.py
│   │   ├── forms.py               # Deck ve Card Ekleme Form Sınıfları
│   │   └── routes.py              # Main Rotaları ve Hata İşleyiciler (404/500/Game)
│   │
│   ├── static/                    # Statik Dosyalar (CSS, JS, Resimler)
│   │
│   ├── templates/                 # Jinja2 HTML Şablonları
│   │   ├── auth/                  # Giriş ve Kayıt Sayfaları
│   │   ├── errors/                # Özel Hata Sayfaları (404.html, 500.html)
│   │   ├── main/                  # Dashboard, Detay, Eşleştirme Oyunu ve 3D Çalışma Sayfaları
│   │   └── base.html              # Ana Layout ve Tasarım İskeleti
│   │
│   ├── __init__.py                # App Factory (create_app) & DB İlklendirmesi
│   ├── models.py                  # Database Modelleri (User, Deck, Card)
│   ├── seeds.py                   # Çok Dilli Veritabanı Seeding (Seed & Backfill) Mekanizması
│   └── vocabulary_data.py         # 1500 Kelimelik Statik Sözlük Verisi (5 Dil, 15 Kategori)
│
├── docs/                          # Geliştirme Dokümanları
│   ├── ai-gunlugu.md              # Geliştirici AI Günlüğü
│   └── rapor.md                   # Proje Raporu (Bu dosya)
│
├── migrations/                    # Flask-Migrate (Alembic) Veritabanı Geçişleri
│
├── tests/                         # Otomatik Birim (Unit) Testleri
│   ├── __init__.py
│   ├── test_errors_and_pagination.py  # Sayfalama ve Hata Yönetimi Testleri
│   ├── test_language.py               # Dil Seçim ve Session Testleri
│   ├── test_seeding.py                # Otomatik Seed ve Backfill Mekanizması Testleri
│   └── test_study.py                  # 3D Çalışma ve Eşleştirme Oyunu Testleri
│
├── config.py                      # Çevresel Değişkenler ve Uygulama Ayarları
├── Dockerfile                     # Flask Servisi Docker Derleme Talimatları
├── docker-compose.yml             # Çoklu Konteyner (Web + PostgreSQL) Orkestrasyonu
├── .dockerignore                  # Docker İmajına Kopyalanmayacak Dosyalar Listesi
├── requirements.txt               # Proje Bağımlılıkları Listesi
└── run.py                         # Geliştirme Sunucusu Başlatma Betiği
```

### Ana Akışların Anlatımı

1. **Uygulamanın Ayağa Kalkması ve Seeding:** `run.py` dosyası çalıştırıldığında `app/__init__.py` içerisindeki `create_app()` fonksiyonu çağrılır. Başlangıçta veritabanı boşsa `app/seeds.py` içerisindeki `seed_db()` fonksiyonu tetiklenerek varsayılan `admin` kullanıcısı ve 5 dildeki 75 deste (1500 kart) sisteme kurulur. Eğer veritabanı doluysa sistemde mevcut olan tüm kullanıcıların eksik dil paketleri (backfill) taranarak otomatik tamamlanır.
2. **Kullanıcı Oturumu ve Dil Seçimi:** Giriş yapan kullanıcının oturumu `Flask-Login` tarafından yönetilir. Navbar üzerinde yer alan dinamik dil seçici (Dropdown), kullanıcının öğrenmek istediği dili değiştirir ve bu bilgiyi Flask Session'da (`learning_language`) saklar. Kullanıcı yeni bir dil seçtiğinde, eğer o dildeki desteler hesabında yoksa `seed_language_decks_for_user()` fonksiyonu arka planda anında çalışarak o dile ait 15 desteyi ve kartlarını kopyalar.
3. **Deste ve Kart Filtreleme:** Dashboard (Ana Sayfa) açıldığında kullanıcının tüm desteleri yerine, o an oturumda seçili olan dile ait desteler listelenir. Sorgu katmanında `Deck.name.like(f"{lang_name} - %")` şeklinde filtreleme yapılarak sadece ilgili dilin içeriği getirilir.
4. **Kelime Eşleştirme Oyunu:** `/deck/<deck_id>/game` rotasında çalışan oyun modülünde destedeki kelimelerden rastgele seçilen en fazla 8 kelime (16 kart) JS ile karıştırılarak 4x4 gridde gösterilir. CSS animasyonları (shake efekti vb.) ve `canvas-confetti` kütüphanesiyle zenginleştirilmiş kullanıcı arayüzü ile kelimelerin eşleştirilmesi sağlanır.
5. **Sayfalama (Pagination):** Dashboard sayfasında SQL yükünü hafifletmek amacıyla sayfa başına en fazla 10 deste listelenmekte, sayfalama bileşeni ile diğer sayfalar yüklenebilmektedir. Test süreçlerinde kararlılık için test destelerine yapay zaman damgası farkları eklenmiştir.

---

## 3. Vibe Coding Deneyimi: Ne İşe Yaradı, Nerede Zorlandık?

Geliştirme sürecinde benimsenen **Vibe Coding** yaklaşımı, geleneksel yazılım geliştirme pratiklerine kıyasla çok farklı bir verimlilik katmanı sunmuştur. Ajan ile adım adım eş programlama (pair programming) yapmanın avantajları ve bu süreçte karşılaşılan zorluklar şunlardır:

### Avantajlar ve Ne İşe Yaradığı
- **Hızlı Fikir Doğrulama ve Entegrasyon:** 1500 kelimelik statik sözlük verisinin entegre edilmesi, çoklu dil geçişlerinin session ile yönetilmesi ve sonrasında 3D kartlar ile eşleştirme oyununun kodlanması gibi aşamalar, yapay zeka ajanının hızlı kod üretimi sayesinde birkaç dakika içinde gerçekleştirilmiştir.
- **Dinamik JS Oyun Mantığı Oluşturma:** Eşleştirme oyununun 4x4 grid üzerinde, kartların durum takibini (seçili, doğru, yanlış, opacity-0) yapan JavaScript kodunun hatasız bir şekilde kurgulanması ve canvas-confetti kütüphanesinin CDN entegrasyonu son derece pürüzsüz ilerlemiştir.
- **Bilişsel Yükün Azalması:** Boilerplate kodların yazılması, test sınıflarının kurgulanması ve Docker konfigürasyonları gibi vakit alan mekanik işler ajana devredilmiş; geliştirici sadece oyun mekaniklerine, dil filtreleme mantığına ve arayüz detaylarına odaklanabilmiştir.

### Zorluk Yaşanılan Noktalar
- **Büyük Veri Yapılarıyla Çalışma:** 1500 kartlık `vocabulary_data.py` dosyası tek başına 176 KB boyutundadır. Ajanın bu kadar büyük veri dosyalarını taraması ve düzenlemesi yüksek token tüketimine sebep olmuş, dosya yapısının büyüklüğü kod değiştirme araçlarının limitlerini zorlamıştır. Ancak veri tabanı ayrıştırılarak statik modül haline getirilerek bu sorun aşılmıştır.
- **CSS ve Animasyon Kararsızlıkları:** Yanlış eşleşmelerdeki "kırmızı shake" efekti veya doğru eşleşmelerde kartların tamamen yok olması yerine gridin bozulmaması adına `opacity-0` ve `pointer-events-none` ile yerinde kalması kararları ajanın ilk denemelerinde ufak tefek kaymalara sebep olmuş, sonrasında CSS düzenlemeleri ile çözüme kavuşturulmuştur.

---

## 4. Antigravity Platformunda En Faydalı Bulunan İki Özellik

Platformun sunduğu geliştirme araçları arasından en yüksek katma değere sahip olan iki özellik ve nedenleri şunlardır:

### 1. Plan Modu (Planning Mode)
Uygulama aşamasına geçmeden önce ajanın bir **Uygulama Planı** (`implementation_plan.md`) hazırlaması ve kullanıcının onayına sunması, projenin başarısındaki en önemli faktördür.
- **Neden Faydalı?** Bu özellik, ajanın kontrolsüz bir şekilde kod tabanında değişiklik yapmasını engellemiştir. Özellikle çoklu dil altyapısı ve eşleştirme oyunu gibi karmaşık modüllerde hangi dosyaların değişeceği, hangi rotaların ekleneceği ve bu değişikliklerin mevcut birim testlerini nasıl etkileyeceği (örneğin sayfalama testine önek ekleme gereksinimi) önceden belirlenmiş ve mimari sapmalar engellenmiştir.

### 2. Eser ve Süreç Takip Yapısı (Artifacts & Walkthroughs)
Projenin her aşamasında güncellenen `task.md` ve `walkthrough.md` dosyalarının kullanımı, geliştirici ile ajan arasındaki koordinasyonu en üst düzeye çıkarmıştır.
- **Neden Faydalı?** `task.md` sayesinde hangi işlerin tamamlandığı, hangilerinin devam ettiği anlık olarak takip edilebilmiştir. `walkthrough.md` ise geliştirme sonunda yapılan değişikliklerin, test kodlarının ve sonuçlarının düzenli bir özetini sunmuştur. Bu yapı, projenin izlenebilirliğini artırmış ve teslim raporu hazırlamayı son derece kolaylaştırmıştır.

---

## 5. Ajanın Yakalayıp Düzelttiğimiz En Kritik Üç Hata

Geliştirme oturumlarında karşılaşılan ve veritabanı kararlılığını veya kullanıcı deneyimini doğrudan etkileyen üç kritik sorun ve çözümleri:

### 1. Çoklu Dil Seçiminde İtalyanca Destelerinin Kilitlenmesi Hatası (Session 8)
Kullanıcı üst bardan hangi dili seçerse seçsin, ana sayfada (dashboard) her zaman İtalyanca destelerinin listelenmesi sorunu yaşanmıştır.
- **Hata Nedeni:** Veritabanına kullanıcının seçtiği/seçeceği dillerin desteleri seed mekanizmasıyla kopyalanmaktaydı. Ancak ana sayfadaki desteleri çeken `/index` sorgusunda oturumda (Flask Session) seçili olan aktif dile göre filtreleme yapılmadığı için veritabanındaki tüm dillerin desteleri çekiliyordu. Sıralama `created_at desc` şeklinde olduğundan ve İtalyanca desteleri en son oluşturulduğundan, sayfalama sınırları nedeniyle ilk sayfanın tamamı İtalyanca desteleriyle doluyor ve sistem kilitlenmiş gibi görünüyordu.
- **Çözüm:** `/index` sorgusuna, o an oturumda seçili dil kodunun Türkçe adına göre (örn: 'en' -> 'İngilizce') `Deck.name.like(f"{lang_name} - %")` filtresi eklendi. Kullanıcı "Yeni Deste" eklediğinde de bu önek otomatik olarak eklendi. Arayüz şablonlarında render edilirken öneklerin temizlenmesi (`deck.name.replace(...)`) sağlanarak temiz bir görünüm elde edildi.

### 2. SQLite Eşzamanlılık ve Test Sıralama Hatası (Session 8)
Sayfalama testleri yazıldığında, döngü içerisinde hızlıca oluşturulan 12 test destesi SQLite veritabanına aynı milisaniyede kaydedildiği için `created_at desc` sıralaması belirsiz (non-deterministic) sonuçlar vermiş ve testlerin çökmesine yol açmıştır.
- **Düzeltme:** Test kurulum aşamasına Python `timedelta` kütüphanesi dahil edilerek her test destesi için aralarında 1'er dakika fark olan `created_at` zaman damgaları elle atanmıştır. Böylece veritabanı sıralamasının her test çalıştırılmasında tamamen kararlı ve tutarlı olması sağlanmıştır.

### 3. WTForms E-posta Doğrulama Kitaplığı Eksikliği (Session 5)
Ajan, kayıt formunu oluştururken `email-validator` kütüphanesinin çalışma ortamında kurulu olduğunu varsaymıştır. Kullanıcı kayıt olmaya çalıştığında sistem `500 Internal Server Error` vermiştir.
- **Düzeltme:** Hata günlükleri incelenerek eksik paket tespit edilmiş; yerel sanal ortama yüklenmiş ve `requirements.txt` güncellenerek üretim ortamında (Docker imajı dahil) bu hatanın tekrarlanması engellenmiştir.

---

## 6. AI Desteği Olmadan Proje Geliştirme Süresi Analizi

LingoRose projesinin sıfırdan, AI desteği olmadan tek bir geliştirici tarafından yapılması durumundaki zaman tahmini ve AI kullanımının sağladığı tasarruf analizi:

| Geliştirme Aşaması | AI Olmadan (Tahmini Süre) | AI ile (Gerçekleşen Süre) | Kazanılan Zaman Oranı |
| :--- | :---: | :---: | :---: |
| Proje Altyapısı & App Factory Kurulumu | 4 Saat | 15 Dakika | %93.7 |
| Auth & WTForms Validasyonları | 6 Saat | 30 Dakika | %91.6 |
| Deste/Kart CRUD Arayüzü & İlişkileri | 8 Saat | 45 Dakika | %90.6 |
| 3D Flip Card Modülü & Dinamik JS | 10 Saat | 60 Dakika | %90.0 |
| Çoklu Dil Seçimi & 1500 Kelime Seeding | 12 Saat | 45 Dakika | %93.7 |
| Kelime Eşleştirme Oyunu (Tailwind+JS) | 10 Saat | 45 Dakika | %92.5 |
| Sayfalama, Hata Sayfaları & Testler | 6 Saat | 45 Dakika | %87.5 |
| Docker & PostgreSQL Orkestrasyonu | 6 Saat | 30 Dakika | %91.6 |
| **Toplam Süre** | **62 Saat (8 İş Günü)** | **~5.25 Saat** | **%91.5 Tasarruf** |

### Analiz Sonucu
Geleneksel yöntemlerle yaklaşık 1.5 haftalık (62 saatlik) tam mesai gerektiren bu proje, AI asistanının kod üretimi, debugging yetenekleri ve hazır arayüz şablonları sunması sayesinde **yaklaşık 5.25 saat içinde** tüm testleri başarıyla geçecek şekilde tamamlanmıştır. Bu durum, yazılım süreçlerinde yapay zekanın geliştirme hızını yaklaşık 12 kat artırdığını doğrulamaktadır.

---

## 7. Projenin Sürdürülebilirliği ve Sonraki Adımlar

LingoRose projesinin gelecekte daha kapsamlı ve ticari olarak sürdürülebilir bir platform haline gelebilmesi için planlanan sonraki aşamalar şunlardır:

1. **Aralıklı Tekrarlama Sistemi (Spaced Repetition System - SRS):** Öğrenme verimliliğini maksimize etmek için SuperMemo (SM-2) algoritması entegre edilebilir. Kullanıcının "Tekrar Et" veya "Öğrendim" yanıtlarına göre, kelimeler hafıza eğrisine göre optimize edilmiş zaman aralıklarıyla (1 gün, 3 gün, 7 gün sonra) tekrar kullanıcının karşısına çıkarılır.
2. **Yapay Zeka Destekli Sesli Okuma (Audio Pronunciation):** Kelime kartlarına ve oyun arayüzüne, kelimelerin doğru telaffuzlarını dinletebilecek bir Metinden Sese (Text-to-Speech) API entegrasyonu yapılarak işitsel öğrenme desteklenebilir.
3. **Kapsamlı İstatistik ve Grafik Modülü:** Kullanıcının günlük çalışma sürelerini, öğrendiği kelime sayılarını ve başarı oranlarını `Chart.js` kütüphanesiyle görselleştiren gelişmiş bir grafik paneli (Dashboard Analytics) eklenebilir.
4. **Sosyal Rekabet ve Liderlik Tablosu (Leaderboard):** Kullanıcıların kelime eşleştirme oyunundaki bitirme sürelerine göre birbirleriyle yarışabilecekleri, puan toplayıp haftalık liderlik tablolarında listelenebilecekleri bir sosyal oyunlaştırma katmanı eklenebilir.

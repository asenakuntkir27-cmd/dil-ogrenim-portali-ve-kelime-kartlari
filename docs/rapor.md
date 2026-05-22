# LingoRose Dil Öğrenim Portali ve Kelime Kartları Proje Raporu

---

## 1. Projenin Amacı ve Genel Özeti

Yabancı bir dil öğreniminde en büyük zorluklardan biri, yeni öğrenilen kelimelerin hafızada kalıcı hale getirilmesidir. Klasik ezberleme yöntemleri, öğreniciyi aktif bir süreç içerisine dahil etmediğinden verimsiz kalmaktadır. **LingoRose**, bu problemi çözmek amacıyla geliştirilmiş etkileşimli bir web tabanlı dil öğrenim portalidir. 

Uygulamanın temel amacı; kullanıcıların kendi çalışma alanlarını özelleştirerek kelime desteleri (decks) oluşturabilmesi, bu destelere diledikleri kelimeleri, anlamlarını ve örnek cümlelerini ekleyebilmesi ve ardından premium bir kullanıcı deneyimi sunan **3D Kart Çevirme (Quiz) Modülü** sayesinde kelimeleri aktif olarak çalışabilmesidir. Kullanıcılar kartların ön yüzündeki yabancı kelimeyi görüp anlamını tahmin etmeye çalışmakta, ardından karta tıklayarak arka yüzündeki anlamını ve örnek cümlesini görüntülemektedir. Çalışma esnasında her kelime için "Öğrendim" veya "Tekrar Et" işaretlemesi yapılarak, çalışma sonunda kişiselleştirilmiş bir başarı skoru elde edilmektedir.

Sistem, modern bir koyu tema (dark mode) üzerine kurulu, pembe ve mor gradyanlarla desteklenen estetik bir tasarım dili (**LingoRose**) sunmakta; hem masaüstü hem de mobil cihazlarda kusursuz bir kullanıcı deneyimi (UX) hedeflemektedir.

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
│   │   └── routes.py              # Main Rotaları ve Hata İşleyiciler (404/500)
│   │
│   ├── static/                    # Statik Dosyalar (CSS, JS, Resimler)
│   │
│   ├── templates/                 # Jinja2 HTML Şablonları
│   │   ├── auth/                  # Giriş ve Kayıt Sayfaları
│   │   ├── errors/                # Özel Hata Sayfaları (404.html, 500.html)
│   │   ├── main/                  # Dashboard, Detay ve 3D Çalışma Sayfaları
│   │   └── base.html              # Ana Layout ve Tasarım İskeleti
│   │
│   ├── __init__.py                # App Factory (create_app) & DB İlklendirmesi
│   └── models.py                  # Database Modelleri (User, Deck, Card)
│
├── docs/                          # Geliştirme Dokümanları
│   ├── ai-gunlugu.md              # Geliştirici AI Günlüğü
│   └── rapor.md                   # Proje Raporu (Bu dosya)
│
├── migrations/                    # Flask-Migrate (Alembic) Veritabanı Geçişleri
│
├── tests/                         # Otomatik Birim (Unit) Testleri
│   ├── __init__.py
│   ├── test_errors_and_pagination.py
│   └── test_study.py
│
├── config.py                      # Çevresel Değişkenler ve Uygulama Ayarları
├── Dockerfile                     # Flask Servisi Docker Derleme Talimatları
├── docker-compose.yml             # Çoklu Konteyner (Web + PostgreSQL) Orkestrasyonu
├── .dockerignore                  # Docker İmajına Kopyalanmayacak Dosyalar Listesi
├── requirements.txt               # Proje Bağımlılıkları Listesi
└── run.py                         # Geliştirme Sunucusu Başlatma Betiği
```

### Ana Akışların Anlatımı

1. **Uygulamanın Ayağa Kalkması:** `run.py` dosyası çalıştırıldığında veya Docker konteyneri başlatıldığında `app/__init__.py` içerisindeki `create_app()` fonksiyonu çağrılır. Bu fonksiyon veritabanını (`SQLAlchemy`), veritabanı göç aracını (`Migrate`) ve oturum yöneticisini (`LoginManager`) başlatır. Ardından `auth` ve `main` blueprint'lerini uygulamaya dahil eder.
2. **Kullanıcı Kaydı ve Girişi:** Kullanıcılar `/auth/register` üzerinden güvenli parola hashleme mekanizması (Werkzeug) ile kaydolurlar. Parolalar veritabanında asla açık metin olarak tutulmaz. Giriş yapan kullanıcının oturumu tarayıcı çerezleri vasıtasıyla `Flask-Login` tarafından yönetilir.
3. **Deste ve Kart Yönetimi:** Giriş yapmış kullanıcılar kendi panellerinde (Dashboard) yeni desteler oluşturabilir. Destelerin detay sayfalarında veritabanı seviyesinde sahiplik kontrolü yapılır; böylece hiçbir kullanıcı bir başkasının destesini görüntüleyemez veya değiştiremez.
4. **Çalışma Modülü:** Kelime çalışması başlatıldığında, JavaScript tabanlı dinamik arayüz çalışılacak kart dizisini yükler. 3D CSS efektleri ile kart döndürülür ve kullanıcının verdiği yanıtlara göre ilerleme barı anlık güncellenir.
5. **Sayfalama (Pagination):** Dashboard sayfasında SQL yükünü hafifletmek amacıyla Flask-SQLAlchemy'nin sayfalama mekanizması kullanılmıştır. Sayfa başına en fazla 10 deste listelenmekte, geri kalan desteler şık sayfalama butonları aracılığıyla yüklenebilmektedir.

---

## 3. Vibe Coding Deneyimi: Ne İşe Yaradı, Nerede Zorlandık?

Geliştirme sürecinde benimsenen **Vibe Coding** yaklaşımı, geleneksel yazılım geliştirme pratiklerine kıyasla çok farklı bir verimlilik katmanı sunmuştur. Ajan ile adım adım eş programlama (pair programming) yapmanın avantajları ve bu süreçte karşılaşılan zorluklar şunlardır:

### Avantajlar ve Ne İşe Yaradığı
- **Hızlı Fikir Doğrulama:** Arayüzün mor-pembe temaya dönüştürülmesi veya 3D kart çevirme mantığının geliştirilmesi gibi fikirler, CSS ve HTML kodlarının manuel yazımına kıyasla çok hızlı şekilde hayata geçirilmiştir.
- **Hata Ayıklama (Debugging) Hızı:** Geliştirme ortamında kütüphane eksikliklerinden veya SQLite eşzamanlılık problemlerinden kaynaklanan 500 hataları, ajan tarafından anında analiz edilerek nokta atışı çözümlerle düzeltilmiştir.
- **Bilişsel Yükün Azalması:** Geliştirici, boilerplate kodları yazmakla vakit kaybetmek yerine sistem tasarımı, mimari kararlar ve kullanıcı deneyimi (UX) detaylarına odaklanabilmiştir.

### Zorluk Yaşanılan Noktalar
- **Bağlam Takibi (Context Window Limit):** Proje büyüdükçe ve dosya sayısı arttıkça, ajanın geçmiş konuşmalardaki tasarım kararlarını (örneğin renk kodlarının tam pembe/mor tonları) hatırlaması zorlaşabilmiştir. Bu durum, şablonlar arasında küçük stil uyumsuzluklarına yol açmıştır ancak sonrasında stil şablonları taranarak düzeltilmiştir.
- **SQLAlchemy Sürüm Farklılıkları:** SQLAlchemy 2.0 ile gelen modern sorgu yazım şekli ile internetteki eski dokümanlarda yer alan 1.x tarzı sorgu yapıları arasında ajanın bazen kararsız kalması, kod yapısında ufak düzeltmeler yapılmasını gerektirmiştir.

---

## 4. Antigravity Platformunda En Faydalı Bulunan İki Özellik

Platformun sunduğu geliştirme araçları arasından en yüksek katma değere sahip olan iki özellik ve nedenleri şunlardır:

### 1. Plan Modu (Planning Mode)
Uygulama aşamasına geçmeden önce ajanın bir **Uygulama Planı** (`implementation_plan.md`) hazırlaması ve kullanıcının onayına sunması, projenin başarısındaki en önemli faktördür.
- **Neden Faydalı?** Bu özellik, ajanın kontrolsüz bir şekilde kod tabanında değişiklik yapmasını engellemiştir. Hangi dosyaların değişeceği, yeni eklenecek şablonlar ve doğrulama yöntemleri kod yazılmadan önce netleştirilmiş; böylece olası tasarım hataları daha fikir aşamasındayken elenmiştir.

### 2. Eser ve Süreç Takip Yapısı (Artifacts & Walkthroughs)
Projenin her aşamasında güncellenen `task.md` ve `walkthrough.md` dosyalarının kullanımı, geliştirici ile ajan arasındaki koordinasyonu en üst düzeye çıkarmıştır.
- **Neden Faydalı?** `task.md` sayesinde hangi işlerin tamamlandığı, hangilerinin devam ettiği görsel olarak takip edilebilmiştir. `walkthrough.md` ise geliştirme sonunda yapılan değişikliklerin, test kodlarının ve sonuçlarının düzenli bir özetini sunmuştur. Bu yapı, projenin izlenebilirliğini artırmış ve teslim raporu hazırlamayı son derece kolaylaştırmıştır.

---

## 5. Ajanın Yakalayıp Düzelttiğimiz En Kritik Üç Hata

Geliştirme oturumlarında karşılaşılan ve veritabanı kararlılığını veya kullanıcı deneyimini doğrudan etkileyen üç kritik sorun ve çözümleri:

### 1. SQLAlchemy 2.0 Standartları Uyumsuzluğu
Uygulama ilk kurulduğunda, ajan veritabanı sorguları için eski tip SQLAlchemy 1.x sözdizimini (`db.session.query(Deck)...`) önermiştir.
- **Düzeltme:** Projenin Flask 3.x ve modern SQLAlchemy tip tanımlamalarıyla uyumlu olması için sorgular yeni stile çevrilmiştir. Rotalardaki sorguların tamamı `sa.select` ve `db.session.scalars(...)` kullanacak şekilde modernize edilmiştir.

### 2. WTForms E-posta Doğrulama Kitaplığı Eksikliği (Session 5)
Ajan, kayıt formunu oluştururken `email-validator` kütüphanesinin çalışma ortamında kurulu olduğunu varsaymıştır. Kullanıcı kayıt olmaya çalıştığında sistem `500 Internal Server Error` vermiştir.
- **Düzeltme:** Hata günlükleri incelenerek eksik paket tespit edilmiş; yerel sanal ortama yüklenmiş ve `requirements.txt` güncellenerek üretim ortamında (Docker imajı dahil) bu hatanın tekrarlanması engellenmiştir.

### 3. SQLite Eşzamanlılık ve Test Sıralama Hatası (Session 8)
Sayfalama testleri yazıldığında, döngü içerisinde hızlıca oluşturulan 12 test destesi SQLite veritabanına aynı milisaniyede kaydedildiği için `created_at desc` sıralaması belirsiz (non-deterministic) sonuçlar vermiş ve testlerin çökmesine yol açmıştır.
- **Düzeltme:** Test kurulum aşamasına Python `timedelta` kütüphanesi dahil edilerek her test destesi için aralarında 1'er dakika fark olan `created_at` zaman damgaları elle atanmıştır. Böylece veritabanı sıralamasının her test çalıştırılmasında tamamen kararlı ve tutarlı olması sağlanmıştır.

---

## 6. AI Desteği Olmadan Proje Geliştirme Süresi Analizi

LingoRose projesinin sıfırdan, AI desteği olmadan tek bir geliştirici tarafından yapılması durumundaki zaman tahmini ve AI kullanımının sağladığı tasarruf analizi:

| Geliştirme Aşaması | AI Olmadan (Tahmini Süre) | AI ile (Gerçekleşen Süre) | Kazanılan Zaman Oranı |
| :--- | :---: | :---: | :---: |
| Proje Altyapısı & App Factory Kurulumu | 4 Saat | 15 Dakika | %93.7 |
| Auth & WTForms Validasyonları | 6 Saat | 30 Dakika | %91.6 |
| Deste/Kart CRUD Arayüzü & İlişkileri | 8 Saat | 45 Dakika | %90.6 |
| 3D Flip Card Modülü & Dinamik JS | 10 Saat | 60 Dakika | %90.0 |
| Sayfalama, Hata Sayfaları & Testler | 6 Saat | 45 Dakika | %87.5 |
| Docker & PostgreSQL Orkestrasyonu | 6 Saat | 30 Dakika | %91.6 |
| **Toplam Süre** | **40 Saat (5 İş Günü)** | **~3.75 Saat** | **%90.6 Tasarruf** |

### Analiz Sonucu
Geleneksel yöntemlerle yaklaşık 1 haftalık (40 saatlik) tam mesai gerektiren bu proje, AI asistanının kod üretimi, debugging yetenekleri ve hazır arayüz şablonları sunması sayesinde **yaklaşık 4 saat içinde** tüm testleri başarıyla geçecek şekilde tamamlanmıştır. Bu durum, yazılım süreçlerinde yapay zekanın geliştirme hızını yaklaşık 10 kat artırdığını doğrulamaktadır.

---

## 7. Projenin Sürdürülebilirliği ve Sonraki Adımlar

LingoRose projesinin gelecekte daha kapsamlı ve ticari olarak sürdürülebilir bir platform haline gelebilmesi için planlanan sonraki aşamalar şunlardır:

1. **Aralıklı Tekrarlama Sistemi (Spaced Repetition System - SRS):** Öğrenme verimliliğini maksimize etmek için SuperMemo (SM-2) algoritması entegre edilebilir. Kullanıcının "Tekrar Et" veya "Öğrendim" yanıtlarına göre, kelimeler hafıza eğrisine göre optimize edilmiş zaman aralıklarıyla (1 gün, 3 gün, 7 gün sonra) tekrar kullanıcının karşısına çıkarılır.
2. **Kapsamlı İstatistik ve Grafik Modülü:** Kullanıcının günlük çalışma sürelerini, öğrendiği kelime sayılarını ve başarı oranlarını `Chart.js` kütüphanesiyle görselleştiren gelişmiş bir grafik paneli (Dashboard Analytics) eklenebilir.
3. **Flask-Mail ile Şifre Sıfırlama ve E-posta Doğrulama:** Güvenliği artırmak adına kullanıcıların kayıt sonrasında e-posta doğrulaması yapması ve şifrelerini unuttuklarında güvenli jetonlar (tokens) aracılığıyla şifre sıfırlama bağlantısı alabilmeleri sağlanabilir.
4. **Çoklu Dil Seçeneği ve Hazır Kütüphaneler:** Kullanıcıların kelimeleri tek tek elle girmesi yerine; sistemde önceden hazırlanmış "A1 İngilizce Kelimeler", "Sık Kullanılan İspanyolca Fiiller" gibi hazır veri setlerini tek tıkla kendi destelerine kopyalayabilme özelliği sunulabilir.

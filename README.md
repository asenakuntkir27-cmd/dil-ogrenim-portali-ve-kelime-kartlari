# LingoRose: Oyunlaştırılmış Dil Öğrenim Portali ve Kelime Kartları Platformu

[![Flask](https://img.shields.io/badge/FLASK-v3.0+-004455?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/TAILWIND_CSS-v3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/SQLALCHEMY-v2.0-CC2927?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/DOCKER-READY-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/83_TESTS-PASSED-4CAF50?style=for-the-badge&logo=github-actions&logoColor=white)](https://docs.python.org/3/library/unittest.html)

---

## Proje Tanıtım ve Demo Videosu
Projenin tüm fonksiyonel akışlarını, güvenlik mekanizmalarını, çift tema yapısını ve 83 birim testlik test süitini içeren detaylı sunum ve demo videosuna aşağıdaki bağlantı üzerinden erişilebilir:

👉 [LingoRose Proje Demo Videosu (Google Drive)](https://drive.google.com/file/d/1vGbzEP5YyxEGtwEXq2zZE1HK74Q5A2E_/view?usp=drivesdk)

---

LingoRose, yabancı dil öğreniminde kelime dağarcığını kalıcı hale getirmek amacıyla tasarlanmış, gelişmiş oyunlaştırma mekanikleriyle desteklenen, web tabanlı interaktif bir dil öğrenim portalıdır. Modern yazılım mühendisliği prensipleri ve yüksek erişilebilirlik standartları gözetilerek geliştirilen platform; çok dilli hazır kelime paketleri, istatistiksel analiz grafikeri, çift tema desteği ve kendi kendini onarabilen veritabanı motoru gibi kurumsal düzeyde özellikler barındırmaktadır. Proje, üretim ortamı standartlarında Dockerize edilmiş olup tam kapsamlı bir otomatik birim test süitiyle kararlı hale getirilmiştir.

---

## 1. Temel Mimari ve Kullanılan Teknolojiler

### Backend
Platform, Python 3.10+ programlama dili ve Flask 3.x mikro-çerçevesi (micro-framework) üzerine inşa edilmiştir. Kod tabanının ölçeklenebilirliğini, modülerliğini ve sürdürülebilirliğini sağlamak adına **Application Factory Pattern (Uygulama Fabrikası Deseni)** uygulanmıştır. Uygulama başlatma süreçleri `create_app` fonksiyonu altında toplanarak konfigürasyon bağımsızlığı kazanmıştır. Uygulama rotaları, form sınıfları ve iş mantığı mimarisi, mantıksal katmanlara ayrılarak Blueprint yapılarıyla organize edilmiştir:
-   **Auth Blueprint (`app/auth`):** Kimlik doğrulama, güvenli parola sıfırlama ve e-posta güncelleme akışlarını yönetir.
-   **Main Blueprint (`app/main`):** Dashboard, kelime kartı işlemleri, kelime oyunları modülleri ve analiz paneli rotalarını barındırır.

### ORM ve Veritabanı
Veritabanı erişim katmanı ve nesne-ilişkisel eşleme işlemleri için modern **SQLAlchemy 2.0** standartları (tip güvenli `Mapped` ve `mapped_column` bildirimleri) kullanılmıştır. SQLite veritabanı altyapısı üzerinde çalışan sistemde, eşzamanlı veri erişim problemlerini ve kilitlenmeleri (database locks) önlemek amacıyla **Scoped Session** mimarisi entegre edilmiştir. Bu sayede her iş parçacığının (thread) kendi veritabanı oturumunu izole bir şekilde yönetmesi sağlanarak veri tutarlılığı maksimum düzeye çıkarılmıştır.

### Frontend
Arayüz bileşenlerinde herhangi bir ağır JavaScript çerçevesine bağımlı kalınmaksızın, yüksek performans sunan **Tailwind CSS** ve saf JavaScript (Vanilla JS) mimarisi tercih edilmiştir. Görsel tasarım dilinde modern ve derinlik hissi uyandıran yarı şeffaf katmanlar, bulanıklaştırma efektleri ve ince kenar sınırlarıyla harmanlanmış **Glassmorphism** stili benimsenmiştir. Tema geçişleri ve animasyonlar CSS 3D Transforms ve geçiş efektleri ile pürüzsüzleştirilmiştir.

---

## 2. Gelişmiş Fonksiyonel Özellikler ve Güvenlik Mekanizmaları

### Kriptografik Kimlik Doğrulama ve Oturum Yönetimi
Sistem oturum güvenliği **Flask-Login** kütüphanesiyle yönetilmektedir. Kullanıcı şifreleri veritabanına açık metin olarak kaydedilmemekte; **Werkzeug** güvenlik kütüphanesinin kriptografik hashleme algoritmaları (`pbkdf2:sha256`) kullanılarak tek yönlü şifrelenmektedir. Giriş denetimlerinde şifre hash doğrulaması yapılarak oturumlar sunucu tarafında güvenli bir şekilde izole edilmektedir.

### Zamana Duyarlı Şifre Sıfırlama
Parolasını unutan kullanıcılar için **itsdangerous** kütüphanesi kullanılarak kriptografik ve zamana duyarlı şifre sıfırlama token altyapısı kurulmuştur. 
-   **Token Süresi:** Oluşturulan sıfırlama bağlantıları güvenlik gereği tam olarak **1 saat (3600 saniye)** geçerlidir.
-   **Arayüz Simülasyonu:** E-posta sunucusu bağımlılığını simüle etmek amacıyla üretilen benzersiz şifre sıfırlama bağlantısı (`/reset-password/<token>`), yerel ortamda doğrudan sistem arayüzünde (`reset_password_requested.html`) gösterilerek test ve doğrulama süreçleri kolaylaştırılmıştır.

### Güvenli E-posta Değiştirme Sistemi
Kullanıcı profil ayarları panelinden e-posta adresini güncellemek istediğinde veri güvenliğini sağlamak adına çift aşamalı doğrulama uygulanır:
-   **Giriş Güvenliği:** Profil sayfasındaki mevcut e-posta alanı salt okunurdur (`readonly`). Değişiklik formunda kullanıcının güncel şifresini girmesi zorunludur.
-   **Kriptografik Onay Süreci:** Girilen yeni adrese `itsdangerous` ile şifrelenmiş bir onay tokenı içeren bağlantı (`/confirm-email-change/<token>`) gönderilir. Bağlantı **24 saatlik** güvenlik onay süresine sahiptir. Kullanıcı bu bağlantıya tıkladığında veritabanı düzeyinde e-posta benzersizlik kontrolü (unique constraint) yapılır ve onaylanırsa güncelleme işlemi tamamlanır.

### Çift Tema ve Kontrast Optimizasyonu
Uygulama, aydınlık ve karanlık olmak üzere iki farklı görsel tema sunar. Her iki tema da Web İçeriği Erişilebilirlik Kılavuzu (WCAG) kontrast standartlarına göre optimize edilmiştir:
-   **Aydınlık Mod (`data-theme="light"`):** Arka planda pastel gül kurusu tonları kullanılırken, metinlerin okunabilirliğini garanti altına almak için başlık elemanları koyu füme (`#0F172A`), gövde metinleri ise koyu gri (`#1E293B`) olarak sabitlenmiştir. Kirlilik ve parlama yaratan neon gölgeler aydınlık modda tamamen pasifize edilmiştir.
-   **Karanlık Mod:** Koyu gri ve siyah zeminler üzerinde neon mor/pembe gradyanlar barındırır. Metin okunabilirliği için etiketler ve girdiler açık gri (`#F1F5F9`) ve saf beyaz (`#FFFFFF`) renk kodlarıyla yüksek kontrastlı hale getirilmiştir.

### Gelişmiş Arama ve Filtreleme Motoru
Ana dashboard üzerinde desteler ve kelimeler arasında gerçek zamanlı, milisaniyeler düzeyinde sonuç dönen bir arama kutusu (`#vocab-search-input`) yer almaktadır. Girdi alanındaki zemin rengi ile yazı renginin çakışıp görünmez olması hatası giderilmiş; karanlık modda girdi zemini yarı şeffaf koyu renk (`rgba(9, 9, 11, 0.7)`), yazı rengi ise saf beyaz yapılarak kontrast dengesi kurulmuştur.

### Harici API Entegrasyonlu Inline Çeviri Sistemi
Kullanıcıların sayfadaki herhangi bir cümleyi veya kelimeyi imleçle seçmesi (highlight) durumunda koordinatları dinamik hesaplanarak fırlayan neon kenarlıklı glassmorphic bir **Tooltip** penceresi tasarlanmıştır. 
-   **API Yapısı:** Çeviri işlemleri sunucu tarafında öncelikli olarak **MyMemory API** üzerinden gerçekleştirilir.
-   **Failover (Yedeklilik):** MyMemory servisinde hata oluşması durumunda sistem otomatik olarak **Lingva API** yedek sunucusuna (failover) yönlenir.
-   **Kullanılabilirlik:** Tooltip ekranı dışında herhangi bir boş alana tıklandığında pencere JavaScript animasyonuyla otomatik olarak kapanır.

### Özel Hata Sayfası Yönetimi
Sistem genelindeki geçersiz rotalarda (`404 Not Found`) kullanıcıyı statik bir hata mesajı yerine eğlenceli bir arayüz karşılar. 404 hata sayfasına gömülü olan mini oyunda, veritabanından dinamik olarak 1 doğru kelime ve 2 yanlış çeldirici çekilerek kullanıcıya kelime eşleştirme bulmacası sunulur. Doğru şık tıklandığında buton yeşil parıldar, `canvas-confetti` ile ekran konfetilerle doldurulur ve ana sayfaya dönüş butonu belirir; yanlış şıkta ise shake (titreme) animasyonu tetiklenir.

### Kendi Kendini İyileştiren Veritabanı Motoru (Auto-Recovery)
İlk kurulumda, farklı işletim sistemlerine taşımalarda ya da veritabanı sürüm uyumsuzluklarında oluşabilecek şema hatalarını çözmek amacıyla **kurşun geçirmez bir auto-recovery mekanizması** geliştirilmiştir. Sistem açılırken SQLAlchemy Inspector vasıtasıyla `User`, `Deck`, `Card` ve `Score` tablolarının varlığını ve şema bütünlüğünü sorgular. Herhangi bir tabloda eksiklik veya tutarsızlık algılanırsa:
1.  Askıda kalan tüm veritabanı oturum kilitlenmelerini çözmek adına scoped session tamamen temizlenir (`db.session.remove()`).
2.  Mevcut tüm bozuk yapılar silinir (`db.drop_all()`).
3.  Sağlıklı tablo şemaları sıfırdan oluşturulur (`db.create_all()`).
4.  Sistem `seeds.py` üzerinden 5 dilde toplam 1500 kelimelik başlangıç sözlük veri setini otomatik olarak yeniden tohumlar (`seed_db()`).

---

## 3. Test Stratejisi ve Kararlılık Kontrolleri

LingoRose kod tabanının kararlılığı, Python `unittest` kütüphanesiyle yazılmış ve tüm kritik iş kurallarını kapsayan bir test süiti ile korunmaktadır. Testler yetkilendirme, veri tohumlama, sayfalama, 404 bulmaca motoru, başarı başarımları ve satır içi çeviri gibi tüm servis katmanlarını doğrulamaktadır. Harici API'lere bağımlılığı kesmek amacıyla çeviri HTTP istekleri mocklanmıştır.

Otomatik test süiti başarı çıktısı aşağıdaki şekildedir:

```text
Ran 83 tests in 41.212s

OK
```

---

## 4. Kurulum ve Dağıtım (Deployment) Verileri

Projenin üretim ortamında platform bağımsız ve izole bir şekilde çalıştırılması için Docker ve Docker Compose entegrasyonu mevcuttur. PostgreSQL 15 veritabanı servisi `healthcheck` mekanizmasıyla izlenmekte, veritabanı hazır olmadan web servisinin ayağa kalkması engellenmektedir.

### Docker ile Çalıştırma
Sistemi tek komutla derleyip çalıştırmak için kök dizinde aşağıdaki komutu yürütün:

```bash
docker-compose up --build
```

---

## 5. Proje Yönetimi ve Geliştirme Metodolojisi

Platform geliştirme sürecinde doğal dil yönlendirmeleriyle kod yazımı prensibine dayanan **Vibe Coding** metodolojisi uygulanmıştır. 
-   **Sürüm Kontrolü:** Proje geçmişinde toplam **69 adet** anlamlı sürüm kaydı (git commit) bulunmaktadır.
-   **Dokümantasyon Senkronizasyonu:** Geliştirme esnasında karşılaşılan tüm teknik zorluklar ve ajanın düzelttiği kritik hatalar `docs/ai-gunlugu.md` içerisinde kronolojik olarak raporlanmış; projenin son çıktısı akademik standartlara uygun olarak `docs/rapor.md` içerisinde belgelenmiştir.

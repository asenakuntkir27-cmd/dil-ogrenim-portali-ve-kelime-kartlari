# LingoRose Proje Sonu Teknik Tasarım Raporu

**Proje Başlığı:** LingoRose Dil Öğrenim Portalı ve Kelime Kartları  

### Öğrenci Bilgileri
* **Adı Soyadı:** Ayşe Sena Kuntkır  
* **Öğrenci Numarası:** 24380102030  
* **Bölüm:** Bilişim Güvenliği Teknolojileri  
* **Sınıf / Şube:** 1. Sınıf / 2. Şube  
* **Teslim Tarihi:** 1 Haziran 2026  

---

## 1. Projenin Amacı ve Hedefleri

Yabancı dil öğreniminde kelimelerin kalıcı hafızaya aktarılamaması ve öğrenme sürecinin tekdüzeliği en büyük engellerdendir. LingoRose, bu sorunları ortadan kaldırmak için etkileşimli, oyunlaştırılmış ve kullanıcı dostu bir dil öğrenim deneyimi sunmak amacıyla tasarlanmıştır. Uygulama; İngilizce, Almanca, İspanyolca, Fransızca ve İtalyanca olmak üzere 5 farklı dili destekler. Kayıt olan her kullanıcının hesabına, 15 temel kategoride her birinde en az 20 kelime bulunan toplam 1500 kelimelik zengin bir başlangıç veri seti (seed data) otomatik olarak aktarılır. Kullanıcılar ayrıca kendi çalışma destelerini ve kelime kartlarını serbestçe oluşturabilirler. 

Öğrenim sürecini pekiştirmek için tasarlanan 3D kart çevirme modülü, kelime eşleştirme oyunu, kelime tetrisi (Word Drop), cümle kurma (Sentence Builder), hafıza kartları (Memory Flip) ve boşluk doldurma (Fill in the Blanks) olmak üzere toplam 6 farklı çalışma ve oyun modülü kullanıcılara sunulmuştur. Bu oyun modüllerine ek olarak, sisteme 12 üniteden oluşan kurumsal "A1 Seviye Kurs Müfredatı" entegre edilmiş; her ünite kendi içinde "Konu Anlatımı" ve "Kelime Çalışması" sunan çift sekmeli bir mimariyle kodlanmıştır. Ayrıca, gelecekteki B ve C seviyelerine de kolayca ölçeklenebilecek şekilde tasarlanan, örnek cümleli ve Web Speech API entegrasyonu sayesinde sesli telaffuz destekli alfabetik "Sözlük" (Dictionary) modülü platforma kazandırılmıştır. Arayüzün tüm bu fonksiyonları, mobil ve masaüstü cihazlar için tam responsive ve esnek (Full Width) grid yapısıyla optimize edilmiştir.

---

## 2. Kullanılan Teknolojiler ve Mimari Tasarım

LingoRose, Python tabanlı mikro-framework olan Flask 3.x üzerine kurulmuştur. Uygulama mimarisinde sürdürülebilirlik, temiz kod prensipleri ve genişletilebilirlik hedeflenerek Application Factory Pattern (Uygulama Fabrikası Deseni) kullanılmıştır. Uygulama başlatma süreçleri `create_app` fonksiyonu altında merkezileştirilmiştir. Rotalar ve formlar mantıksal modüllere ayrılacak şekilde Blueprint yapısı ile yapılandırılmıştır. Kullanıcı kimlik doğrulama, şifre yenileme ve profil işlemleri için `auth` Blueprint'i; kelime desteleri, oyunlar, analiz paneli ve ana dashboard akışları için ise `main` Blueprint'i geliştirilmiştir. 

Bölümümüzün odak noktası olan siber güvenlik katmanı kapsamında, tarayıcı düzeyinde siber saldırıları (XSS, Clickjacking, MIME Sniffing vb.) önlemek adına **Flask-Talisman** kütüphanesi sisteme entegre edilmiştir. Ayrıca, kayıt formunda (Register Form) kurumsal düzeyde siber güvenlik kurallarına uygun Regex tabanlı **"Güçlü Parola Politikası Doğrulaması"** uygulanmıştır. Veritabanı yönetiminde modern SQLAlchemy 2.0 standartları benimsenmiş ve veri modeli sorgularının tamamı tip güvenli, performanslı ve sürdürülebilir SQL ifadelerine dönüştürülmüştür. Çevresel yapılandırmalar `config.py` ve `.env` üzerinden yönetilirken, uygulama Docker ve PostgreSQL orkestrasyonu sayesinde üretim ortamına hazır (production-ready) hale getirilmiştir.

---

## 3. Veritabanı Şeması ve İlişkileri

Uygulamanın ilişkisel veri modeli, modern SQLAlchemy 2.0 stili (`Mapped`, `mapped_column`) kullanılarak `app/models.py` dosyasında tanımlanmıştır. Veritabanı şeması aşağıdaki temel tablolar ve ilişkiler etrafında şekillenmiştir:

*   **User (Kullanıcı):** Kullanıcı adı, e-posta, parola hash bilgileri, streak (ardışık gün) takibi, günlük hedef ve günlük ilerleme puanlarını barındırır.
*   **Deck (Deste):** Kullanıcıya ait kelime gruplarını temsil eder. `user_id` yabancı anahtarı (ForeignKey) ile `User` tablosuna bağlıdır. Ayrıca, destenin ana kategori mi yoksa sözlük destesi mi olduğunu belirleyen `deck_type` alanını barındırır.
*   **Card (Kelime Kartı):** Kelime, anlamı ve örnek cümle bilgilerini tutar. `deck_id` yabancı anahtarı ile ilişkili olduğu `Deck` tablosuna bağlıdır.
*   **Score (Skor):** Kullanıcıların oyun modüllerinde elde ettikleri puanları ve oynanma tarihlerini kaydeder. `user_id` üzerinden `User` tablosu ile ilişkilidir.

İlişkisel yapı bire-çok (One-to-Many) mantığına dayanmaktadır. Bir kullanıcının birden fazla destesi ve skoru olabilir; bir destenin ise birden fazla kelime kartı bulunur. Modeller arasındaki bu ilişkiler `cascade="all, delete-orphan"` parametresi ile tanımlanarak, bir üst kayıt (örneğin bir deste veya kullanıcı) silindiğinde ilişkili tüm alt verilerin (kartlar, skorlar) veritabanında yetim kalmadan otomatik olarak temizlenmesi sağlanmıştır.

| Tablo Adı | Birincil Anahtar | İlişkili Olduğu Tablo | İlişki Tipi | Cascade Özelliği |
| :--- | :--- | :--- | :--- | :--- |
| **User** | `id` | - | - | - |
| **Deck** | `id` | `User` (`user_id`) | Çoktan Bire (Many-to-One) | `all, delete-orphan` |
| **Card** | `id` | `Deck` (`deck_id`) | Çoktan Bire (Many-to-One) | `all, delete-orphan` |
| **Score** | `id` | `User` (`user_id`) | Çoktan Bire (Many-to-One) | `all, delete-orphan` |

---

## 4. Kullanıcı Deneyimi (UX) ve Çift Tema Tasarımı

LingoRose, kullanıcıların göz sağlığını korumak ve etkileşimi artırmak amacıyla çift tema desteği sunmaktadır.

*   **Karanlık Mod:** Koyu gri ve siyah zeminler üzerine neon pembe ve mor gradyanların kullanıldığı, buzlu cam (glassmorphism) efektli, görsel açıdan son derece zengin ve premium bir arayüze sahiptir.
*   **Aydınlık Mod:** Aydınlık modda göz yormayan, pastel gül kurusu tonlarında yumuşak bir arka plan (`#FFF5F7` - `#FCECEF`) tercih edilmiştir. Okunabilirliği artırmak amacıyla tüm neon ışımalar ve gölgeler kaldırılmış; başlıklar için koyu füme (`#0F172A`), gövde metinleri için ise koyu gri (`#1E293B`) renk kodları kullanılmıştır. Kelime kartlarının arka planı fildişi beyazına çekilerek kontrast oranı en üst seviyeye taşınmıştır.

Kullanıcı deneyimini güçlendirmek amacıyla CSS 3D Transforms kullanılarak 3D kart çevirme animasyonları entegre edilmiştir. JavaScript tarafında `sessionStorage` ve `localStorage` kullanılarak kullanıcının seçtiği aktif modül durumu, son oynanan oyun filtresi ve gizlilik tercihleri tarayıcı hafızasında saklanmakta; sayfa yenilense dahi arayüz durum kaybı yaşamadan kesintisiz çalışmaktadır.

---

## 5. Ajan Hatalarının Tespiti ve Mühendislik Müdahaleleri

Geliştirme sürecinde yapay zeka ajanının ürettiği kodlarda tespit edilen ve sistem kararlılığını tehdit eden 4 kritik hata, mühendislik müdahaleleriyle giderilmiştir:

1.  **SQLAlchemy 1.x Sorgu Stilinin Kullanılması:** Ajan, veritabanı sorgularında eskiyen ve SQLAlchemy 2.0 ile önerilmeyen `User.query.filter_by(...)` yapısını kullanmıştır. Bu durum modern sürüm uyumluluğu için `sa.select(User).where(...)` yapısına dönüştürülmüştür.
2.  **Tek Tablo Denetimli Eksik Şema Çakışması:** Uygulama açılışında sadece `User` tablosunun varlığı kontrol ediliyor, diğer tabloların (Card, Deck vb.) eksik olması durumunda 500 hatası alınıyordu. SQLAlchemy Inspector entegre edilerek tüm tabloların mevcudiyeti taranmış; hata durumunda scoped session temizlenerek (`db.session.remove()`) güvenli bir drop-all ve create-all auto-recovery (otomatik kurtarma) mekanizması kurulmuştur.
3.  **routes.py Dosyasındaki login_required NameError Hatası:** Rotalara eklenen `@login_required` dekoratörü için gereken import ifadesi, ajan tarafından modül düzeyi yerine fonksiyon içine eklenmiş; bu da uygulamanın load-time (yüklenme) anında `NameError` vermesine yol açmıştır. Import ifadesi modül seviyesine çekilerek hata çözülmüştür.
4.  **Arama Kutusu Kontrast Çakışması:** Karanlık modda, girdi alanının zemin rengi ile yazı renginin beyaz olması nedeniyle yazılan metinlerin okunamaz hale geldiği fark edilmiştir. Arama girdi alanı arka planı karanlık modda yarı şeffaf koyu renk (`rgba(9, 9, 11, 0.7)`), yazı rengi ise parlak açık gri (`#F1F5F9`) yapılarak sorun giderilmiştir.

---

## 6. Test Stratejisi ve Kararlılık

LingoRose projesinin kararlılığı, Python `unittest` kütüphanesi üzerine kurulu kapsamlı bir test suite ile güvence altına alınmıştır. Test süreçleri; kimlik doğrulama (`test_auth.py`), çalışma modülü (`test_study.py`), tohumlama mekanizması (`test_seeding.py`), dil tercihleri (`test_language.py`), sayfalama ve hata sayfaları (`test_errors_and_pagination.py`), başarı rozetleri (`test_achievements.py`) ve satır içi çeviri API'si (`test_inline_translate.py`) gibi uygulamanın tüm kritik yollarını kapsamaktadır.

Toplam **88 birim test (unit test)** yazılmış ve testlerin tamamı **%100 başarı oranıyla (OK)** çalıştırılmıştır. Testlerin harici ağlara bağımlılığını kesmek amacıyla MyMemory ve Lingva gibi çeviri API'lerine yapılan HTTP istekleri mocklanmış, böylece testlerin çevrimdışı ortamlarda bile hızlı ve kararlı çalışması sağlanmıştır.

---

## 7. Sonuç ve Gelecek Çalışmalar

Yapay zeka pair programming desteği (Vibe Coding) sayesinde, normal şartlarda tek bir geliştirici için yaklaşık **70 saat (9 iş günü)** sürecek olan altyapı kurulumu, form doğrulamaları, siber güvenlik katmanı, 3D animasyonlar, oyun modülleri, müfredat ve sözlük entegrasyonu, Dockerize etme ve 88 testlik test suite yazımı süreçleri **yaklaşık 6 saatte** tamamlanarak **%91.4 oranında zaman tasarrufu** sağlanmıştır. Geliştirme esnasında Antigravity platformunun Plan Modu (Planning Mode) ve Walkthrough/Task takip özellikleri, kontrolsüz kod yazımını engelleyerek mimari bütünlüğün korunmasına katkı sunmuştur.

Geliştirilen Web Speech API tabanlı işitsel telaffuz altyapısı ve siber güvenlik sertleştirme önlemleri sayesinde platform hem güvenli hem de modern eğitim standartlarına kavuşturulmuştur. Gelecek çalışmalarda, kelime öğrenimini kalıcı kılmak adına SuperMemo (SM-2) algoritmasına dayalı bir Aralıklı Tekrarlama Sistemi (Spaced Repetition System) entegrasyonu ve kullanıcılar arası rekabeti artıracak haftalık Liderlik Tablosu motorunun daha da zenginleştirilmesi planlanmaktadır.

# 🌹 LingoRose - Dil Öğrenim Portalı ve Kelime Kartları

LingoRose; kullanıcıların yeni diller öğrenmesine, kelime dağarcığını geliştirmesine ve pratik yapmasına yardımcı olmak amacıyla tasarlanmış, kelime kartları (flashcards) yöntemiyle desteklenen ve mor/pembe neon temalı vizyoner bir interaktif web uygulamasıdır.

---

## 🚀 Temel Özellikler (Core Features)

- **Gelişmiş Çalışma (Flashcards) Modülü:** CSS 3D Transforms ile güçlendirilmiş çift taraflı kart çevirme (flip card) animasyonlu öğrenim alanı.
- **Deste & Kart Yönetimi (CRUD):** Kullanıcıların kendi özel destelerini ve kartlarını oluşturup, düzenleyip silebileceği modüler altyapı.
- **Hazır Kelime Paketleri (1500+ Kelime):** İngilizce, Almanca, İspanyolca, Fransızca ve İtalyanca olmak üzere 5 dilde, 15 temel kategoride önceden hazırlanmış devasa kelime seti.
- **İlerleme ve İstatistik Analiz Paneli:** Chart.js tabanlı mor/pembe neon gradyanlı çizgisel (Line), sütun (Bar) ve halka (Doughnut) performans grafikleri.
- **Modüler Profil Yönetimi:** AJAX Fetch API destekli profil günleme, şifre değiştirme, `localStorage` uyumlu gizlilik ayarları ve anlık güncellenen interaktif avatar modalı.
- **📄 PDF / Sözlük Çıktı Al Özelliği:** `@media print` CSS kuralları ile optimize edilmiş, A4 boyutunda iki kolonlu temiz yazdırma ve PDF kaydetme mekanizması.
- **🔔 Tarayıcı Bildirimleri ve Hatırlatıcı:** Günlük hedeflerini tamamlamamış kullanıcıları uyaran tarayıcı bildirimleri, `sessionStorage` optimizasyonu ve tarayıcı engelleri için **Neon Toast** yedek arayüzü.
- **🎨 Premium Arayüz ve Çift Mod Tasarımı:** Karanlık modda mor/pembe neon & glassmorphism şıklığı; aydınlık modda gözü yormayan pastel pembe/gül kurusu gradyan arka planı, yüksek kontrastlı gül kurusu başlık metinleri (#4A2834), fildişi beyazı kelime kartları ve marka uyumlu mat gül kırmızısı (#C85A7E) buton tasarımları. Beyaz arka planda kirlilik yaratan neon parlamaların sıfırlanması.

---

## 🏆 Oyunlaştırma ve Eğlence (Gamification)

LingoRose öğrenim sürecini eğlenceli hale getirmek için gelişmiş oyun modülleri ve rozetler barındırır:

1. **Kelime Eşleştirme Oyunu (Matching Game):** 4x4 gridde kartları karıştırarak doğru ve yanlış eşleşmeleri görsel animasyonlarla (shake ve yeşil parıltı) yöneten eşleştirme motoru.
2. **Kelime Tetrisi (Word Drop):** Yukarıdan düşen harfleri kelimeyle eşleştirmeye dayalı hızlı refleks oyunu.
3. **Cümle Kurma (Sentence Builder):** Karışık verilen kelimelerden doğru cümleyi kurma pratiği.
4. **Hafıza Kartları (Memory Flip):** 3D ayna yansımaları giderilmiş, minimalist çizgisel simgelerle donatılmış akıllı eşleştirme oyunu.
5. **Boşluk Doldurma (Fill in the Blanks):** Zamana karşı yarış (10 saniye süre barı) ve 3 can hakkı sunan interaktif boşluk doldurma oyunu.
6. **📊 Başarı Madalyaları (Achievements):** Kullanıcının veritabanı durumuna göre açılan neon parıltılı 3 başarı rozeti:
   * **🔥 İlk Kıvılcım:** 3 Günlük Streak Başarısı.
   * **🧠 Kelime Profesörü:** Oyunlarda en yüksek 100+ Puan Başarısı.
   * **📚 Deste Koleksiyoncusu:** 5+ Deste Sahibi Olma Başarısı.
7. **🎮 İnteraktif 404 Hata Sayfası Oyunu:** Yanlış URL'ye girildiğinde tetiklenen, veritabanından rastgele çeldiricili şıklar üreten, doğru tahminde konfetiler patlatan mini oyun hata sayfası.

---

## 🛡️ Güvenilirlik ve Kendi Kendini İyileştirme (Robustness & Self-Healing)

LingoRose, yeni klonlanan ortamlarda veya farklı bilgisayarlarda hiçbir manuel veritabanı kurulum adımı gerektirmeyen **"Plug-and-Play" (Tak-Çalıştır)** yapısına sahiptir:

- **Çoklu Tablo Denetimi (Multi-Table Verification):** Uygulama her başladığında SQLAlchemy Inspector kullanarak model şemasındaki tüm tabloların ('user', 'deck', 'card', 'score') veritabanında kurulu olup olmadığını denetler.
- **Hata Kurtarma (Auto-Recovery):** Tabloların eksik, bozuk olması veya şema uyumsuzluğu halinde veritabanı kilitlenmelerini önlemek adına scoped session temizlenir (`db.session.remove()`), ardından `db.drop_all()` ve `db.create_all()` komutları sırasıyla çalıştırılarak veritabanı şeması otomatik olarak sıfırdan yeniden oluşturulur ve default 1500 kelimelik veri setiyle otomatik tohumlanır (`seed_db()`).

---

## 🛠️ Teknik Kurulum ve Çalıştırma Adımları

### 1. Ortam Kurulumu ve Bağımlılıklar
```bash
# Sanal Ortam Oluşturma
python -m venv venv

# Sanal Ortamı Aktifleştirme (Windows)
venv\Scripts\activate
# (macOS/Linux için: source venv/bin/activate)

# Bağımlılıkları Yükleme
pip install -r requirements.txt
```

### 2. Ortam Değişkenleri
` .env.example` dosyasını `.env` olarak kopyalayın ve gerekli `SECRET_KEY` tanımlamalarını yapın:
```bash
copy .env.example .env
```

### 3. Veritabanı Yönetimi & Migrasyonlar
```bash
# Tabloları Yansıtma / Şemayı Güncelleme
flask db upgrade

# Yeni Veritabanı Migrasyonu Oluşturma (Modeller değiştiğinde)
flask db migrate -m "migrasyon_aciklamasi"
```

### 4. Veritabanını Tohumlama (Database Seeding)
Uygulama ilk kez ayağa kalktığında 1500 kelimelik hazır destelerin veritabanına otomatik yüklenmesi için:
```bash
flask seed
```

### 5. Uygulamayı Çalıştırma
```bash
flask run
```
Uygulama `http://127.0.0.1:5000` adresinde çalışmaya başlayacaktır.

---

## 🧪 Birim Testleri Çalıştırma (Testing)

Projenin kararlılığını ve hata yönetimini test etmek için entegre edilmiş 67 başarılı birim testi bulunmaktadır. Test süitini çalıştırmak için sanal ortam aktifken aşağıdaki komutu yürütün:

```bash
python -m unittest discover -s tests
```

*Tüm testlerin başarı çıktısı:*
```text
Ran 67 tests in 32.724s

OK
```

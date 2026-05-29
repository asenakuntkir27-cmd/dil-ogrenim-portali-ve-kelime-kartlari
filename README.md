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
Ran 67 tests in 42.860s

OK
```

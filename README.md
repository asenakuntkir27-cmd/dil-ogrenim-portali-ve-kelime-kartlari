# Dil Öğrenim Portalı ve Kelime Kartları

Bu proje, kullanıcıların yeni diller öğrenmesine, kelime dağarcığını geliştirmesine ve pratik yapmasına yardımcı olmak amacıyla tasarlanmış, kelime kartları (flashcards) yöntemiyle desteklenen interaktif bir web uygulamasıdır.

## Kullanılan Teknolojiler

Proje geliştirilirken aşağıdaki güncel teknolojiler ve kütüphaneler kullanılmıştır:
- **Flask 3.x**: Ana web framework.
- **Flask-SQLAlchemy**: Veritabanı ORM işlemleri.
- **Flask-Migrate**: Veritabanı şema değişiklikleri ve migrasyon yönetimi.
- **Flask-Login**: Kullanıcı oturum ve kimlik yönetimi.
- **Flask-WTF**: Güvenli web formları oluşturma.
- **Python-dotenv**: Ortam değişkenlerinin yönetimi.

## Kurulum Adımları

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin.

1. **Sanal Ortamın (Virtual Environment) Oluşturulması**
   Proje bağımlılıklarını izole etmek için bir sanal ortam oluşturun:
   ```bash
   python -m venv venv
   ```

2. **Sanal Ortamın Aktifleştirilmesi**
   Oluşturduğunuz sanal ortamı başlatın (Windows için):
   ```bash
   venv\Scripts\activate
   ```
   *(Not: macOS/Linux için `source venv/bin/activate` komutunu kullanabilirsiniz.)*

3. **Gerekli Kütüphanelerin Yüklenmesi**
   Sanal ortam aktifken projeye ait kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ortam Değişkenlerinin Ayarlanması**
   Proje kök dizininde bulunan örnek konfigürasyon dosyasını kopyalayarak `.env` dosyanızı oluşturun:
   ```bash
   cp .env.example .env
   ```
   *Windows (CMD/PowerShell) için kopyalama komutu olarak `copy .env.example .env` kullanabilirsiniz.*
   Oluşturulan `.env` dosyası içindeki `SECRET_KEY` ve diğer ayarları ortamınıza göre güncelleyin.

5. **Veritabanının İlklendirilmesi (Database Init)**
   Modellerin veritabanına yansıması ve tabloların oluşturulması için migrasyon işlemlerini uygulayın:
   ```bash
   flask db upgrade
   ```

## Geliştirme Komutları

Uygulamanın çalıştırılması ve veritabanı değişikliklerinin yönetilmesi için aşağıdaki temel komutları kullanabilirsiniz:

- **Uygulamayı Çalıştırma:**
  ```bash
  flask run
  ```
  Komut çalıştıktan sonra uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde yayına başlayacaktır.

- **Yeni Veritabanı Migrasyonu Oluşturma:**
  Veritabanı modellerinde bir değişiklik yaptığınızda (yeni tablo, kolon vb.) bu değişikliği kaydetmek için:
  ```bash
  flask db migrate -m "migrasyon_aciklamasi"
  ```
  Ardından değişiklikleri veritabanına uygulamak için tekrar `flask db upgrade` komutunu çalıştırmalısınız.

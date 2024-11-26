
Django Projesi - İzin Yönetim Sistemi

Bu proje, bir şirketin personel izin taleplerini yönetmek için geliştirilmiş basit bir Django uygulamasıdır. Personel ekleme, izin talep etme, ve izin onayları gibi özellikleri barındırmaktadır.

Özellikler:

- Personel Ekleme: Yöneticiler, yeni personel ekleyebilir.
- İzin Talepleri: Personel, izin talep edebilir.
- Dashboard: Yöneticiler, tüm izin taleplerini ve personel bilgilerini görüntüleyebilir.

Teknolojiler:

- Django 5.1.3
- Python 3.x
- SQLite (varsayılan veritabanı)
- Bootstrap (frontend tasarımı için)

Kurulum:

1. Ortamı Kurma

Proje için sanal bir ortam oluşturun ve aktif hale getirin:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts ctivate  # Windows

2. Gerekli Paketlerin Yüklenmesi

Proje bağımlılıklarını yüklemek için şu komutu çalıştırın:

pip install -r requirements.txt

3. Veritabanı Migrasyonları

Veritabanı tablolarını oluşturmak için migrasyonları çalıştırın:

python manage.py migrate

4. Superuser Oluşturma

Yönetici paneline erişim sağlamak için bir süper kullanıcı oluşturun:

python manage.py createsuperuser

Yönetici kullanıcı ve şifresi istenecektir.

5. Sunucuyu Başlatma

Django geliştirme sunucusunu başlatın:

python manage.py runserver

Şimdi, uygulamanızı http://127.0.0.1:8000/ adresinden görebilirsiniz.

Kullanım:

Personel Ekleme

1. dashboard/ sayfasına gidin.
2. Sağ üst köşede "Personel Ekle" butonuna tıklayın.
3. Yeni personel bilgilerini girin ve "Personel Ekle" butonuna tıklayarak kaydedin.

İzin Talep Etme

1. Personel, "İzin Talep Et" sayfasına gidip izin talep formunu doldurabilir.
2. Formu gönderdiğinde, yönetici onayını bekleyen izin talepleri görüntülenir.

Yönetici Paneli

- /adminSytem(System yazmayın Sytem olucak dikkat ediniz.) adresine giderek, tüm gidilebilecek URL'leri görebilirsiniz (eksik kaldı urllerin hepsini buton veyahut yönlendirme yapamadığım için bu kısımda page404 hatası alacaksınız kusura bakmayın.)
 
------DİKKAT adminSystem değil adminSytem---------------------------


/personSystem adresine giderek, tüm gidilebilecek URL'leri görebilirsiniz (eksik kaldı urllerin hepsini buton veyahut yönlendirme yapamadığım için bu kısımda page404 hatası alacaksınız kusura bakmayın.)







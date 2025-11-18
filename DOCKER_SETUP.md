# Docker Kurulum Rehberi

## 1. Docker Desktop Kurulumu

### Windows için:
1. Docker Desktop for Windows'u indirin:
   - https://www.docker.com/products/docker-desktop
   - "Download for Windows" butonuna tıklayın

2. İndirilen `.exe` dosyasını çalıştırın ve kurulum sihirbazını takip edin

3. Kurulum sonrası bilgisayarı yeniden başlatın (gerekirse)

4. Docker Desktop'u başlatın ve sistem tepsisinde çalıştığını doğrulayın

### Kurulum Kontrolü:
```powershell
docker --version
docker-compose --version
```

Her iki komut da versiyon bilgisi döndürmelidir.

## 2. Projeyi Docker ile Çalıştırma

### İlk Kurulum:
```powershell
# Proje dizinine gidin
cd "E:\Repositories\Software Projects\Game Data Hub (GDH)"

# Tüm servisleri başlatın (PostgreSQL, Backend, Frontend)
docker-compose up -d

# Logları görüntüleyin
docker-compose logs -f
```

### Servisleri Durdurma:
```powershell
docker-compose down
```

### Veritabanını Sıfırlama:
```powershell
# Tüm container'ları ve volume'ları sil
docker-compose down -v

# Yeniden başlat
docker-compose up -d
```

## 3. Servis Erişim Adresleri

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **PostgreSQL**: localhost:5432
  - User: `gdh_user`
  - Password: `gdh_password`
  - Database: `gdh_db`

## 4. Yaygın Komutlar

### Container durumunu kontrol et:
```powershell
docker-compose ps
```

### Backend loglarını görüntüle:
```powershell
docker-compose logs backend
```

### Frontend loglarını görüntüle:
```powershell
docker-compose logs frontend
```

### PostgreSQL'e bağlan:
```powershell
docker-compose exec postgres psql -U gdh_user -d gdh_db
```

### Backend container'ına gir:
```powershell
docker-compose exec backend bash
```

### Frontend container'ına gir:
```powershell
docker-compose exec frontend sh
```

## 5. Sorun Giderme

### Port zaten kullanılıyor hatası:
- 8000, 3000 veya 5432 portlarını kullanan uygulamaları kapatın
- Veya `docker-compose.yml` dosyasındaki port numaralarını değiştirin

### Container'lar başlamıyor:
```powershell
# Logları kontrol edin
docker-compose logs

# Container'ları yeniden oluşturun
docker-compose up -d --build
```

### Veritabanı bağlantı hatası:
- PostgreSQL container'ının çalıştığını kontrol edin: `docker-compose ps`
- Health check'in geçmesini bekleyin (birkaç saniye)

## 6. Development vs Production

### Development (Hot Reload):
- `docker-compose.yml` dosyası volume mount kullanır
- Kod değişiklikleri anında yansır
- Backend ve frontend otomatik reload yapar

### Production:
- Volume mount'ları kaldırın
- Environment variable'ları güvenli şekilde ayarlayın
- `SECRET_KEY` değiştirin


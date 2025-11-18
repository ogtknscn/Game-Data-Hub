# Game Data Hub - Hızlı Başlangıç Kılavuzu

## Ön Gereksinimler

1. **Python 3.11+** (3.13 bazı paketlerle uyum sorunu olabilir, 3.11-3.12 önerilir)
2. **PostgreSQL 15+** (veya Docker ile PostgreSQL)
3. **Node.js 18+** (frontend için)

## Hızlı Kurulum

### 1. Backend Kurulumu

```bash
cd backend

# Virtual environment oluştur
python -m venv venv

# Virtual environment'ı aktif et
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Paketleri yükle
pip install -r requirements.txt

# Environment variables ayarla
# .env dosyasını düzenle (DATABASE_URL'yi PostgreSQL'inize göre ayarlayın)

# Veritabanı migration'larını çalıştır
alembic upgrade head

# Server'ı başlat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend şu adreste çalışacak: http://localhost:8000
API Docs: http://localhost:8000/api/docs

### 2. Frontend Kurulumu

```bash
cd frontend

# Paketleri yükle
npm install

# Development server'ı başlat
npm run dev
```

Frontend şu adreste çalışacak: http://localhost:3000

### 3. PostgreSQL Kurulumu (Docker ile)

Eğer Docker yüklüyse:

```bash
docker run --name gdh-postgres -e POSTGRES_USER=gdh_user -e POSTGRES_PASSWORD=gdh_password -e POSTGRES_DB=gdh_db -p 5432:5432 -d postgres:15-alpine
```

### 4. PostgreSQL Kurulumu (Manuel)

1. PostgreSQL'i yükleyin
2. Veritabanı oluşturun:
```sql
CREATE DATABASE gdh_db;
CREATE USER gdh_user WITH PASSWORD 'gdh_password';
GRANT ALL PRIVILEGES ON DATABASE gdh_db TO gdh_user;
```

## İlk Kullanım

1. Frontend'de http://localhost:3000 adresine gidin
2. "Register" ile yeni bir kullanıcı oluşturun
3. Login yapın
4. İlk projenizi oluşturun
5. Tablolarınızı oluşturun ve veri girin

## Sorun Giderme

### Python 3.13 Uyumluluk Sorunları

Python 3.13 çok yeni olduğu için bazı paketler henüz tam desteklemeyebilir. Python 3.11 veya 3.12 kullanmanız önerilir.

### PostgreSQL Bağlantı Hatası

- PostgreSQL'in çalıştığından emin olun
- `backend/.env` dosyasındaki `DATABASE_URL`'i kontrol edin
- Firewall ayarlarını kontrol edin

### Port Çakışması

- Backend varsayılan port: 8000
- Frontend varsayılan port: 3000
- PostgreSQL varsayılan port: 5432

Bu portlar kullanılıyorsa, ilgili dosyalardaki port ayarlarını değiştirin.

## Docker Compose ile Çalıştırma (Önerilen)

Eğer Docker yüklüyse:

```bash
# Tüm servisleri başlat
docker-compose up -d

# Migration'ları çalıştır
cd backend
alembic upgrade head

# Logları görüntüle
docker-compose logs -f
```

## Test

Backend API'yi test etmek için:

```bash
# Health check
curl http://localhost:8000/health

# API Docs
# Tarayıcıda: http://localhost:8000/api/docs
```

## Sonraki Adımlar

- README.md dosyasını okuyun
- API dokümantasyonunu inceleyin: http://localhost:8000/api/docs
- İlk projenizi oluşturun ve tablolarınızı yönetin


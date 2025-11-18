# 🎮 Game Data Hub (GDH)

> **Merkezi Oyun Veri Yönetim Platformu**  
> Oyun geliştirme süreçlerinde tasarım niyetini, oyun konfigürasyon verilerini ve LiveOps parametrelerini tek bir platformda birleştiren merkezi bir veri orkestrasyon katmanı.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Mimari](#-mimari)
- [Kullanım](#-kullanım)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Geliştirme](#-geliştirme)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## ✨ Özellikler

### 🎯 Faz 1 MVP Özellikleri

#### 1. **Kodsuz Veri Editörü**
- 📊 Web tabanlı, e-tablo benzeri arayüz
- ➕ Tablo oluşturma/düzenleme
- ✏️ Hücre bazında veri girişi
- 🔢 Temel veri tipleri: integer, float, boolean, string, enum

#### 2. **Görsel Şema Tanımlama**
- 🗂️ Tablo oluşturma ve yönetimi
- 📐 Sütun tipi tanımlama (integer, float, boolean, enum, reference)
- 🔗 Tablolar arası ilişki tanımlama (foreign key)
- ✅ Veri validasyonu kuralları

#### 3. **Otomatik Kod Üretimi**
- 🎮 Unity C# ScriptableObjects
- 🚀 Unreal Engine JSON/DataTables
- 📄 Tipli JSON şemaları

#### 4. **Temel Versiyon Kontrolü**
- 📝 Hücre bazında değişiklik takibi
- 💾 Commit/commit mesajı sistemi
- 🔍 Diff görüntüleme (önceki vs şimdiki)
- ↩️ Geri alma (rollback) özelliği

#### 5. **CLI ve REST API**
- 🔌 RESTful API endpoints
- 🔐 API authentication (JWT)
- 📚 API dokümantasyonu (Swagger)

## 🛠️ Teknoloji Yığını

### Backend
- **Dil:** Python 3.11+
- **Framework:** FastAPI
- **Veritabanı:** PostgreSQL 15+ (SQLite development için)
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Authentication:** JWT tokens
- **Code Generation:** Jinja2 templates

### Frontend
- **Framework:** React 18+ (TypeScript)
- **UI Kütüphanesi:** Material-UI (MUI)
- **State Management:** React Query + Zustand
- **Build Tool:** Vite
- **HTTP Client:** Axios

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions (planned)

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler

- Docker ve Docker Compose
- Git

### Docker ile Çalıştırma (Önerilen)

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/ogtknscn/Game-Data-Hub.git
cd Game-Data-Hub
```

2. **Docker Compose ile tüm servisleri başlatın:**
```bash
docker-compose up -d --build
```

3. **Veritabanı migration'larını çalıştırın:**
```bash
docker-compose exec backend alembic upgrade head
```

4. **Uygulamaya erişin:**
- 🌐 Frontend: [http://localhost:3000](http://localhost:3000)
- 🔧 Backend API: [http://localhost:8000](http://localhost:8000)
- 📖 API Docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

> 📝 **Not:** Detaylı Docker kurulum rehberi için [DOCKER_SETUP.md](DOCKER_SETUP.md) dosyasına bakın.

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# PostgreSQL'i başlatın (Docker ile)
docker-compose up -d postgres

# SQLite kullanmak için (development)
$env:USE_SQLITE="true"  # PowerShell
# veya
export USE_SQLITE=true  # Linux/Mac

# Migration'ları çalıştırın
alembic upgrade head

# Server'ı başlatın
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🏗️ Mimari

Proje, **SOLID prensipleri** ve **OOP best practices**'e uygun olarak **katmanlı mimari** kullanır:

```
┌─────────────────────────────────────┐
│         API Layer                   │  ← HTTP request/response handling
├─────────────────────────────────────┤
│      Application Layer              │  ← Use cases, business logic
├─────────────────────────────────────┤
│        Domain Layer                 │  ← Pure business logic, entities
├─────────────────────────────────────┤
│     Infrastructure Layer            │  ← DB, cache, code generation
└─────────────────────────────────────┘
```

### Design Patterns

- **Repository Pattern:** Abstract data access layer
- **Dependency Injection:** FastAPI's built-in DI + custom container
- **Service Layer:** Business logic orchestration
- **Value Objects:** Type-safe domain primitives

### Katman Sorumlulukları

- **API Layer**: HTTP request/response handling, authentication
- **Application Layer**: Use cases, business logic orchestration
- **Domain Layer**: Pure business logic, entities, interfaces
- **Infrastructure Layer**: External concerns (DB, cache, code generation)

## 📖 Kullanım

### İlk Kullanıcı Oluşturma

1. Frontend'de `/register` sayfasına gidin
2. Yeni bir kullanıcı hesabı oluşturun
3. Login yapın

### Proje Oluşturma

1. Dashboard'da **"New Project"** butonuna tıklayın
2. Proje adı ve açıklama girin
3. Projeyi oluşturun

### Tablo Oluşturma

1. Proje sayfasında **"New Table"** butonuna tıklayın
2. Tablo adı ve açıklama girin
3. Sütunları ekleyin (name, data_type, vb.)
4. Tabloyu oluşturun

### Veri Girişi

1. Tablo sayfasını açın
2. Hücrelere veri girin
3. Değişiklikleri commit edin

### Kod Üretimi

1. Tablo verilerini hazırlayın
2. **Code Generation** menüsünden format seçin (Unity, Unreal, JSON)
3. Kodu indirin

## 📚 API Dokümantasyonu

API dokümantasyonu Swagger UI üzerinden erişilebilir:

- **Swagger UI:** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **ReDoc:** [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

### Temel Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Kullanıcı kaydı
- `POST /api/v1/auth/login` - Login

#### Projects
- `GET /api/v1/projects` - Projeleri listele
- `POST /api/v1/projects` - Proje oluştur
- `GET /api/v1/projects/{project_id}` - Proje detayı
- `PATCH /api/v1/projects/{project_id}` - Proje güncelle
- `DELETE /api/v1/projects/{project_id}` - Proje sil

#### Tables
- `GET /api/v1/tables/project/{project_id}` - Proje tablolarını listele
- `POST /api/v1/tables` - Tablo oluştur
- `GET /api/v1/tables/{table_id}` - Tablo detayı
- `PATCH /api/v1/tables/{table_id}` - Tablo güncelle
- `DELETE /api/v1/tables/{table_id}` - Tablo sil

#### Columns
- `POST /api/v1/tables/{table_id}/columns` - Sütun oluştur
- `PATCH /api/v1/columns/{column_id}` - Sütun güncelle
- `DELETE /api/v1/columns/{column_id}` - Sütun sil

#### Data
- `GET /api/v1/data/table/{table_id}` - Tablo verilerini getir
- `POST /api/v1/data/rows` - Satır oluştur
- `PATCH /api/v1/data/rows/{row_id}` - Satır güncelle
- `DELETE /api/v1/data/rows/{row_id}` - Satır sil
- `PATCH /api/v1/data/cell` - Hücre güncelle

#### Versions
- `POST /api/v1/versions/commit` - Commit oluştur
- `GET /api/v1/versions/{version_id}/diff` - Diff görüntüle
- `POST /api/v1/versions/{version_id}/rollback` - Rollback yap

#### Code Generation
- `GET /api/v1/code/tables/{table_id}/generate` - Kod üret (Unity/Unreal/JSON)

## 👨‍💻 Geliştirme

### Proje Yapısı

```
Game-Data-Hub/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── application/ # Application services
│   │   ├── domain/      # Domain entities & interfaces
│   │   ├── infrastructure/ # Repositories & external services
│   │   └── core/        # Core configuration
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Page components
│   │   ├── components/ # Reusable components
│   │   ├── services/   # API clients
│   │   └── store/      # State management
│   └── package.json
└── docker-compose.yml   # Docker services
```

### Code Quality

**Backend:**
```bash
cd backend
black app/
flake8 app/
mypy app/
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run type-check
```

### Testing

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Environment Variables

Backend için `.env` dosyası oluşturun:

```env
DATABASE_URL=postgresql://gdh_user:gdh_password@localhost:5432/gdh_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
USE_SQLITE=false  # SQLite kullanmak için true yapın
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları takip edin:

1. 🍴 Fork yapın
2. 🌿 Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. 💾 Commit yapın (`git commit -m 'Add amazing feature'`)
4. 📤 Push yapın (`git push origin feature/amazing-feature`)
5. 🔄 Pull Request açın

### Kod Standartları

- Python için PEP 8 standartlarına uyun
- TypeScript için ESLint kurallarına uyun
- Tüm yeni özellikler için test yazın
- Documentation güncelleyin

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 📞 İletişim

- **Repository:** [https://github.com/ogtknscn/Game-Data-Hub](https://github.com/ogtknscn/Game-Data-Hub)
- **Issues:** [GitHub Issues](https://github.com/ogtknscn/Game-Data-Hub/issues)

## 🙏 Teşekkürler

Bu proje, oyun geliştirme süreçlerindeki veri yönetimi zorluklarını çözmek için geliştirilmiştir. 

---

⭐ **Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!** ⭐

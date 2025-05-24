# Travel AI Backend

Backend complet pentru aplicația Travel AI, dezvoltat cu FastAPI și PostgreSQL.

## 🚀 Caracteristici

- **Autentificare JWT** - Sistem securizat de login/register
- **Validări robuste** - Format email, telefon românesc, username alfanumeric
- **Securitate** - Hash parole cu bcrypt, token-uri cu expirare
- **Base de date** - PostgreSQL cu SQLAlchemy ORM
- **API Documentation** - Swagger UI automată la `/docs`

## 📋 Cerințe

- Python 3.8+
- PostgreSQL 12+
- pip (pentru instalarea dependențelor)

## 🛠️ Instalare

### 1. Clonează repository-ul
```bash
git clone <repository-url>
cd travel-ai-be
```

### 2. Creează un environment virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate  # Windows
```

### 3. Instalează dependențele
```bash
pip install -r requirements.txt
```

### 4. Configurează baza de date
```bash
# Creează baza de date PostgreSQL
sudo -u postgres psql
CREATE DATABASE travel_ai_db;
CREATE USER travel_user WITH PASSWORD 'travel_password';
GRANT ALL PRIVILEGES ON DATABASE travel_ai_db TO travel_user;
\q
```

### 5. Configurează variabilele de mediu
Editează fișierul `.env`:
```env
DATABASE_URL=postgresql://travel_user:travel_password@localhost/travel_ai_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

## 🏃‍♂️ Rulare

### Dezvoltare
```bash
uvicorn app.main:app --reload --host localhost --port 8000
```

### Producție
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 API Endpoints

### Autentificare

#### POST `/api/auth/register`
Înregistrează un utilizator nou.

**Request:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "0712345678",
  "username": "johndoe",
  "age": 25,
  "password": "securepassword",
  "confirmPassword": "securepassword"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "0712345678",
    "username": "johndoe",
    "age": 25,
    "is_first_login": true,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### POST `/api/auth/login`
Autentifică un utilizator existent.

**Request:**
```json
{
  "identifier": "john@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "0712345678",
    "username": "johndoe",
    "age": 25,
    "is_first_login": false,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

## 🔒 Validări

### Email
- Format valid conform RFC 5322
- Unic în sistem

### Telefon
- Format românesc: `07xxxxxxxx`
- Unic în sistem

### Username
- Minim 3 caractere
- Doar caractere alfanumerice (a-Z, 0-9)
- Unic în sistem

### Parolă
- Minim 6 caractere
- Hash-uită cu bcrypt

### Vârstă
- Între 13 și 120 ani

## 🗂️ Structura Proiectului

```
travel-ai-be/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicația principală
│   ├── database.py          # Configurare PostgreSQL
│   ├── config.py            # Configurare environment
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # Model SQLAlchemy User
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # Scheme Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth.py          # Rute autentificare
│   └── utils/
│       ├── __init__.py
│       ├── auth.py          # Utilitare JWT
│       └── password.py      # Utilitare parole
├── requirements.txt         # Dependențe Python
├── .env                     # Variabile de mediu
└── README.md               # Documentație
```

## 🧪 Testare

### Acces la documentația API
După pornirea serverului, accesează:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test rapid cu curl

**Register:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "0712345678",
    "username": "testuser",
    "age": 25,
    "password": "testpass",
    "confirmPassword": "testpass"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "test@example.com",
    "password": "testpass"
  }'
```

## 🔧 Troubleshooting

### Eroare conexiune bază de date
- Verifică că PostgreSQL rulează
- Verifică credențialele din `.env`
- Verifică că baza de date `travel_ai_db` există

### Eroare import module
- Asigură-te că environment-ul virtual este activat
- Rulează `pip install -r requirements.txt`

### Port deja ocupat
- Schimbă portul în `.env`: `PORT=8001`
- Sau oprește procesul care folosește portul 8000

## 🤝 Contribuție

1. Fork repository-ul
2. Creează o ramură pentru feature: `git checkout -b feature/numele-feature`
3. Commit modificările: `git commit -m 'Adaugă feature nou'`
4. Push la ramură: `git push origin feature/numele-feature`
5. Deschide un Pull Request

## 📄 Licență

Acest proiect este licențiat sub [MIT License](LICENSE).

## 📞 Contact

Pentru întrebări sau suport, contactează echipa de dezvoltare. 
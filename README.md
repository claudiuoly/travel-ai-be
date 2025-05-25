# Travel AI Backend

Backend complet pentru aplicația Travel AI, dezvoltat cu FastAPI și PostgreSQL, cu integrare Gemini AI pentru chat.

## 🚀 Caracteristici

- **Autentificare JWT** - Sistem securizat de login/register
- **Chat AI** - Integrare cu Google Gemini AI pentru asistență turistică
- **Validări robuste** - Format email, telefon românesc, username alfanumeric
- **Securitate** - Hash parole cu bcrypt, token-uri cu expirare
- **Base de date** - PostgreSQL cu SQLAlchemy ORM
- **API Documentation** - Swagger UI automată la `/docs`

## 📋 Cerințe

- Python 3.8+
- PostgreSQL 12+
- Google Gemini API Key
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
GEMINI_API_KEY=your-gemini-api-key-here
HOST=localhost
PORT=8000
DEBUG=True
```

## 🏃‍♂️ Rulare

### Dezvoltare
```bash
# Mod standard cu auto-reload
python start_server.py

# Mod curat fără warning-uri GUI
python start_server_clean.py

# Sau direct cu uvicorn
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

### Chat AI

#### POST `/api/chat/message`
Trimite un mesaj către asistentul AI pentru călătorii.

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Request:**
```json
{
  "message": "Ce atracții turistice îmi recomanzi în București?"
}
```

**Response:**
```json
{
  "message": "În București îți recomand să vizitezi Palatul Parlamentului, Centrul Vechi, Parcul Herăstrău, Muzeul Satului și Arcul de Triumf. Pentru o experiență completă, nu rata nici Ateneul Român și Calea Victoriei pentru shopping și cafenele."
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

### Mesaje Chat
- Minim 1 caracter, maxim 1000 caractere

## 🗂️ Structura Proiectului

```
travel-ai-be/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicația principală FastAPI
│   ├── database.py          # Configurare PostgreSQL
│   ├── config.py            # Configurare environment
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Model SQLAlchemy User
│   │   └── chat.py          # Model SQLAlchemy ChatMessage
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Scheme Pydantic User
│   │   └── chat.py          # Scheme Pydantic Chat
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Rute autentificare
│   │   └── chat.py          # Rute chat AI
│   └── utils/
│       ├── __init__.py
│       ├── auth.py          # Utilitare JWT
│       ├── password.py      # Utilitare parole
│       └── chat.py          # Integrare Gemini AI
├── requirements.txt         # Dependențe Python
├── start_server.py          # Script pornire server (cu debug)
├── start_server_clean.py    # Script pornire server (fără warning-uri)
├── .env                     # Variabile de mediu
├── .gitignore              # Fișiere ignorate de Git
└── README.md               # Documentație
```

## 🤖 Integrare Gemini AI

Aplicația folosește Google Gemini AI pentru a oferi răspunsuri inteligente la întrebările despre călătorii. Caracteristici:

- **Context specializat** - Asistentul este optimizat pentru sfaturi de călătorie
- **Răspunsuri concise** - Limitate la 200 cuvinte pentru claritate
- **Istoric conversații** - Toate mesajele sunt salvate în baza de date
- **Rate limiting** - Gestionarea automată a limitelor API

### Configurare Gemini API

1. Obține o cheie API de la [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Adaugă cheia în fișierul `.env`:
   ```env
   GEMINI_API_KEY=your-api-key-here
   ```

### Limite API Gemini (Free Tier)

- **15 cereri pe minut** pentru modelul `gemini-1.5-flash`
- Aplicația gestionează automat erorile de rate limiting
- Pentru utilizare intensivă, consideră upgrade la plan plătit

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

**Chat (necesită token din login):**
```bash
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Ce îmi recomanzi să vizitez în Cluj-Napoca?"
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

### Eroare Gemini API
- Verifică că `GEMINI_API_KEY` este setat corect în `.env`
- Verifică că nu ai depășit limita de 15 cereri pe minut
- Pentru erori persistente, verifică [documentația oficială](https://ai.google.dev/gemini-api/docs/rate-limits)

### Port deja ocupat
- Schimbă portul în `.env`: `PORT=8001`
- Sau oprește procesul care folosește portul 8000

### Warning-uri GUI (Chromium/Electron)
- Folosește `python start_server_clean.py` pentru a evita warning-urile
- Sau setează manual variabilele de mediu:
  ```bash
  export EDITOR=true
  unset DISPLAY WAYLAND_DISPLAY
  ```

## 📊 Dependențe

### Core
- **FastAPI** - Framework web modern și rapid
- **SQLAlchemy** - ORM pentru PostgreSQL
- **Pydantic** - Validare și serializare date
- **Uvicorn** - Server ASGI

### Securitate
- **python-jose** - JWT token handling
- **passlib** - Hash parole cu bcrypt

### AI Integration
- **google-generativeai** - Client oficial Gemini AI

### Database
- **psycopg2-binary** - Driver PostgreSQL

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
# Quran API

Modern REST API for the Holy Quran (Hafs 'an 'Asim), Uthmanic script, full tashkeel.

---

## What it is

This API serves the complete Quran text in Uthmanic script with full diacritics (tashkeel), sourced from the Tanzil project. It's not trying to be everything — it's scoped to one riwayah, one script, and one purpose: give you the correct text with the right metadata, fast.

- **Riwayah:** Hafs 'an 'Asim
- **Script:** Uthmanic (Medina Mushaf)
- **Font recommendation:** KFGQPC Uthman Taha Naskh

---

## Stack

- **Python** + FastAPI
- **PostgreSQL**: stores all 6,236 ayat
- **Redis**: API key storage and rate limiting
- **Docker Compose**: everything runs in containers

---

## Getting started

### Prerequisites
- Docker + Docker Compose

### Setup

1. Clone the repo and create your `.env`:

```env
DATABASE_URL=postgresql://user:yourpassword@db:5432/quran_api
REDIS_URL=redis://redis:6379
POSTGRES_USER=user
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=quran_api
```

2. Build and start:

```bash
docker compose up --build -d
```

3. Import the data (one time only):

```bash
docker compose exec api python scripts/import_tanzil.py
docker compose exec api python scripts/update_surahs.py
```

5. Generate your first API key:

```bash
docker compose exec api python scripts/create_api_key.py userapp
```

---

## Authentication

Every request requires an API key passed as a header:

```
x-api-key: your_key_here
```

Requests without a valid key return `401`. Rate limit is **60 requests per minute** per IP.

---

## Endpoints

All endpoints are prefixed with `/v1`. Pagination is available on list endpoints via `?limit=20&offset=0` (max limit: 100).

### Surah

```
GET /v1/surah               
GET /v1/surah/{id}           
GET /v1/surah/{id}/ayat       
```

### Ayah

```
GET /v1/ayah/{surah}/{ayah} 
```

### Navigation

```
GET /v1/juz/{number}         
GET /v1/hizb/{number}         
GET /v1/page/{number}          
```

### Search

```
GET /v1/search?q=              
```

---

## Response shape

```json
{
  "id": 262,
  "surah_id": 2,
  "ayah_number": 255,
  "juz_number": 3,
  "hizb_number": 17,
  "page_number": 42,
  "text_uthmani": "TEXT_TASHKEEL",
  "text_simple": "TEXT_SIMPLE",
  "sajdah": false,
  "font_recommendation": "KFGQPC Uthman Taha Naskh"
}
```

- `text_uthmani`: full tashkeel, use this for display
- `text_simple`: clean text without diacritics, use this for search or indexing
- `font_recommendation`: the font this text is designed to render with

---

## API docs

FastAPI generates live docs automatically:

```json
http://localhost:8000/docs
```

---

## Data source

Quran text sourced from [Tanzil.net](https://tanzil.net).
A trusted Quran text project used widely across Islamic apps. 

> The Uthmanic text follows the standard Medina Mushaf encoding.


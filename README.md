# 💊 Medicine Search System

The project implements a *medicine search system* over a structured dataset using *PostgreSQL, with multiple search modes exposed via a **FastAPI backend* and a *Streamlit frontend*.

The system allows searching medicines by:

* *Prefix Search* → Par → Paracetamol
* *Substring Search* → Injection → Clexane Injection
* *Full-text Search* → antibiotic → Amoxicillin, Ciprofloxacin
* *Fuzzy Search (typo-tolerant)* → Paracetmol → Paracetamol

---

## 1. Requirements

* *fastapi* → backend API framework
* *uvicorn* → ASGI server to run FastAPI
* *psycopg2-binary* → PostgreSQL database driver
* *python-multipart* → required by FastAPI for form handling
* *requests* → used in submission.py and Streamlit app to call API
* *streamlit* → frontend UI

---

## 2. Database Setup

### 2.1 Create Database

sql
CREATE DATABASE medicinedb;
\c medicinedb

<img width="1817" height="1012" alt="pharma1" src="https://github.com/user-attachments/assets/08c56c5e-742e-4f47-bdf6-008bb5b62428" />
<img width="1918" height="1006" alt="pharma2" src="https://github.com/user-attachments/assets/e2baca09-7472-4e8a-8b63-1a11dab4861e" />

<img width="1851" height="1013" alt="pharma3" src="https://github.com/user-attachments/assets/a4454e8c-2567-4fd5-be19-09f6f4dea80e" />



### 2.2 Create Schema & Indexes

Run the SQL schema file:

bash
psql -U postgres -d medicinedb -f schema.sql


Schema includes:

* *Table*: medicines
* *Extensions*: pg_trgm, unaccent
* *Indexes*:

  * idx_medicines_search_vector (GIN)
  * idx_medicines_name_trgm (Trigram)

### 2.3 Import Data

bash
python import_data.py


This will load all JSON/CSV data into the medicines table and populate the search_vector column.

### 2.4 Dataset

The dataset contains detailed medicine information:

* id, sku_id, name
* manufacturer_name, marketer_name
* type, price, pack_size_label
* short_composition
* is_discontinued, available

---

## 3. Run the API

Start FastAPI server:

bash
uvicorn main:app --reload


By default, it runs at: *[http://127.0.0.1:8000](http://127.0.0.1:8000)*

### 3.1 API Endpoints

| Endpoint                  | Description                            |
| ------------------------- | -------------------------------------- |
| /search/prefix?q=...    | Search medicines starting with q     |
| /search/substring?q=... | Search medicines containing q        |
| /search/fulltext?q=...  | Full-text search in name + composition |
| /search/fuzzy?q=...     | Fuzzy search for similar names         |

*Example:*

http
GET http://127.0.0.1:8000/search/prefix?q=pa


### 3.2 Swagger Documentation

Interactive API docs:
👉 *[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

You can test all endpoints directly here.

### 3.3 Streamlit UI

Run the frontend:

bash
streamlit run app.py

<img width="1915" height="965" alt="pharma4" src="https://github.com/user-attachments/assets/2a5a3614-511c-461b-8a52-f0c0510c2727" />



---

## 4. Benchmarking

Run EXPLAIN ANALYZE in psql for each query type (prefix, substring, full-text, fuzzy).

Record:

* Latency
* Rows processed
* Indexes used

Results documented in benchmark.md.

### Output of submission.py

json
{
  "results": {
    "1": ["Avastin", "Avastin Injection"],
    "2": ["Paracetamol"],
    "3": ["Clexane Injection", "Avastin Injection"],
    "4": ["Amoxicillin", "Azithromycin", "Ciprofloxacin"],
    "5": ["Ibuprofen", "Diclofenac", "Paracetamol"]
  }
}


---

## 5. Notes on Performance

* *Prefix & Substring Search* → Trigram index on name
* *Full-Text Search* → GIN index on search_vector
* *Fuzzy Search* → Trigram index with % operator + similarity() function

Optimized for quick retrieval (~ms level response**).

---

## 6. Project Structure

```bash
.
├── main.py               # FastAPI backend (all search endpoints)
├── app.py                # Streamlit frontend (UI for search)
├── submission.py         # Benchmark runner (creates submission.json)
├── python.py             # Data import (loads JSON from ZIP into DB)
├── benchmark_queries.json
├── submission.json       # Auto-generated benchmark results
└── README.md             # Documentation


---
```


## 7. Features

* REST API with *FastAPI*
* Optimized *PostgreSQL queries & indexes*
* Typo-tolerant *fuzzy search with pg_trgm*
* Interactive *Streamlit frontend*
* Benchmark runner to generate results
* Clear & well-documented *README.md*

---





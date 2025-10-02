Medicine Search System
The project implements a medicine search system over a structured dataset using PostgreSQL, with multiple search modes exposed via a FastAPI backend and a Streamlit frontend.

The system allows searching medicines by:

Prefix Search → Par → Paracetamol
Substring Search → Injection → Clexane Injection
Full-text Search → antibiotic → Amoxicillin, Ciprofloxacin
Fuzzy Search (typo-tolerant) → Paracetmol → Paracetamol

1. Requirements

fastapi → backend API framework
uvicorn → ASGI server to run FastAPI
psycopg2-binary → PostgreSQL database driver
python-multipart → required by FastAPI for form handling
requests → used in submission.py and Streamlit app to call API
streamlit → frontend UI

2. Database Setup
   2.1 Create Database

Open psql and run:

CREATE DATABASE medicinedb;
\c medicinedb

2.2 Create Schema & Indexes

Run the SQL schema file:

psql -U postgres -d medicinedb -f schema.sql

Schema includes:

Table medicines

Extensions: pg_trgm, unaccent

Indexes:

idx_medicines_search_vector (GIN)

idx_medicines_name_trgm (Trigram)

2.3 Import Data

Use the Python import script:

python import_data.py

This will load all JSON/CSV data into the medicines table and populate the search_vector column.

2.4 Dataset

The dataset contains detailed medicine information:
id, sku_id, name
manufacturer_name, marketer_name
type, price, pack_size_label
short_composition
is_discontinued, available

3. Run the API

Start FastAPI server:

uvicorn main:app --reload

By default, it runs at:

http://127.0.0.1:8000

3.1 API Endpoints
Endpoint Description
/search/prefix?q=... Search medicines starting with q
/search/substring?q=... Search medicines containing q
/search/fulltext?q=... Full-text search in name + composition
/search/fuzzy?q=... Fuzzy search for similar names

Example:

GET http://127.0.0.1:8000/search/prefix?q=pa

3.2 Swagger Documentation

Interactive docs available at:

http://127.0.0.1:8000/docs

You can test all endpoints directly here.

3.3 API Endpoints
Endpoint Description
/search/prefix?q=... Prefix search
/search/substring?q=... Substring search
/search/fulltext?q=... Full-text search
/search/fuzzy?q=... Fuzzy (typo-tolerant) search

3.4 Streamlit UI

Run:
streamlit run app.py

4. Benchmarking

Run EXPLAIN ANALYZE in psql for each query type: prefix, substring, full-text, fuzzy.

Record latency, rows processed, and indexes used.

Document results in benchmark.md.

output of submission.py-
{
"results": {
"1": ["Avastin", "Avastin Injection"],
"2": ["Paracetamol"],
"3": ["Clexane Injection", "Avastin Injection"],
"4": ["Amoxicillin", "Azithromycin", "Ciprofloxacin"],
"5": ["Ibuprofen", "Diclofenac", "Paracetamol"]
}
}

5. Notes on Performance

Prefix & Substring Search: Trigram index on name

Full-Text Search: GIN index on search_vector

Fuzzy Search: Trigram index with % operator + similarity() function

Optimized for quick retrieval (~ms level response).

6. Project Structure
   .
   ├── main.py # FastAPI backend (all search endpoints)
   ├── app.py # Streamlit frontend (UI for search)
   ├── submission.py # Benchmark runner (creates submission.json)
   ├── python.py # Data import (loads JSON from ZIP into DB)
   ├── benchmark_queries.json
   ├── submission.json # Auto-generated benchmark results
   └── README.md # Documentation

7. Features

REST API with FastAPI
Optimized PostgreSQL queries & indexes
Typo-tolerant fuzzy search with pg_trgm
Interactive Streamlit frontend
Benchmark runner to generate submission results
Clear and well-documented README.md

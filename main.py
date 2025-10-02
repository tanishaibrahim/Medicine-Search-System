from fastapi import FastAPI, Query
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Medicine Search API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


conn = psycopg2.connect(
    dbname="medicinedb",
    user="postgres",
    password="Tanisha.si@235",
    host="localhost",
    port="5432"
)

def search_medicines(query: str, mode: str = "prefix"):
    cur = conn.cursor()

    try:
        if mode == "prefix":
            cur.execute("""
                SELECT name FROM medicines
                WHERE name ILIKE %s
                ORDER BY name
                LIMIT 20;
            """, (query + '%',))

        elif mode == "substring":
            cur.execute("""
                SELECT name FROM medicines
                WHERE name ILIKE %s
                ORDER BY name
                LIMIT 20;
            """, ('%' + query + '%',))

        elif mode == "fulltext":
            cur.execute("""
                SELECT name FROM medicines
                WHERE search_vector @@ plainto_tsquery('english', %s)
                ORDER BY name
                LIMIT 20;
            """, (query,))

        elif mode == "fuzzy":
          
            cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
            cur.execute("SET pg_trgm.similarity_threshold = 0.2;")

            cur.execute("""
                SELECT name
                FROM medicines
                WHERE similarity(name, %s) > 0.2
                ORDER BY similarity(name, %s) DESC
                LIMIT 20;
            """, (query, query))

        results = [row[0] for row in cur.fetchall()]
    except Exception as e:
        results = [f" Database error: {e}"]
    finally:
        cur.close()

    return results


@app.get("/search/prefix")
def prefix_search(q: str = Query(...)):
    return {"query": q, "type": "prefix", "results": search_medicines(q, "prefix")}

@app.get("/search/substring")
def substring_search(q: str = Query(...)):
    return {"query": q, "type": "substring", "results": search_medicines(q, "substring")}

@app.get("/search/fulltext")
def fulltext_search(q: str = Query(...)):
    return {"query": q, "type": "fulltext", "results": search_medicines(q, "fulltext")}

@app.get("/search/fuzzy")
def fuzzy_search(q: str = Query(...)):
    return {"query": q, "type": "fuzzy", "results": search_medicines(q, "fuzzy")}


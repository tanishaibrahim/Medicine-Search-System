Benchmark Report

1. Environment
   Database: PostgreSQL 18.0
   Database Name: medicinedb
   Table: medicines

Extensions: pg_trgm, unaccent

Indexes:
idx_medicines_search_vector (GIN for full-text)
idx_medicines_name_trgm (trigram for fuzzy/prefix)

Python Version: 3.13

2. Benchmark Queries

CREATE INDEX idx_medicines_name_trgm ON medicines USING gin (name gin_trgm_ops);

2.1 Prefix Search

Query:
EXPLAIN ANALYZE
SELECT name
FROM medicines
WHERE name ILIKE 'pa%'
ORDER BY name
LIMIT 20;

Output:
Limit (cost=12371.50..12371.55 rows=20 width=22) (actual time=36.838..36.842 rows=20.00 loops=1)
Buffers: shared hit=436 read=810
-> Sort (cost=12371.50..12385.65 rows=5661 width=22) (actual time=36.831..36.834 rows=20.00 loops=1)
Sort Key: name
Sort Method: still in progress Memory: 0kB
Buffers: shared hit=436 read=810
-> Bitmap Heap Scan on medicines (cost=67.99..12220.86 rows=5661 width=22) (actual time=9.594..30.703 rows=5640.00 loops=1)
Recheck Cond: (name ~~_ 'pa%'::text)
Rows Removed by Index Recheck: 529
Heap Blocks: exact=1227
Buffers: shared hit=436 read=810
-> Bitmap Index Scan on idx_medicines_name_trgm (cost=0.00..66.58 rows=5661 width=0) (actual time=3.950..3.950 rows=6169.00 loops=1)
Index Cond: (name ~~_ 'pa%'::text)
Index Searches: 1
Buffers: shared hit=19
Planning:
Buffers: shared hit=26 dirtied=1
Planning Time: 5.124 ms
Execution Time: 36.968 ms
(19 rows)

2.2 Substring Search

Query:
EXPLAIN ANALYZE
SELECT name
FROM medicines
WHERE name ILIKE '%para%'
ORDER BY name
LIMIT 20;

Output:

Limit (cost=139.93..139.98 rows=20 width=22) (actual time=2.761..2.765 rows=20.00 loops=1)
Buffers: shared hit=715
-> Sort (cost=139.93..140.00 rows=28 width=22) (actual time=2.759..2.762 rows=20.00 loops=1)
Sort Key: name
Sort Method: still in progress Memory: 0kB
Buffers: shared hit=715
-> Bitmap Heap Scan on medicines (cost=30.17..139.26 rows=28 width=22) (actual time=0.622..2.261 rows=950.00 loops=1)
Recheck Cond: (name ~~_ '%para%'::text)
Heap Blocks: exact=706
Buffers: shared hit=715
-> Bitmap Index Scan on idx_medicines_name_trgm (cost=0.00..30.16 rows=28 width=0) (actual time=0.469..0.469 rows=950.00 loops=1)
Index Cond: (name ~~_ '%para%'::text)
Index Searches: 1
Buffers: shared hit=9
Planning:
Buffers: shared hit=1
Planning Time: 0.278 ms
Execution Time: 2.865 ms
(18 rows)

2.3 Full-Text Search

Query:
EXPLAIN ANALYZE
SELECT name
FROM medicines
WHERE search_vector @@ plainto_tsquery('paracetamol')
LIMIT 20;

Output:
Limit (cost=154.50..178.63 rows=20 width=22) (actual time=14.324..14.625 rows=20.00 loops=1)
Buffers: shared hit=16 read=8
-> Bitmap Heap Scan on medicines (cost=154.50..25038.83 rows=20625 width=22) (actual time=14.320..14.617 rows=20.00 loops=1)
Recheck Cond: (search_vector @@ plainto_tsquery('paracetamol'::text))
Heap Blocks: exact=14
Buffers: shared hit=16 read=8
-> Bitmap Index Scan on idx_medicines_search_vector (cost=0.00..149.34 rows=20625 width=0) (actual time=10.747..10.747 rows=21670.00 loops=1)
Index Cond: (search_vector @@ plainto_tsquery('paracetamol'::text))
Index Searches: 1
Buffers: shared hit=1 read=8
Planning:
Buffers: shared hit=1
Planning Time: 0.630 ms
Execution Time: 15.993 ms
(14 rows)

2.4 Fuzzy Search

Query:
EXPLAIN ANALYZE
SELECT name
FROM medicines
WHERE name % 'paracetmol'
ORDER BY similarity(name, 'paracetmol') DESC
LIMIT 20;

Output:
Limit (cost=260.66..260.71 rows=20 width=26) (actual time=9.357..9.359 rows=3.00 loops=1)
Buffers: shared hit=591 read=4
-> Sort (cost=260.66..260.73 rows=28 width=26) (actual time=9.355..9.357 rows=3.00 loops=1)
Sort Key: (similarity(name, 'paracetmol'::text)) DESC
Sort Method: quicksort Memory: 25kB
Buffers: shared hit=591 read=4
-> Bitmap Heap Scan on medicines (cost=150.82..259.98 rows=28 width=26) (actual time=4.086..8.994 rows=3.00 loops=1)
Recheck Cond: (name % 'paracetmol'::text)
Rows Removed by Index Recheck: 810
Heap Blocks: exact=537
Buffers: shared hit=591 read=4
-> Bitmap Index Scan on idx_medicines_name_trgm (cost=0.00..150.81 rows=28 width=0) (actual time=2.503..2.503 rows=813.00 loops=1)
Index Cond: (name % 'paracetmol'::text)
Index Searches: 1
Buffers: shared hit=58
Planning:
Buffers: shared hit=3 read=1 dirtied=1
Planning Time: 1.595 ms
Execution Time: 9.840 ms
(19 rows)

| Query Type               | Index Used    | Rows Processed | Execution Time | Notes                                    |
| ------------------------ | ------------- | -------------- | -------------- | ---------------------------------------- |
| Prefix (`pa%`)           | Trigram Index | ~5.6K          | ~37 ms         | Efficient prefix search                  |
| Substring (`%para%`)     | Trigram Index | ~950           | ~2.8 ms        | Efficient substring search               |
| Full-text (GIN Index)    | GIN Index     | ~21.6K         | ~16 ms         | Full-text search with `search_vector`    |
| Fuzzy (`% 'paracetmol'`) | Trigram Index | ~813           | ~9.8 ms        | Returns most similar matches efficiently |

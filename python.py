import json
import psycopg2
import zipfile


conn = psycopg2.connect(
    dbname="medicinedb",
    user="postgres",             
    password="Your Password",   
    host="localhost",
    port="5432"
)
cur = conn.cursor()


cur.execute("SELECT COUNT(*) FROM medicines;")
count = cur.fetchone()[0]

if count == 0:
    
    zip_path = r"C:\Users\tanis\Downloads\DB_Dataset\DB_Dataset\data.zip"

   
    with zipfile.ZipFile(zip_path, 'r') as z:
        
        for filename in z.namelist():
            if filename.endswith('.json'):
                print(f"Importing {filename}...")
                with z.open(filename) as f:
                    data = json.load(f)
                    for record in data:
                        cur.execute("""
                            INSERT INTO medicines (
                                id, sku_id, name, manufacturer_name, marketer_name,
                                type, price, pack_size_label, short_composition,
                                is_discontinued, available
                            )
                            VALUES (%(id)s, %(sku_id)s, %(name)s, %(manufacturer_name)s, %(marketer_name)s,
                                    %(type)s, %(price)s, %(pack_size_label)s, %(short_composition)s,
                                    %(is_discontinued)s, %(available)s)
                            ON CONFLICT (id) DO NOTHING;
                        """, record)
    conn.commit()
    print("All JSON files imported successfully!")
else:
    print(f"Database already has {count} records. Skipping import.")

cur.close()
conn.close()

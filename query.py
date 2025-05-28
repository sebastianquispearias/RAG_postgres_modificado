import os
from psycopg import connect
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.embeddings.create(
    input="¿Hubo un pico en costo de combustible este mes?",
    model="text-embedding-ada-002"
)
qemb = resp.data[0].embedding

conn = connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    dbname=os.getenv("PG_DATABASE")
)

with conn.cursor() as cur:
    cur.execute("""
    SELECT source,
            content,
            (embedding <-> %s::vector) AS distancia
        FROM documents
    ORDER BY distancia
    LIMIT 5;
    """, (qemb,))



    for src, txt, dist in cur.fetchall():
        print(f"{src}: {txt}  (dist={dist:.4f})")

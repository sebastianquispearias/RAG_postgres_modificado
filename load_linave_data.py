import os
import psycopg
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # carga variables de .env

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conexión PostgreSQL
conn = psycopg.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    dbname=os.getenv("PG_DATABASE")
)

def get_embedding(text: str) -> list[float]:
    resp = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp.data[0].embedding

def insert_document(source: str, content: str):
    emb = get_embedding(content)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO documents (source, content, embedding) VALUES (%s, %s, %s)",
            (source, content, emb)
        )
    conn.commit()
    print(f"✔ Insertado: {source}")

def main():
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        # Ajusta el nombre de la tabla y columnas a tu esquema
        cur.execute("SELECT * FROM abastecimentos")
        rows = cur.fetchall()

    for row in rows:
        # Construye un texto a partir de los campos que te interesen
        texto = (
            f"Veículo #{row['Numero Veiculo']} | "
            f"Placa: {row['Placa']} | "
            f"Data: {row['Data']} | "
            f"Custo Combustível: {row['Custo Combustivel']}"
        )
        # Usa, por ejemplo, "abastecimentos:ID" como fuente
        fuente = f"abastecimentos:{row['Numero Veiculo']}"
        insert_document(fuente, texto)

if __name__ == "__main__":
    main()

import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# 1. Carga variables de entorno
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db   = os.getenv("DB_NAME")

# 2. Crea la URL de conexión
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

# 3. Crea el engine de SQLAlchemy
engine = create_engine(url, echo=False)

# 4. Lee una tabla completa (o una consulta) directamente a pandas
df_abastecimientos = pd.read_sql("SELECT * FROM public.abastecimentos", engine)

print(df_abastecimientos.head())

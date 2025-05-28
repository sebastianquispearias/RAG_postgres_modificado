-- Habilita la extensión vector, si no está ya
CREATE EXTENSION IF NOT EXISTS vector;

-- Crea la tabla de documentos para almacenar embeddings
CREATE TABLE IF NOT EXISTS documents (
  id        SERIAL PRIMARY KEY,
  source    TEXT    NOT NULL,      -- de dónde viene (tabla, id, etc.)
  content   TEXT    NOT NULL,      -- el texto plano
  embedding vector(1536) NOT NULL  -- tamaño del embedding
);

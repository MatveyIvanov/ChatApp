#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER chat_admin;
    CREATE DATABASE chat;
    GRANT ALL PRIVILEGES ON DATABASE chat TO chat_admin;
EOSQL
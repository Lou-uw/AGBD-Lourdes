"""Migración mínima del esquema existente.

`Base.metadata.create_all()` crea las tablas que faltan, pero no modifica
las tablas que ya existen. Este script agrega con `ALTER TABLE` las columnas
que necesita el backend Kotlin, solamente si todavía no están.

Uso:
    python migrar.py

No crea tablas ni carga datos: si una tabla no existe, avisa y la omite
(en ese caso conviene correr primero `python schema.py`).
"""

from sqlalchemy import inspect, text

from schema import engine

# (tabla, columna, definición SQL) — deben coincidir con schema.py
COLUMNAS_NUEVAS = [
    ("pedidos", "notas", "VARCHAR(300)"),
    ("detalle_pedido", "es_regalo", "TINYINT(1) DEFAULT 0"),
]


def migrar(engine_):
    inspector = inspect(engine_)
    tablas = set(inspector.get_table_names())
    agregadas = 0
    existentes = 0
    omitidas = 0

    with engine_.begin() as conexion:
        for tabla, columna, definicion in COLUMNAS_NUEVAS:
            if tabla not in tablas:
                print(f"AVISO: la tabla '{tabla}' no existe; se omite {tabla}.{columna}.")
                omitidas += 1
                continue

            columnas = {c["name"] for c in inspector.get_columns(tabla)}
            if columna in columnas:
                print(f"OK: {tabla}.{columna} ya existe.")
                existentes += 1
                continue

            conexion.execute(
                text(f"ALTER TABLE `{tabla}` ADD COLUMN `{columna}` {definicion}")
            )
            print(f"Agregada: {tabla}.{columna} ({definicion})")
            agregadas += 1

    print(
        f"Migración terminada: {agregadas} columna(s) agregada(s), "
        f"{existentes} ya existían, {omitidas} omitida(s)."
    )


if __name__ == "__main__":
    migrar(engine)

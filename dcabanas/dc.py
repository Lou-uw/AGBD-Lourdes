
from sqlalchemy import URL, create_engine, text

DB_HOST = "10.9.120.5"
DB_PORT = 3306
DB_DATABASE = "D-Cabanas"
DB_USERNAME = "dCabana"
DB_PASSWORD = "dc123456"

url = URL.create(
    "mysql+pymysql",
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
    username=DB_USERNAME,
    password=DB_PASSWORD,
)

engine = create_engine(url, connect_args={"connect_timeout": 10, "read_timeout": 10})

conexion = engine.connect()
print("Conectado:", conexion.execute(text("SELECT DATABASE()")).scalar())

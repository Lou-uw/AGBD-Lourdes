from sqlalchemy import URL, create_engine, text, Column, Integer, String, Boolean, ForeignKey, Float, Text, DATETIME
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass


class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)      # Pizzas, Papas fritas, Bebidas

class Tamanios(Base):
    __tablename__ = "tamanios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)      # Mediana, Grande, Familiar

class TiposSabor(Base):
    __tablename__ = "tipos_sabor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)      # Clásico, Especial

class Bordes(Base):
    __tablename__ = "bordes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)      # los 3 sabores de borde


class PreciosPizza(Base):
    __tablename__ = "precios_pizza"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_sabor_id = Column(Integer, ForeignKey("tipos_sabor.id"), nullable=False)
    tamanio_id = Column(Integer, ForeignKey("tamanios.id"), nullable=False)
    precio = Column(Float, nullable=False)

class PreciosBorde(Base):
    __tablename__ = "precios_borde"
    id = Column(Integer, primary_key=True, autoincrement=True)
    borde_id = Column(Integer, ForeignKey("bordes.id"), nullable=False)
    tamanio_id = Column(Integer, ForeignKey("tamanios.id"), nullable=False)
    precio = Column(Float, nullable=False)

class Clientes(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    telefono = Column(String(100))
    direccion = Column(String(300))

    pedidos = relationship("Pedidos", back_populates="cliente")

class Productos(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    tipo_sabor_id = Column(Integer, ForeignKey("tipos_sabor.id"))   # solo pizzas
    precio = Column(Float)                                           # solo papas y bebidas
    stock = Column(Integer)
    activo = Column(Boolean, default=True)

class Pedidos(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATETIME)
    total = Column(Float)
    estado = Column(String(100))
    forma_pago = Column(String(30))
    direccion_entrega = Column(String(300))  
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Clientes", back_populates="pedidos")

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tamanio_id = Column(Integer, ForeignKey("tamanios.id"))   # vacío en papas y bebidas
    borde_id = Column(Integer, ForeignKey("bordes.id"))       # vacío si no pidió borde
    cantidad = Column(Integer)
    precio_unitario = Column(Float)                           # precio de la pizza/producto en ese pedido
    precio_borde = Column(Float, default=0)                   # precio del borde en ese pedido
    descripcion = Column(Text)     

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
    password=DB_PASSWORD
)

engine = create_engine(url, connect_args={"connect_timeout": 10, "read_timeout": 10})

Base.metadata.create_all(engine)

conexion = engine.connect()
print("Conectado:", conexion.execute(text("SELECT DATABASE()")).scalar())
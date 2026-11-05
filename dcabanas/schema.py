from sqlalchemy import URL, create_engine, text, Column, Integer, String, Boolean, ForeignKey, Float, Text, DATETIME
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)   # Pizzas Clásicas, Pizzas Especiales, Papas Fritas, Gaseosas, Adicionales

    productos = relationship("Productos", back_populates="categoria")


class Tamanios(Base):
    __tablename__ = "tamanios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)   # Mediana, Grande, Familiar
    porciones = Column(Integer)
    precio_clasica = Column(Float, nullable=False)
    precio_especial = Column(Float, nullable=False)
    precio_borde = Column(Float, nullable=False)


class Productos(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    precio = Column(Float)                        # vacío en pizzas (el precio sale del tamaño)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)

    categoria = relationship("Categorias", back_populates="productos")


class Pedidos(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DATETIME)
    total = Column(Float)
    estado = Column(String(50))
    forma_pago = Column(String(30))
    cliente_nombre = Column(String(100))
    cliente_telefono = Column(String(50))
    direccion_entrega = Column(String(300))

    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tamanio_id = Column(Integer, ForeignKey("tamanios.id"))   # vacío en papas, gaseosas y adicionales
    con_borde = Column(Boolean, default=False)                # solo pizzas
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    precio_borde = Column(Float, default=0)

    pedido = relationship("Pedidos", back_populates="detalles")
    producto = relationship("Productos")
    tamanio = relationship("Tamanios")


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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with engine.connect() as conexion:
        print("Conectado:", conexion.execute(text("SELECT DATABASE()")).scalar())
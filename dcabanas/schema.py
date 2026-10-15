from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Cliente(Base): 
    __tablename__ = "clientes" 
    id = Column(Integer, primary_key=True, autoincrement = True) 
    nombre = Column(String) 
    apellido = Column(String) 
    telefono = Column(String) 
    direccion = Column(String) 

    pedidos = relationship("Pedido", back_populates="cliente")

class Producto(Base): 
    __tablename__ = "productos" 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    categoria = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    activo = Column(Boolean, default=True)

class Pedido(Base): 
    __tablename__ = "pedidos" 
    id = Column(Integer, primary_key=True, autoincrement = True) 
    fecha = Column(String) 
    total = Column(Integer) 
    estado = Column(String) 
    cliente_id = Column(Integer, ForeignKey("clientes.id")) 
    repartidor_id = Column(Integer, ForeignKey("repartidores.id")) 

    cliente = relationship("Cliente", back_populates="pedidos")

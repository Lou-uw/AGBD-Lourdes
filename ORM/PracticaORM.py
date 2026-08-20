from sqlalchemy import Column, Integer, String, Boolean, create_engine 
from sqlalchemy.orm import DeclarativeBase, Session 

class Base(DeclarativeBase): 
    pass 

class Producto(Base): 
    __tablename__ = "productos" 

    id = Column(Integer, primary_key=True) 
    nombre = Column(String) 
    precio = Column(Integer) 
    stock = Column(Integer) 
    categoria = Column(String) 
    activo = Column(Boolean, default=True) 

 
engine = create_engine("sqlite:///mi_app_tecno.db") 
Base.metadata.create_all(engine) 

with Session(engine) as session: 
    productos = [ 
        Producto(nombre = "Teclado mecanico", precio = 8500, stock = 15, categoria = "perifericos"),  
        Producto(nombre = "Mouse inalambrico", precio = 4200, stock = 30, categoria = "perifericos"), 
        Producto(nombre = "Monitor 24 pulgadas", precio = 62000, stock = 8, categoria = "monitores"), 
        Producto(nombre = "Auriculares bluetooth", precio = 6000, stock = 12300, categoria = "audio"),  
        Producto(nombre = "Webcam Full HD", precio = 9800, stock = 12, categoria = "perifericos"),  
        Producto(nombre = "SSD 1TB", precio = 18500, stock = 25, categoria = "almacenamiento"), 
        Producto(nombre = "RAM 16GB", precio = 15600, stock = 18, categoria = "componentes"), 
        Producto(nombre = "Mousepad XL", precio = 2100, stock = 40, categoria = "perifericos"), 
        Producto(nombre = "Hub USB-C", precio = 5400, stock = 6, categoria = "accesorios", activo = False), 
        Producto(nombre = "Cable HDMI", precio = 1800, stock = 50, categoria = "accesorios"), 
    ] 

    

    session.add_all(productos) 
    session.commit()
        
    cantidad_total = session.query(Producto).count() 
    print(f"Total en la base de datos: {cantidad_total}") 

    # Punto 3: Traigan todos los productos de la categoria &quot;perifericos&quot; y muestren nombre y precio. 

    productos_perifericos = session.query(Producto).filter(Producto.categoria == "perifericos").all() 

    for p in productos_perifericos: 
    print(p.nombre, p.precio) 

    # Punto 4: Traigan los productos cuyo precio sea mayor a $10000. Ordenenlos de mayor a menor precio. 

    productos_mayor_10000 = session.query(Producto).filter(Producto.precio > 10000).order_by(Producto.precio.desc()) 

    print("--- Productos mayores a 10000 ---") 
    for p in productos_mayor_10000: 
    print(p.nombre, p.precio) 

    # Punto 5: Traigan los productos con stock menor o igual a 12 que esten activos. 
    # ¿Por que no aparece el Hub USB-C si tiene stock 6? 

    productos_activos_12 = session.query(Producto).filter(Producto.stock <= 12).filter(Producto.activo == True).order_by(Producto.stock.desc()) 

    print("--- Productos con stock menor o igual a 12 ---") 
    for p in productos_activos_12: 
    print(p.nombre, p.precio, p.stock) 

    



from sqlalchemy import Column, Integer, String, Boolean, create_engine, or_
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
        Producto(nombre = "Auriculares inalambricos", precio = None, stock = 10, categoria = None)
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
    # No aparece porque tiene que estar activo y no lo está.

    productos_activos_12 = session.query(Producto).filter(Producto.stock <= 12).filter(Producto.activo == True).order_by(Producto.stock.desc()) 

    print("--- Productos con stock menor o igual a 12 ---") 
    for p in productos_activos_12: 
        print(p.nombre, p.precio, p.stock) 
   # Punto 6: Traigan los productos cuyo precio este entre $5000 y $20000. 
   # Usen dos .filter() o and_().

    productos_entre_5000_y_20000 = session.query(Producto).filter(Producto.precio >= 5000).filter(Producto.precio <= 20000)

    print("--- Productos entre $5000 y $20000 ---")
    for p in productos_entre_5000_y_20000: 
        print(p.nombre, p.precio, p.stock)
   # Punto 7: Traigan el producto mas caro de toda la tabla. Usen .order_by() y .first().

    producto_mas_caro = session.query(Producto).order_by(Producto.precio.desc()).first()

    print("--- Producto más caro ---")
    print(producto_mas_caro.nombre, producto_mas_caro.precio, producto_mas_caro.stock)

  # Punto 8: Filtren los productos que esten inactivos (activo == False). Tienen que aparecer solo el Hub USB-C.

    productos_inactivos = session.query(Producto).filter(Producto.activo == False)

    print("--- Producto inactivo ---")
    for p in productos_inactivos:
     print(p.nombre)
 # Punto 9:  Traigan los productos que sean de la categoría "audio" o de la categoría "componentes". Usen or_() de sqlalchemy.

    productos_audio_o_componentes = session.query(Producto).filter(or_(Producto.categoria == "audio", Producto.categoria == "componentes"))

    print("--- Productos categoria especificas ---")
    for p in productos_audio_o_componentes:
        print(p.nombre, p.categoria)

# Punto 10: Traigan todos los productos cuyo nombre contenga la letra "a" (minuscula). Usen .contains(). ¿Cuántos aparecen?
# Son 8 productos que contienen la letra a en su nombre
    productos_con_a = session.query(Producto).filter(Producto.nombre.contains("a"))

    print("--- Productos que su nombre contiene a ---")
    for p in productos_con_a:
        print(p.nombre)

# Punto 11: Traigan los productos cuyo nombre empiece con "M". Usen .startswith(). Tienen que aparecer 3.

    productos_que_empiezan_con_m =session.query(Producto).filter(Producto.nombre.startswith("M"))

    print("--- Productos que su nombre empieza con M ---")
    for p in productos_que_empiezan_con_m:
        print(p.nombre)
# Punto 12: Agreguen un producto nuevo sin categoria (categoria=None) y sin precio (precio=None). Despues traigan con una query todos los productos que tengan categoria en NULL. 
# Usen .filter(Producto.categoria == None).
#¿Que pasa si filtran por precio == None? ¿Aparece el mismo producto? Si, porque el producto cumple con las dos condiciones

    productos_categoria_NULL = session.query(Producto).filter(Producto.categoria == None).all()

    print("--- Productos con categoria NULL ---")
    for p in productos_categoria_NULL: 
        print(f"Nombre: {p.nombre} | Categoría: {p.categoria} | Precio: {p.precio}")

    # 3. Prueba filtrando por precio == None
    productos_precio_NULL = session.query(Producto).filter(Producto.precio == None).all()

    print("--- Productos con precio NULL ---")
    for p in productos_precio_NULL: 
        print(f"Nombre: {p.nombre} | Categoría: {p.categoria} | Precio: {p.precio}")

# Punto 13: Busquen el Hub USB-C por id con session.get() y actualicen su stock a 20 y su activo a True. 
# Hagan commit y verifiquen que los cambios quedaron guardados haciendo una query por id.
    hub = session.get(Producto, 9)
     
    if hub:  

        print(f"Antes del cambio: Stock = {hub.stock}, Activo = {hub.activo}")  

        hub.stock = 20 
        hub.activo = True  

        session.commit()  
        print("¡Cambios guardados con éxito!")  

        hub_actualizado = session.get(Producto, 9)  
        print(f"Después del cambio: Stock = {hub_actualizado.stock}, Activo = {hub_actualizado.activo}")  

    else:  
        print("No se encontró el producto con ese ID.") 

# Punto 14: Actualicen el precio de todos los productos de la categoria "perifericos" aplicandoles un aumento del 10%.
# Traigan los productos, recorranlos en un for, modifiquen el precio y hagan un solo commit al final.

    productos_categoria_perifericos = session.query(Producto).filter(Producto.categoria == "perifericos") 

    def SacarPorcentaje (precio): 
        porcentaje = (precio * 10) / 100 
        return porcentaje 

    print("-- Precios normales --") 
    for p in productos_categoria_perifericos: 
        print(p.precio) 

    print("-- Precios con el aumento del 10% --") 
    for p in productos_categoria_perifericos: 
        precios_aumento = SacarPorcentaje(p.precio) + p.precio 
        print(precios_aumento) 

# Punto 15: Eliminen el Cable HDMI de la base de datos. Busquenlo por id, usen session.delete() y hagan 
# commit. Verifiquen que el .count() quedo en 10 (o en 11 si agregaron el del ej 12). 

    cable_hdmi = session.get(Producto, 10) 

    if cable_hdmi: 
        session.delete(cable_hdmi) 
        session.commit()

        print(f"Producto eliminado: {cable_hdmi.nombre}") 

    else: 

        print("No se encontro el producto con ese ID") 

total_actualizado = session.query(Producto).count()
print(f"Total de productos en la base de datos: {total_actualizado}") 

# Punto 16: Eliminen todos los productos que tengan precio menor a $2000 o que esten inactivos. Traigan 
# los que cumplen la condicion, recorranlos y eliminenlos uno por uno con session.delete(). ¿Cuantos 
# borraron? 

productos_a_eliminar = session.query(Producto).filter(or_(Producto.precio < 2000, Producto.activo == False)).all()

contador_borrados = 0

print("--- Eliminando productos uno por uno ---")
for p in productos_a_eliminar:
    print(f"Borrando: {p.nombre} (Precio: {p.precio}, Activo: {p.activo})")
    session.delete(p)
    contador_borrados += 1

session.commit()

# 4. Respuesta a la pregunta: ¿Cuántos borraron?
print(f"\nSe borraron un total de {contador_borrados} productos.")

total_productos_actualizados = session.query(Producto).count()
print(f"Total de productos que quedaron en la base de datos: {total_productos_actualizados}")

 # Luego de terminar: 



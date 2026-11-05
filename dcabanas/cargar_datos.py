import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from schema import Base, Categorias, DetallePedido, Pedidos, Productos, Tamanios, engine

CATEGORIAS = ["Pizzas Clásicas", "Pizzas Especiales", "Papas Fritas", "Gaseosas", "Adicionales"]

# (nombre, porciones, precio clásica, precio especial, precio borde)
TAMANIOS = [
    ("Mediana", 8, 30000, 40000, 5000),
    ("Grande", 10, 40000, 50000, 8000),
    ("Familiar", 12, 60000, 70000, 10000),
]

# Las pizzas no llevan precio: sale del tamaño
CLASICAS = [
    ("Napolitana", "Salsa de tomate, mozzarella, jamón, tomate, orégano."),
    ("Jamón", "Salsa de tomate, mozzarella, jamón, orégano."),
    ("Mozzarella", "Salsa de tomate, mozzarella, tomate, orégano."),
    ("Margarita", "Salsa de tomate, mozzarella, tomate, albahaca, orégano."),
    ("Calabreza", "Salsa de tomate, mozzarella, calabresa, cebolla (opcional), orégano."),
    ("Calabresa picante", "Salsa de tomate, mozzarella, calabresa, pimienta de calabresa, orégano."),
    ("Calabresa al ajo", "Salsa de tomate, mozzarella, calabresa, ajo frito, orégano."),
    ("Bacon", "Salsa de tomate, mozzarella, bacon, orégano."),
    ("Bacon al ajo", "Salsa de tomate, mozzarella, bacon, ajo frito, orégano."),
    ("Pollo catupiry", "Salsa de tomate, mozzarella, pollo, catupiry, orégano."),
    ("Caipira", "Salsa de tomate, mozzarella, pollo, choclo, orégano."),
    ("Pizza al ajo", "Salsa de tomate, mozzarella, ajo frito, orégano."),
    ("Choclo", "Salsa de tomate, mozzarella, choclo, orégano."),
    ("Palmito", "Salsa de tomate, mozzarella, palmito, orégano."),
]

ESPECIALES = [
    ("Especial de la cabaña", "Salsa de tomate, mozzarella, pollo, jamón, calabresa, choclo, catupiry, orégano."),
    ("Pepperoni", "Salsa de tomate, mozzarella, pepperoni, orégano."),
    ("Cuatro quesos", "Salsa de tomate, mozzarella, catupiry, cheddar, queso gorgonzola, orégano."),
    ("Atún", "Salsa de tomate, mozzarella, atún, cebolla, orégano."),
    ("Portuguesa", "Salsa de tomate, mozzarella, jamón, tomate, locote, huevo rayado, cebolla, orégano."),
    ("Vegetariana", "Salsa de tomate, mozzarella, palmito, tomate, locote, cebolla, choclo, aceituna, orégano."),
    ("Mexicana", "Salsa de tomate, mozzarella, calabresa, cebolla colorada, locote, picante, orégano."),
    ("Española", "Salsa de tomate, mozzarella, calabresa, bacon, tomate, picante, orégano."),
]

# (nombre, precio, descripcion)
PAPAS = [
    ("Papas fritas mediana", 10000, "Porción de 200 gramos."),
    ("Papas fritas grande", 20000, "Porción de 400 gramos."),
]
GASEOSAS = [
    ("Coca-Cola 1 L", 10000, "Gaseosa Coca-Cola de 1 litro."),
    ("Coca-Cola 1,5 L", 15000, "Gaseosa Coca-Cola de 1,5 litros."),
    ("Coca-Cola 2 L", 17000, "Gaseosa Coca-Cola de 2 litros."),
]
ADICIONALES = [
    ("Adicional bacon y cheddar", 5000, "Adicional para las papas fritas."),
]

CLIENTES = [
    ("Lucía Fernández", "0981 123 456", "Av. Mariscal López 1234, Asunción"),
    ("Mateo González", "0982 234 567", "Calle Palma 567, Asunción"),
    ("Sofía Rodríguez", "0983 345 678", "Av. España 890, Asunción"),
    ("Martín Pérez", "0984 456 789", "Calle Colón 234, Lambaré"),
    ("Valentina López", "0985 567 890", "Av. Eusebio Ayala 678, Asunción"),
    ("Joaquín Martínez", "0986 678 901", "Calle 14 de Mayo 345, San Lorenzo"),
]

ESTADOS = ["Pendiente", "En preparación", "En camino", "Entregado", "Entregado", "Entregado", "Cancelado"]
FORMAS_PAGO = ["Efectivo", "Tarjeta", "Transferencia"]


def cargar_datos(session):
    if session.query(Categorias).count() > 0:
        print("La base ya tiene datos. No se carga nada para no duplicar.")
        return

    random.seed(2024)

    # Categorías
    categorias = {}
    for nombre in CATEGORIAS:
        categoria = Categorias(nombre=nombre)
        session.add(categoria)
        categorias[nombre] = categoria

    # Tamaños (con los precios reales de la carta)
    tamanios = []
    for nombre, porciones, clasica, especial, borde in TAMANIOS:
        tamanio = Tamanios(
            nombre=nombre,
            porciones=porciones,
            precio_clasica=clasica,
            precio_especial=especial,
            precio_borde=borde,
        )
        session.add(tamanio)
        tamanios.append(tamanio)

    # Productos
    for nombre, descripcion in CLASICAS:
        session.add(Productos(nombre=nombre, descripcion=descripcion,
                              categoria=categorias["Pizzas Clásicas"], precio=None, activo=True))
    for nombre, descripcion in ESPECIALES:
        session.add(Productos(nombre=nombre, descripcion=descripcion,
                              categoria=categorias["Pizzas Especiales"], precio=None, activo=True))
    for nombre, precio, descripcion in PAPAS:
        session.add(Productos(nombre=nombre, descripcion=descripcion,
                              categoria=categorias["Papas Fritas"], precio=precio, activo=True))
    for nombre, precio, descripcion in GASEOSAS:
        session.add(Productos(nombre=nombre, descripcion=descripcion,
                              categoria=categorias["Gaseosas"], precio=precio, activo=True))
    for nombre, precio, descripcion in ADICIONALES:
        session.add(Productos(nombre=nombre, descripcion=descripcion,
                              categoria=categorias["Adicionales"], precio=precio, activo=True))
    session.flush()

    pizzas = session.query(Productos).filter(Productos.precio.is_(None)).all()
    otros = session.query(Productos).filter(Productos.precio.isnot(None)).all()

    # Pedidos de prueba
    for _ in range(15):
        nombre, telefono, direccion = random.choice(CLIENTES)
        pedido = Pedidos(
            fecha=datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 12)),
            estado=random.choice(ESTADOS),
            forma_pago=random.choice(FORMAS_PAGO),
            cliente_nombre=nombre,
            cliente_telefono=telefono,
            direccion_entrega=direccion,
            total=0.0,
        )

        items = random.sample(pizzas, k=random.randint(1, 2))
        if random.random() < 0.6:
            items += random.sample(otros, k=1)

        total = 0.0
        for producto in items:
            if producto.precio is None:  # es pizza
                tamanio = random.choice(tamanios)
                es_especial = producto.categoria.nombre == "Pizzas Especiales"
                precio_unitario = tamanio.precio_especial if es_especial else tamanio.precio_clasica
                con_borde = random.random() < 0.5
                precio_borde = tamanio.precio_borde if con_borde else 0.0
                cantidad = random.randint(1, 2)
            else:
                tamanio = None
                precio_unitario = producto.precio
                con_borde = False
                precio_borde = 0.0
                cantidad = 1

            pedido.detalles.append(DetallePedido(
                producto=producto,
                tamanio=tamanio,
                con_borde=con_borde,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_borde=precio_borde,
            ))
            total += (precio_unitario + precio_borde) * cantidad

        pedido.total = total
        session.add(pedido)

    session.commit()

    print("Datos cargados correctamente.")
    print("  Categorías:", session.query(Categorias).count())
    print("  Tamaños:   ", session.query(Tamanios).count())
    print("  Productos: ", session.query(Productos).count())
    print("  Pedidos:   ", session.query(Pedidos).count())
    print("  Detalles:  ", session.query(DetallePedido).count())


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        cargar_datos(session)
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from schema import (
    Base,
    Categorias,
    DetallePedido,
    Pedidos,
    Productos,
    Tamanios,
    engine,
)


CATEGORIAS = [
    "Pizzas Clásicas",
    "Pizzas Especiales",
    "Pizzas Dulces",
    "Papas Fritas",
    "Bebidas",
    "Bordes",
]

TAMANIOS = [
    {"nombre": "Chica", "porciones": 4, "factor_precio": 0.80},
    {"nombre": "Mediana", "porciones": 6, "factor_precio": 1.00},
    {"nombre": "Grande", "porciones": 8, "factor_precio": 1.30},
    {"nombre": "Familiar", "porciones": 12, "factor_precio": 1.60},
]

# (nombre, precio, descripcion)
PRODUCTOS = {
    "Pizzas Clásicas": [
        ("Muzzarella", 8500, "Salsa de tomate, muzzarella y orégano."),
        ("Napolitana", 9500, "Salsa de tomate, muzzarella, tomate y ajo."),
        ("Jamón y Morrones", 10500, "Muzzarella, jamón cocido y morrones."),
        ("Fugazzeta", 10000, "Muzzarella, cebolla y orégano."),
        ("Cuatro Quesos", 11500, "Muzzarella, provolone, roquefort y parmesano."),
        ("Calabresa", 11000, "Muzzarella, salame calabrés y morrones."),
        ("Anchoas", 12000, "Salsa de tomate, muzzarella y anchoas."),
    ],
    "Pizzas Especiales": [
        ("Pepperoni", 12500, "Muzzarella, pepperoni y orégano."),
        ("Palmitos", 13000, "Muzzarella, palmitos, salsa golf y huevo."),
        ("Rúcula y Provolone", 14000, "Muzzarella, rúcula fresca y provolone."),
        ("Panceta y Cheddar", 14500, "Muzzarella, panceta ahumada y cheddar."),
        ("Pollo BBQ", 13500, "Muzzarella, pollo, salsa BBQ y cebolla morada."),
        ("Vegetariana", 12000, "Muzzarella, tomate, morrón, cebolla y aceitunas."),
        ("Tentación", 15000, "Muzzarella, jamón, panceta, huevo y morrones."),
    ],
    "Pizzas Dulces": [
        ("Dulce de Leche y Banana", 9000, "Dulce de leche, banana y azúcar impalpable."),
        ("Chocolate y Almendras", 9500, "Chocolate negro, almendras y crema."),
        ("Frutilla y Crema", 10000, "Crema pastelera, frutillas y merengue."),
    ],
    "Papas Fritas": [
        ("Papas Clásicas", 5500, "Papas fritas con sal fina."),
        ("Papas con Cheddar", 7500, "Papas fritas con salsa cheddar."),
        ("Papas con Bacon", 8500, "Papas fritas con cheddar y bacon."),
        ("Papas Rústicas", 6500, "Papas rústicas con piel y especias."),
    ],
    "Bebidas": [
        ("Coca-Cola 1.5L", 3500, "Gaseosa línea Coca-Cola."),
        ("Coca-Cola Zero 1.5L", 3500, "Gaseosa sin azúcar."),
        ("Sprite 1.5L", 3200, "Gaseosa sabor limón."),
        ("Agua Mineral 500ml", 1800, "Agua mineral sin gas."),
        ("Cerveza Rubia 1L", 4500, "Cerveza rubia artesanal."),
        ("Jugo de Naranja 1L", 3000, "Jugo exprimido."),
    ],
    "Bordes": [
        ("Borde de Queso", 1500, "Borde relleno con muzzarella."),
        ("Borde de Cheddar", 1800, "Borde relleno con cheddar."),
        ("Borde de Bacon", 2000, "Borde relleno con cheddar y bacon."),
        ("Borde de Provolone", 1700, "Borde relleno con provolone."),
    ],
}

CLIENTES = [
    ("Lucía Fernández", "11 4567-8901", "Av. Rivadavia 1234, CABA"),
    ("Mateo González", "11 4567-8902", "Calle Mitre 567, Lanús"),
    ("Sofía Rodríguez", "11 4567-8903", "Av. San Martín 890, Quilmes"),
    ("Martín Pérez", "11 4567-8904", "Belgrano 234, Avellaneda"),
    ("Valentina López", "11 4567-8905", "Sarmiento 678, Lomas de Zamora"),
    ("Joaquín Martínez", "11 4567-8906", "Av. Alsina 345, Banfield"),
    ("Camila Sánchez", "11 4567-8907", "Moreno 123, Temperley"),
    ("Tomás Romero", "11 4567-8908", "Brown 456, Adrogué"),
    ("Mía Díaz", "11 4567-8909", "Rivadavia 789, Ezeiza"),
    ("Benjamín Torres", "11 4567-8910", "Italia 234, Monte Grande"),
]

ESTADOS = ["Pendiente", "En preparación", "En camino", "Entregado", "Entregado", "Entregado", "Cancelado"]

FORMAS_PAGO = ["Efectivo", "Tarjeta", "Mercado Pago", "Transferencia"]


def cargar_datos(session):
    random.seed(2024)

    categorias = {}
    for nombre in CATEGORIAS:
        categoria = Categorias(nombre=nombre)
        session.add(categoria)
        categorias[nombre] = categoria
    session.flush()

    tamanios = []
    for datos in TAMANIOS:
        tamanio = Tamanios(**datos)
        session.add(tamanio)
        tamanios.append(tamanio)
    session.flush()

    productos = {}
    for nombre_categoria, items in PRODUCTOS.items():
        productos[nombre_categoria] = []
        for nombre, precio, descripcion in items:
            producto = Productos(
                nombre=nombre,
                descripcion=descripcion,
                categoria=categorias[nombre_categoria],
                precio=precio,
                stock=random.randint(20, 120),
                activo=True,
            )
            session.add(producto)
            productos[nombre_categoria].append(producto)
    session.flush()

    pizzas = productos["Pizzas Clásicas"] + productos["Pizzas Especiales"] + productos["Pizzas Dulces"]
    acompanamientos = productos["Papas Fritas"] + productos["Bebidas"]
    bordes = productos["Bordes"]

    for _ in range(30):
        cliente = random.choice(CLIENTES)
        pedido = Pedidos(
            fecha=datetime.now()
            - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59),
            ),
            estado=random.choice(ESTADOS),
            forma_pago=random.choice(FORMAS_PAGO),
            cliente_nombre=cliente[0],
            cliente_telefono=cliente[1],
            direccion_entrega=cliente[2],
            total=0.0,
        )

        cantidad_items = random.randint(1, 3)
        items = random.sample(pizzas, k=min(2, cantidad_items))
        if cantidad_items > len(items):
            items += random.sample(acompanamientos, k=cantidad_items - len(items))

        total = 0.0
        for producto in items:
            es_pizza = producto.categoria.nombre.startswith("Pizzas")
            tamanio = random.choice(tamanios) if es_pizza else None
            borde = random.choice(bordes) if es_pizza and random.random() < 0.55 else None
            cantidad = random.randint(1, 2) if es_pizza else 1

            factor = tamanio.factor_precio if tamanio else 1.0
            precio_unitario = round(producto.precio * factor, 2)
            precio_borde = round(borde.precio * factor, 2) if borde else 0.0

            detalle = DetallePedido(
                producto=producto,
                tamanio=tamanio,
                borde=borde,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_borde=precio_borde,
            )
            pedido.detalles.append(detalle)
            total += (precio_unitario + precio_borde) * cantidad

        pedido.total = round(total, 2)
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

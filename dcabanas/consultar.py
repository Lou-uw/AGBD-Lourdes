from schema import Categorias, Productos


def listar_productos_por_categoria(session, nombre_categoria):
    return (
        session.query(Productos)
        .join(Productos.categoria)
        .filter(Categorias.nombre == nombre_categoria, Productos.activo.is_(True))
        .order_by(Productos.nombre)
        .all()
    )

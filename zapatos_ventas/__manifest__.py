{
    'name': 'Ventas de Zapatos',
    'version': '1.0',
    'summary': 'Módulo para registrar ventas de zapatos',
    'description': 'Permite registrar ventas, calcular el total y actualizar el inventario.',
    'author': 'Mateo',
    'depends': ['base', 'zapatos'],
    'data': [
        'security/ir.model.access.csv',
        'views/venta_views.xml',
    ],
    'installable': True,
    'application': True,
}
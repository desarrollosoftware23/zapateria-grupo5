{
    'name': 'Zapatería manejo proveedores',
    'version': '1.0',
    'summary': 'Módulo para registrar pedidos a proveedores de zapatos',
    'description': 'Permite registrar y gestionar pedidos realizados a proveedores del inventario de zapatos.',
    'author': 'Alejo',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['zapatos', 'zapatos_extension'],
    'data': [
        'security/ir.model.access.csv',
        'views/zapato_pedido_proveedor.xml',
    ],
    'installable': True,
    'application': False,
}

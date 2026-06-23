{
    'name': 'Zapatos Proveedores',
    'version': '1.0',
    'summary': 'Gestión de proveedores de la zapatería',
    'description': 'Módulo independiente para registrar y gestionar proveedores.',
    'author': 'Alejo',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['zapatos'],
    'data': [
        'security/ir.model.access.csv',
        'views/proveedor_views.xml',
    ],
    'installable': True,
    'application': False,
}
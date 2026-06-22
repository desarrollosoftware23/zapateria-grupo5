{
    'name': 'zapatos_extension',
    'version': '1.0',
    'summary': 'Es una extension de  zapateria',
    'description': 'Agregar informacion adicional a zapateria.',
    'author': 'Alejo',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['zapatos'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/zapato_extension_views.xml',
        'views/proveedor_views.xml',

    ],
    'installable': True,
    'application': True,
}


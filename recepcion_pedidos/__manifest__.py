# -*- coding: utf-8 -*-
{
    # Nombre que aparece en la lista de aplicaciones de Odoo
    'name': 'Recepción de Pedidos',
    'version': '1.0.0',
    'summary': 'Gestión y control de la recepción de pedidos de clientes o proveedores',
    'description': """
Módulo para registrar y controlar la recepción de pedidos.
Permite llevar un seguimiento del estado de cada pedido, comparar las
cantidades pedidas contra las recibidas y calcular el total de forma automática.
    """,
    'author': 'Grupo - Universidad UTE',
    'category': 'Inventory',
    # Dependemos del módulo padre 'zapatos' porque cada línea del pedido
    # referencia un zapato del catálogo definido ahí (zapatos.zapato).
    # Al depender de 'zapatos' ya no es necesario declarar 'product' ni 'base'
    # por separado, porque 'zapatos' ya los trae como dependencia.
    'depends': ['zapatos'],
    # El orden de carga importa: primero la seguridad, luego los datos y al final las vistas
    'data': [
        'security/ir.model.access.csv',
        'data/secuencia_pedido.xml',
        'views/recepcion_pedido_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    # No es una aplicación independiente: es una extensión de la app "Zapatos"
    'application': False,
    'license': 'LGPL-3',
}
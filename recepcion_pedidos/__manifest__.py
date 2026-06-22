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
    # Dependemos de 'base' para las funciones generales y de 'product'
    # porque cada línea del pedido referencia un producto del catálogo
    'depends': ['base', 'product'],
    # El orden de carga importa: primero la seguridad, luego los datos y al final las vistas
    'data': [
        'security/ir.model.access.csv',
        'data/secuencia_pedido.xml',
        'views/recepcion_pedido_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
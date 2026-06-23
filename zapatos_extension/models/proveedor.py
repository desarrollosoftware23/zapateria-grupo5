from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Proveedor(models.Model):
    _name = 'zapatos.proveedor'
    _description = 'Proveedor'

    imagen = fields.Image(
        string='Foto'
    )

    proveedor_id = fields.Char(
        string='ID Proveedor',
        readonly=True,
        default='Nuevo'
    )

    razon_social = fields.Char(
        string='Nombre o Empresa',
        required=True
    )

    ruc = fields.Integer(
        string='RUC',
        required=True
    )

    tipo_proveedor = fields.Selection(
        [
            ('nacional', 'Nacional'),
            ('internacional', 'Internacional')
        ],
        string='Tipo de Proveedor',
        required=True,
        default='nacional'
    )

    estado = fields.Selection(
        [
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo')
        ],
        string='Estado',
        default='activo'
    )

    nombre_contacto = fields.Char(
        string='Nombre del Proveedor',
        required=True
    )

    telefono = fields.Integer(
        string='Teléfono',
        required=True
    )

    correo = fields.Char(
        string='Correo Electrónico',
        required=True
    )

    pais = fields.Char(
        string='País'
    )

    ciudad = fields.Char(
        string='Ciudad'
    )

    direccion = fields.Text(
        string='Dirección'
    )

    @api.model
    def create(self, vals):
        if vals.get('proveedor_id', 'Nuevo') == 'Nuevo':
            ultimo = self.search([], order='id desc', limit=1)
            numero = ultimo.id + 1 if ultimo else 1
            vals['proveedor_id'] = f'PROV-{numero:03d}'
        return super().create(vals)

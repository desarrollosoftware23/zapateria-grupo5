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

    ruc = fields.Char(
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

    telefono = fields.Char(
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

    @api.constrains('ruc')
    def _check_ruc(self):
        for record in self:
            if record.ruc:
                if not re.match(r'^\d{13}$', record.ruc):
                    raise ValidationError(
                        'El RUC debe contener exactamente 13 dígitos numéricos.'
                    )

    @api.constrains('correo')
    def _check_correo(self):
        for record in self:
            if record.correo:
                if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', record.correo):
                    raise ValidationError(
                        'El correo electrónico no tiene un formato válido.'
                    )

    @api.model
    def create(self, vals):
        if vals.get('proveedor_id', 'Nuevo') == 'Nuevo':
            ultimo = self.search([], order='id desc', limit=1)
            numero = ultimo.id + 1 if ultimo else 1
            vals['proveedor_id'] = f'PROV-{numero:03d}'
        return super().create(vals)
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VentaZapato(models.Model):
    _name = 'zapatos.ventas'
    _description = 'Venta de Zapatos'

    name = fields.Char(
        string='ID de venta',
        required=True,
        copy=False,
        readonly=True,
        default='Nueva venta'
    )

    producto_id = fields.Many2one(
        'zapatos.zapato',
        string='Producto o zapato vendido',
        required=True
    )

    cantidad_vendida = fields.Integer(
        string='Cantidad vendida',
        required=True
    )

    precio_unitario = fields.Float(
        string='Precio unitario',
        required=True
    )

    total_venta = fields.Float(
        string='Total de la venta',
        compute='_calcular_total_venta',
        store=True
    )

    fecha_venta = fields.Date(
        string='Fecha de venta',
        default=fields.Date.context_today
    )

    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ], string='Método de pago', required=True)

    estado_venta = fields.Selection([
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado de venta', default='completada', required=True)

    observacion = fields.Text(
        string='Observación'
    )

    stock_disponible = fields.Integer(
        string='Stock disponible',
        compute='_calcular_stock_disponible'
    )

    @api.depends('cantidad_vendida', 'precio_unitario')
    def _calcular_total_venta(self):
        for venta in self:
            venta.total_venta = venta.cantidad_vendida * venta.precio_unitario

    @api.depends('producto_id')
    def _calcular_stock_disponible(self):
        for venta in self:
            if venta.producto_id:
                venta.stock_disponible = venta.producto_id.stock
            else:
                venta.stock_disponible = 0

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.precio

    @api.constrains('cantidad_vendida')
    def _validar_cantidad_vendida(self):
        for venta in self:
            if venta.cantidad_vendida <= 0:
                raise ValidationError('La cantidad vendida debe ser mayor a 0.')

    @api.model
    def create(self, vals):
        venta = super(VentaZapato, self).create(vals)

        if venta.estado_venta == 'completada':
            venta._descontar_stock()

        return venta

    def write(self, vals):
        for venta in self:
            if venta.estado_venta == 'completada':
                if 'producto_id' in vals or 'cantidad_vendida' in vals:
                    raise ValidationError(
                        'No puedes cambiar el producto o la cantidad de una venta completada.'
                    )

        estados_anteriores = {}
        for venta in self:
            estados_anteriores[venta.id] = venta.estado_venta

        resultado = super(VentaZapato, self).write(vals)

        for venta in self:
            estado_anterior = estados_anteriores[venta.id]

            if estado_anterior == 'cancelada' and venta.estado_venta == 'completada':
                venta._descontar_stock()

            if estado_anterior == 'completada' and venta.estado_venta == 'cancelada':
                venta._devolver_stock()

        return resultado

    def _descontar_stock(self):
        for venta in self:
            if venta.cantidad_vendida > venta.producto_id.stock:
                raise ValidationError(
                    'No hay stock suficiente para realizar esta venta.'
                )

            nuevo_stock = venta.producto_id.stock - venta.cantidad_vendida
            venta.producto_id.stock = nuevo_stock

    def _devolver_stock(self):
        for venta in self:
            nuevo_stock = venta.producto_id.stock + venta.cantidad_vendida
            venta.producto_id.stock = nuevo_stock
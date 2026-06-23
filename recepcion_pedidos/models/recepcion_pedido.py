# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RecepcionPedido(models.Model):
    # Nombre técnico del modelo, con este identificador se referencia en todo el sistema
    _name = 'recepcion.pedido'
    _description = 'Recepción de Pedido'
    # Ordenamos los registros del más reciente al más antiguo
    _order = 'fecha_recepcion desc, id desc'

    # Folio o referencia del pedido, se genera automáticamente con una secuencia
    name = fields.Char(
        string='Folio',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo',
    )
    # Cliente o proveedor que origina el pedido
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente / Proveedor',
        required=True,
    )
    # Fecha en que se registró el pedido
    fecha_pedido = fields.Date(
        string='Fecha del pedido',
        default=fields.Date.context_today,
        required=True,
    )
    # Fecha en que físicamente se recibe la mercancía
    fecha_recepcion = fields.Date(
        string='Fecha de recepción',
    )
    # Empleado responsable de revisar la recepción
    responsable_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user,
    )
    # Estado del documento, controla el flujo de trabajo mediante botones
    state = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('recibido', 'Recibido'),
            ('verificado', 'Verificado'),
            ('completado', 'Completado'),
            ('cancelado', 'Cancelado'),
        ],
        string='Estado',
        default='borrador',
        tracking=True,
    )
    # Notas u observaciones libres sobre la recepción
    notas = fields.Text(string='Observaciones')
    # Relación uno a muchos con las líneas de detalle del pedido
    linea_ids = fields.One2many(
        'recepcion.pedido.linea',
        'pedido_id',
        string='Líneas del pedido',
    )
    # Total calculado automáticamente a partir de los subtotales de cada línea
    total = fields.Float(
        string='Total',
        compute='_calcular_total',
        store=True,
    )

    @api.depends('linea_ids.subtotal')
    def _calcular_total(self):
        # Recorremos cada pedido y sumamos los subtotales de todas sus líneas
        for pedido in self:
            pedido.total = sum(linea.subtotal for linea in pedido.linea_ids)

    @api.model
    def create(self, vals):
        # Si el folio sigue en 'Nuevo' pedimos a la secuencia el siguiente número
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('recepcion.pedido') or 'Nuevo'
        return super(RecepcionPedido, self).create(vals)

    def accion_recibir(self):
        # Marca el pedido como recibido y registra la fecha de recepción del día
        for pedido in self:
            pedido.write({
                'state': 'recibido',
                'fecha_recepcion': fields.Date.context_today(pedido),
            })

    def accion_verificar(self):
        # Antes de verificar validamos que el pedido tenga al menos una línea
        for pedido in self:
            if not pedido.linea_ids:
                raise ValidationError('No puede verificar un pedido sin líneas de detalle.')
            pedido.state = 'verificado'

    def accion_completar(self):
        # Cierra el pedido dándolo por completado
        self.write({'state': 'completado'})

    def accion_cancelar(self):
        # Permite anular el pedido en cualquier momento
        self.write({'state': 'cancelado'})

    def accion_borrador(self):
        # Devuelve el pedido a borrador para corregir datos
        self.write({'state': 'borrador'})


class RecepcionPedidoLinea(models.Model):
    _name = 'recepcion.pedido.linea'
    _description = 'Línea de Recepción de Pedido'

    # Enlace al pedido al que pertenece esta línea
    pedido_id = fields.Many2one(
        'recepcion.pedido',
        string='Pedido',
        required=True,
        ondelete='cascade',
    )
    # Zapato que se está recibiendo (modelo del módulo padre 'zapatos')
    zapato_id = fields.Many2one(
        'zapatos.zapato',
        string='Zapato',
        required=True,
    )
    # Cantidad que se solicitó originalmente
    cantidad_pedida = fields.Float(
        string='Cantidad pedida',
        default=1.0,
    )
    # Cantidad que realmente llegó
    cantidad_recibida = fields.Float(
        string='Cantidad recibida',
        default=0.0,
    )
    # Precio por unidad del producto
    precio_unitario = fields.Float(string='Precio unitario')
    # Subtotal de la línea, se calcula multiplicando cantidad recibida por precio
    subtotal = fields.Float(
        string='Subtotal',
        compute='_calcular_subtotal',
        store=True,
    )
    # Diferencia entre lo pedido y lo recibido, útil para detectar faltantes
    diferencia = fields.Float(
        string='Diferencia',
        compute='_calcular_diferencia',
        store=True,
    )

    @api.depends('cantidad_recibida', 'precio_unitario')
    def _calcular_subtotal(self):
        # El subtotal solo considera lo que efectivamente se recibió
        for linea in self:
            linea.subtotal = linea.cantidad_recibida * linea.precio_unitario

    @api.depends('cantidad_pedida', 'cantidad_recibida')
    def _calcular_diferencia(self):
        # Una diferencia positiva indica faltante respecto a lo solicitado
        for linea in self:
            linea.diferencia = linea.cantidad_pedida - linea.cantidad_recibida

    @api.onchange('zapato_id')
    def _onchange_zapato(self):
        # Al elegir un zapato traemos su precio del catálogo como valor sugerido
        if self.zapato_id:
            self.precio_unitario = self.zapato_id.precio

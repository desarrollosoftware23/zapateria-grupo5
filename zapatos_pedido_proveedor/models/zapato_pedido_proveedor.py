from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ZapatoPedidoProveedor(models.Model):
    _name = 'zapatos.pedido.proveedor'
    _description = 'Proveedor pedido'

    name = fields.Char(
        string='ID del pedido', required=True,
        copy=False,
        readonly=True,
        default='Nuevo')
    
    proveedor_id = fields.Many2one('zapatos.proveedor',
        string='Proveedor', required=True)

    zapato_id = fields.Many2one(
        'zapatos.zapato', string='Zapato solicitado',
        required=True)
    
    cantidad = fields.Integer(
        string='Cantidad solicitada',
        default=0,
        required=True)
    
    fecha = fields.Date(
        string='Fecha pedido',
        default=fields.Date.today,
        required=True)
    
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),], string='Estado', default='pendiente', required=True)

    observacion = fields.Text(string='Observación')
    tipo_observacion= fields.Selection([('info','Información'),
                                        ('damage','Daño de productos / Perdida de productos'),
                                        ('ninguno','Ninguno')],string='Especificación de observación',
                                        default='ninguno',required=True)

    def action_enviar(self):
        for rec in self:
            if rec.estado != 'pendiente':
                raise UserError('Solo se pueden enviar pedidos en estado Pendiente.')
            rec.estado = 'enviado'

    def action_recibir(self):
        for rec in self:
            if rec.estado != 'enviado':
                raise UserError('Solo se pueden recibir pedidos en estado Enviado.')
            rec.estado = 'recibido'

    def action_cancelar(self):
        for rec in self:
            if rec.estado == 'recibido':
                raise UserError('No se puede cancelar un pedido ya recibido.')
            rec.estado = 'cancelado'

    def action_restablecer(self):
        for rec in self:
            rec.estado = 'pendiente'
            rec.name = 'Nuevo'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('zapatos.pedido.proveedor') or 'Nuevo'
        return super().create(vals_list)

    @api.constrains('observacion')
    def validad_longitud_observacion(self):
        for rec in self:
            if rec.observacion:
                if len(rec.observacion) > 20:
                    raise ValidationError('No puede exceder los 20 caracteres')
    
    @api.constrains('observacion','tipo_observacion')
    def validar_observacion_ninguno(self):
        for rec in self:
            if rec.tipo_observacion == 'ninguno' and rec.observacion:
                raise ValidationError('Seleccione algún tipo de observación diferente de ninguno')
            elif rec.tipo_observacion != 'ninguno' and not rec.observacion:
                raise ValidationError('Debe ingresar un texto instructivo')
            
    @api.constrains('fecha')
    def validar_fecha(self):
        for rec in self:
            if rec.fecha and rec.fecha <= fields.Date.today():
                raise ValidationError('La fecha ingresada deber ser proxima')
            
    @api.constrains('cantidad')
    def validar_cantidad(self):
        for rec in self:
            if rec.cantidad < 0:
                raise ValidationError('El pedido debe ser mayor a cero')
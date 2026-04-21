from odoo import models, fields


class HelpdeskContrato(models.Model):
    _name = 'helpdesk.contrato'
    _description = 'Contrato de servicio'

    name = fields.Char(string='Referencia', required=True)

    cliente_id = fields.Many2one(
        'helpdesk.cliente',
        string='Cliente',
        required=True,
        ondelete='restrict')

    tipo_servicio = fields.Selection([
        ('movil', 'Móvil'),
        ('fibra', 'Fibra'),
        ('tv', 'TV'),
        ('paquete', 'Paquete'),
    ], string='Tipo de servicio', required=True)

    plan = fields.Selection([
        ('basico', 'Básico'),
        ('estandar', 'Estándar'),
        ('premium', 'Premium'),
    ], string='Plan', default='basico')

    estado = fields.Selection([
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='activo')

    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id)
    precio_mensual = fields.Monetary(
        string='Precio mensual',
        currency_field='currency_id')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'La referencia del contrato debe ser única.'),
    ]
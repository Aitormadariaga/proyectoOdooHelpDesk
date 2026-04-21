from odoo import models, fields

class HelpdeskContrato(models.Model):
    _name = 'helpdesk.contrato'
    _description = 'Contrato de servicio'

    # name es un campo calculado para mostrar algo legible en desplegables
    name = fields.Char(
        string='Referencia', required=True)

    # *** AQUÍ ESTÁ LA RELACIÓN ***
    # Many2one = "muchos contratos pertenecen a UN cliente"
    # Es el equivalente a tu FK id_cliente en el modelo ER
    cliente_id = fields.Many2one(
        'helpdesk.cliente',          # modelo al que apunta
        string='Cliente',
        required=True)

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
    precio_mensual = fields.Float(
        string='Precio mensual', digits=(8, 2))
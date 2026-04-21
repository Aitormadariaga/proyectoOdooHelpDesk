from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket de soporte'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_creacion desc'

    name = fields.Char(string='Asunto', required=True, tracking=True)
    codigo = fields.Char(string='Código', readonly=True, copy=False, default='Nuevo')
    descripcion = fields.Text(string='Descripción')

    cliente_id = fields.Many2one(
        'helpdesk.cliente', string='Cliente', required=True, tracking=True)
    tecnico_id = fields.Many2one(
        'helpdesk.tecnico', string='Técnico asignado', tracking=True)
    categoria_id = fields.Many2one(
        'helpdesk.categoria', string='Categoría', required=True)
    contrato_id = fields.Many2one('helpdesk.contrato', string='Contrato')

    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ], string='Prioridad', default='media', tracking=True)
    estado = fields.Selection([
        ('abierto', 'Abierto'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='abierto', tracking=True)

    fecha_creacion = fields.Datetime(
        string='Fecha creación', default=fields.Datetime.now, readonly=True)
    fecha_cierre = fields.Datetime(string='Fecha cierre', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'helpdesk.ticket') or 'Nuevo'
        return super().create(vals_list)

    def write(self, vals):
        # Al pasar a resuelto o cerrado, sellamos la fecha de cierre
        if vals.get('estado') in ('resuelto', 'cerrado'):
            for ticket in self:
                if not ticket.fecha_cierre:
                    vals.setdefault('fecha_cierre', fields.Datetime.now())
        # Si se reabre, limpiamos la fecha de cierre
        if vals.get('estado') in ('abierto', 'en_proceso'):
            vals['fecha_cierre'] = False
        return super().write(vals)
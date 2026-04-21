from odoo import models, fields

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket de soporte'
    _order = 'fecha_creacion desc'

    name = fields.Char(string='Asunto', required=True)
    codigo = fields.Char(string='Código', readonly=True, copy=False, default='Nuevo')
    descripcion = fields.Text(string='Descripción')

    cliente_id = fields.Many2one('helpdesk.cliente', string='Cliente', required=True)
    tecnico_id = fields.Many2one('helpdesk.tecnico', string='Técnico asignado')
    categoria_id = fields.Many2one('helpdesk.categoria', string='Categoría', required=True)
    contrato_id = fields.Many2one('helpdesk.contrato', string='Contrato')

    prioridad = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ], string='Prioridad', default='media')
    estado = fields.Selection([
        ('abierto', 'Abierto'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='abierto')

    fecha_creacion = fields.Datetime(string='Fecha creación', default=fields.Datetime.now)
    fecha_cierre = fields.Datetime(string='Fecha cierre')

    def create(self, vals):
        if vals.get('codigo', 'Nuevo') == 'Nuevo':
            vals['codigo'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or 'Nuevo'
        return super().create(vals)
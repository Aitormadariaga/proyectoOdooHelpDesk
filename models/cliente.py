from odoo import models, fields


class HelpdeskCliente(models.Model):
    _name = 'helpdesk.cliente'
    _description = 'Cliente'

    name = fields.Char(string='Nombre completo', required=True)
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    # 'active' es un campo reservado de Odoo: activa archivado,
    # filtro automático en búsquedas y botón de archivar en la UI.
    active = fields.Boolean(string='Activo', default=True)
    user_id = fields.Many2one(
        'res.users',
        string='Usuario vinculado',
        domain=[('share', '=', False)])

    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Ya existe un cliente con ese email.'),
    ]
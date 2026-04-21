from odoo import models, fields


class HelpdeskTecnico(models.Model):
    _name = 'helpdesk.tecnico'
    _description = 'Técnico de soporte'

    name = fields.Char(string='Nombre completo', required=True)
    email = fields.Char(string='Email corporativo')
    nivel_soporte = fields.Selection([
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
    ], string='Nivel de soporte', default='1')
    especialidad = fields.Char(string='Especialidad')
    # 'active' es un campo reservado de Odoo: activa archivado,
    # filtro automático en búsquedas y botón de archivar en la UI.
    active = fields.Boolean(string='Activo', default=True)
    user_id = fields.Many2one(
        'res.users',
        string='Usuario vinculado',
        domain=[('share', '=', False)])
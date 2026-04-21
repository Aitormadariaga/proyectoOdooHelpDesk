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
        string='Fecha creación', default=fields.Datetime.now,
        readonly=True, copy=False)
    fecha_cierre = fields.Datetime(
        string='Fecha cierre', readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'helpdesk.ticket') or 'Nuevo'
        return super().create(vals_list)

    def write(self, vals):
        nuevo_estado = vals.get('estado')

        # Si se reabre, limpiar fecha_cierre para todos: vale un solo write
        if nuevo_estado in ('abierto', 'en_proceso'):
            vals['fecha_cierre'] = False
            return super().write(vals)

        # Si se cierra/resuelve y el usuario NO ha pasado fecha_cierre explícita,
        # sellamos por registro para respetar los que ya la tenían.
        if nuevo_estado in ('resuelto', 'cerrado') and 'fecha_cierre' not in vals:
            ahora = fields.Datetime.now()
            # Separar los que aún no tienen fecha_cierre
            sin_fecha = self.filtered(lambda t: not t.fecha_cierre)
            con_fecha = self - sin_fecha

            res = True
            if con_fecha:
                res = super(HelpdeskTicket, con_fecha).write(vals) and res
            if sin_fecha:
                vals_sellado = dict(vals, fecha_cierre=ahora)
                res = super(HelpdeskTicket, sin_fecha).write(vals_sellado) and res
            return res

        return super().write(vals)
from odoo import models, fields

class HelpdeskCategoria(models.Model):
    # _name = nombre técnico. Odoo crea la tabla 'helpdesk_categoria' en PostgreSQL
    _name = 'helpdesk.categoria'
    # _description = nombre legible para los usuarios
    _description = 'Categoría de incidencia'

    # fields.Char = campo de texto corto (VARCHAR en tu ER)
    name = fields.Char(
        string='Nombre',          # Etiqueta que se ve en la interfaz
        required=True,             # Obligatorio (no puede estar vacío)
    )
    # fields.Text = campo de texto largo (TEXT en tu ER)
    descripcion = fields.Text(
        string='Descripción',
    )

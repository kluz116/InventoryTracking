from odoo import models, fields

class res_user(models.Model):
    _inherit = 'res.partner'
    
    user_role = fields.Selection([('infrastructure_admin', 'Infrastructure Admin'),('infrastructure_manager', 'Infrastructure Manager')], string="User Role")
    supervisor = fields.Many2one('res.partner',string ='Supervisor')
    loaction_id_invetory = fields.Many2one('inventory_track.asset_location',string ='Location')


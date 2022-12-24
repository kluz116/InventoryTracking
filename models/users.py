from odoo import models, fields

class res_user(models.Model):
    _inherit = 'res.partner'
    
    user_roles = fields.Selection([('infrastructure_admin', 'Infrastructure Admin'),('infrastructure_manager', 'Infrastructure Manager'),('asset_custodian', 'Asset Custodian'),('cyber_admin', 'Cyber'),('ftb_admin', 'Tag Admin')], string="User Role")
    supervisor = fields.Many2one('res.partner',string ='Supervisor')
    loaction_id_invetory = fields.Many2one('inventory_track.asset_location',string ='Location')


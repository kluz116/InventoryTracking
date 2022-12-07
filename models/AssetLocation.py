from odoo import models, fields

class AssetLocation(models.Model):
    _name = "inventory_track.asset_location"
    _description = "This is an asset location model"
    _rec_name ="location_name"
    
    status = fields.Selection([('active', 'Active'),('innactive', 'Innactive')],default="active", string="Status")
    location_name = fields.Char(string="Location Name", required=True)
    user_id = fields.One2many('res.partner','loaction_id_invetory', string="Name")
  
    
   
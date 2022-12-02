from odoo import models,api,fields,exceptions

class Inventory(models.Model):
    _name = "inventory_track.asset_location"
    _description = "This is an asset location"
    _rec_name ="make"
    
    asset_location = fields.Char(string="Asset Location",required=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
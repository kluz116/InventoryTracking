from odoo import models,api,fields,exceptions

class Make(models.Model):
    _name = "inventory_track.make"
    _description = "This is a make model"
    _rec_name ="make_name"

    make_name = fields.Char(string="Make")

class Asset_Models(models.Model):
    _name = "inventory_track.asset_models"
    _rec_name ='asset_model'
    _description = "This is a description of asset model"

    asset_model = fields.Char(string="Asset Model",required=True)
    asset_make = fields.Many2one('inventory_track.make',ondelete='cascade',string='Asset Make')
 


 

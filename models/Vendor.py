from odoo import models,api,fields,exceptions

class Vendor(models.Model):
    _name = "inventory_track.vendor"
    _description = "This is an vendor model"
    _rec_name ="vendor_name"

    vendor_name = fields.Char(string="Name")
    vendor_email = fields.Char(string="Vendor Email")
    vendor_phone = fields.Char(string="Phone")
 

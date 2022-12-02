from odoo import models,api,fields,exceptions

class Inventory(models.Model):
    _name = "inventory_track.inventory"
    _description = "This is an Inventory model"
    _rec_name ="make"

    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True, default="laptop")
    vendor_id = fields.Many2one('inventory_track.vendor',string='Vendor',required=True)
    make = fields.Many2one('inventory_track.make',ondelete='cascade',string='Asset Make')
    model = fields.Many2one('inventory_track.asset_models',string="Asset Model",domain = " [('asset_make','=',make)] " )
    asset_status = fields.Selection([('available','Available'),('verified','Verified'),('rejected','Rejected'),('dispatched','Dispatched'),('recieved','Recieved')],string="Asset Status", required=True, default="available")
    serial = fields.Char(string="Serial",required=True)
    tag = fields.Char(string="Asset TAG", required=True)
    ram = fields.Selection([('one','1 GB'),('two','2 GB'),('three','3 GB'),('four','4 GB'),('six','6 GB'),('eight','8 GB'),('twelve','12 GB'),('sixteen','16 GB'),('thirty_two','32 GB')],string="RAM Size",  default="one")
    hdd = fields.Char(string="HDD OR SDD Size")
    os =  fields.Selection([('windows_10','Windows 10'),('windows_11','Windows 11'),('windows_12','Windows 12')],string="OS", required=True, default="windows_10")
    comment = fields.Char(string="comment",required=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
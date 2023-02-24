from odoo import api, fields, models
from datetime import datetime

class DisposeLog(models.Model):
    _name = "inventory_track.asset_dispose_log"
    _description = "Dispose Asset "
    _rec_name = 'asset_id'
    
    
    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True)
    asset_id = fields.Many2one('inventory_track.inventory',string='Asset',required=True)
    serial =  fields.Many2many('inventory_track.asset_serial',relation='disposal_logs',string='Asset Serial',required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="active")
    dispose_comment = fields.Text(string="Disposal Comment")
    dispose_date =  fields.Datetime(string='Disposal Date', default=lambda self: fields.datetime.now())
    dispose__by = fields.Many2one('res.users','Disposed By:',default=lambda self: self.env.user)
   
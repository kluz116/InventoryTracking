from odoo import api, fields, models
from datetime import datetime

class ActivatedLog(models.Model):
    _name = "inventory_track.asset_repair_log"
    _description = "Activate Asset "
    _rec_name = 'asset_id'
    
    
    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True)
    asset_id = fields.Many2one('inventory_track.inventory',string='Asset',required=True)
    serial =  fields.Many2many('inventory_track.asset_serial',relation='repair_logs',string='Asset Serial',required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="active")
    repaire_comment = fields.Text(string="Comment")
    repaire_date =  fields.Datetime(string='Repaire Date', default=lambda self: fields.datetime.now())
    repaired_by = fields.Many2one('res.users','Initiated By:',default=lambda self: self.env.user)
   
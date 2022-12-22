from odoo import api, fields, models
from datetime import datetime

class ActivatedLog(models.Model):
    _name = "inventory_track.asset_activate_log"
    _description = "Activate Asset "
    _rec_name = 'asset_status'

    asset_id = fields.Many2one('inventory_track.inventory',string='Asset',required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="active")
    activated_comment = fields.Text(string="Comment")
    activated_date =  fields.Datetime(string='Activated Date', default=lambda self: fields.datetime.now())
    activated_by = fields.Many2one('res.users','Activated By:',default=lambda self: self.env.user)
   
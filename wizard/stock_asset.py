from odoo import api, fields, models
from datetime import datetime

class StockAsset(models.TransientModel):
    _name = "inventory_track.stock_asset"
    _description = "Stock Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="new")
    stock_comment = fields.Text(string="Comment")
    stock_date =  fields.Datetime(string='Stock Date', default=lambda self: fields.datetime.now())
   
    
    def stock__asset(self):
        self.write({'asset_status': 'stocked'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.stock_comment = self.stock_comment
            req.stock_date = self.stock_date
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_verify').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

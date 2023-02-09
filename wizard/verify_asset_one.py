from odoo import api, fields, models
from datetime import datetime

class VerifyAssetCyber(models.TransientModel):
    _name = "inventory_track.verify_asset_cyber"
    _description = "Verify Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="new")
    cyber_comment = fields.Text(string="Comment")
    cyber_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
   
    
    def verify_cyber_asset(self):
        self.write({'asset_status': 'verified_one'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.cyber_comment = self.cyber_comment
            req.cyber_date = self.cyber_date
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

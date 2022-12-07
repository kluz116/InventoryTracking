from odoo import api, fields, models
from datetime import datetime

class VerifyAsset(models.TransientModel):
    _name = "inventory_track.verify_asset"
    _description = "Verify Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('available','Available'),('verified','Verified'),('rejected','Rejected'),('dispatched','Dispatched'),('recieved','Recieved')],string="Asset Status", required=True, default="available")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
   
    
    def verify__asset(self):
        self.write({'asset_status': 'verified'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.from_manager_comment = self.from_manager_comment
            req.from_manager_date = self.from_manager_date
            

           # template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

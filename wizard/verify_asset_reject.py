from odoo import api, fields, models
from datetime import datetime

class VerifyAssetReject(models.TransientModel):
    _name = "inventory_track.reject_verify_asset"
    _description = "Verify Asset Reject"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('available','Available'),('verified','Verified'),('rejected','Rejected'),('dispatched','Dispatched'),('recieved','Recieved'),('reject_verify','Reject Verification')],string="Asset Status", required=True, default="reject_verify")
    verify_reject_comment = fields.Text(string="Comment")
    verify_reject_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
    verify_reject_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
    
    def verify_reject_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.verify_reject_comment = self.verify_reject_comment
            req.verify_reject_date = self.verify_reject_date
            req.verify_reject_by = self.verify_reject_by
            req.tag.status ='approved'
            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_verify_cyber').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

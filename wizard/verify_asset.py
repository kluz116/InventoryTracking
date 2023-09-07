from odoo import api, fields, models
from datetime import datetime

class VerifyAsset(models.TransientModel):
    _name = "inventory_track.verify_asset"
    _description = "Verify Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('available','Available'),('verified','Verified'),('rejected','Rejected'),('dispatched','Dispatched'),('recieved','Recieved')],string="Asset Status", required=True, default="verified")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
    manager_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
    
    def verify__asset(self):
        self.write({'asset_status': 'verified'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.from_manager_comment = self.from_manager_comment
            req.from_manager_date = self.from_manager_date
            req.manager_by = self.manager_by
            

            template_id = self.env.ref('InventoryTracking.email_template_asset_stocked_infra').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

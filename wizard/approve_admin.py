from odoo import api, fields, models
from datetime import datetime

class ApproveAssetTags(models.TransientModel):
    _name = "inventory_track.asset_tag_approval"
    _description = "Approve Asset "
    _rec_name = 'status'

    
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('approved','Approved'),('rejected','Rejected')],string="Status", required=True, default="innactive")
    approval_comment = fields.Text(string="Approval Comment",required=True)
    approval_date =  fields.Datetime(string='Approval Date', default=lambda self: fields.datetime.now())
    approval_by = fields.Many2one('res.users','Approval By:',default=lambda self: self.env.user)
    
    def approve_tag_asset(self):
        self.write({'status': 'approved'})
        asset = self.env['inventory_track.asset_tags'].browse(self._context.get('active_ids'))
        for req in asset:
            req.status = self.status
            req.approval_comment = self.approval_comment
            req.approval_date = self.approval_date
            req.approval_by = self.approval_by
            
    
            template_id = self.env.ref('InventoryTracking.email_template_approve_asset_tag').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

from odoo import  fields, models


class ApproveAssetTags(models.TransientModel):
    _name = "inventory_track.asset_tag_rejection"
    _description = "Approve Asset "
    _rec_name = 'status'

    
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('approved','Approved'),('rejected','Rejected')],string="Status", required=True, default="rejected")
    reject_comment = fields.Text(string="Rejection Comment",required=True)
    reject_date =  fields.Datetime(string='Rejection Date', default=lambda self: fields.datetime.now())
    rejected_by = fields.Many2one('res.users','Rejected By:',default=lambda self: self.env.user)
    
    def reject_tag_asset(self):
        self.write({'status': 'rejected'})
        asset = self.env['inventory_track.asset_tags'].browse(self._context.get('active_ids'))
        for req in asset:
            req.status = self.status
            req.reject_comment = self.reject_comment
            req.reject_date = self.reject_date
            req.rejected_by = self.rejected_by
            
            

            template_id = self.env.ref('InventoryTracking.email_template_reject_asset_tag').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

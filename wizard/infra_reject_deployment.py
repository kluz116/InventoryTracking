from odoo import api, fields, models
from datetime import datetime

class InfraReject(models.TransientModel):
    _name = "inventory_track.infra_reject_deployment"
    _description = "Deploymen Approval"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('diagnosis_approved','Diagnosis Approved'),('diagnosis_rejected','Diagnosis Rejected'),('infra_approve','Deployment Approved'),('infra_reject','Deployment Rejected')],string="Asset Status", required=True, default="infra_reject")
    infra_reject_comment = fields.Text(string="Comment", required=True)
    infra_reject_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    infra_reject_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
    
    def infra_rejected_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.infra_reject_comment = self.infra_reject_comment
            req.infra_reject_date = self.infra_reject_date
            req.infra_reject_by = self.infra_reject_by
            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_diagnosis_approved').id
            ##template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

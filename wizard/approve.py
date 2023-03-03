from odoo import api, fields, models
from datetime import datetime

class DiagnosisApproved(models.TransientModel):
    _name = "inventory_track.diagnosis_approved"
    _description = "Diagnosis approved Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('diagnosis_approved','Diagnosis Approved'),('diagnosis_rejected','Diagnosis Rejected')],string="Asset Status", required=True, default="diagnosis_approved")
    diagnosis_approved_comment = fields.Text(string="Comment", required=True)
    diagnosis_approved_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    diagnosis_approved_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
    
    def diagnosis_approved_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.diagnosis_approved_comment = self.diagnosis_approved_comment
            req.diagnosis_approved_date = self.diagnosis_approved_date
            req.diagnosis_approved_by = self.diagnosis_approved_by
            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_verify').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

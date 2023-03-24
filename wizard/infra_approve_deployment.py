from odoo import api, fields, models
from datetime import datetime

class InfraApprove(models.TransientModel):
    _name = "inventory_track.infra_approve_deployment"
    _description = "Deployment Approval"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('diagnosis_approved','Diagnosis Approved'),('diagnosis_rejected','Diagnosis Rejected'),('infra_approve','Deployment Approved'),('infra_reject','Deployment Rejected')],string="Asset Status", required=True, default="infra_approve")
    infra_comp_name = fields.Char(string="Computer Name", required=True)
    Operating_system_Build = fields.Char(string=" Operating system Build", required=True)
    Microsoft_office = fields.Selection([('2016','2016'),('2019','2019')],string="Microsoft Office", required=True)
    browser = fields.Selection([('no','No'),('yes','Yes')],string="Browsers Firefox and Chrome installed", required=True,default='no')
    Antivirus = fields.Selection([('no','No'),('yes','Yes')],string="Antivirus: Kaspersky installed and activated", required=True,default='no')
    os_updates = fields.Selection([('no','No'),('yes','Yes')],string="OS updates installed and up to date", required=True,default='no')
    user_file = fields.Selection([('no','No'),('yes','Yes')],string="User files transferred/backed up", required=True,default='no')
    guest_account = fields.Selection([('no','No'),('yes','Yes')],string="Guest Accounts disabled", required=True,default='no')
    ou = fields.Selection([('no','No'),('yes','Yes')],string="Computer added to correct OU", required=True,default='no')
    user_department = fields.Char(string="Computer User Department", required=True)
    other_information = fields.Char(string="Other information", required=True)
    

    infra_approve_comment = fields.Text(string="Comment", required=True)
    infra_approve_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    infra_approve_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
    
    def infra_approved_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.infra_approve_comment = self.infra_approve_comment
            req.infra_approve_date = self.infra_approve_date
            req.infra_approve_by = self.infra_approve_by
            req.infra_comp_name = self.infra_comp_name
            req.Operating_system_Build = self.Operating_system_Build
            req.Microsoft_office = self.Microsoft_office
            req.browser = self.browser
            req.Antivirus = self.Antivirus
            req.os_updates = self.os_updates
            req.user_file = self.user_file
            req.guest_account = self.guest_account
            req.ou = self.ou
            req.user_department = self.user_department
            req.other_information = self.other_information


            
            vals = { 'asset_id': req.id, 
                 'infra_comp_name': self.infra_comp_name,
                 'Operating_system_Build': self.Operating_system_Build,
                 'Microsoft_office': self.Microsoft_office,
                 'browser': self.browser,
                 'Antivirus': self.Antivirus,
                 'os_updates': self.os_updates,
                 'user_file': self.user_file,
                 'guest_account': self.guest_account,
                 'ou': self.ou,
                 'user_department': self.user_department,
                 'other_information': self.other_information,
                 'infra_approve_by': self.infra_approve_by.id
                 }

            self.env['inventory_track.asset_checklist_log'].create(vals)

            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_diagnosis_approved').id
            ##template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

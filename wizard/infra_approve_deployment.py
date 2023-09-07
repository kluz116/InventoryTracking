from odoo import api, fields, models
from datetime import datetime

class InfraApprove(models.TransientModel):
    _name = "inventory_track.infra_approve_deployment"
    _description = "Deployment Approval"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('diagnosis_approved','Diagnosis Approved'),('diagnosis_rejected','Diagnosis Rejected'),('infra_approve','Deployment Approved'),('infra_reject','Deployment Rejected')],string="Asset Status", required=True, default="infra_approve")
    infra_approve_comment = fields.Text(string="Comment", required=True)
    infra_approve_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    infra_approve_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)

    def comp_asset_tag_id(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.infra_comp_name


    infra_comp_name = fields.Char(string="Computer Name",default=comp_asset_tag_id)

    def Operating_system_Builds(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.Operating_system_Build

    Operating_system_Build = fields.Char(string=" Operating system Build",default=Operating_system_Builds)

    def Microsoft_offices(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.Microsoft_office
    Microsoft_office = fields.Selection(default=Microsoft_offices,selection=[('2016','2016'),('2019','2019')])

    def browsers(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.browser
        
    browser = fields.Selection(default=browsers,selection=[('no','No'),('yes','Yes')],string='Browsers Firefox and Chrome installed')

    def Antiviruss(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.Antivirus
        
    Antivirus = fields.Selection(default=Antiviruss,selection=[('no','No'),('yes','Yes')],string="Antivirus: Kaspersky installed and activated")

    def os_updatess(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.os_updates
        
    os_updates = fields.Selection(default=os_updatess,selection=[('no','No'),('yes','Yes')],string="OS updates installed and up to date")

    
    def user_files(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.user_file
        
    user_file = fields.Selection(default=user_files,selection=[('no','No'),('yes','Yes')],string="User files transferred/backed up",)

    def guest_accounts(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.guest_account
        
    guest_account = fields.Selection(default=guest_accounts,selection=[('no','No'),('yes','Yes')],string="Guest Accounts disabled")
    
    
    def ous(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.ou
        
    ou = fields.Selection(default=ous,selection=[('no','No'),('yes','Yes')],string="Computer added to correct OU")

    
    def user_departments(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.user_department
        
    user_department = fields.Char(default=user_departments,string="Computer User Department")
    
    def other_informations(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.other_information

    other_information = fields.Char(default=other_informations,string="Other information")


    def infra_approved_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.infra_approve_comment = self.infra_approve_comment
            req.infra_approve_date = self.infra_approve_date
            req.infra_approve_by = self.infra_approve_by
     
            template_id = self.env.ref('InventoryTracking.email_template_cyber_approval_deployment').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

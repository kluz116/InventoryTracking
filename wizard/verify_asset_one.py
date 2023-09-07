from odoo import api, fields, models
from datetime import datetime

class VerifyAssetCyber(models.TransientModel):
    _name = "inventory_track.verify_asset_cyber"
    _description = "Verify Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="verified_one")
    cyber_comment = fields.Text(string="Comment")
    cyber_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
   
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
         

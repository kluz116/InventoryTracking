from odoo import api, fields, models
from datetime import datetime

class ApproveAsset(models.TransientModel):
    _name = "inventory_track.asset_approval"
    _description = "Approve Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation')],string="Asset Status", required=True, default="approved")
    approval_comment = fields.Text(string="Approval Comment",required=True)
    approval_date =  fields.Datetime(string='Approval Date', default=lambda self: fields.datetime.now())
    approval_by = fields.Many2one('res.users','Approval By:',default=lambda self: self.env.user)
    
    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',ondelete='cascade',string='Asset Serial')
    #serial_set = fields.One2many(related='tag.asset_serial' ,string='Asset Serial')
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    def comp_asset_location(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.location_id.location_name 

    location_name = fields.Char(string="Asset Location",default=comp_asset_location,required=True)
    
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

    

    
    def approve__asset(self):
        #self.write({'asset_status': 'approved'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.approval_comment = self.approval_comment
            req.approval_date = self.approval_date
            req.approval_by = self.approval_by
            
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment_user').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

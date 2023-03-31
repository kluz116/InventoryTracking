from odoo import models, fields, api,exceptions
from datetime import datetime

class DispatchAsset(models.TransientModel):
    _name = "inventory_track.dispatch_asset"
    _description = "dispatched asset"
    _rec_name ="asset_status"
  
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="diployment")
    courier = fields.Many2one('inventory_track.courier',ondelete='cascade',string='Courier ')
    location_id = fields.Many2one('inventory_track.asset_location',string ='Asset Location', required=True)
    dispatched_to = fields.Many2one('res.partner','Custodian',domain="[('loaction_id_invetory', '=', location_id)]")
    dispach_comment = fields.Text(string="Comment")
    dispach_date =  fields.Datetime(string='Deployment Date', default=lambda self: fields.datetime.now())
    dispatched_by = fields.Many2one('res.users','Deployed By:',default=lambda self: self.env.user)

    infra_comp_name = fields.Char(string="Computer Name", required=True)
    Operating_system_Build = fields.Char(string=" Operating system Build", required=True)
    Microsoft_office = fields.Selection([('2016','2016'),('2019','2019')],string="Microsoft Office", required=True,default='2016')
    browser = fields.Selection([('no','No'),('yes','Yes')],string="Browsers Firefox and Chrome installed", required=True,default='no')
    Antivirus = fields.Selection([('no','No'),('yes','Yes')],string="Antivirus: Kaspersky installed and activated", required=True,default='no')
    os_updates = fields.Selection([('no','No'),('yes','Yes')],string="OS updates installed and up to date", required=True,default='no')
    user_file = fields.Selection([('no','No'),('yes','Yes')],string="User files transferred/backed up", required=True,default='no')
    guest_account = fields.Selection([('no','No'),('yes','Yes')],string="Guest Accounts disabled", required=True,default='no')
    ou = fields.Selection([('no','No'),('yes','Yes')],string="Computer added to correct OU", required=True,default='no')
    user_department = fields.Char(string="Computer User Department", required=True)
    other_information = fields.Char(string="Other information", required=True)

    #@api.one
    @api.constrains('browser','Antivirus','os_updates','user_file','guest_account','ou','dispatched_by')
    def _checkList_Validate(self):

        for record in self:
            if record.browser != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, Browsers Firefox and Chrome must be installed. Value can not be {record.browser} for this field")
            elif record.Antivirus != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, Antivirus: Kaspersky must be installed and activated.Value can not be {record.Antivirus} for this field")
            elif record.os_updates != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, OS updates must be installed and up to date.Value can not be {record.os_updates} for this field")
            elif record.user_file != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, User files must be transferred/backed up.Value can not be {record.user_file} for this field")
            elif record.guest_account != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, Guest Accounts must be disabled.Value can not be {record.guest_account} for this field")
            elif record.ou != 'yes':
                raise exceptions.ValidationError(f"Hello {record.dispatched_by.name}, Computer must be added to correct OU.Value can not be {record.ou} for this field")
        

    def dispatch__asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        
        for req in asset:
            req.asset_status = self.asset_status
            req.location_id = self.location_id.id
            req.dispatched_to = self.dispatched_to.id
            req.dispach_comment = self.dispach_comment
            req.dispach_date = self.dispach_date
            req.dispatched_by = self.dispatched_by.id
            req.courier = self.courier.id
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
                 'infra_approve_by': self.dispatched_by.id
                 }

            self.env['inventory_track.asset_checklist_log'].create(vals)
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_notify_approver').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

   

        

       
 

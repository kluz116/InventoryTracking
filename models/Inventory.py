from odoo import models,api,fields,exceptions
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

class Inventory(models.Model):
    _name = "inventory_track.inventory"
    _inherit="mail.thread"
    _description = "Inventory Tracking"
    _rec_name ="tag"

    #asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True, default="laptop")
    #vendor_id = fields.Many2one('inventory_track.vendor',string='Vendor',required=True)
    make = fields.Many2one('inventory_track.make',ondelete='cascade',string='Asset Make',track_visibility='always')
    model = fields.Many2one('inventory_track.asset_models',string="Asset Model",domain = " [('asset_make','=',make)] ",track_visibility='always' )
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Deployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Approved'),('pending_diagnosis_approval','Diagnosis Approval'),('diagnosis_approved','Diagnosis Approved'),('diagnosis_rejected','Diagnosis Rejected'),('repair_mode','Repair Mode'),('infra_approve','Deployment Approved'),('infra_reject','Deployment Rejected'),('reject_verify','Reject Verification')],string="Asset Status",track_visibility='always', required=True, default="new")
    tag = fields.Many2one('inventory_track.asset_tags',string="Asset Tag",domain = " [('status','=','approved')] ",track_visibility='always' )
    serial =   fields.Many2many(related='tag.asset_serial',track_visibility='always')
    batch_id = fields.Char(related='tag.batch_id', string='Batch')
    #serial = fields.One2many(related='tag.asset_serial' ,string='Asset Serial',domain = " [('status','in',['active'])] ")
    asset_type = fields.Selection(related='tag.asset_type',selection=[('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')])
    ram = fields.Selection([('one','1 GB'),('two','2 GB'),('three','3 GB'),('four','4 GB'),('six','6 GB'),('eight','8 GB'),('twelve','12 GB'),('sixteen','16 GB'),('thirty_two','32 GB')],string="RAM Size",  default="one")
    hdd = fields.Char(string="HDD OR SDD Size", required=True)
    os =  fields.Selection([('windows_10','Windows 10'),('windows_11','Windows 11'),('windows_12','Windows 12')],string="OS", required=True, default="windows_10")
    comp_names=fields.Char(string="Computer Name")
    Processor=fields.Char(string="Processor",required=True)
    bios=fields.Char(string="BIOS Version/Date",required=True)
    os_build=fields.Char(string="OS & Build")
    mac_address=fields.Char(string="MAC ADDRESS")
    mac_address_wifi=fields.Char(string="MAC ADDRESS WIFI")
    comment = fields.Text(string="comment",required=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Verified Date')
    location_id = fields.Many2one('inventory_track.asset_location',string ='Asset Location')
    dispatched_to = fields.Many2one('res.partner','User')
    dispach_comment = fields.Text(string="Comment")
    dispach_date =  fields.Datetime(string='Deployed Date')
    dispatched_by = fields.Many2one('res.users','Dispatched By:',track_visibility='always')
    stock_comment = fields.Text(string="Comment")
    stock_date =  fields.Datetime(string='Stock Date',track_visibility='always')
    cyber_comment = fields.Text(string="Comment")
    cyber_date =  fields.Datetime(string='Cyber Verified Date',track_visibility='always')
    activated_comment = fields.Text(string="Activation Comment")
    activated_date =  fields.Datetime(string='Activation Date',track_visibility='always')
    activated_by = fields.Many2one('res.users','Activated By:',track_visibility='always')
    repaire_comment = fields.Text(string="Comment")
    repaire_date =  fields.Datetime(string='Repair Date',track_visibility='always')
    repaired_by = fields.Many2one('res.users','Initiated By:',track_visibility='always')
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date',track_visibility='always')
    disposed_by = fields.Many2one('res.users','Disposed By:',track_visibility='always')
    reject_comment = fields.Text(string="Rejection Comment")
    reject_date =  fields.Datetime(string='Rejection Date',track_visibility='always')
    rejected_by = fields.Many2one('res.users','Rejected By:',track_visibility='always')
    approval_comment = fields.Text(string="Approval Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    approval_by = fields.Many2one('res.users','Approval By:',track_visibility='always')
    
   
    #effective_date =  fields.Date(string='Effective Date',default=lambda self: fields.date.today())
    #waranty_date =  fields.Date(string='Warranty Due Date',compute='comp_time_hod', store=True)
    #year =  fields.Integer(string="Warranty Period (Years)", default="1")
    file_attach = fields.Binary('File',attachment=True)
    file_attach_diagnosis = fields.Binary('File',attachment=True)
    infr_manager = fields.Integer(string='Infrastructure Manager',compute='_compute_manager')
    #warrant_status =  fields.Selection([('off','OFF'),('on','ON')],string="Warrant Status", required=True, compute='get_warrant_status')

    current_ifra_manager = fields.Boolean('is current user ?', compute='_get_infran_manager')
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')

    base_url = fields.Char('Base Url', compute='_get_url_id',store='True')
    unique_field = fields.Char(compute='comp_name', string='Ref', store=True)
    courier = fields.Many2one('inventory_track.courier',ondelete='cascade',string='Courier ',track_visibility='always')
    repair_courier = fields.Many2one('inventory_track.courier',ondelete='cascade',string='Repair Courier',track_visibility='always')
    initiate_comment = fields.Text(string="Approval Comment")
    initiated_date =  fields.Datetime(string='Intiated Date',track_visibility='always')
    initiated_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')
    diagnosis_approved_comment = fields.Text(string="Comment")
    diagnosis_approved_date =  fields.Datetime(string='Date',track_visibility='always')
    diagnosis_approved_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')
    diagnosis_comment = fields.Text(string="Approval Comment")
    diagnosis_date =  fields.Datetime(string='Date', track_visibility='always')
    diagnosis_by = fields.Many2one('res.users','Diagnosed By:',track_visibility='always')
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    repair_amount = fields.Monetary(string='Repair Amount', required=True,)
    initiate_repair_comment = fields.Text(string="Repair Comment")
    initiate_repair_date =  fields.Datetime(string='Repair Date',track_visibility='always')
    initiate_repair_by = fields.Many2one('res.users','Repair By:',track_visibility='always')
    file_attach_initiate_repair = fields.Binary('Repair File',attachment=True)
    infra_approve_comment = fields.Text(string="Comment")
    infra_approve_date =  fields.Datetime(string='Date',track_visibility='always')
    infra_approve_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')
    infra_reject_comment = fields.Text(string="Comment")
    infra_reject_date =  fields.Datetime(string='Date',track_visibility='always')
    infra_reject_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')
    verify_reject_comment = fields.Text(string="Comment")
    verify_reject_date =  fields.Datetime(string='Verified Date' ,track_visibility='always')
    verify_reject_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')
    manager_by = fields.Many2one('res.users','Intiated By:',track_visibility='always')


    infra_comp_name = fields.Char(string="Computer Name")
    Operating_system_Build = fields.Char(string=" Operating system Build")
    Microsoft_office = fields.Selection([('2016','2016'),('2019','2019')])
    browser = fields.Selection([('no','No'),('yes','Yes')],string="Browsers Firefox and Chrome installed")
    Antivirus = fields.Selection([('no','No'),('yes','Yes')],string="Antivirus: Kaspersky installed and activated")
    os_updates = fields.Selection([('no','No'),('yes','Yes')],string="OS updates installed and up to date")
    user_file = fields.Selection([('no','No'),('yes','Yes')],string="User files transferred/backed up")
    guest_account = fields.Selection([('no','No'),('yes','Yes')],string="Guest Accounts disabled")
    ou = fields.Selection([('no','No'),('yes','Yes')],string="Computer added to correct OU")
    user_department = fields.Char(string="Computer User Department")
    other_information = fields.Char(string="Other information")
   
   
   
    
   
    
    
    
    

    @api.depends('created_on')
    def _get_url_id(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('InventoryTracking.inventory_lists_action', raise_if_not_found=False)
            rec.base_url = """{}/web#id={}&view_type=form&model=inventory_track.inventory&action={}""".format(web_base_url,rec.id,action_id.id)




    
    @api.depends('infr_manager')
    def _get_infran_manager(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_ifra_manager = (True if partner.id == self.infr_manager else False)
 

    @api.depends('dispatched_to')
    def _get_current_user(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_user = (True if partner.id == self.dispatched_to.id else False)


    @api.depends('created_by')
    def _compute_manager(self):
        for record in self:
            record.infr_manager = record.created_by.partner_id.supervisor


    @api.depends('created_by')
    def _compute_serial(self):
        for record in self:
            record.infr_manager = record.created_by.partner_id.supervisor


    @api.depends('created_on')
    def comp_name(self):
        for rec in self:
            value = 'INV'
            date_time = rec.created_on.strftime("%m%d%Y")
            last= '000'
            rec.unique_field = (value or '')+''+(date_time or '')+''+(last or '')+''+(str(rec.id))



   

   
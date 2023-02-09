from odoo import models,api,fields,exceptions
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

class Inventory(models.Model):
    _name = "inventory_track.inventory"
    _description = "This is an Inventory model"
    _rec_name ="tag"

    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True, default="laptop")
    vendor_id = fields.Many2one('inventory_track.vendor',string='Vendor',required=True)
    make = fields.Many2one('inventory_track.make',ondelete='cascade',string='Asset Make')
    model = fields.Many2one('inventory_track.asset_models',string="Asset Model",domain = " [('asset_make','=',make)] " )
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Deployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Deployment Rejected'),('approved','Pending Activation')],string="Asset Status", required=True, default="new")
    tag = fields.Many2one('inventory_track.asset_tags',string="Asset Tag",domain = " [('status','=','approved')] " )
    serial =   fields.Many2many(related='tag.asset_serial')
    ram = fields.Selection([('one','1 GB'),('two','2 GB'),('three','3 GB'),('four','4 GB'),('six','6 GB'),('eight','8 GB'),('twelve','12 GB'),('sixteen','16 GB'),('thirty_two','32 GB')],string="RAM Size",  default="one")
    hdd = fields.Char(string="HDD OR SDD Size")
    os =  fields.Selection([('windows_10','Windows 10'),('windows_11','Windows 11'),('windows_12','Windows 12')],string="OS", required=True, default="windows_10")
    comment = fields.Text(string="comment",required=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Verified Date')
    location_id = fields.Many2one('inventory_track.asset_location',string ='Asset Location')
    dispatched_to = fields.Many2one('res.partner','User')
    dispach_comment = fields.Text(string="Comment")
    dispach_date =  fields.Datetime(string='Deployed Date')
    dispatched_by = fields.Many2one('res.users','Dispatched By:')
    stock_comment = fields.Text(string="Comment")
    stock_date =  fields.Datetime(string='Stock Date')
    cyber_comment = fields.Text(string="Comment")
    cyber_date =  fields.Datetime(string='Cyber Verified Date')
    activated_comment = fields.Text(string="Activation Comment")
    activated_date =  fields.Datetime(string='Activation Date')
    activated_by = fields.Many2one('res.users','Activated By:')
    repaire_comment = fields.Text(string="Comment")
    repaire_date =  fields.Datetime(string='Repair Date')
    repaired_by = fields.Many2one('res.users','Initiated By:')
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date')
    disposed_by = fields.Many2one('res.users','Disposed By:')
    reject_comment = fields.Text(string="Rejection Comment")
    reject_date =  fields.Datetime(string='Rejection Date')
    rejected_by = fields.Many2one('res.users','Rejected By:')
    approval_comment = fields.Text(string="Approval Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    approval_by = fields.Many2one('res.users','Approval By:')
    
   
    effective_date =  fields.Date(string='Effective Date',default=lambda self: fields.date.today())
    waranty_date =  fields.Date(string='Warranty Due Date',compute='comp_time_hod', store=True)
    year =  fields.Integer(string="Warranty Period (Years)", default="1")
    file_attach = fields.Binary('File',attachment=True)
    infr_manager = fields.Integer(string='Infrastructure Manager',compute='_compute_manager')
    warrant_status =  fields.Selection([('off','OFF'),('on','ON')],string="Warrant Status", required=True, compute='get_warrant_status')

    current_ifra_manager = fields.Boolean('is current user ?', compute='_get_infran_manager')
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')

    base_url = fields.Char('Base Url', compute='_get_url_id',store='True')
    
    

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


    @api.depends('effective_date')
    def comp_time_hod(self):
        currentTimeDate = self.effective_date + relativedelta(years=self.year)
        #currentTimeDate = date.today() + relativedelta(years=self.year)
        self.waranty_date = currentTimeDate.strftime('%Y-%m-%d')

    @api.depends('created_by')
    def _compute_manager(self):
        for record in self:
            record.infr_manager = record.created_by.partner_id.supervisor
    
    @api.depends('waranty_date')
    def get_warrant_status(self):
        for record in self:
            if record.waranty_date > date.today():
                record.warrant_status ='on'
            else:
                record.warrant_status ='off'


    @api.model
    def _update_warrant(self):
        self.search([('&'),('waranty_date', '<', date.today()),('warrant_status','=','on')]).write({'warrant_status': "off"})

  
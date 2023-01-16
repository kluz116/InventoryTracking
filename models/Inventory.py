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
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Deployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="new")
    tag = fields.Many2one('inventory_track.asset_tags',string="Asset Tag",domain = " [('status','=','innactive')] " )
    serial =   fields.Many2many(related='tag.asset_serial')
    ram = fields.Selection([('one','1 GB'),('two','2 GB'),('three','3 GB'),('four','4 GB'),('six','6 GB'),('eight','8 GB'),('twelve','12 GB'),('sixteen','16 GB'),('thirty_two','32 GB')],string="RAM Size",  default="one")
    hdd = fields.Char(string="HDD OR SDD Size")
    os =  fields.Selection([('windows_10','Windows 10'),('windows_11','Windows 11'),('windows_12','Windows 12')],string="OS", required=True, default="windows_10")
    comment = fields.Char(string="comment",required=True)
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
    effective_date =  fields.Date(string='Effective Date',default=lambda self: fields.date.today())
    waranty_date =  fields.Date(string='Warranty Due Date',compute='comp_time_hod', store=True)
    year =  fields.Integer(string="Warranty Period (Years)", default="1")
    file_attach = fields.Binary('File',attachment=True)
    


    @api.depends('effective_date')
    def comp_time_hod(self):
        currentTimeDate = self.effective_date + relativedelta(years=self.year)
        #currentTimeDate = date.today() + relativedelta(years=self.year)
        self.waranty_date = currentTimeDate.strftime('%Y-%m-%d')

   

  
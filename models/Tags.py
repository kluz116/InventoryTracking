from odoo import models,api,fields,exceptions
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

class AssetSerial(models.Model):
    _name = "inventory_track.asset_serial"
    _description = "This is a serial model"
    _rec_name ="serial"

    asset_id = fields.Many2one('inventory_track.asset_tags', string='Asset Tag')
    serial = fields.Char(string="Asset Serial", required=True)
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('disposed','Disposed')],string="Status", required=True, default="innactive")
    serial_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)

class Tag(models.Model):
    _name = "inventory_track.asset_tags"
    _description = "This is a tag model"
    _rec_name ="tag"
    
    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True, default="laptop")
    vendor_id = fields.Many2one('inventory_track.vendor',string='Vendor',required=True)
    tag = fields.Char(string="Asset TAG", required=True)
    asset_serial = fields.One2many('inventory_track.asset_serial','asset_id' ,string='Asset Serial')
    #asset_serial = fields.Many2many('inventory_track.asset_serial',ondelete='cascade',string='Asset Serial',domain = " [('status','=','innactive')] " )
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('approved','Approved'),('rejected','Rejected')],string="Status", required=True, default="innactive")
    tag_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
    approval_comment = fields.Text(string="Approval Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    approval_by = fields.Many2one('res.users','Approval By:')
    reject_comment = fields.Text(string="Rejection Comment")
    reject_date =  fields.Datetime(string='Rejection Date')
    rejected_by = fields.Many2one('res.users','Rejected By:')
    effective_date =  fields.Date(string='Effective Date',default=lambda self: fields.date.today())
    waranty_date =  fields.Date(string='Warranty Due Date',compute='comp_time_hod', store=True)
    year =  fields.Integer(string="Warranty Period (Years)", default="1")
    warrant_status =  fields.Selection([('off','OFF'),('on','ON')],string="Warrant Status", required=True, compute='get_warrant_status')
    recievd_date =  fields.Date(string='Recieved Date',default=lambda self: fields.date.today())
    base_url = fields.Char('Base Url', compute='_get_url_id',store='True')
    
    
    

    @api.depends('tag_date')
    def _get_url_id(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('InventoryTracking.asset_tags_lists_action', raise_if_not_found=False)
            rec.base_url = """{}/web#id={}&view_type=form&model=inventory_track.asset_tags&action={}""".format(web_base_url,rec.id,action_id.id)

   
    
    @api.depends('effective_date')
    def comp_time_hod(self):
        for e in self:
            currentTimeDate = e.effective_date + relativedelta(years=e.year)
            e.waranty_date = currentTimeDate.strftime('%Y-%m-%d')

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
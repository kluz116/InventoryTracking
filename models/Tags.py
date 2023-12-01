from odoo import models,api,fields,exceptions,_
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date


class Courier(models.Model):
    _name = "inventory_track.courier"
    _description = "This model is for courier services"
    _rec_name ="courier_name"

    
    courier_name = fields.Char(string="Courier Name ", required=True)
    email = fields.Char(string="Email ")
    phone = fields.Char(string="Phone ", required=True)
    id = fields.Binary('National ID',attachment=True, required=True)
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
   

class AssetSerial(models.Model):
    _name = "inventory_track.asset_serial"
    _description = "This is a serial model"
    _rec_name ="serial"

    #asset_id = fields.Many2one('inventory_track.asset_tags', string='Asset Tag')
    #tag = fields.Char(related='asset_id.tag', string='Tag')
    serial = fields.Char(string="Asset Serial", required=True)
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('disposed','Disposed'),(('repair','Repair'))],string="Status", required=True, default="innactive")
    serial_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)

    @api.constrains('serial')
    def _check_Serial_unique(self):
        for rec in self:
            serial_counts = self.search_count([('serial', '=', rec.serial), ('id', '!=', rec.id)])
            if serial_counts > 0:
                raise ValidationError(f"Serial number {rec.serial} already exists!")

class Tag(models.Model):
    _name = "inventory_track.asset_tags"
    _inherit="mail.thread"
    _description = "Asset Tag"
    _rec_name ="tag"
    
    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer'),('switch','Switch'),('router','Router')],string="Asset Type", required=True, default="laptop",track_visibility='always')
    vendor_id = fields.Many2one('inventory_track.vendor',string='Vendor',required=True,track_visibility='always')
    tag = fields.Char(string="Asset TAG", required=True,track_visibility='always')
    #asset_serial = fields.One2many('inventory_track.asset_serial','asset_id' ,string='Asset Serial')
    asset_serial = fields.Many2many('inventory_track.asset_serial',ondelete='cascade',string='Asset Serial',domain = " [('status','=','innactive')] " ,track_visibility='always')
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('approved','Approved'),('rejected','Rejected'),('disposed','Disposed Off')],string="Status", required=True, default="innactive",track_visibility='always')
    tag_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(),track_visibility='always')
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
    approval_comment = fields.Text(string="Approval Comment")
    approval_date =  fields.Datetime(string='Approval Date',track_visibility='always')
    approval_by = fields.Many2one('res.users','Approval By:',track_visibility='always')
    reject_comment = fields.Text(string="Rejection Comment")
    reject_date =  fields.Datetime(string='Rejection Date',track_visibility='always')
    rejected_by = fields.Many2one('res.users','Rejected By:',track_visibility='always')
    effective_date =  fields.Date(string='Effective Date',default=lambda self: fields.date.today())
    waranty_date =  fields.Date(string='Warranty Due Date',compute='comp_time_hod', store=True)
    year =  fields.Integer(string="Warranty(Years)", default="3")
    warrant_status =  fields.Selection([('off','OFF'),('on','ON')],string="Warrant Status", required=True, compute='get_warrant_status')
    recievd_date =  fields.Date(string='Recieved Date',default=lambda self: fields.date.today(),track_visibility='always')
    base_url = fields.Char('Base Url', compute='_get_url_id',store='True')
    batch_id = fields.Char(compute='comp_name', string='Batch', store=True)
    
    
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('tag'):
            default['tag'] = _("%s (copy)") % (self.tag)
        return super(Tag, self).copy(default)
    
    

    def action_duplicate_tag(self):
        for obj in self.browse(self.env.context['active_ids']):
            obj.copy()
    
    
    @api.depends('tag_date')
    def _get_url_id(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('InventoryTracking.asset_tags_lists_action', raise_if_not_found=False)
            rec.base_url = """{}/web#id={}&view_type=form&model=inventory_track.asset_tags&action={}""".format(web_base_url,rec.id,action_id.id)

   
    
    @api.depends('effective_date','year')
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


    @api.constrains('tag')
    def _check_tag_unique(self):
        for rec in self:
            tag_counts = self.search_count([('tag', '=', rec.tag), ('id', '!=', rec.id)])
            if tag_counts > 0:
                raise ValidationError(f"Asset Tag {rec.tag} already exists!")
            
    @api.depends('recievd_date')
    def comp_name(self):
        for rec in self:
            value = 'BATCHID'
            date_time = rec.recievd_date.strftime("%m%d%Y")
            rec.batch_id = (value or '')+'-'+(date_time or '')
            
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {},
                       name=_("%s (copy)", self.tag))
        return super().copy(default=default)
    
   
 
        

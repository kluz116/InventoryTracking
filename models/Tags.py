from odoo import models,api,fields,exceptions


class AssetSerial(models.Model):
    _name = "inventory_track.asset_serial"
    _description = "This is a serial model"
    _rec_name ="serial"

    serial = fields.Char(string="Asset Serial", required=True)
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('disposed','Disposed')],string="Status", required=True, default="innactive")
    serial_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)

class Tag(models.Model):
    _name = "inventory_track.asset_tags"
    _description = "This is a tag model"
    _rec_name ="tag"

    tag = fields.Char(string="Asset TAG", required=True)
    asset_serial = fields.Many2many('inventory_track.asset_serial',ondelete='cascade',string='Asset Serial',domain = " [('status','=','innactive')] " )
    status =  fields.Selection([('active','Active'),('innactive','Innactive'),('approved','Approved'),('rejected','Rejected')],string="Status", required=True, default="innactive")
    tag_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
    approval_comment = fields.Text(string="Approval Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    approval_by = fields.Many2one('res.users','Approval By:')
    reject_comment = fields.Text(string="Rejection Comment")
    reject_date =  fields.Datetime(string='Rejection Date')
    rejected_by = fields.Many2one('res.users','Rejected By:')
    base_url = fields.Char('Base Url', compute='_get_url_id',store='True')
    
    
    

    @api.depends('tag_date')
    def _get_url_id(self):
        for rec in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('InventoryTracking.asset_tags_lists_action', raise_if_not_found=False)
            rec.base_url = """{}/web#id={}&view_type=form&model=inventory_track.asset_tags&action={}""".format(web_base_url,rec.id,action_id.id)

   

from odoo import models,api,fields,exceptions

class Tag(models.Model):
    _name = "inventory_track.asset_tags"
    _description = "This is a tag model"
    _rec_name ="tag"

    tag = fields.Char(string="Asset TAG", required=True)
    status =  fields.Selection([('active','Active'),('innactive','Innactive')],string="Status", required=True, default="innactive")
    tag_date =  fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Created By:',default=lambda self: self.env.user)
   
    
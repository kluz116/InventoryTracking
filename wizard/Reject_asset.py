from odoo import api, fields, models
from datetime import datetime

class RejectAsset(models.TransientModel):
    _name = "inventory_track.asset_rejected"
    _description = "Reject Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected')],string="Asset Status", required=True, default="rejected")
    reject_comment = fields.Text(string="Rejection Comment",required=True)
    reject_date =  fields.Datetime(string='Rejection Date', default=lambda self: fields.datetime.now())
    rejected_by = fields.Many2one('res.users','Rejected By:',default=lambda self: self.env.user)
    
    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',ondelete='cascade',string='Asset Serial')
    
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    def comp_asset_location(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.location_id.location_name 

    location_name = fields.Char(string="Asset Location",default=comp_asset_location,required=True)

    
    def reject__asset(self):
        self.write({'asset_status': 'rejected'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.reject_comment = self.reject_comment
            req.reject_date = self.reject_date
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment_rejected').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

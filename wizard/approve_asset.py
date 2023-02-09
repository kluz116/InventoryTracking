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
    
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    def comp_asset_location(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.location_id.location_name 

    location_name = fields.Char(string="Asset Location",default=comp_asset_location,required=True)

    
    def approve__asset(self):
        self.write({'asset_status': 'approved'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.approval_comment = self.approval_comment
            req.approval_date = self.approval_date
            req.approval_by = self.approval_by
            
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment_user').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

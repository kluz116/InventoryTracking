from odoo import api, fields, models
from datetime import datetime

class VerifyAssetCyberNetwork(models.TransientModel):
    _name = "inventory_track.verify_asset_cyber_network"
    _description = "Verify Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation')],string="Asset Status", required=True, default="approved")
    cyber_comment = fields.Text(string="Comment")
    cyber_date =  fields.Datetime(string='Verified Date', default=lambda self: fields.datetime.now())
   
    
    def comp_asset_tag_id(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.tag


    infra_comp_name = fields.Char(string="Asset Tag",default=comp_asset_tag_id)
    
    def comp_asset_tag_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial.serial
    asset_serial = fields.Char(string="Serial",default=comp_asset_tag_serial)

    def comp_asset_type(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_type
    asset_type = fields.Char(string="Type",default=comp_asset_type)
    
    def comp_asset_make(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.make.make_name
    asset_make = fields.Char(string="Make",default=comp_asset_make)
    
    def comp_asset_model(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.model.asset_model
    asset_model = fields.Char(string="Asset Model",default=comp_asset_model)
        
        


    def verify_cyber_asset_net(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.cyber_comment = self.cyber_comment
            req.cyber_date = self.cyber_date
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

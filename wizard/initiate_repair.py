from odoo import api, fields, models
from datetime import datetime

class InitiateRepair(models.TransientModel):
    _name = "inventory_track.asset_initiate_repair"
    _description = "Initiate Repair"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation'),('repair_mode','Repair Mode')],string="Asset Status", required=True, default="verified_one")
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    repair_amount = fields.Monetary(string='Amount', required=True,track_visibility='always')
    initiate_repair_comment = fields.Text(string="Repair Comment",required=True)
    initiate_repair_date =  fields.Datetime(string='Repair Date', default=lambda self: fields.datetime.now())
    initiate_repair_by = fields.Many2one('res.users','Repair By:',default=lambda self: self.env.user)
    file_attach_initiate_repair = fields.Binary('Repair File',attachment=True)
    
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



    def initiate_repair_req(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.initiate_repair_comment = self.initiate_repair_comment
            req.initiate_repair_date = self.initiate_repair_date
            req.initiate_repair_by = self.initiate_repair_by
            req.file_attach_initiate_repair = self.file_attach_initiate_repair
            
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_repair_ini').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

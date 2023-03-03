from odoo import api, fields, models
from datetime import datetime

class InitiateDiagonosis(models.TransientModel):
    _name = "inventory_track.intiatediagnosis"
    _description = "Intiate diagnosis "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation'),('pending_diagnosis_approval','Pending Diagnosis Approval')],string="Asset Status", required=True, default="pending_diagnosis_approval")
    initiate_comment = fields.Text(string="Intiated Comment",required=True)
    initiated_date =  fields.Datetime(string='Intiated Date', default=lambda self: fields.datetime.now())
    initiated_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
    
    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',ondelete='cascade',string='Asset Serial')
    #serial_set = fields.One2many(related='tag.asset_serial' ,string='Asset Serial')
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    
    def initiated_diagnosis(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.initiate_comment = self.initiate_comment
            req.initiated_date = self.initiated_date
            req.initiated_by = self.initiated_by
            
            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment_user').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

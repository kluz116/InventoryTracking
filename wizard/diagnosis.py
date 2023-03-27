from odoo import api, fields, models
from datetime import datetime

class AssetDiagnosis(models.TransientModel):
    _name = "inventory_track.asset_diagnosis"
    _description = "Asset Diagnosis"
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation'),('repair_mode','Repair Mode')],string="Asset Status", required=True, default="repair_mode")
    diagnosis_comment = fields.Text(string="Diagnosis Comment",required=True)
    diagnosis_date =  fields.Datetime(string='Diagnosis Date', default=lambda self: fields.datetime.now())
    diagnosis_by = fields.Many2one('res.users','Diagnosis By:',default=lambda self: self.env.user)
    file_attach_diagnosis = fields.Binary('Diagnosis File',attachment=True)
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    Proposed_cost_of_repair = fields.Monetary(string='Proposed cost of repair', required=True,track_visibility='always')
    book_value = fields.Monetary(string='Book Value or Asset Value(UGX)', required=True,track_visibility='always')
    
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



    def diagnosis_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.diagnosis_comment = self.diagnosis_comment
            req.diagnosis_date = self.diagnosis_date
            req.diagnosis_by = self.diagnosis_by
            req.file_attach_diagnosis = self.file_attach_diagnosis
            req.Proposed_cost_of_repair = self.Proposed_cost_of_repair
            req.book_value = self.book_value
            req.currency_id = self.currency_id
            
            
            

            template_id = self.env.ref('InventoryTracking.email_template_create_asset_diagnosis').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         

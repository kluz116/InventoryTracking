from odoo import api, fields, models
from datetime import datetime

class RepairApproval(models.TransientModel):
    _name = "inventory_track.asset_reject_repair"
    _description = "Reject Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal'),('rejected','Rejected'),('approved','Pending Activation'),('repair_approval','Repair Approved'),('repair_rejected','Repair Rejected')],string="Asset Status", required=True, default="repair_rejected")
    repair_reject_comment = fields.Text(string="Rejection Comment",required=True)
    repair_reject_date =  fields.Datetime(string='Rejection Date', default=lambda self: fields.datetime.now())
    repair_reject_by = fields.Many2one('res.users','Rejected By:',default=lambda self: self.env.user)
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    def comp_asProposed_cost_of_repairset_tags(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.Proposed_cost_of_repair 

 
    Proposed_cost_of_repair = fields.Monetary(string='Proposed cost of repair',default=comp_asProposed_cost_of_repairset_tags)

    def book_values(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.book_value 
        
    book_value = fields.Monetary(string='Book Value or Asset Value(UGX)',default=book_values)
    
    
    def reject_repair_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.repair_reject_comment = self.repair_reject_comment
            req.repair_reject_date = self.repair_reject_date
            req.repair_reject_by = self.repair_reject_by
            
            

            #template_id = self.env.ref('InventoryTracking.email_template_create_asset_deployment_user').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

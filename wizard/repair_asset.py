from odoo import api, fields, models
from datetime import datetime

class RepairAsset(models.TransientModel):
    _name = "inventory_track.repair"
    _description = "Repair Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="active")
    repaire_comment = fields.Text(string="Comment", required=True)
    repaire_date =  fields.Datetime(string='Repair Date', default=lambda self: fields.datetime.now())
    repaired_by = fields.Many2one('res.users','Initiated By:',default=lambda self: self.env.user)
   
    
    def activate_asset(self):
        self.write({'asset_status': 'repair'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.activated_comment = self.activated_comment
            req.activated_date = self.activated_date
            req.activated_by = self.activated_by

            vals = { 'asset_id': req.id, 
                 'asset_status': self.asset_status,
                 'repaire_comment': self.repaire_comment,
                 'repaire_date': self.repaire_date,
                 'repaired_by': self.repaired_by.id,
                 }

            self.env['inventory_track.asset_repair_log'].create(vals)
            

           # template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

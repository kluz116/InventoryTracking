from odoo import api, fields, models
from datetime import datetime

class ActivateAsset(models.TransientModel):
    _name = "inventory_track.verify_asset_activate"
    _description = "Activate Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="active")
    activated_comment = fields.Text(string="Comment")
    activated_date =  fields.Datetime(string='Activated Date', default=lambda self: fields.datetime.now())
    activated_by = fields.Many2one('res.users','Activated By:',default=lambda self: self.env.user)
    activated_by_id = fields.Integer(related='activated_by.id')
    #asset_id = fields.Many2one('inventory_track.inventory',string='Asset',required=True)
   
    
    def activate_asset(self):
        self.write({'asset_status': 'active'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.activated_comment = self.activated_comment
            req.activated_date = self.activated_date
            req.activated_by = self.activated_by

            vals = { 'asset_id': req.id, 
                 'asset_status': self.asset_status,
                 'activated_comment': self.activated_comment,
                 'activated_date': self.activated_date,
                 'activated_by': self.activated_by_id,
                 }

            self.env['inventory_track.asset_activate_log'].create(vals)
            

           # template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

from odoo import models, fields, api
from datetime import datetime

class DispatchAsset(models.TransientModel):
    _name = "inventory_track.dispatch_asset"
    _description = "dispatched asset"
    _rec_name ="asset_status"
  
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="new")
    location_id = fields.Many2one('inventory_track.asset_location',string ='Asset Location', required=True)
    dispatched_to = fields.Many2one('res.partner','User',domain="[('loaction_id_invetory', '=', location_id)]")
    dispach_comment = fields.Text(string="Comment")
    dispach_date =  fields.Datetime(string='Deployment Date', default=lambda self: fields.datetime.now())
    dispatched_by = fields.Many2one('res.users','Deployed By:',default=lambda self: self.env.user)

  

    def dispatch__asset(self):
        self.write({'asset_status': 'diployment'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        
        for req in asset:
            req.asset_status = self.asset_status
            req.location_id = self.location_id.id
            req.dispatched_to = self.dispatched_to.id
            req.dispach_comment = self.dispach_comment
            req.dispach_date = self.dispach_date
            req.dispatched_by = self.dispatched_by.id
            

           # template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

   

        

       
 

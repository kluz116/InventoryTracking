from odoo import api, fields, models


class DisPoseAsset(models.TransientModel):
    _name = "inventory_track.dispose_asset"
    _description = "Disposal Asset "
    _rec_name = 'asset_status'

    
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="new")
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date', default=lambda self: fields.datetime.now())
    disposed_by = fields.Many2one('res.users','Disposed By:',default=lambda self: self.env.user)
   
    
    def disposal_asset(self):
        self.write({'asset_status': 'disposal'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.disposal_comment = self.disposal_comment
            req.disposal_date = self.disposal_date
            req.disposed_by = self.disposed_by

           # template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

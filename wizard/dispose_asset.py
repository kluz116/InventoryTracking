from odoo import api, fields, models


class DisPoseAsset(models.TransientModel):
    _name = "inventory_track.dispose_asset"
    _description = "Disposal Asset "
    _rec_name = 'asset_status'

    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="disposal")
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date', default=lambda self: fields.datetime.now())
    disposed_by = fields.Many2one('res.users','Disposed By:',default=lambda self: self.env.user)

    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',string='Asset Serial')
    
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    serial = fields.Many2many('inventory_track.asset_serial',default=comp_asset_serial,string='Asset Serial',domain = " [('status','in',[serial_set])] ")
 
   
    
    def disposal_asset(self):
        self.write({'asset_status': 'disposal'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.asset_status = self.asset_status
            req.disposal_comment = self.disposal_comment
            req.disposal_date = self.disposal_date
            req.disposed_by = self.disposed_by

            for i in req.tag.asset_serial:
                if i.serial == self.serial.serial and i.status=='active':
                    i.status = 'disposed'  

            
            vals = { 
                'asset_type':self.asset_type,
                'asset_id': req.id, 
                'serial': self.serial.id,
                'asset_status': self.asset_status,
                'dispose_comment': self.disposal_comment,
                 'dispose_date': self.disposal_date,
                 'dispose__by': self.disposed_by.id
                 }

            self.env['inventory_track.asset_dispose_log'].create(vals)

            template_id = self.env.ref('cash_managment.email_template_create_asset_disposed').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         

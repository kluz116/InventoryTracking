from odoo import api, fields, models
from datetime import datetime

class RepairAsset(models.TransientModel):
    _name = "inventory_track.repair"
    _description = "Repair Asset "
    _rec_name = 'asset_status'

    asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="repair")
    repaire_comment = fields.Text(string="Comment", required=True)
    repaire_date =  fields.Datetime(string='Repair Date', default=lambda self: fields.datetime.now())
    repaired_by = fields.Many2one('res.users','Initiated By:',default=lambda self: self.env.user)

    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',ondelete='cascade',string='Asset Serial')
    #serial_set = fields.One2many('inventory_track.asset_serial','asset_id' ,string='Asset Serial')
    
    
    def comp_asset_serial(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag.asset_serial

    serial = fields.Many2many('inventory_track.asset_serial',default=comp_asset_serial,string='Asset Serial',domain = " [('status','in',[serial_set])] ")
 

    
    def repair_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            #req.asset_status = self.asset_status
            req.repaire_comment = self.repaire_comment
            req.repaire_date = self.repaire_date
            req.repaired_by = self.repaired_by


            if len(req.tag.asset_serial) > 1 :
                for i in req.tag.asset_serial:
                    if i.serial == self.serial.serial and i.status=='active':
                        i.status = 'repair'
                        req.asset_status = 'repair' 

            else:
                req.asset_status = 'repair'
                req.tag.asset_serial.status = 'repair'

            vals = { 
                'asset_type':self.asset_type,
                 'asset_id': req.id, 
                 'serial': self.serial.id,
                 'asset_status': self.asset_status,
                 'repaire_comment': self.repaire_comment,
                 'repaire_date': self.repaire_date,
                 'repaired_by': self.repaired_by.id,
                 }



            self.env['inventory_track.asset_repair_log'].create(vals)
            template_id = self.env.ref('InventoryTracking.email_template_create_asset_repair').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         




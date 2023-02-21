from odoo import api, fields, models,exceptions


class DisPoseAsset(models.TransientModel):
    _name = "inventory_track.dispose_asset"
    _description = "Disposal Asset "
    _rec_name = 'asset_status'


    #asset_type =  fields.Selection([('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')],string="Asset Type", required=True)
    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="disposal")
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date', default=lambda self: fields.datetime.now())
    disposed_by = fields.Many2one('res.users','Disposed By:',default=lambda self: self.env.user)

    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    #serial_set =   fields.Many2many(related='tag.asset_serial',string='Asset Serial')
    serial_set = fields.One2many(related='tag.asset_serial' ,string='Asset Serial')
    asset_type = fields.Selection(related='tag.asset_type',selection=[('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')])
    
    #def comp_asset_serial(self):
       # asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        #for req in asset:
            #return req.tag.asset_serial

    #serial = fields.one2many('inventory_track.asset_serial',default=comp_asset_serial,string='Asset Serial',domain = " [('status','in',[serial_set])] ")
 
    #serial = fields.One2many('inventory_track.asset_serial',default=comp_asset_serial  ,string='Asset Serial')
   # serial = fields.One2many('inventory_track.asset_serial','asset_id' ,string='Asset Serial',domain = " [('id','in',serial_set)]")
    serial = fields.Many2many('inventory_track.asset_serial' ,string='Asset Serial',domain = " ['&',('id','in',serial_set),('status','in',['active'])]")
    
    def disposal_asset(self):
        #self.write({'asset_status': 'disposal'})
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            #req.asset_status = self.asset_status
            req.disposal_comment = self.disposal_comment
            req.disposal_date = self.disposal_date
            req.disposed_by = self.disposed_by

            
            if len(req.tag.asset_serial) > 1 :
                #raise exceptions.ValidationError(f"Hmmmmm Length of string {len(req.tag.asset_serial)} and List  {req.tag.asset_serial}  Type of {type(req.tag.asset_serial)}")
                for i in req.tag.asset_serial:
                    if i.serial == self.serial.serial and i.status=='active':
                        #raise exceptions.ValidationError(f"Hmmmmm Length of string {i.serial } {i.status} {self.serial.serial }")

                        serial_id = []
                        
                        #i.status = 'disposed'
                        #req.asset_status = 'active' 
                        serial_id.append(self.serial.id)
                        #req.tag.asset_serial = self.serial.id
                        #raise exceptions.ValidationError(f"Serial ID {serial_id}")
                        #raise exceptions.ValidationError(f"Hmmmmm Length of string {req.tag.asset_serial}")

                        #self.env['inventory_track.asset_serial'].write({'asset_id': [(4, self.serial)] })
                        #self.env['inventory_track.asset_tags'].update({'asset_serial' :[( 6, 0, serial_id)]})
                        #  req.tag.asset_serial.write({'asset_serial' :[( 6, 0, serial_id)]})  
                        req.tag.write({'asset_serial' : serial_id}) 
                        #raise exceptions.ValidationError(f"ID to Be Flagged OFF {serial_id}")

                        
            else:
                pass
                #req.asset_status = 'disposal'
                #req.tag.asset_serial.status = 'disposed'
                

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
               
            template_id = self.env.ref('InventoryTracking.email_template_create_asset_disposed').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
        
            ''''
            @api.model
                def create(self,vals):
                    project_ids = []
                    stage_obj = self.env['project.task.type']
                    result = super(Project, self).create(vals)
                    for resource in result:
                        for source in resource.stage_ids:
                            if source:
                                stage_id = stage_obj.search([('id', '=',source.name.id)])
                                project_ids.append(result.id)
                                stage_id.update({'project_ids': [( 6, 0, project_ids)]})
                    return result
          '''
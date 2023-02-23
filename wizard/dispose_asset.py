from odoo import api, fields, models,exceptions


class DisPoseAsset(models.TransientModel):
    _name = "inventory_track.dispose_asset"
    _description = "Disposal Asset "
    _rec_name = 'asset_status'

    asset_status = fields.Selection([('new','New'),('stocked','Stocked'),('verified','Verified'),('verified_one','Cyber Verified'),('diployment','Diployment'),('active','Active'),('repair','Repair'),('disposal','Disposal')],string="Asset Status", required=True, default="disposal")
    disposal_comment = fields.Text(string="Disposal Comment")
    disposal_date =  fields.Datetime(string='Disposal Date', default=lambda self: fields.datetime.now())
    disposed_by = fields.Many2one('res.users','Disposed By:',default=lambda self: self.env.user)

    def comp_asset_tag(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            return req.tag 

    tag = fields.Many2one('inventory_track.asset_tags',string="Asset TAG",default=comp_asset_tag, required=True)
    serial_set =   fields.Many2many(related='tag.asset_serial',ondelete='cascade',string='Asset Serial')
    asset_type = fields.Selection(related='tag.asset_type',selection=[('laptop','Laptop Computer'),('desktop_cpu','Desktop & CPU'),('cpu','CPU Only'),('monitor','Monitor'),('printer','Printer')])
    
    serial = fields.Many2many('inventory_track.asset_serial' ,string='Disposable Serial',domain = " ['&',('id','in',serial_set),('status','in',['active'])]")
    
    def disposal_asset(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        for req in asset:
            req.disposal_comment = self.disposal_comment
            req.disposal_date = self.disposal_date
            req.disposed_by = self.disposed_by
             
            list1 = []
            for i in req.tag.asset_serial:
                list1.append(i.id)
            
            if len(req.tag.asset_serial) > 1 :
                for i in req.tag.asset_serial:
                    if i.serial == self.serial.serial and i.status=='active':
                        
                        serial_id = []
                      
                        #serial_id.append(self.serial.id)
                        serial_id.append(i.id)
                     
                        req.tag.write({'asset_serial' :[( 6, False, list(filter(lambda serial: serial != self.serial.id, list1)))]})  
                        i.status = 'disposed'
                        req.asset_status = 'active' 

                        #req.tag.write({'asset_serial' : list(filter(lambda serial: serial != serial_id, list1))}) 
                        #raise exceptions.ValidationError(f"ID to Be Flagged OFF {list(filter(lambda serial: serial != serial_id, list1))} and {{'asset_serial' :[( 6, 0, {serial_id})]}} Lists {list1} hmmmm {req.tag.asset_serial}")  
                        #raise exceptions.ValidationError(f"What A Fuck a You Getting {list1}  hhhhh {serial_id} Filtered {list(filter(lambda serial: serial != self.serial.id, list1))}")    
                     
            else:
                req.asset_status = 'disposal'
                req.tag.asset_serial.status = 'disposed'


      

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
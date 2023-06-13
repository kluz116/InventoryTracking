from odoo import models, fields, api,exceptions
 
class TagNotify(models.Model):
    _inherit = 'inventory_track.asset_tags'

    @api.model
    def create(self, values):
        res = super(TagNotify, self).create(values)
        res.asset_serial.status='active'

        #tags = self.env['inventory_track.asset_serial'].search([('serial', '=',res.asset_serial.serial)])
        #print(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX: {tags} XXXXXXXXXXXXXXXXXXXXXXXXX")

    
        #for tag in tags.id:
            #tag.status = 'active'
        
        

        #template_id = self.env.ref('InventoryTracking.email_template_create_asset_tag').id
        #template =  self.env['mail.template'].browse(template_id)
        #template.send_mail(res.id,force_send=True)
        return res



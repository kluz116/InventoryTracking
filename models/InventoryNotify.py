from odoo import models, fields, api
 
class InventoryNotify(models.Model):
    _inherit = 'inventory_track.inventory'

    @api.model
    def create(self, values):
        res = super(InventoryNotify, self).create(values)

        tags = self.env['inventory_track.asset_tags'].search([('tag', '=',res.tag.tag)])
        for tag in tags:
            tag.status = 'active'

        #template_id = self.env.ref('cash_managment.email_template_create_request').id
        #template =  self.env['mail.template'].browse(template_id)
        #template.send_mail(res.id,force_send=True)
        return res

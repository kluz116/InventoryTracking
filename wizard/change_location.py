from odoo import models, fields, api,exceptions
from datetime import datetime

class ChangeLocation(models.TransientModel):
    _name = "inventory_track.change_location"
    _description = "Change User"
    _rec_name ="location_id"

    location_id = fields.Many2one('inventory_track.asset_location',string ='Asset Location', required=True)
    dispatched_to = fields.Many2one('res.partner','Custodian',domain="[('loaction_id_invetory', '=', location_id)]")

   
    def change_location(self):
        asset = self.env['inventory_track.inventory'].browse(self._context.get('active_ids'))
        
        for req in asset:
            req.location_id = self.location_id.id
            req.dispatched_to = self.dispatched_to.id


         

   

        

       
 

from odoo import api, fields, models
from datetime import datetime

class AssetCheckList(models.Model):
    _name = "inventory_track.asset_checklist_log"
    _description = "Asset Check List "
    _rec_name = 'infra_comp_name'

    asset_id = fields.Many2one('inventory_track.inventory',string='Asset',required=True)
    infra_comp_name = fields.Char(string="Computer Name", required=True)
    Operating_system_Build = fields.Char(string=" Operating system Build", required=True)
    Microsoft_office = fields.Selection([('2016','2016'),('2019','2019')],string="Microsoft Office", required=True)
    browser = fields.Selection([('no','No'),('yes','Yes')],string="Browsers Firefox and Chrome installed", required=True,default='no')
    Antivirus = fields.Selection([('no','No'),('yes','Yes')],string="Antivirus: Kaspersky installed and activated", required=True,default='no')
    os_updates = fields.Selection([('no','No'),('yes','Yes')],string="OS updates installed and up to date", required=True,default='no')
    user_file = fields.Selection([('no','No'),('yes','Yes')],string="User files transferred/backed up", required=True,default='no')
    guest_account = fields.Selection([('no','No'),('yes','Yes')],string="Guest Accounts disabled", required=True,default='no')
    ou = fields.Selection([('no','No'),('yes','Yes')],string="Computer added to correct OU", required=True,default='no')
    user_department = fields.Char(string="Computer User Department", required=True)
    other_information = fields.Char(string="Other information", required=True)
    infra_approve_by = fields.Many2one('res.users','Intiated By:',default=lambda self: self.env.user)
   
   
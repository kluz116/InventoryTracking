
from odoo import models,exceptions


class InventoryXlsx(models.AbstractModel):

    _name = 'report.inventory_track.inventory_list'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, inventory):
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet("Asset Inventory report")
         
        sheet.write(0, 0, "Ref",bold)
        sheet.write(0, 1, "Make",bold)
        sheet.write(0, 2, "Model",bold)
        sheet.write(0, 3, "Asset Status",bold)
        sheet.write(0, 4, "Tag",bold)
        sheet.write(0, 5, "Serial",bold)
        sheet.write(0, 6, "Batch",bold)
        sheet.write(0, 7, "Asset Type",bold)
        sheet.write(0, 8, "RAM",bold)
        sheet.write(0, 9, "HDD",bold)
        sheet.write(0, 10, "OS",bold)
        sheet.write(0, 11, "Comp Name",bold)
        sheet.write(0, 12, "Processor",bold)
        sheet.write(0, 13, "BIOS",bold)
        sheet.write(0, 14, "OS Build",bold)  

        for obj in inventory:
            #report_name = obj.name
            # One sheet by partner
         
            #write column names
  
        
            sheet.write(1, 0, obj.unique_field)
            sheet.write(1, 1, obj.make.make_name)
            sheet.write(1, 2, obj.model.asset_model)
            sheet.write(1, 3, obj.asset_status)
            sheet.write(1, 4, obj.tag.tag)
            sheet.write(1, 5, 'Serial')
            sheet.write(1, 6, obj.batch_id)
            sheet.write(1, 7, obj.asset_type)
            sheet.write(1, 8, obj.ram)
            sheet.write(1, 9, obj.hdd)
            sheet.write(1, 10, obj.os)
            sheet.write(1, 11, obj.comp_names)
            sheet.write(1, 12, obj.Processor)
            sheet.write(1, 13, obj.bios)
            sheet.write(1, 14, obj.os_build)
            




# -*- coding: utf-8 -*-
import os
from odoo import models, fields, api, _
from odoo.exceptions import Warning,ValidationError, UserError
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class ProductStockWiz(models.TransientModel):
    _name = 'product.stock.wiz'
    _description = 'Product stock wizard'

    location_ids = fields.Many2many('stock.location', string='Locations')
    category_ids = fields.Many2many('product.category', string='Categories')
    product_ids = fields.Many2many('product.product', string='Products')


    @api.multi
    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        return self.env['report'].get_action(self, 'product_stock_report.product_stock_xls_temp',
        data=data)



class ProductStockReportXls(ReportXlsx):
    
    
    @api.multi
    def generate_xlsx_report(self, workbook, input_records, wiz):
        domain = []
        if wiz.product_ids:
            domain = [('product_id', 'in', wiz.product_ids.ids)]
        if wiz.location_ids:
            domain.append(('location_id', 'in', wiz.location_ids.ids))
        if wiz.category_ids:
            domain.append(('product_id.categ_id', 'in', wiz.category_ids.ids))
        quant_ids = self.env['stock.quant'].search(domain)
        if not quant_ids:
            raise ValidationError("No records match your given filters")

        location_ids = quant_ids.mapped('location_id')
        locations = {}
        for loc in location_ids:
            loc_quant_ids = quant_ids.filtered(lambda r:r.location_id == loc)
            location_qty = sum(loc_quant_ids.mapped('qty'))
            location_cost =  sum([l.product_id.standard_price * l.qty for l in loc_quant_ids])
            location_lst_price = sum([l.product_id.lst_price * l.qty for l in loc_quant_ids])
            loc_cat_ids = quant_ids.mapped('product_id.categ_id')
            cats = {}
            for cat in loc_cat_ids:
                cat_quant_ids = loc_quant_ids.filtered(lambda r:r.product_id.categ_id == cat)
                cat_qty = sum(cat_quant_ids.mapped('qty'))
                cat_cost = sum([l.product_id.standard_price * l.qty for l in cat_quant_ids])
                cat_lst_price = sum([l.product_id.lst_price * l.qty for l in cat_quant_ids])
                cats[cat.name] = {
                    'qty':cat_qty,
                    'cost':cat_cost,
                    'sale':cat_lst_price,
                    'quants': cat_quant_ids
                }
            locations [loc.name] = {
                'qty':location_qty,
                'cost':location_cost,
                'sale':location_lst_price,
                'cats':cats
            }
    
        main_heading = workbook.add_format({
            "bold": 1, 
            "border": 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color":'black',
            "bg_color": '#D3D3D3',
            'font_size': '10',
            })

        main_heading1 = workbook.add_format({
            "bold": 1, 
            "border": 1,
            "align": 'left',
            "valign": 'vcenter',
            "font_color":'black',
            "bg_color": '#D3D3D3',
            'font_size': '16',
            })

        main_heading2 = workbook.add_format({
            "bold": 1, 
            "border": 1,
            "align": 'left',
            "valign": 'vcenter',
            "font_color":'black',
            'font_size': '14',
            })

        main_heading3 = workbook.add_format({
            "bold": 1, 
            "border": 1,
            "align": 'left',
            "valign": 'vcenter',
            "font_color":'black',
            'font_size': '12',
            })

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '13',
            "font_color":'black',
            'bg_color': '#D3D3D3'})

        main_data = workbook.add_format({
            "align": 'center',
            "valign": 'vcenter',
            'font_size': '14',
            })
         
        merge_format.set_shrink()
        main_heading.set_text_justlast(1)
        main_data.set_border()
        worksheet = workbook.add_worksheet('Product Stock Report -  ')
        worksheet.set_column(0, 3, 50)
        worksheet.merge_range('A1:F1','Product Stock Report',merge_format)
        worksheet.write('A4', 'Locations/Categories', main_heading1)
        worksheet.write('B4',  'Quantity', main_heading1)
        worksheet.write('C4', 'Cost Price', main_heading1)
        worksheet.write('D4',  'Sale Price', main_heading1)

        row = 4
        col = 0
        total_qty = 0
        toal_cost = 0
        total_sale = 0
        for key, val in locations.items():
            col = 0
            worksheet.write_string (row, col,str(key), main_heading2)
            loc_qty = val.get('qty')
            total_qty+=loc_qty
            worksheet.write_number (row, col+1,loc_qty ,main_data)
            loc_cost = val.get('cost')
            toal_cost += loc_cost
            worksheet.write_number (row, col+2, loc_cost,main_data)
            loc_sale = val.get('sale')
            total_sale  += loc_sale
            worksheet.write_number (row, col+3, loc_sale,main_data)
            row+=1
            for k, v in val.get('cats').items():
                col = 0
                worksheet.write_string (row, col,"      "+str(k), main_heading2)
                worksheet.write_number (row, col+1,v.get('qty') ,main_data)
                worksheet.write_number (row, col+2,v.get('cost') ,main_data)
                worksheet.write_number (row, col+3,v.get('sale') ,main_data)
                row+=1
                #for quant in v.get('quants'):
                    #col = 0
                    #worksheet.write_string (row, col,"               "+str(quant.product_id.name), main_heading3)
                    #qqty = quant.qty
                    #worksheet.write_number (row, col+1,qqty ,main_data)
                    #worksheet.write_number (row, col+2,quant.product_id.standard_price * qqty ,main_data)
                    #worksheet.write_number (row, col+3,quant.product_id.lst_price * qqty ,main_data)
                    #row+=1
        col=0
        row+=1
        worksheet.write_string (row, col,str('Total'), main_heading1)
        worksheet.write_number (row, col+1,total_qty ,main_heading1)
        worksheet.write_number (row, col+2, toal_cost,main_heading1)
        worksheet.write_number (row, col+3, total_sale,main_heading1)


ProductStockReportXls('report.product_stock_report.product_stock_xls_temp',
            'product.stock.wiz')

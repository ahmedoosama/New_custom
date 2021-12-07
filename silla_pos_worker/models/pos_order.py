from odoo import models, fields, api, _ 

class POSOrder(models.Model):
	_inherit = 'pos.order'

	worker_id = fields.Many2one('hr.employee', string='Worker',)

	@api.model
	def create_from_ui(self, orders):	
		order_ids = super(POSOrder, self).create_from_ui(orders)
		for order in orders:
			if order['data']['worker_id'] > 0:
				for worker in self.env['hr.employee'].search([('id', '=',order['data']['worker_id'])]):
					for created_order in self.env['pos.order'].search([('pos_reference','=',order['data']['name'])]):
						created_order.worker_id = worker.id			
		return order_ids
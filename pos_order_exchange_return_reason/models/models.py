# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning

class PosOrder(models.Model):
	_inherit = 'pos.order'

	exchange_return_reason = fields.Selection([
		('color', 'Color'),
		('size', 'Size'),
		('fabric', 'Fabric'),
		('price', 'Price'),
		('others', 'Others')], 'Exchange/Return Reason', readonly=True)

	@api.model
	def _order_fields(self, ui_order):
		vals = super(PosOrder, self)._order_fields(ui_order)
		vals.update({
			'exchange_return_reason': ui_order.get('exchange_return_reason', False)
		})
		return vals
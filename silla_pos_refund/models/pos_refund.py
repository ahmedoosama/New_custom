from odoo import models, fields, api, _ 

class POSRefund(models.TransientModel):

	_name = 'refund.wizard'

	name = fields.Char(sting='Search')
	order_ids = fields.Many2many('pos.order',string='Orders')





	@api.onchange('name')
	def onchange_name(self):
		print '\n\n\n\n'
		ids_list = []	
		if self.name : 
			for order in self.env['pos.order'].search([('pos_reference','ilike',self.name)]):
				print 'NAAAAAAAAAME = ', order.name
				ids_list.append(order.id)
			self.order_ids = [(6 , 0 , ids_list)]

		print '\n\n\n\n'
		print '############ onchange name clicked'
		print '\n\n\n\n'


class POSOrder(models.Model):

	_inherit = 'pos.order'


	@api.multi
	def do_refund(self):
		"""Create a copy of order  for refund order"""
		PosOrder = self.env['pos.order']
		current_session = self.env['pos.session'].search([('state', '!=', 'closed'), ('user_id', '=', self.env.uid)], limit=1)
		if not current_session:
			raise UserError(_('To return product(s), you need to open a session that will be used to register the refund.'))
		for order in self:
			clone = order.copy({
				# ot used, name forced by create
				'name': order.name + _(' REFUND'),
				'session_id': current_session.id,
				'date_order': fields.Datetime.now(),
				'pos_reference': order.pos_reference,
				'is_return_order' : True,
			})
			PosOrder += clone

		for clone in PosOrder:
			for order_line in clone.lines:
				order_line.write({'qty': -order_line.qty})
		return {
			'name': _('Return Products'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'pos.order',
			'res_id': PosOrder.ids[0],
			'view_id': False,
			'context': self.env.context,
			'type': 'ir.actions.act_window',
			'target': 'current',
		}


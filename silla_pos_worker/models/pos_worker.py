from odoo import models, fields, api, _ 

class Worker(models.Model):
	_inherit = 'hr.employee'

	is_pos_worker = fields.Boolean(default=False,string='Is He a Worker In POS ?')
	worker_id = fields.Char(string="Worker ID")

	@api.model
	def create(self, vals):
		if not vals.get('worker_id'):
			vals['worker_id'] = self.env['ir.sequence'].next_by_code('worker.id') or '/'
		return super(Worker,self).create(vals)

	@api.multi
	def write(self, vals):
		if vals.get('worker_id'):
			vals['worker_id'] = vals.get('worker_id')
		else:
			vals['worker_id'] = self.env['ir.sequence'].next_by_code('worker.id') or '/'
		return super(Worker,self).write(vals)

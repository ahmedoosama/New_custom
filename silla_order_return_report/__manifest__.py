# -*- coding: utf-8 -*-
##############################################################################
#
#    
#    
#    Author: Alargm Ahmed Ibrahim
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    You can publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Silla Order Return Report',
    'version': '1.0',
    'category': 'Silla',
    'author': 'Alargm Ahmed Ibrahim',
    'depends': ['pos_order_return','silla_pos_worker'],
    'website': 'http://www.sillatech.net',
    'data': ['views/order_return_report.xml', 'security/ir.model.access.csv'],
    'qweb': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence' : 0,
}

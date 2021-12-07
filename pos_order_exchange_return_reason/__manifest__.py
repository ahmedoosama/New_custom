# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Exchange Return Reason",
  "summary"              :  "This module enforces exchange/return reason.",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Sillatech",
  "license"              :  "Other proprietary",
  "website"              :  "www.silla.net",
  "description"          :  """This module enforces exchange/return reason.""",
  "depends"              :  ['pos_product_exchange'],
  "data"                 :  [
                             'views/template.xml',
                             'views/pos_order_view.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_order_exchange_return_reason.xml'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  50,
  "currency"             :  "USD",
}

/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_order_exchange_return_reason.pos_exchange_return_reason', function (require) {
"use strict";
	console.log("in file11");
	// var pos_orders = require('pos_orders.pos_orders');
	var core = require('web.core');
	// var gui = require('point_of_sale.gui');
	var screens = require('point_of_sale.screens');
	var models = require('point_of_sale.models');
	// var PopupWidget = require('point_of_sale.popups');
	var _t = core._t;
	// var SuperOrder = models.Order;
	// var SuperPosOrder =  pos_orders.prototype;
	var SuperPaymentScreen = screens.PaymentScreenWidget.prototype;
	var OrderSuper = models.Order;
	screens.PaymentScreenWidget.include({
		events : _.extend({}, SuperPaymentScreen.events, {
            'change #exchange_return_reason': 'set_exchange_return_reason'
		}),
		init: function(parent) {
            return this._super(parent);
        },
		set_exchange_return_reason: function(){
			var order = this.pos.get_order();
			order.exchange_return_reason = $("#exchange_return_reason").val();
		},
		
        order_is_valid: function(force_validation) {
            var self =  this;
            var res = self._super(force_validation);
            var order = self.pos.get_order();
            if ((order.is_exchange_order || order.is_return_order) && order.exchange_return_reason == ""){
				self.$("#exchange_return_reason").addClass("wk-error")
					this.gui.show_popup('error',{
						'title': _t('Empty Exchange/Return/Refund Reason'),
						'body':  _t('TPlease Select Exchange/Return/Refund Reason!'),
					});
                return false;
                
            }
            else{
                return res;
            }
            
        }
    });

	models.Order = models.Order.extend({

        initialize: function(attributes,options){
            this.exchange_return_reason = "";
            // this.worker_id = $("#worker-select").value;

            return OrderSuper.prototype.initialize.call(this, attributes,options);;
        },
        export_as_JSON: function () {
            var self = OrderSuper.prototype.export_as_JSON.call(this);
			// self.coupon = this.coupon;
            self.exchange_return_reason = this.exchange_return_reason
            return self;
		},
        init_from_JSON: function(json) {
            self.exchange_return_reason = this.exchange_return_reason
            this.exchange_return_reason = json.exchange_return_reason;
            // this.coupon = json.coupon;
            // this.coupon_status = json.coupon_status;
            OrderSuper.prototype.init_from_JSON.call(this, json);

        },
    });


	
});

odoo.define("silla_pos_workers.workers", function (require) {
    "use strict";
    var core = require('web.core');
    var pos_screen = require('point_of_sale.screens');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var pos_model = require('point_of_sale.models');
    var pos_popup = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var models = pos_model.PosModel.prototype.models;
    var SuperPaymentScreenWidget = pos_screen.PaymentScreenWidget;
    var PosModelSuper = pos_model.PosModel;
    var OrderSuper = pos_model.Order;
    var Model = require('web.DataModel');
    var core = require('web.core');
    var _t = core._t;
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var pos_orders = require('pos_orders.pos_orders');


    models.push(
        {
            model: 'hr.employee',
            fields: ['id', 'name','worker_id'],
            loaded: function (self, workers) {
                self.workers = workers;
                self.db.workers_by_worker_id = {}
                _.each(workers, function(data) {
                    if(data.worker_id)
                        self.db.workers_by_worker_id[data.worker_id] = data;
                });
            }

        });

    pos_screen.PaymentScreenWidget.include({

        events:_.extend({},SuperPaymentScreenWidget.prototype.events,{
            'click #worker_id': 'clicked_show',
            'blur #worker_id':  'worker_focus_out'
        }),
        show_validate:function(){
            this.$('.button.next').css('visibility', 'visible');
        },

        hide_validate:function(){
            this.$('.button.next').css('visibility', 'hidden');
        },

        renderElement: function(){
            this._super();
            var self = this;
            this.workers = new WorkerWidget(this,{});
            this.workers.replace(this.$('.placeholder-WorkerWidget'));
            if(self.pos.get_order().worker_id && self.pos.get_order().worker_id == -1){
                self.$('.button.next').css('visibility', 'hidden');
            }
        },

        clicked_show: function(){
            var self = this;
            window.document.body.removeEventListener('keypress',self.keyboard_handler);
            window.document.body.removeEventListener('keydown',self.keyboard_keydown_handler);
        },

        worker_focus_out:function(){
            var self = this;
            window.document.body.addEventListener('keypress',self.keyboard_handler);
            window.document.body.addEventListener('keydown',self.keyboard_keydown_handler);
        },
        order_is_valid: function(force_validation) {
            var self =  this;
            var res = self._super(force_validation);
            var order = self.pos.get_order();
            if (order.worker_id == -1){
                self.$("#worker_id").addClass("wk-error")
                return false;
                
            }
            else{
                return res;
            }
            
        }
    });


    var WorkerWidget = PosBaseWidget.extend({
        template:'WorkerWidget',
        events:{
            'keypress #worker_id': 'add_worker_id',
            'focus #worker_id' : 'worker_id_focus',
            'click .correct_worker': 'correct_worker'
        },


        init: function(parent) {
            return this._super(parent);
        },

        renderElement: function () {
            var self = this;
            this._super();
            console.log('bfore ');
            var current_order = self.pos.get_order();
            console.log(current_order);
            if(current_order != null && current_order.is_return_order){
                var loaded = self.fetch('pos.order',['name','id','worker_id'],[['id','=', current_order.return_order_id]])
                .then(function(orders){
                    for(var i = 0, len = orders.length; i < len; i++){
                        current_order.set_worker_id(parseInt(orders[i].worker_id[0])) ;
                        current_order.set_all_workers(self.all_workers);
                        current_order.export_as_JSON();
                        var worker_name = orders[i].worker_id[1]
                        var worker = self.pos.get_order().worker_id;
                        var direction = $("#direction-select").val();
                        var customer = $("#customer-select").val();
                        self.$('#worker-footer').replaceWith('<div id="worker-name">'+worker_name+'</div>')
                        if(self.pos && self.pos.chrome && self.pos.chrome.screens && self.pos.chrome.screens.payment){
                            if(direction == undefined && customer == undefined  && worker && worker != -1   )
                                self.pos.chrome.screens.payment.show_validate()
                            else
                                self.pos.chrome.screens.payment.hide_validate()
                        }
                    }//end of for
                });
            }
        },

        correct_worker:function(){
            var self = this
          this.renderElement();
          if(self.pos && self.pos.chrome && self.pos.chrome.screens && self.pos.chrome.screens.payment)
            this.pos.chrome.screens.payment.hide_validate()
          this.pos.get_order().worker_id = -1;
        },

        worker_id_focus: function(){
            this.$('#worker_id').removeClass('wk-error')
        },

        check_worker_value: function(){

            var worker = this.pos.get_order().worker_id;
            var direction = $("#direction-select").val();
            var customer = $("#customer-select").val();
            if(direction && customer && worker && worker != -1)
                this.pos.chrome.screens.payment.show_validate()
            else if(direction == undefined && customer == undefined && worker && worker != -1)
                this.pos.chrome.screens.payment.show_validate()
            else
                this.pos.chrome.screens.payment.hide_validate()
        },

        add_worker_id: function(ev){
            var self = this
            if(ev.which == 13){
                var worker_id = self.$('#worker_id').val()
                if(worker_id in self.pos.db.workers_by_worker_id){
                        var id = self.pos.db.workers_by_worker_id[worker_id].id;
                        var worker_name = self.pos.db.workers_by_worker_id[ worker_id].name
                        self.$('#worker-footer').replaceWith('<div id="worker-name" style="margin-top: 13px;">'+worker_name+'</div>')
                        var order = self.pos.get_order();
                        order.set_worker_id(parseInt(id)) ;
                        order.set_all_workers(self.all_workers);
                        order.export_as_JSON();
                        if(self.pos && self.pos.chrome && self.pos.chrome.screens && self.pos.chrome.screens.payment)
                            self.check_worker_value();
                        self.$('.correct_worker').show()
                    }
                else{
                    self.$("#worker_id").addClass("wk-error")
                }
            }
        },

        fetch: function(model, fields, domain){
            return new Model(model).query(fields).filter(domain).all()
        },

        get_workers: function(config_id){
            var self = this;
            self.all_workers = [];

            var loaded = self.fetch('hr.employee',['name','id'],[['is_pos_worker','=', true]])
                .then(function(workers){
                     for(var i = 0, len = workers.length; i < len; i++){
                        self.all_workers[workers[i].id] = workers[i].name;
                     }
                });
        },
    });


    pos_screen.ProductScreenWidget.include({
        start: function(){
            this._super();
            this.workers = new WorkerWidget(this,{});
            this.workers.replace(this.$('.placeholder-WorkerWidget'));
        }
    });

    pos_model.PosModel = pos_model.PosModel.extend({
        initialize: function(session, attributes) {
            PosModelSuper.prototype.initialize.call(this, session, attributes)
            // this.vouchers = [''];
            this.workers = [];
            this.all_workers = {};
            // this.applied_coupon = [];
        },
        _flush_orders: function(orders, options){
            var result = PosModelSuper.prototype._flush_orders.call(this, orders, options)
            $('.receipt-screen.screen span.button.next').show();
            return result
        }

    });


    pos_model.Order = pos_model.Order.extend({

        initialize: function(attributes,options){
            this.worker_id = -1;
            this.all_workers = {};
            // this.worker_id = $("#worker-select").value;

            return OrderSuper.prototype.initialize.call(this, attributes,options);;
        },

        set_worker_id: function (id) {
            this.worker_id = id;
            return;
        },

        set_all_workers(workers){
            this.all_workers = workers;
            return;
        },

        export_as_JSON: function () {
            var self = OrderSuper.prototype.export_as_JSON.call(this);
            // self.coupon = this.coupon;
            self.worker_id = this.worker_id
            return self;
        },

        init_from_JSON: function(json) {
            this.worker_id = json.worker_id;
            // this.coupon = json.coupon;
            // this.coupon_status = json.coupon_status;
            OrderSuper.prototype.init_from_JSON.call(this, json);

        },
    });


});

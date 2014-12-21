"use strict";

define(['underscore', 'jquery', 'backbone', 'config', 'models','templates'],
    function(_, $, Backbone, Config, Models, Templates) {
        var Views = {};

        Views.Toolbar = Backbone.View.extend({
            home: true,
            logout: true,
            refresh: false,
            refresh_watch: false,
            save: false,
            save_warn: false,
            help: false,
            events: {
                "click #home_button": "onHome",
                "click #logout_button": "onLogout",
                "mousedown #refresh_button": "onMouseDownRefresh",
                "contextmenu #refresh_button": function() { return false; },
                "click #save_button": "onSave",
                "click #help_button": "onHelp"
            },
            onHome: function () {
                window.location.href = Config.uri.home;
            },
            onLogout: function () {
                window.location.href = Config.uri.logout;
            },
            onMouseDownRefresh: function (ev) {
                if (ev.which == 1) {
                    this.onRefresh(ev);
                } else if (ev.which == 3) {
                    this.onWatch(ev);
                }
            },
            onRefresh: function () {
                throw "No onRefresh applied to this toolbar.";
            },
            onWatch: function () {
                throw "No onWatch applied to this toolbar.";
            },
            onSave: function () {
                throw "No onSave applied to this toolbar.";
            },
            onHelp: function () {
                throw "No onHelp applied to this toolbar.";
            },
            render: function () {
                this.$el.html(Templates.Toolbar(this));
            }
        });

        Views.Locations = Backbone.View.extend({
            /* Locations manager view. */
            id: "locations",
            events: {
                "click .field": "onClickRow",
                "click .field > *": function () { return false }, // Do not bubble click event up.
            },
            watchInterval: 5000,
            selectedRow: null,
            selectedCol: null,
            changed: false,
            onClickRow: function(ev) {
                /* Simply select a row and update the row with the
                "info" class.
                */
                var cell = $(ev.target),
                    row = cell.parent(),
                    data_field = cell.attr("data-field"),
                    col;

                if (this.selectedRow) {
                    this.selectedRow.removeClass("info");
                }

                if (this.selectedCol) {
                    this.selectedCol.removeClass("active");
                }

                if (data_field && data_field.startsWith("day_quantity")) {
                    this.selectedCol = $(".col_day_quantity[data-field='"+data_field+"']");
                    this.selectedCol.addClass("active");
                }

                row.addClass("info");
                this.selectedRow = row;

                return false;
            },
            // Abstract this to Toolbar view.
            onRefresh: function (ev) {
                this.locationsModel.fetch({reset: true});
                this.daysModel.fetch({reset: true});
            },
            render: function() {
                this.selectedRow = null;
                this.$el.html(Templates.Locations(this));
                $(window).unbind('beforeunload');
                this.changed = false;
                this.toolBarView.setElement($("#toolbar"));
                this.toolBarView.render();
                return this;
            },
            conditionalRender: function () {
                if (this.locationsModel.length > 0 &&
                        this.daysModel.length > 0) {
                    this.render();
                }
            },
            initialize: function() {
                var self = this;

                this.toolBarView = new Views.Toolbar();
                this.toolBarView.refresh = true;
                this.toolBarView.onRefresh = function () {
                    self.onRefresh.apply(self, arguments);
                }
                this.toolBarView.onWatch = function () {
                    self.onWatch.apply(self, arguments);
                };

                this.locationsModel = new Models.Locations();
                this.daysModel = new Models.Days();

                this.listenTo(this.locationsModel, "add remove reset sync",
                              _.debounce(this.render));

                this.locationsModel.fetch();
                this.daysModel.fetch();
            },
            onWatch: function () {
                if (!this.watchTimer) {
                    this.watch();
                } else {
                    this.unwatch();
                }
            },
            watch: function () {
                var self = this;
                function poll () {
                    self.onRefresh.apply(self, arguments);
                }
                this.watchTimer = setInterval(poll, this.watchInterval);
                //poll();
                this.toolBarView.refresh_watch = true;
                this.toolBarView.render();
            },
            unwatch: function () {
                clearTimeout(this.watchTimer);
                this.watchTimer = null;
                this.toolBarView.refresh_watch = false;
                this.toolBarView.render();
            }
        });

        Views.LocationsManage = Views.Locations.extend({
            events: {
                "click .field": "onClickRow",
                "click .field > *": function () { return false }, // Do not bubble click event up.
                "dblclick .editable.field": "onDblClick",
                "dblclick .field > *": function() { return false; }, // Do not bubble dblclick event up.
                "focusout input.form-control": "onLeaveField",
                "keyup input.form-control": "keyupInField"
            },
            render: function () {
                Views.Locations.prototype.render.apply(this, arguments);
                if (this.editWatchTimer) {
                    this.editWatchTimer = null;
                    this.watch();
                }
            },
            // Abstract to the toolbar View.
            onRefresh: function (ev) {
                var doSave = true;
                if (this.changed) {
                    doSave = confirm("There are unsaved changed. Are you sure you want to reload data?");
                }
                if (doSave) {
                    this.locationsModel.fetch({reset: true});
                    this.daysModel.fetch({reset: true});
                }
            },
            // Abstract to the toolbar View.
            onSave: function (ev) {
                this.locationsModel.each(function (location) {
                    if (location.hasChanged() || location.get("day_quantities").find(
                                                    function (day_quantity) {
                                                        return day_quantity.hasChanged("amount");
                                                    })) {
                        location.save();
                    }
                });
                this.toolBarView.save_warn = false;
            },
            onDblClick: function (ev) {
                // Edit the cell.
                var cell = $(ev.target),
                    row = cell.parent(),
                    location_id = row.attr("data-location-id");

                if (cell.hasClass("field_capacity") ||
                    cell.hasClass("field_display_name") ||
                    cell.hasClass("field_day_quantity")) {
                    this.editingCell = cell.html();
                    var input = $('<input class="form-control" value="'+cell.html()+'" type="text" />');
                    cell.html(input);

                    if (this.watchTimer) {
                        this.editWatchTimer = this.watchTimer;
                        this.unwatch();
                    }
                }

                input.focus();
                input.select();
                return false;
            },
            keyupInField: function (ev) {
                if (ev.which == 13) {
                    $(ev.target).blur();
                    ev.preventDefault();
                }
            },
            onLeaveField: function (ev) {
                var field = $(ev.target),
                    value = field.val(),
                    cell = field.parent(),
                    row = cell.parent(),
                    field_name = cell.attr("data-field"),
                    location_id = row.attr("data-location-id"),
                    location = this.locationsModel.get(location_id),
                    model;

                if (field_name === "capacity" || field_name === "display_name") {
                    // Updating Location Model.
                    model = location.castSet(field_name, value,
                                             {validate:true});
                    value = model.get(field_name);
                } else if (field_name === "day_quantity") {
                    // Updating LocationDayQuantity Model.
                    model = location.setDayQuantity(cell.attr("data-field-date"), value,
                                                    {validate:true});
                    value = model.get("amount");
                }

                if (model.validationError) {
                    cell.addClass("danger");
                    $("#form_error").html(model.validationError);
                    setTimeout(function () {
                        $("#form_error").html("&nbsp;");
                        cell.removeClass("danger");
                    }, 3000);
                } else if (model.hasChanged()) {
                    row.removeClass("info");
                    this.selectedRow = null;
                    cell.addClass("success");
                    $(window).bind('beforeunload', function(){
                        return 'You have unsaved changes.';
                    });
                    this.changed = true;

                    //$("#save_button").addClass("btn-warning");
                    this.toolBarView.save_warn = true;
                    this.toolBarView.render();

                    $("#form_warning").html("Form is unsaved.");
                }

                cell.html(value);
            },
            onHelp: function () {
            },
            initialize: function () {
                var self = this;
                Views.Locations.prototype.initialize.apply(this, arguments)
                this.toolBarView.edit = false;
                this.toolBarView.locations = true;
                this.toolBarView.save = true;
                this.toolBarView.onSave = function () {
                    self.onSave.apply(self, arguments);
                }
                //this.toolBarView.help = true;
            }
        });

        return Views;
    }
);
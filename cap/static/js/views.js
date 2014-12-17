"use strict";

define(['underscore', 'jquery', 'backbone', 'models','templates'],
    function(_, $, Backbone, Models, Templates) {
        var Views = {};

        Views.Toolbar = Backbone.View.extend({
            home: true,
            locations: false,
            logout: true,
            refresh: false,
            edit: false,
            save: false,
            help: false,
            events: {
                "click #home_button": "onHome",
                "click #locations_button": "onLocations",
                "click #logout_button": "onLogout",
                "click #refresh_button": "onRefresh",
                "click #edit_button": "onEdit",
                "click #save_button": "onSave",
                "click #help_button": "onHelp"
            },
            onHome: function () {
                window.location.href = "/";
            },
            onLocations: function () {
                window.location.href = "/locations"
            },
            onLogout: function () {
                window.location.href = "/logout";
            },
            onRefresh: function () {
                throw "No onRefresh applied to this toolbar.";
            },
            onEdit: function () {
                throw "No onEdit applied to this toolbar.";
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
            selectedRow: null,
            selectedCol: null,
            changed: false,
            manage: false,
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
                this.toolBarView.edit = true;
                this.toolBarView.onRefresh = function () {
                    self.onRefresh.apply(self, arguments);
                }
                this.toolBarView.onEdit = function () {
                    window.location.href = "/locations/edit";
                }

                this.locationsModel = new Models.Locations();
                this.daysModel = new Models.Days();

                this.listenTo(this.locationsModel, "add remove reset sync",
                              _.debounce(this.render));
                this.listenTo(this.daysModel, "add remove reset",
                              _.debounce(this.render));

                this.locationsModel.fetch();
                this.daysModel.fetch();
            },
            watch: function () {
                setInterval(this.onRefresh, 5000);
                this.onRefresh();
            }
        });

        Views.LocationsManage = Views.Locations.extend({
            manage: true,
            events: {
                "click .field": "onClickRow",
                "click .field > *": function () { return false }, // Do not bubble click event up.
                "dblclick .field": "onDblClick",
                "dblclick .field > *": function() { return false; }, // Do not bubble dblclick event up.
                "focusout input.form-control": "onLeaveField"
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
            },
            onDblClick: function (ev) {
                /* Edit the cell.
                */
                var cell = $(ev.target),
                    row = cell.parent(),
                    location_id = row.attr("data-location-id");

                if (cell.hasClass("field_capacity") ||
                    cell.hasClass("field_display_name") ||
                    cell.hasClass("field_day_quantity")) {
                    this.editingCell = cell.html();
                    var input = $('<input class="form-control" value="'+cell.html()+'" type="text" />');
                    cell.html(input);
                }

                input.focus();
                input.select();
                return false;
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
                    $("#save_button").addClass("btn-warning");
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

        Views.Location = Backbone.View.extend({
            id: "location",
            render: function() {
                this.$el.html(Templates.Location(this));
            },
            initialize: function(attrs, options) {
                this.date = attrs.date;
                this.locationModel = new Models.Location({id: attrs.locationId});
                this.listenTo(this.locationModel, "add remove reset sync",
                              _.debounce(this.render));
            },
            onRefresh: function () {
                this.locationModel.fetch({reset: true});
            },
            watch: function () {
                var self = this;
                function poll() {
                    self.onRefresh();
                }
                setInterval(poll, 5000);
                poll();
            }
        });

        Views.LocationsShortlist = Backbone.View.extend({
            id: "locations_short_list",
            render: function() {
                this.$el.html(Templates.LocationsShortlist(this));
            },
            initialize: function() {
                this.locationsShortlistModel = new Models.Locations();
                this.listenTo(this.locationsShortlistModel, "add remove reset",
                              _.debounce(this.render));
                this.locationsShortlistModel.fetch({data: 'list'});
            }
        });

        return Views;
    }
);
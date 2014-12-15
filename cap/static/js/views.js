"use strict";

define(['underscore', 'jquery', 'backbone', 'models','templates'],
    function(_, $, Backbone, Models, Templates) {
        var Views = {};

        Views.Locations = Backbone.View.extend({
            /* Locations manager view.
            */
            id: "locations",
            admin: true,
            events: {
                "click .field": "onClickRow",
                "click .field > *": function () { return false }, // Do not bubble click event up.
                "dblclick .field": "onDblClick",
                "dblclick .field > *": function() { return false; }, // Do not bubble dblclick event up.
                "click #refresh_button": "onRefresh",
                "click #save_button": "onSave",
                "focusout input.form-control": "onLeaveField"
            },
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
            render: function() {
                this.selectedRow = null;
                this.$el.html(Templates.Locations(this));
                $(window).unbind('beforeunload');
                this.changed = false;
                return this;
            },
            conditionalRender: function () {
                if (this.locationsModel.length > 0 &&
                        this.daysModel.length > 0) {
                    this.render();
                }
            },
            initialize: function() {
                this.locationsModel = new Models.Locations();
                this.daysModel = new Models.Days();

                this.listenTo(this.locationsModel, "add remove reset sync",
                              _.debounce(this.render));
                this.listenTo(this.daysModel, "add remove reset",
                              _.debounce(this.render));

                this.locationsModel.fetch();
                this.daysModel.fetch();
            }
        });

        return Views;
    }
);
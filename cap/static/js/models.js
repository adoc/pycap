"use strict";

define(['backbone'],
    function(Backbone) {
        var Models = {};

        /* Location Day Quantity. */
        Models.LocationDayQuantity = Backbone.Model.extend({});

        /* Collection of Location Day Quantity objects. */
        Models.LocationDayQuantities = Backbone.Collection.extend({
            model: Models.LocationDayQuantity
        });

        /* Location Model. */
        Models.Location = Backbone.Model.extend({
            urlRoot: "/api/v1/locations",
            /* Overloaded Backbone.Model.set function */
            castSet: function (key, val, options) {

                if (key === "capacity") {
                    val = parseInt(val);
                } else if (key.startsWith("day_quantity") === true) {
                    val = parseInt(val);
                }

                Backbone.Model.prototype.set.call(this, key, val, options);
            },
            validate: function (attrs, options) {
                for (var key in attrs) {
                    var val = attrs[key];
                    if (key === "capacity" && isNaN(val) === true) {
                        return "Capacity must be a number";
                    } else if (key === "display_name" && val.length <= 3 && val.length > 32) {
                        return "Display name length must be greater than 3 characters and less than 33.";
                    } else if (key.startsWith("day_quantity") === true && isNaN(val) === true) {
                        return "Location quantity must be a number";
                    }
                }
            },
            constructor: function (attrs, options) {

                if (attrs.hasOwnProperty("day_quantities")) {
                    for (var i in attrs["day_quantities"]) {
                        if (!(attrs["day_quantities"][i] instanceof Backbone.Model)) {
                            attrs["day_quantities"][i] = new Models.LocationDayQuantity(attrs["day_quantities"][i]);
                        }
                    }
                    attrs["day_quantities"] = new Models.LocationDayQuantities(attrs["day_quantities"]);
                } else {
                    attrs["day_quantities"] = new Models.LocationDayQuantities();
                }

                Backbone.Model.call(this, attrs, options);
            }
        });

        /* Collection of Location objects. */
        Models.Locations = Backbone.Collection.extend({
            url: "/api/v1/locations",
            model: Models.Location
        });

        Models.Day = Backbone.Model.extend({});

        Models.Days = Backbone.Collection.extend({
            url: "/api/v1/days",
            model: Models.Day
        });

        return Models;
    }
);
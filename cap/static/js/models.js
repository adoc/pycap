"use strict";

define(['backbone'],
    function(Backbone) {
        var Models = {};

        Models.Location = Backbone.Model.extend({
            urlRoot: "/api/v1/locations",
            castSet: function (key, val, options) {

                if (key === "capacity") {
                    val = parseInt(val);
                } else if (key.startsWith("day_quantity")===true) {
                    val = parseInt(val);
                }

                Backbone.Model.prototype.set.call(this, key, val, options)
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
            }
        });

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
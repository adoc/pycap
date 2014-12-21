"use strict";

define(['backbone', 'config'],
    function(Backbone, Config) {
        var Models = {};

        /* Location Day Quantity. */
        Models.LocationDayQuantity = Backbone.Model.extend({
            defaults: {
                amount: -1
            },
            castSet: function (key, val, options) {
                if (key === "amount") {
                    val = parseInt(val);
                }
                Backbone.Model.prototype.set.call(this, key, val, options);
                return this;
            },
            validate: function (attrs, options) {
                var key, val;
                for (key in attrs) {
                    val = attrs[key];
                    if (key === "date" && typeof val !== "string") {
                        return "Date must be a string.";
                    } else if (key === "date" && val.length < 6 || val.length > 10) {
                        return "Date appears malformed.";
                    } else if (key === "amount" && val < 0) {
                        return "Location quantity must not be less than 0";
                    } else if (key === "amount" && isNaN(val)) {
                        return "Location quantity must be a number";
                    }
                }
            },
        });

        /* Collection of Location Day Quantity objects. */
        Models.LocationDayQuantities = Backbone.Collection.extend({
            model: Models.LocationDayQuantity
        });

        /* Location Model. */
        Models.Location = Backbone.Model.extend({
            urlRoot: Config.uri.api.locations,
            castSet: function (key, val, options) {
                if (key === "capacity") {
                    val = parseInt(val);
                }
                Backbone.Model.prototype.set.call(this, key, val, options);
                return this;
            },
            setDayQuantity: function (date, amount, options) {
                return this.getDayQuantity(date, options).castSet("amount", amount, options);
            },
            /* Return the LocationDayQuantity record by date.
            If that record doesn't exist, add it to the collection. */
            getDayQuantity: function (date, options) {
                var day_quantities = this.get("day_quantities"),
                    day_quantity = day_quantities.find(
                        function(day_quantity) {
                            return day_quantity.get("date") == date;
                        }) || new Models.LocationDayQuantity({date: date});
                return day_quantities.add(day_quantity);
            },
            validate: function (attrs, options) {
                for (var key in attrs) {
                    var val = attrs[key];
                    if (key === "capacity" && isNaN(val)) {
                        return "Location capacity must be a number";
                    } else if (key ==="capacity" && val < 0) {
                        return "Location capacity must be 0 or greater."
                    } else if (key === "display_name" && val.length <= 3 || val.length > 32) {
                        return "Display name length must be greater than 3 characters and less than 33.";
                    }
                }
            },
            constructor: function (attrs, options) {
                attrs || (attrs = {});
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
            url: Config.uri.api.locations,
            model: Models.Location,
            showCapacity: function () {
                return this.find(function(location) {
                    return location.get("perm_manage") === true;
                }) !== undefined;
            }
        });

        Models.Day = Backbone.Model.extend({});

        Models.Days = Backbone.Collection.extend({
            url: Config.uri.api.days,
            model: Models.Day
        });

        return Models;
    }
);
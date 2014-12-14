"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl"],
    function(_, locationsTemplate) {
        return {
            Locations: _.template(locationsTemplate)
        }
    }
);
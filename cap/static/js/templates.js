"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl",
        "text!/static/tmpl/location.html.tmpl"],
    function(_, locationsTemplate, locationTemplate) {
        /* Pre-render templates */
        return {
            Locations: _.template(locationsTemplate),
            Location: _.template(locationTemplate)
        }
    }
);
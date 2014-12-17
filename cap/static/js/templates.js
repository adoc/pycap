"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl",
        "text!/static/tmpl/location.html.tmpl",
        "text!/static/tmpl/locations_short_list.html.tmpl",
        "text!/static/tmpl/toolbar.html.tmpl"],
    function(_, locationsTemplate,
            locationTemplate,
            locationsShortlistTemplate,
            toolbarTemplate) {
        /* Pre-render templates */
        return {
            Locations: _.template(locationsTemplate),
            Location: _.template(locationTemplate),
            LocationsShortlist: _.template(locationsShortlistTemplate),
            Toolbar: _.template(toolbarTemplate)
        }
    }
);
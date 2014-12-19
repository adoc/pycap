"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl",
        "text!/static/tmpl/locations_short_list.html.tmpl",
        "text!/static/tmpl/toolbar.html.tmpl"],
    function(_, locationsTemplate,
            locationsShortlistTemplate,
            toolbarTemplate) {
        // Pre-render templates
        return {
            Locations: _.template(locationsTemplate),
            Toolbar: _.template(toolbarTemplate)
        }
    }
);
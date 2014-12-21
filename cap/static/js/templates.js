"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl",
        "text!/static/tmpl/toolbar.html.tmpl"],
    function(_,
            locationsTemplate,
            toolbarTemplate) {
        return {
            // Pre-render templates
            Locations: _.template(locationsTemplate),
            Toolbar: _.template(toolbarTemplate)
        }
    }
);
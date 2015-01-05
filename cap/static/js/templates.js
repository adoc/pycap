"use strict";

define(['underscore',
        "text!/static/tmpl/locations.html.tmpl",
        "text!/static/tmpl/users.html.tmpl",
        "text!/static/tmpl/toolbar.html.tmpl"],
    function(_,
            locationsTemplate,
            usersTemplate,
            toolbarTemplate) {
        return {
            // Pre-render templates
            Locations: _.template(locationsTemplate),
            Users: _.template(usersTemplate),
            Toolbar: _.template(toolbarTemplate)
        }
    }
);
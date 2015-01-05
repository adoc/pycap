"use strict";

define(['underscore',
        text_url("tmpl/locations.html.tmpl"),
        text_url("tmpl/users.html.tmpl"),
        text_url("tmpl/toolbar.html.tmpl")],
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
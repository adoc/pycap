"use strict";

define(['underscore',
        "text!"+window.static_uri+"tmpl/locations.html.tmpl",
        "text!"+window.static_uri+"tmpl/users.html.tmpl",
        "text!"+window.static_uri+"tmpl/toolbar.html.tmpl"],
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
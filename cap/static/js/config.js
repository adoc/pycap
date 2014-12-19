"use strict";

define([], function () {
    var Config = {};

    Config.uri = {
        home: "/",
        login: "/login",
        logout: "/logout",
        locations_manage: "/manage",
        api: {
            days: "/api/v1/days",
            locations: "/api/v1/locations"  // RESTful.
        }
    };

    return Config;
});
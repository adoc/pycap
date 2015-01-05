"use strict";

define([], function () {
    var Config = {};

    Config.uri = {
        home: "/",
        login: "/login",
        logout: "/logout",
        api: {
            days: "/api/v1/days",
            locations: "/api/v1/locations",
            users: "/api/v1/users"
        }
    };

    return Config;
});
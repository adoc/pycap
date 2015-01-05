"use strict";

define([], function () {
    var Config = {};

    Config.uri = {
        home: "${request.route_path("home")}",
        users: "${request.route_path("users")}",
        login: "${request.route_path("login")}",
        logout: "${request.route_path("logout")}",
        api: {
            days: "${request.route_path("api_days")}",
            locations: "${request.route_path("api_locations_get")}",
            users: "${request.route_path("api_users_get")}"
        }
    };

    return Config;
});
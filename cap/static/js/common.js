"use strict";

require.config({
    baseUrl: "static/js",
    paths: {
        jquery: 'lib/jquery.min',
        underscore: 'lib/underscore.min',
        backbone: 'lib/backbone.min',
        bootstrap: 'lib/bootstrap.min',
        text: 'lib/text.min'
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }
});

// src: http://stackoverflow.com/a/646643
// Add `startsWith` and `endsWith` to the String prototype.
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function (str){
        return this.slice(-str.length) == str;
    };
}

// src: http://stackoverflow.com/a/1418059
// Add a whitespace strip to the String prototype.
if(typeof(String.prototype.trim) === "undefined") {
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}
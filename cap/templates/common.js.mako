"use strict";

require.config({
    baseUrl: "${request.sstatic_url('static_dir', 'js')}",
    paths: {
        config: "${request.route_path('config.js').rstrip('.js')}",
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

window.text_url = function (path) {
    var base = "${request.sstatic_path('static_dir', '')}";
    return "text!" + path_join(base, path);
}

window.assert = function (condition, message) {
    if (!condition) {
        throw message || "AssertionError";
    }
}

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

function path_join(a) {
    /* Direct port of Python std posixpath.join.
    src: https://hg.python.org/cpython/file/v2.7.3/Lib/posixpath.py:60
    */
    var path = a;
    for(var i=1; i<arguments.length; i++) {
        var b = arguments[i];
        if(b.startsWith('/')) {
            path = b;
        } else if (path == '' || path.endsWith('/')) {
            path = path.concat(b);
        } else {
            path = path.concat('/' + b);
        }
    }
    return path;
}
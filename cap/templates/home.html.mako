<%inherit file="base.html.mako" />
<div id="container" class="container">
</div>
<%def name="title()">
View Locations
</%def>
<%def name="scripts()">
    require(['jquery', 'views'], function($, Views) {
        var view = new Views.Locations();
        $("#container").html(view.$el);

        view.watch();
    });
</%def>
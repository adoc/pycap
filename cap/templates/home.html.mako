<%inherit file="base.html.mako" />
<style>
.btn-group {
    margin-top: 8px;
}
</style>
<div class="container">
    <div id="toolbar" class="btn-group"></div>
    <h3>Individual Locations</h3>
    <div id="locations_short_list"></div>
</div>
<%def name="title()">
View Locations
</%def>
<%def name="scripts()">
    require(['jquery', 'views'], function($, Views) {
        var locations_short_list = new Views.LocationsShortlist();
        $("#locations_short_list").html(locations_short_list.$el);

        var toolbar = new Views.Toolbar();
        toolbar.home = false;
        toolbar.locations = true;
        toolbar.setElement($("#toolbar"));
        toolbar.render();
    });
</%def>
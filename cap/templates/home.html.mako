<%inherit file="base.html.mako" />
<div id="container" class="container">
</div>
<%def name="title()">
Locations
</%def>
<%def name="scripts()">
    require(['jquery', 'views'], function($, Views) {
        var toolBarView = new Views.Toolbar({users: ${perm_admin}}),
            locationsView = new Views.LocationsManage({
                toolBarView: toolBarView});
        $("#container").html(locationsView.$el);
        locationsView.watch();
    });
</%def>
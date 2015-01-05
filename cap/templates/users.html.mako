<%inherit file="base.html.mako" />
<div id="container" class="container">
</div>
<%def name="title()">
Manage Users
</%def>
<%def name="scripts()">
    require(['jquery', 'views'], function($, Views) {
        var toolBarView = new Views.Toolbar({locations: true}),
            usersView = new Views.UsersManage({
                    toolBarView: toolBarView});
        $("#container").html(usersView.$el);
    });
</%def>
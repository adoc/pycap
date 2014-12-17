<%inherit file="base.html.mako" />
<style>
.btn-group {
    margin-top: 8px;
}
</style>
<div class="container">
    <div id="toolbar" class="btn-group"></div>
    <h1>Shop Capacity</h1>
%if error:
    <p class="text-danger">${error}</p>
%elif location:
    <h2><small>${location.display_name} - ${date}</small></h2>
    <div style="margin-top: 64px;" id="container"></div>
%else:
    <p class="text-danger">Internal Server Error</p>
%endif
</div>
<%def name="title()">
    Shop Location Capacity
</%def>
<%def name="scripts()">
%if location:
    require(['jquery', 'views'], function($, Views) {
        var view = new Views.Location({locationId: ${location.id}, date: "${date}"});
        $("#container").html(view.$el);
        view.watch();

        var toolbar = new Views.Toolbar();
        toolbar.home = true;
        toolbar.locations = true;
        toolbar.refresh = true;
        toolbar.onRefresh = function () {
            view.onRefresh.apply(view, arguments);
        }
        toolbar.setElement($("#toolbar"));
        toolbar.render();
    });
%endif
</%def>
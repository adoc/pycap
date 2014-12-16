<%inherit file="base.html.mako" />
<div class="container">
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
    });
%endif
</%def>
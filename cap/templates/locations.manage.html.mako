<%inherit file="base.html.mako" />

<div id="container" class="container">
</div>

<%def name="scripts()">
    <script type="text/javascript">
        require(['jquery', 'views'], function($, Views) {
            var view = new Views.Locations();
            $("#container").html(view.$el);
        });
    </script>
</%def>
<!DOCTYPE html>
<%!
import datetime
%>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Seidner's Shop Capacity App">
        <meta name="author" content="http://github.com/adoc">
        <title>${hasattr(next, 'title') and next.title().strip()+' - ' or ''}SCC Shop Capacity</title>
        <link rel="stylesheet" type="text/css" href="/static/css/lib/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="/static/css/style.css" />
    </head>
    <body>
        ${next.body()}
        <footer class="footer">
            <div class="container">
                <p class="text-muted">&copy; ${datetime.date.today().year} Seidner's Collision Centers.</p>
            </div>
        </footer>
        <script type="text/javascript" src="/static/js/lib/require.min.js"></script>
        <script type="text/javascript" src="/static/js/common.js"></script>
    %if hasattr(next, "scripts"):
        <script type="text/javascript">
            ${next.scripts()}
        </script>
    %endif
    </body>
</html>
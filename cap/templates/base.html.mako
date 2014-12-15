<!DOCTYPE html>
<%!
import datetime
%>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="pyramid web application">
        <meta name="author" content="Pylons Project">
        <link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" />
        <style>
            /* Sticky footer styles
            -------------------------------------------------- */
            html {
              position: relative;
              min-height: 100%;
            }
            body {
              /* Margin bottom by footer height */
              margin-bottom: 80px;
            }
            .footer {
              position: absolute;
              bottom: 0;
              width: 100%;
              /* Set the fixed height of the footer here */
              height: 80px;
              background-color: #f5f5f5;
              padding-top: 16px;
            }
        </style>
    </head>
    <body>
        <div>
            ${next.body()}
        </div>
        <footer class="footer">
            <div class="container">
                <p class="text-muted">&copy; ${datetime.date.today().year} Seidner's Collision Centers.</p>
            </div>
        </footer>
        <script type="text/javascript" src="/static/js/lib/require.min.js"></script>
        <script type="text/javascript" src="/static/js/common.js"></script>
    %if hasattr(next, "scripts"):
        ${next.scripts()}
    %endif
    </body>
</html>
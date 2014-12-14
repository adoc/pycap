<!DOCTYPE html>
<html lang="${request.locale_name}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="pyramid web application">
        <meta name="author" content="Pylons Project">
        <link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" />
    </head>
    <body>
        <div>
            ${next.body()}
        </div>
        <script type="text/javascript" src="/static/js/lib/require.min.js"></script>
        <script type="text/javascript" src="/static/js/common.js"></script>
    %if hasattr(next, "scripts"):
        ${next.scripts()}
    %endif
    </body>
</html>
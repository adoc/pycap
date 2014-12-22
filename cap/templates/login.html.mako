<%inherit file="base.html.mako" />
<div style="height: 200px;"></div>
<div style="width: 300px" class="container">
    %if failed:
    <p class="text-danger">Login failed...</p>
    %endif
    <form method="post" role="form">
        <div class="form-group">
            <label>Login</label>
            <input type="text" name="login" class="form-control" placeholder="Enter user..." />
        </div>
        <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" class="form-control" placeholder="Enter password..." />
        </div>
        <div class="form-group">
            <button type="submit" name="submit" class="btn btn-primary">Submit</button>
        </div>
    </form>
</div>
<%def name="title()">
Login
</%def>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>SimpliSearch: A Simple Search Engine</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://bootswatch.com/simplex/bootstrap.css" media="screen">
  </head>
  <body>


    <div class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a href="#" class="navbar-brand">SimpliSearch</a>
        </div>
        <div class="navbar-collapse collapse" id="navbar-main">
          <ul class="nav navbar-nav navbar-right">
          	%if sgn == 1:
            <li><a href="#" target="_blank">{{u_email}}</a></li>
            %end
            %if sgn == 0:
            <form action="/" method="get">
              <button class="btn btn-default" type="submit" name="sign_in">Login</button>
            </form>
            %elif sgn == 1:
            <form action="/" method="get">
              <button class="btn btn-default" type="submit" name="sign_out">Logout</button>
            </form>
            %end
          </ul>
        </div>
      </div>
    </div>
    <br ><br ><br >
    <div class="container">
      <div class="bs-docs-section clearfix">
        <div class="row">
          <div class="col-lg-12">
            <div class="bs-component">
            </div>
          </div>
        </div>
      </div>


      <form action="/" method="get">
	  <div class="input-group">
	    <span class="input-group-addon">Search</span>
	    <input class="form-control" type="text" name="keywords">
	    <span class="input-group-btn">
	      <button class="btn btn-default" type="submit" value="submit" name="submit">Go</button>
	    </span>
	  </div>
	  </form>

	  %if results:
		<br >
		<div class="col-lg-12">
		    <h4>Results</h4>
		</div>
		<div class="col">
		    <div class="bs-component">
		      <ul class="list-group">
		      	%for keyword in results:
		        <li class="list-group-item"><span class="badge">{{results[keyword]}}</span>{{keyword}}</li>
		        %end
		      </ul>
		    </div>
		</div>
		%end

		%if sgn == 1 and history:
		<br >
		<div class="col-lg-12">
		    <h4>History</h4>
		</div>
		<div class="col">
		    <div class="bs-component">
		      <ul class="list-group">
		      	%for i in history:
		        <li class="list-group-item">{{i}}</li>
		        %end
		      </ul>
		    </div>
		</div>
		%end
<br ><br ><br ><br ><br ><br >
      <footer>
        <div class="row">
          <div class="col-lg-12">
            <ul class="list-unstyled">
              <li class="pull-right"><a href="#top">Back to top</a></li>
            </ul>
            <p>Made by <a href="#">Hossein Haider</a>, and <a href="#">Paul McPhaden</a>.</p>
          </div>
        </div>
      </footer>
    </div>
  </body>
</html>

<form action="/" method="get">
	<input type="text" name="keywords">
	<input type="submit" name="submit" value="submit">
</form>

%if sgn == 0 :
    <form action="/" method="get">
        <input type="submit" name="sign_in" value = "Sign In">
    </form>
    
%elif sgn == 1:
    <strong>{{u_email}}</strong>
    <form action="/" method="get">
        <input type="submit" name="sign_out" value = "Sign Out">
    </form>
%end

<strong>Results:</strong>
<table id="results">
%for result in results:
	<tr>
		<td><a href="{{result[0]}}">{{result[0]}}</a> ( {{result[1]}} )</td>
	</tr>
%end
</table>

%if sgn == 1:
    <strong>History:</strong>
    <table id="history">
    %for i in history:
        <tr>
            <td>{{i}}</td>
        </tr>
    %end
    </table>

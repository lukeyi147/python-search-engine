<script>
/**
 * http://stackoverflow.com/a/10997390/11236
 */
function updateURLParameter(url, param, paramVal){
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}
</script>
<h1><font color="#1645AE">Si</font><font color="#D62408">mp</font><font color="#EFBA00">le</font><font color="#1645AE">Se</font><font color="#007D08">ar</font><font color="#D62408">ch</font></h1>

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
		<td><a href="{{result[0]}}">{{result[0]}}</a></td>
        <td>{{result[1]}}</td>
	</tr>
%end
    <tr>
        <td>&nbsp;</td>
    </tr>
    <tr>
        <td>

        %if has_prev == 1:
        <script>
            var prev = updateURLParameter(window.location.href, 'start', '{{int(start)-int(page_limit)}}');
        </script>
        <a href="javascript:document.location=prev" id="prev">&laquo; previous</a>
        %end 

        %if has_prev == 0:
        &laquo; previous
        %end 

        &nbsp; 

        %if has_next == 1:
        <script>
            var next = updateURLParameter(window.location.href, 'start', '{{int(start)+int(page_limit)}}');
        </script>
        <a href="javascript:document.location=next" id="next">next &raquo;</a>
        %end

        %if has_next == 0:
        next &raquo;
        %end 
        
        </td>
    </tr>
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
%end
function viewProfile() {

	var userEmail = localStorage.getItem("userEmail");

	var ajaxRequest;  // The variable that makes Ajax possible!

	try {
	     // Opera 8.0+, Firefox, Safari
	     ajaxRequest = new XMLHttpRequest();
	 }
	 catch(e) {
	    // Internet Explorer Browsers
	    try{
	    	ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
	    }
	    catch(e) {
	    	try{
	    		ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
	    	}
	    	catch(e) {
	    		alert("Your browser broke!");
	    		return false;
	    	}
	    }
	}
	 
	// Create a function that will receive data 
	// sent from the server and will update
	// div section in the same page.
	ajaxRequest.onreadystatechange = function() {
		if(ajaxRequest.readyState == 4) {
        var textResponse= ajaxRequest.responseText;
	    //alert("Ajax Response: "+ajaxRequest.responseText);

	    if(!(textResponse.indexOf("Error:") > -1))
	    {
	    	//No error. Valid Email Id and Password
	    	//Checking for Customer or Retailer to take them to appropriate dashboards
	    	if(textResponse.indexOf("Retailer")> -1)
	    	{
	    		//Retailer Logged In
	    		window.location.href = "/retailerDashboard";
	    	}
	    	else
	    	{
	    		//Customer Logged In
	    		window.location.href = "/search";
	    	}

	    	localStorage.setItem("userEmail", document.getElementById("Email_Id").value );
	    }
	    else
	    	document.getElementById("pswd_validation").innerHTML= textResponse;
		}
		
	}
	
	var queryString = "Email=" + document.getElementById("Email_Id").value;
	ajaxRequest.open("GET", "/viewUserDetails" + "?" + queryString , true);
	//ajaxRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded;application/json");
	//ajaxRequest.setRequestHeader("dataType","html");
	ajaxRequest.send(null);

	return true;
}

function editProfile() {

	if((document.getElementById("Email_Id").value) == "") {
		document.getElementById("email_validation").innerHTML="Enter email";
		return false;
	} 	
	 
	var p1 = document.getElementById("Password_Valid");	 
	if(p1.value== ""){
		document.getElementById("pswd_validation").innerHTML="Enter Password";
		return false;
	}


	var ajaxRequest;  // The variable that makes Ajax possible!

	try {
	     // Opera 8.0+, Firefox, Safari
	     ajaxRequest = new XMLHttpRequest();
	 }
	 catch(e) {
	    // Internet Explorer Browsers
	    try{
	    	ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
	    }
	    catch(e) {
	    	try{
	    		ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
	    	}
	    	catch(e) {
	    		alert("Your browser broke!");
	    		return false;
	    	}
	    }
	}
	 
	// Create a function that will receive data 
	// sent from the server and will update
	// div section in the same page.
	ajaxRequest.onreadystatechange = function() {
		if(ajaxRequest.readyState == 4) {
        var textResponse= ajaxRequest.responseText;
	    //alert("Ajax Response: "+ajaxRequest.responseText);

	    if(!(textResponse.indexOf("Error:") > -1))
	    {
	    	//No error. Valid Email Id and Password
	    	//Checking for Customer or Retailer to take them to appropriate dashboards
	    	if(textResponse.indexOf("Retailer")> -1)
	    	{
	    		//Retailer Logged In
	    		window.location.href = "/retailerDashboard";
	    	}
	    	else
	    	{
	    		//Customer Logged In
	    		window.location.href = "/search";
	    	}

	    	localStorage.setItem("userEmail", document.getElementById("Email_Id").value );
	    }
	    else
	    	document.getElementById("pswd_validation").innerHTML= textResponse;
		}
		
	}
	
	var dataString = "Email=" + document.getElementById("Email_Id").value + "&Password=" + document.getElementById("Password_Valid").value;
	ajaxRequest.open("POST", "/login" , true);
	ajaxRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded;application/json");
	//ajaxRequest.setRequestHeader("dataType","html");
	ajaxRequest.send(dataString);

	return true;
}
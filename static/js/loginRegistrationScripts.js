var deploymentLink = "http://localhost:5000/";

function signup() {
	if((document.getElementById("Email").value) == "") {
		
		document.getElementById("errorBox").innerHTML="Enter email";
		 return false;
	} 
	else {
		document.getElementById("errorBox").innerHTML="";
	}
	
	re = /^[\w\-\.\+]+\@[a-zA-Z0-9\.\-]+\.[a-zA-z0-9]{2,4}$/;
	if(!re.test(document.getElementById("Email").value)) {
		
			document.getElementById("errorBox").innerHTML="Enter the valid Email";
			return false;
	}
	else {
		 document.getElementById("errorBox").innerHTML="";
	 }
	 
	if((document.getElementById("Uname").value) == "") {
		document.getElementById("errorBox1").innerHTML="Enter username";
		return false;
	}
	else {
			document.getElementById("errorBox1").innerHTML="";
	}
	re = /^\w+$/;
	if(!re.test(document.getElementById("Uname").value)) {
		document.getElementById("errorBox1").innerHTML="Username must contain only letters, numbers and underscores!";
		return false;
	}
	else {
	    	document.getElementById("errorBox1").innerHTML="";
	    }
	    
	    var p1 = document.getElementById("Password");
	    var p2 = document.getElementById("Confirm_Password");
	   	   
	        if(p1.value.length < 6) {
	        	
	    		document.getElementById("errorBox2").innerHTML="Password should be minimum of 6 characters";
	          return false;
	        }
	          re = /[0-9]/;
	          if(!re.test(p1.value)) {
	        	
	      		document.getElementById("errorBox2").innerHTML="Password must contain at least one number (0-9)!";
	            return false;
	          }
	          re = /[a-z]/;
	          if(!re.test(p1.value)) {
	        	 
	        	document.getElementById("errorBox2").innerHTML="Password must contain at least one lowercase letter (a-z)!" ;
	           
	            return false;
	          }
	          re = /[A-Z]/;
	          if(!re.test(p1.value)) {
	        	
	          	document.getElementById("errorBox2").innerHTML="Password must contain at least one uppercase letter (A-Z)!" ;
	            
	            return false;
	          }
	          if(p1.value != p2.value)
	        {

            	document.getElementById("errorBox3").innerHTML="Passwords do not match!";
            	return false;
	        	
	        }

	        var index_picked = document.getElementById("select").selectedIndex;
	      	var type_picked = document.getElementById("select").options[index_picked].value;

	      	//alert("type_picked: " + type_picked);

	      	registerCall(type_picked);	          
}

function registerCall(type_picked) {
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

	    // alert(ajaxRequest.responseText);

		if(!((ajaxRequest.responseText).indexOf("Error:") > -1))
		{
	       	if(type_picked == "yes")
	      		window.location.href= "/retailerDashboard";
	      	else if (type_picked == "no")
	      			window.location.href= "/search";
	      	else 
	      		window.location.href="";
	      	localStorage.setItem("userEmail", document.getElementById("Email").value );
	    }
	    else
	    	document.getElementById("errorBox").innerHTML= ajaxRequest.responseText;
	}
}
	
	var dataString = "Email=" + document.getElementById("Email").value + "&Uname=" + document.getElementById("Uname").value
			+ "&Password=" + document.getElementById("Password").value + "&IsRetailer=" + type_picked;
	ajaxRequest.open("POST", "/register" , true);
	ajaxRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	ajaxRequest.send(dataString);

	//Set local Storage for Useremail
}

function login_user() {

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

	//Set localstorage for username


	return true;
}

function logout(){
	window.location.href = "/";

	//Reset Local Storage for username


}

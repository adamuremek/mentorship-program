let btnLogin = document.getElementById("li-btn");
let btnSAMLLogin = document.getElementById("saml-li-btn");

let txtUname = document.getElementById("email");
let txtPassword = document.getElementById("password");

let txtWarning = document.getElementById("frm-warning-message");

btnLogin.onclick = async () => {
	let response = await attempt_login_uname_password(txtUname.value,txtPassword.value);
	if (response.status == 401) {
		let server_response_json = await response.json();
		console.log(server_response_json);
		txtWarning.innerText = server_response_json.warning;
		txtPassword.value = "";
	} else if (response.status == 200) {
		let server_response_json = await response.json();
		window.location.replace(server_response_json.new_web_location);
	}
};

btnSAMLLogin.onclick = () => {
	window.location.href = "/saml2/login";
};

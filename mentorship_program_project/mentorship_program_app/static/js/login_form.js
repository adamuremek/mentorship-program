let btnLogin = document.getElementById("btnLogin");
let txtUname = document.getElementById("txtUname");
let txtPassword = document.getElementById("txtPassword");

let txtWarning = document.getElementById("login-form-warning");

btnLogin.onclick = async () => {
	let response = await attempt_login_uname_password(txtUname.value,txtPassword.value);
	if (response.status == 401) {
		let server_response_json = await response.json();
		console.log(server_response_json);
		txtWarning.innerText = server_response_json.warning;
	}
};
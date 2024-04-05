let btnVerify = document.getElementById("mfa-btn");

let txtPassword = document.getElementById("password");

let txtWarning = document.getElementById("frm-warning-message");

btnVerify.onclick = async () => {
	let response = await attempt_mentor_mfa_password(txtPassword.value);
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

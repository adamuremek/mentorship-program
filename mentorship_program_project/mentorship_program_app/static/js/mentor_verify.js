let btnVerify = document.getElementById("mfa-btn");

let txtPassword = document.getElementById("passcode");

let txtWarning = document.getElementById("frm-warning-message");

btnVerify.onclick = async () => {
	//console.log("Button has been clicked :)	");
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

//Limit the input of passcode to numbers and display a warning.
document.getElementById("passcode").addEventListener("input", function(event) {
	const frm_warning_message = document.getElementById('frm-warning-message')

    let inputValue = event.target.value;
	let newValue = inputValue.replace(/\D/g, '');

	if (newValue == '') {
		frm_warning_message.innerText = "Must be a number 0 - 9."
	} 
	else {
		frm_warning_message.innerText = ""
	}

	event.target.value = newValue;
});

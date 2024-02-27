/*
 * this file is the main file for the javascript dashboard page
 * it is mostly inteanded to run front end glue that holds together stuff for the back end
 *
 * see backend_requests.js for where the back end functions live
 * */
async function request_user(requested_user_id,is_mentee,session_user_id) {
	is_mentee = is_mentee == 'True'; //python uses T true -_-

	let btn = document.getElementById("btn-request-" + requested_user_id);
	let response = null;


	if (is_mentee)
		response = await attempt_mentor_request(session_user_id,requested_user_id);
	else
		response = await attempt_mentor_request(requested_user_id,session_user_id);

	if (response.status == 200) {
		btn.innerText = "requested!";
		btn.onclick = ()=>{};
	}
}

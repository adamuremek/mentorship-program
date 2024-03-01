/*
 * this file contains code to make the buttons on the dashboard actually send a request to the 
 * backend systems and create a mentor ship / mentee request
 * it is mostly inteanded to run front end glue that holds together stuff for the back end
 *
 * see backend_requests.js for where the back end functions live
 *
 * note that in order to use this function 
 * session_user_id and is_mentee must get populated from the back end before use
 * */
async function request_user(requested_user_id) {
	let response = null;

	if (is_mentee)
		response = await attempt_mentor_request(session_user_id,requested_user_id);
	else
		response = await attempt_mentor_request(requested_user_id,session_user_id);

	if (response.status == 200) {
		let btns = document.getElementsByClassName("card-request-btn-user-id:" + requested_user_id);
		for (const btn of btns) {
			btn.classList.add("card-button-disabled");
			btn.innerText = "requested!";
			btn.onclick = null;
		}
	}
}


//actually setup each button to be clickable


const request_mentor = document.getElementsByClassName("card-request-btn");


for (let btnRequest of request_mentor) {
	let split_ids = Array.from(btnRequest.classList).filter(
											(x)=>x.split(":")[0]=="card-request-btn-user-id"
										).map(
											(x)=>x.split(":")[1]
										);
	let request_user_id = split_ids[0];

	
	btnRequest.onclick = async () => {
		request_user(request_user_id);
	}
}

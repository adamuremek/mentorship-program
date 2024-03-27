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
      let data = await response.json();
      
      //let the user know when they max out their mentee requests
      //as soon as we get the information
      if (data.has_maxed_mentee_requests) {
         display_requests_maxed();
      }

		let btns = document.getElementsByClassName("card-request-btn-user-id:" + requested_user_id);
		for (const btn of btns) {
			btn.classList.add("card-button-cancel");
			btn.innerText = "Cancel Request";
		}
	} else if (response.status == 400) { //permission denied request
      let error = await response.json();
      if (error.result == 'MENTEE_MAXED_REQUEST_AMOUNT') {
         display_requests_maxed();
      }
   }
}

async function reject_user(requested_user_id) {
	let response = null;

	if (is_mentee)
		response = await attempt_reject_mentorship_request(session_user_id,requested_user_id);
	else
		response = await attempt_reject_mentorship_request(requested_user_id,session_user_id);

	if (response.status == 200) {
		let btns = document.getElementsByClassName("card-request-btn-user-id:" + requested_user_id);
		for (const btn of btns) {
			btn.classList.remove("card-button-cancel");
			btn.innerText = "Request";
		}
	}
}

/*
 * this function sets all buttons of non requested mentees to be disabled from a maximum request amount
 * so that the front end user is aware of the request limit on the main page, it does NOT
 * have any effect on the back end, and purly exists as an indicator for the front end user of the app
 * */
function display_requests_maxed() {
   const requested_buttons = document.getElementsByClassName("card-request-btn");
   for (let btn of requested_buttons) {
      //we do NOT apply the tranformation to buttons of mentors that we already requested
      if (btn.classList.contains("card-button-cancel"))
         continue;

      btn.classList.add("card-button-disabled");
      btn.innerText = "Maximum Request Amount Reached";
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
	   //determine if we are a reject or accept button based on our display class
	   if (btnRequest.classList.contains("card-button-cancel"))
	      reject_user(request_user_id);
	   else
		   request_user(request_user_id);
	}
}

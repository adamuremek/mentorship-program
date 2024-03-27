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


/*
 * convinence function to get all buttons on the page that match a given user id for a request
 * */
function get_all_buttons_of_id(requested_user_id) {
   return document.getElementsByClassName("card-request-btn-user-id:" + requested_user_id);
}

/*
 * function connected to a button that requests the given user id and updates the main display
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

		let btns = get_all_buttons_of_id(requested_user_id);
		for (const btn of btns) {
			btn.classList.add("card-button-cancel");
			btn.classList.remove("pending");
			btn.innerText = "Cancel Request";
		}
	} else if (response.status == 400) { //permission denied request
      let error = await response.json();
      if (error.result == 'MENTEE_MAXED_REQUEST_AMOUNT') {
         display_requests_maxed();
      }
   }
}

/*
 * function connected to the buttons on the main display page that rejects the given user from id and updates 
 * the display
 * */
async function reject_user(requested_user_id) {
	let response = null;

	if (is_mentee)
		response = await attempt_reject_mentorship_request(session_user_id,requested_user_id);
	else
		response = await attempt_reject_mentorship_request(requested_user_id,session_user_id);

	if (response.status == 200) {

	   //we could query the database again to ensure that we have not maxed our requests,
	   //but if were canceling a request then we do NOT have maxed requests, so we can save
	   //a hit to the database
	   //let maxed_requests_query = await attempt_query_session_user(["has_maxed_mentee_requests"]); //from backend_requests.js
	   //let data = await maxed_requests_query.json();

      //if (!data.has_maxed_mentee_requests) {
         undisplay_requests_maxed();
      //}
		let btns = get_all_buttons_of_id(requested_user_id);
		for (const btn of btns) {
			btn.classList.remove("card-button-cancel");
			btn.classList.remove("pending");
			btn.innerText = get_request_string();
		}
	}
}
function get_request_string() {
   return "Request " + (is_mentee ? "Mentor" : "Mentee");
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
/*
 * this function hides all maximized request buttons from the front end user
 *
 * note that it ONLY works on the front end, back end data is not touched with this
 * */
function undisplay_requests_maxed() {
   const requested_buttons = document.getElementsByClassName("card-request-btn");
   for (let btn of requested_buttons) {
      //we do NOT apply the tranformation to buttons of mentors that we already requested
      if (btn.classList.contains("card-button-cancel"))
         continue;

      btn.classList.remove("card-button-disabled");
      btn.innerText = get_request_string();
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
	   //get ALL buttons of our id
	   let btns = get_all_buttons_of_id(request_user_id);
	   
	   //let the end user know that something is happening while we wait for queries
	   for (let button of btns) {
         button.classList.add("pending");
      }

	   //determine if we are a reject or accept button based on our display class
	   if (btnRequest.classList.contains("card-button-cancel"))
	      reject_user(request_user_id);
	   else
		   request_user(request_user_id);
	}
}



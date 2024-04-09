/*
 * this file contains functions to interact with and talk to the back end
 * to make creating requests to and from easier for front end :D
 * */

/*
 * gets the given named cookie from django, straight from the django documentation page
 *
 * see: https://docs.djangoproject.com/en/5.0/howto/csrf/
 *
 * */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//store the csrftoken in a convinent manner
const csrftoken = getCookie('csrftoken');


/*
 * tries to log in with the given user name password combination
 *
 * returns a response object, where 200 means you can log in, and an
 * error message for the user encoded as json in the body of the response
 *
 * response = await attempt_login_uname_passowrd('blah@blah.com','password PAAAAARTAY');
 * response.json() //should work to decode the json data
 *
 * in order to use this request make sure that you include the csrf token in your
 * django includes up at the top of the file
 * 
 * */
async function attempt_login_uname_password(username,password) {
	let login_request = {type:"username_password",username:username,password:password};
	
	const req = new Request("/login/",{
							method:"POST",
							body: JSON.stringify(login_request),
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
								},
							mode: 'same-origin'
	});
	
	let response = await fetch(req);
	return response;
}

/*
 * requests that the server log out the current user
 *
 * status code 200 means succesful logout
 * status code 500 means that you were already logged in
 * */
async function attempt_logout_request() {
	const req = new Request("/logout/",{
							method:"POST",
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
								},
							mode: 'same-origin'
	});
	let response = await fetch(req);
	return response;
}

/*
 * requests that the back end creates a mentor request for the given mentee/ mentor
 *
 * this may or may not work depending on the permissions of the logged in user
 * and if the request already exists
 * */
async function attempt_mentor_request(mentor_id,mentee_id = null) {
	let request_url = "/request_mentor/" + mentor_id;
	

	if (mentee_id)
		request_url += "/"+mentee_id;

	const req = new Request(request_url,{
							method: "POST",
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
							},
							mode: "same-origin"
	});

	let response = await fetch(req);
	return response;
}

/*
* requests that the back end creates a mentor report for the given mentor
*/
async function attempt_mentor_report(mentor_id) {
	let request_url = "/report_mentor/" + mentor_id

	const req = new Request(request_url,{
							method: "POST",
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
								},
							mode: "same-origin"
	});

	let response = await fetch(req);
	return response;
}

/*
* requests that the back end creates a new organization using the pasted organization name --ANTHONY PETERS
*/
function attempt_create_new_organziation(organzation_name)
{
	// return "/create_new_orgnization/" + organzation_name;

    return new Request("/create_new_orgnization/" + organzation_name, {
                            method: "POST",
                            headers: {
                                "Content-type": "application/json; charset=UTF-8",
                                'X-CSRFToken': csrftoken
                            },
                            mode: 'same-origin'
    });
}

/*
* requests that the back end removes a organization based on the pasted organization id --ANTHONY PETERS
*/
function attempt_remove_organization(orgnaization_id)
{
	// return "/delete_orgnization/" + orgnaization_id;

	return new Request("/delete_orgnization/" + orgnaization_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* requests that the back end edits the organization of passed mentor to the a organization based on the passed id --ANTHONY PETERS
*/
function attempt_edit_mentor_organization(mentor_id, orgnaization_id)
{
	return new Request("/edit_mentor_organization/" + mentor_id + "/" + orgnaization_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* requests that the back end removes the organization of passed mentor, based on the passed organization id --ANTHONY PETERS
*/
function attempt_remove_mentors_org(mentor_id, orgnaization_id)
{
	return new Request("/remove_mentors_org/" + mentor_id + "/" + orgnaization_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* requests that the back end edits the organization to promote passed mentor to organization admin based on the passed id --ANTHONY PETERS
*/
function attempt_promote_mentor_to_organization_admin(mentor_id)
{
	return new Request("/promote_organization_admin/" + mentor_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* requests that the back end disabled passed user based on the passed id --ANTHONY PETERS
*/
function attempt_disable_user(user_id)
{
	return new Request("/disable_user", {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({ id: user_id }),
			mode: 'same-origin'
	});
}

/*
* requests that the back end enabled passed user based on the passed id --ANTHONY PETERS
*/
function attempt_enable_user(user_id)
{
	return new Request("/enable_user", {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({ id: user_id }),
			mode: 'same-origin'
	});
}

/*
* requests that the back end creates a mentorship of passed mentee and mentor ids --ANTHONY PETERS
*/
function attempt_create_mentorship(mentee_id, mentor_id)
{
	return new Request("/create_mentorship/" + mentee_id + "/" + mentor_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* requests that the back end removes a mentorship of passed mentee ids --ANTHONY PETERS
*/
function attempt_delete_mentorship(mentee_id)
{
	return new Request("/delete_mentorship/" + mentee_id, {
			method: "POST",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-CSRFToken': csrftoken
			},
			mode: 'same-origin'
	});
}

/*
* Loops through passed request array executing in order --ANTHONY PETERS
*/
async function execute_request(request_array)
{
	// Inintlizae valid flag to true
	let valid_flag = true;

	// Cycles through passed request array and exeuctes them in order
	for (let index = 0; index < request_array.length; index++) {

		// Determine response to request
		let response = await fetch(request_array[index]);

		// Fetch request and wait for response
		if (String(response.status) != "200")
		{
			// Update valid flag to false
			valid_flag = false;
			
			break;
		}
	}

	return valid_flag;

}

/*
* Opens profile page of passed user id --ANTHONY PETERS
*/
async function view_profile(user_id)
{
	// Opens the profile page in a new tab
	window.open("/universal_profile/" + user_id, '_blank');
}







/*
* requests that the back end removes a mentorship request for the given mentee then adds one for the mentee and mentor
*/
async function attempt_reject_mentorship_request(mentor_id,mentee_id = null) {
	let request_url = "/reject_mentorship_request/" + mentor_id;
	

	if (mentee_id)
		request_url += "/"+mentee_id;

	const req = new Request(request_url,{
							method: "POST",
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
							},
							mode: "same-origin"
	});

	let response = await fetch(req);
	return response;
}

async function attempt_query_session_user(request=null,data=null) {
   let query_string = "/api/get_session_data?"
   if (request) {
      query_string += "request=" + request.join(",");
   }
   if (data) {
      query_string += "data=" + data.join(",");
   }

   const req = new Request(query_string,{
      method: "GET",
      headers: {
                  "Content-type": "application/json; charset=UTF-8",
                  'X-CSRFToken': csrftoken
      },
      mode: "same-origin"
   });
   
   let response = await fetch(req);
   return response;
}



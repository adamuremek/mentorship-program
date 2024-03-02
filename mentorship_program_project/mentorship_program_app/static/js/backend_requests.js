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
 * status code 200 means sucesful logout
 * status code 500 means that you were already logged in
 *
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
/*********************************************************************/
/* FILE NAME: admin_dashboard.js                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew Pyscher (???)                                  */
/* (OFFICIAL) DATE CREATED: April 15, 2024                           */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the JavaScript necessary to use functional     */
/*      aspects of the Settings Page                                 */
/* This file is included in 'settings.html'                          */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- ----------------------- -------------------- \\
// -------------------- <<< CHANGE PASSWORD >>> -------------------- \\
// -------------------- ----------------------- -------------------- \\

function validateForm(event) {
        let newPassword1 = document.getElementById("new-password1").value;
        let newPassword2 = document.getElementById("new-password2").value;
        let message = document.getElementById("message")
        const uppercaseRegex = /[A-Z]/;
        const lowercaseRegex = /[a-z]/;
        const numberRegex = /[0-9]/;
        const symbolRegex = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/;
        const emojiRegex = /([\u{1F600}-\u{1F64F}|\u{1F300}-\u{1F5FF}|\u{1F680}-\u{1F6FF}|\u{1F700}-\u{1F77F}|\u{1F780}-\u{1F7FF}|\u{1F800}-\u{1F8FF}|\u{1F900}-\u{1F9FF}|\u{1FA00}-\u{1FA6F}|\u{1FA70}-\u{1FAFF}|\u{2600}-\u{26FF}|\u{2700}-\u{27BF}|\u{231A}-\u{231B}|\u{23E9}-\u{23EC}|\u{23F0}|\u{23F3}|\u{25FD}-\u{25FE}|\u{2614}-\u{2615}|\u{2648}-\u{2653}|\u{267F}|\u{2693}|\u{26A1}|\u{26AA}-\u{26AB}|\u{26BD}-\u{26BE}|\u{26C4}-\u{26C5}|\u{26CE}|\u{26D4}|\u{26EA}-\u{26EB}|\u{26F2}-\u{26F3}|\u{26F5}|\u{26FA}|\u{26FD}|\u{2705}|\u{270A}-\u{270B}|\u{2728}|\u{274C}|\u{274E}|\u{2753}-\u{2755}|\u{2757}|\u{2795}-\u{2797}|\u{27B0}|\u{27BF}|\u{2934}-\u{2935}|\u{2B05}-\u{2B07}|\u{2B1B}-\u{2B1C}|\u{2B50}|\u{2B55}|\u{3030}|\u{303D}|\u{3297}|\u{3299}|\u{FE0F}|\u{200D}|\u{20E3}|\u{E0020}-\u{E007F}]+|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]|\uD83D[\uDE80-\uDEFF])/gu;
        
        // Show error messages for passwords which do not conform to our standards.
        // This is repeated code and is certainly a weak point in redundancy.
        // Oh well. These things happen when 6 people do the work of 20 ¯\_(ツ)_/¯

        // Check if new passwords match
        if (newPassword1 !== newPassword2) {
            event.preventDefault()
            message.innerHTML = "Passwords don't match"
            message.style.display = "inline-block"
        }
        // Ensure passwords have at least 12 characters
        if (newPassword1.length < 12){
            console.log("here")
            event.preventDefault()
            message.innerHTML = "Passwords must be more than 12 characters"
            message.style.display = "inline-block"
        }
        // Ensure password is less than 36 characters
        if (newPassword1.length > 36){
            event.preventDefault()
            message.innerHTML = "Passwords must be less than 36 characters"
            message.style.display = "inline-block"
        }
        // Ensure password passes all relevant regex patterns
        if (
          !uppercaseRegex.test(newPassword1) ||
          !lowercaseRegex.test(newPassword1) ||
          !numberRegex.test(newPassword1) ||
          !symbolRegex.test(newPassword1) ||
          emojiRegex.test(newPassword1)
        ) {
            event.preventDefault()
            message.innerHTML = "Passwords must contain one capital letter, lowercase letter, a number, and a symbol"
            message.style.display = "inline-block"
        }
}

// -------------------- --------------------- -------------------- \\
// -------------------- <<< NOTIFICATIONS >>> -------------------- \\
// -------------------- --------------------- -------------------- \\

// Make toggle enable/disable notifications
const togglebox = document.getElementById('toggler');
togglebox.addEventListener('change', (event)=>{
        if (event.currentTarget.checked) {
            attempt_notification_status_change(true)
        } else {
            attempt_notification_status_change(false)
        }
    });


// Send POST request to change a user's Notification policy
async function attempt_notification_status_change(status) {
	let request_url = "/toggle_notifications/"+ status ;
	const req = new Request(request_url,{
							method: "GET",
							headers: {
									"Content-type": "application/json; charset=UTF-8",
									'X-CSRFToken': csrftoken
							},
							mode: "same-origin"
	});
	let response = await fetch(req);
	console.log(response)
	return response
}
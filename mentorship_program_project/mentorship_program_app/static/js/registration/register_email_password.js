/*********************************************************************/
/* FILE NAME: register_email_password                                */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp, Andrew P, Caleb Hunter                    */
/* (OFFICIAL) DATE CREATED: April 14, 2024                           */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the JavaScript necessary to use functional     */
/*      aspects of the profile pages for mentees/mentors             */
/* This file is included in 'combined_views.html'                    */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\


var emailInput = document.getElementById('email');
var emailPrompt = document.getElementById('email-prompt');
var nextButton = document.getElementById('next-btn');
var phoneInput = document.getElementById('phone');
var passwordInput = document.getElementById('password');
var emailParts;
var email_error_message;

//emailNameRegex allows the alphabet, numbers, periods, dashes, and underscores
const emailNameRegex = /^[a-zA-Z0-9._-]+$/;
//emailDomainNameRegex allows the alphabet, numbers, periods, and dashes
const emailDomainNameRegex = /^[a-zA-Z0-9.-]+$/;
//emailTLDRegex must start with a period and only contain the alphabet
const emailTLDRegex = /.[a-zA-Z]{2,}/;

email_error_message = 'Invalid Email Format'

// Show email validity as it is being typed
// Different error messages displayed for each incorrect portion of email
emailInput.addEventListener('input', () => {
    emailText = emailInput.value;
    
    //parse email into name, domain and TLD, because they all have different rules
    emailParts = emailText.split("@");
    var emailDomain = emailParts[1].split(".");
    emailParts[1] = emailDomain[0];
    emailParts[2] = emailDomain[1];

    //if any parts of email are not formatted correctly, display message to user and don't let them move on
    if (!emailNameRegex.test(emailParts[0]) || !emailDomainNameRegex.test(emailParts[1]) || !emailTLDRegex.test(emailParts[2])) {
        emailPrompt.innerText = 'Email: ' + email_error_message;
        nextButton.disabled = true;
        phoneInput.disabled = true;
        passwordInput.disabled = true;
    }
    else {
        emailPrompt.innerText = 'Email:';
        nextButton.disabled = false;
        phoneInput.disabled = false;
        passwordInput.disabled = false;
    }
});


// 🤑🤑🤑

// -------------------- --------------------- -------------------- \\
// -------------------- <<< SHOW PASSWORD >>> -------------------- \\
// -------------------- --------------------- -------------------- \\

// Image components for show/hide password
// Two constants -> Initial + Confirmation
const password_toggle_wrapper = document.getElementById('toggle-password')
const confirm_password_toggle_wrapper = document.getElementById('toggle-confirm-password')

// Image components for show/hide password
// Two constants -> Initial + Confirmation
const eye_image = document.getElementById('testertest')
const eye_image_confirm = document.getElementById('confirm-eye-image')

// Input components for show/hide password
// Two constants -> Initial + Confirmation
const input_password = document.getElementById('password')
const input_confirm_password = document.getElementById('confirm-password')

// If eye is clicked, change the image and type of input (text/password)
password_toggle_wrapper.addEventListener('click', e => {
    if (input_password.type === "password") {
        input_password.type = "text";
        eye_image.src = eye_image.src.replace('open', 'closed')
        } else {
        input_password.type = "password";
        eye_image.src = eye_image.src.replace('closed', 'open')
        }
})

// If eye is clicked, change the image and type of input (text/password)
// Same thing as above, but this is for the password confirmation
confirm_password_toggle_wrapper.addEventListener('click', e => {
    if (input_confirm_password.type === "password") {
        input_confirm_password.type = "text";
        eye_image_confirm.src = eye_image_confirm.src.replace('open', 'closed')
        } else {
        input_confirm_password.type = "password";
        eye_image_confirm.src = eye_image_confirm.src.replace('closed', 'open')
        }
})
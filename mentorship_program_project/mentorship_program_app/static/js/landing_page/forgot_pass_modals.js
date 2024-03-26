const forgot_pass_btn = document.querySelector('#forgot-pass-btn');
const forgot_pass_modal_1 = document.querySelector('#forgot-pass-modal-1');
const modal_exit = document.querySelector('#modal-exit');
const reset_email_field = document.getElementById('reset-email');
const email_status_bad = document.getElementById('email-status-bad');

forgot_pass_btn.addEventListener("click", () => {
    forgot_pass_modal_1.showModal();
});

modal_exit.addEventListener("click", () => {
    forgot_pass_modal_1.close();

    // Reset the reset-email field when the modal is closed
    reset_email_field.value = "";

    // Set the background color using box-shadow to simulate an inset effect
    reset_email_field.style.backgroundColor = "rgba(255, 255, 255, 0.07)";

    // Clear the 'user not found' prompt when closing
    email_status_bad.innerText = "";
    email_status_bad.style.display = "none";
});

const input_email = document.getElementById('reset-email')

// const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/


// input_email.addEventListener("input", e => {

//     if (e.target.value === "") {
//         input_email.style.backgroundColor = 'rgba(255, 255, 255, 0.07)';
//         return;
//     }

//     let regex_custom = regex_email

//     const regex_result = regex_custom.test(e.target.value)


//     //change background color green if correct email format, red if incorrect email format
//     if (regex_result)
//         input_email.style.backgroundColor = 'forestgreen'
//     else
//         input_email.style.backgroundColor = 'firebrick'
// })

function checkEmail(event) {
    event.preventDefault(); // Prevent the default form submission action                                                                  🦞

    // Clear any existing timeout to hide the 'email-status-bad' message
    if (window.emailInputTimeout) clearTimeout(window.emailInputTimeout);

    var email = document.getElementById("reset-email").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response.exists) {
                document.getElementById("email-status-good").innerText = "Email Sent!";
                sendEmail(email);
                document.getElementById("pass-reset").style.display = "none"; // Hide the button
                document.getElementById("reset-email").style.display = "none"; // Hide the textbox
                document.getElementById("email-status-bad").style.display = "none"; // if visible hide it
            } else {
                document.getElementById("email-status-bad").innerText = "Sorry we could not find that account.";
                document.getElementById("email-status-bad").style.display = ""; // Make sure it's visible
            }
        }
    };
    xhttp.open("GET", "/check_email_for_password_reset?email=" + email, true);
    xhttp.send();
}

// Set up an input event listener on the 'reset-email' field
const inputEmail = document.getElementById("reset-email");

// This routine hides the email-status-bad text 2.5 seconds after the event
inputEmail.addEventListener("input", () => {
    // Clear any existing timeout to ensure we don't have multiple clears queued
    if (window.emailInputTimeout) clearTimeout(window.emailInputTimeout);

    // Set a new timeout when the user starts typing
    window.emailInputTimeout = setTimeout(() => {
        // Clear and hide the message 2.5 seconds after the user stops typing
        document.getElementById("email-status-bad").innerText = "";
        document.getElementById("email-status-bad").style.display = "none";
    }, 2500);
});

function sendEmail(email) {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Handle the response of the POST request if needed
            console.log("POST request successful");
        }
    };
    xhttp.open("POST", "/reset_request", true); // Change endpoint to your reset_request URL
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var params = "email=" + email; // Constructing POST parameters
    xhttp.send(params);
}
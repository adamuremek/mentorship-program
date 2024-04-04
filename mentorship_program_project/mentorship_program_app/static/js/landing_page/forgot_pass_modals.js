const forgot_pass_btn = document.querySelector('#forgot-pass-btn');
const forgot_pass_modal_1 = document.querySelector('#forgot-pass-modal-1');
const exitButton = document.getElementById('modal-exit');
const reset_email_field = document.getElementById('reset-email');
const email_status_bad = document.getElementById('email-status-bad');

// This routine when invoked assigns focus to the reset email element.
function focusInput() {
    // Use setTimeout to delay the focus action ~ allow modal to show
    setTimeout(() => {
        reset_email_field.focus();
    }, 0); // Starting with 0 milliseconds
}

// This function when invoked shows the forgotten password modal, and focuses
// the input on the email input field. 
function showModalAndFocusInput() {
    forgot_pass_modal_1.showModal();
    focusInput();
}

// Event listener for click event
forgot_pass_btn.addEventListener("click", showModalAndFocusInput);

// Event listener for keydown event
forgot_pass_btn.addEventListener("keydown", (event) => {
    // Check if Enter or Spacebar was pressed
    if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
        event.preventDefault(); // Prevent the default action
        showModalAndFocusInput();
    }
});

async function closeModal() {
    // Reset the reset-email field when the modal is closed
    reset_email_field.value = "";

    // Set the background color using box-shadow to simulate an inset effect
    reset_email_field.style.backgroundColor = "rgba(255, 255, 255, 0.07)";

    // Clear the 'user not found' prompt when closing
    email_status_bad.innerText = "";
    email_status_bad.style.display = "none";

    // Close the modal
    forgot_pass_modal_1.close();
}

// Add click event listener
exitButton.addEventListener('click', closeModal);

// Add keydown event listener for Enter key and Spacebar
exitButton.addEventListener('keydown', (event) => {
    // Check if the Enter key or Spacebar is pressed
    if (event.key === 'Enter' || event.key === ' ') {
        // Prevent default behavior (e.g., scrolling the page)
        event.preventDefault();
        // Close the modal
        closeModal();
    }
});
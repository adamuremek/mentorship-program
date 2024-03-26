const forgot_pass_btn = document.querySelector('#forgot-pass-btn');
const forgot_pass_modal_1 = document.querySelector('#forgot-pass-modal-1');
const modal_exit = document.querySelector('#modal-exit');
const reset_email_field = document.getElementById('reset-email');

forgot_pass_btn.addEventListener("click", () => {
    forgot_pass_modal_1.showModal();
});

modal_exit.addEventListener("click", () => {
    forgot_pass_modal_1.close();

    // Reset the reset-email field when the modal is closed
    reset_email_field.value = "";

    // Set the background color using box-shadow to simulate an inset effect
    reset_email_field.style.backgroundColor = "rgba(255, 255, 255, 0.07)";
});
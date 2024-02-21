

const forgot_pass_btn = document.querySelector('#forgot-pass-btn');
const forgot_pass_modal_1 = document.querySelector('#forgot-pass-modal-1');
const modal_exit = document.querySelector('#modal-exit');


forgot_pass_btn.addEventListener("click", () => {
    forgot_pass_modal_1.showModal();
});

modal_exit.addEventListener("click", () => {
    forgot_pass_modal_1.close();
});
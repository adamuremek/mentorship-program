
const btn_add_note = document.querySelector("#btn-add-note");
const modal_exit = document.querySelector('#modal-exit');
const note_creator_modal = document.querySelector("#note-creator-modal");

// Listen for btn-add-note click
btn_add_note.addEventListener("click", () => {
    note_creator_modal.showModal(); // Show note creator modal
});

// Listen for modal exit click
modal_exit.addEventListener("click", () => {
    note_creator_modal.close(); // Close note creator modal
});

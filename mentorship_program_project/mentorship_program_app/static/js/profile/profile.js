/*********************************************************************/
/* FILE NAME: profile.js                                             */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp & Others                                   */
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
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/* (MAX_MENTEES) | int: A mentor's max number of possible mentees    */
/* (IS_PAGE_OWNER_MENTEE) | bool: Is the OWNER of the page a mentee? */
/*                                                                   */
/* (PAGE_OWNER_MENTEE_ID) | int: ID of page owner -if user is mentee */
/* (PAGE_OWNER_MENTOR_ID) | int: ID of page owner -if user is mentor */
/*                                                                   */
/* (SIGNED_IN_MENTOR_ID) | int: ID of cur-user (if they are mentor)  */
/* (SIGNED_IN_MENTEE_ID) | int: ID of cur-user (if they are mentee)  */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

//The max length that can be stored in the profile bio is 5000
const MAX_OVERVIEW_LENGTH = 5000;  
const TOO_LONG_ERROR_MSG = 'Overview must be less than ' + MAX_OVERVIEW_LENGTH + ' characters'
var bioTextArea;   
var saveButton;
var bioLength;
var overviewTitle;

saveButton = document.getElementById('button-save');        // Btn responsible for saving profile changes
bioTextArea = document.getElementById('bio');               // TextArea where user bio resides
overviewTitle = document.getElementById('overview-title');  // Relevant header component above TextArea 

//when user types & overview's length is over max length, make overview text red and add warning in header
bioTextArea.addEventListener('input', function () {
    var bioLength = bioTextArea.value.length;

    if (bioLength > MAX_OVERVIEW_LENGTH) {
        bioTextArea.style.color = 'red';
        overviewTitle.innerText = 'Overview: ' + TOO_LONG_ERROR_MSG;
    }
    else {
        bioTextArea.style.color = '';
        overviewTitle.innerText = 'Overview:'
    }
});
let submitable = true
//when user clicks save button and overview's length is over max length, alert user and keep them on page
if(saveButton)
saveButton.addEventListener('click', function () {
    bioLength = bioTextArea.value.length;
    if (bioLength > MAX_OVERVIEW_LENGTH) {
        alert('Overview exceeds 5000 characters. Please shorten Overview');
        event.preventDefault();
    }
});


// -------------------- ------------------------------------------- -------------------- \\
// -------------------- <<< MENTORSHIP TERMINATION CONFIRMATION >>> -------------------- \\
// -------------------- ------------------------------------------- -------------------- \\

var removeButton;
var confirmationBln;

removeButton = document.getElementById('remove-btn');

// Assuming 'Remove' button exists,
// Show a confirmation message before process execution
if(removeButton)
removeButton.addEventListener('click', function () {
    confirmationBln = confirm('Are you sure you want to remove this user?');

    if (!confirmationBln) {
        event.preventDefault();
    }
});


// -------------------- ----------------------------------- -------------------- \\
// -------------------- <<< MAX NUMBER OF MENTEES ALERT >>> -------------------- \\
// -------------------- ----------------------------------- -------------------- \\

// var MAX_MENTEES = "{{ max_mentees }}";
var cur_num_mentees;
var acceptButton;

acceptButton = document.getElementById('accept-mentee-btn');
cur_num_mentees = document.querySelectorAll('#current-mentee').length;

// Display message if user tries to accept mentees after limit has been reached
if(acceptButton)
acceptButton.addEventListener('click', function () {
    //message for if user just filled their capacity
    if (cur_num_mentees == (MAX_MENTEES - 1)) {
        alert('You are now at your max capacity for mentees. To continue adding mentees, edit your Max Mentees');
    } 
    //message for if user already is at their capacity
    else if (cur_num_mentees > (MAX_MENTEES - 1)) {
        alert('You have already reached your max capactity for mentees. To continue adding mentees, edit your Max Mentees');
    }
});


// Attempt to send a mentorship request to another user.
// Backend is designed to fail safely if request cannot be sent.
async function attempt_mentorship_request(mentee_id, mentor_id)
{
    // Create a new POST request to the request_mentor route
    const req = new Request("/request_mentor/" + mentee_id + "/" + mentor_id, {
                            method: "POST",
                            headers: {
                                "Content-type": "application/json; charset=UTF-8",
                                'X-CSRFToken': csrftoken
                            },
                            mode: 'same-origin'
    });

    let response = await fetch(req);
    // Route user to their profile after sending 

    window.location.href = `/universal_profile/${PAGE_OWNER_ID}` //{{page_owner_user.id}}
}

document.addEventListener('DOMContentLoaded', winloaded => {
    
    const btn_profile_request = document.getElementById('btn_profile_request')
    
////////////////////////////////////////////////////// Needed for max mentees option box to display properly, old method wasnt workin on certain cases 🦞
    // Get the max mentees value from the context
    // const MAX_MENTEES = "{{ max_mentees }}";

    
    const select_max_mentees = document.getElementById('select-max-mentees');

    if (select_max_mentees){
    const options = select_max_mentees.getElementsByTagName('option');
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === MAX_MENTEES) {
        
            options[i].selected = true;
            break;  // Exit the loop after setting the selected option
        }
    }
    }
//////////////////////////////////////////////


    if(!btn_profile_request){
        return
    }

    btn_profile_request.addEventListener('click', () => {
        let mentee = null
        let mentor = null
        
        // These variables are imported from the bottom of the combined_views.html page
        // Comments on the side are the original code that powers these constants
        if(IS_PAGE_OWNER_MENTEE === "True"){                 // "{{page_owner_user.is_mentee}}" === "True"
            mentee = PAGE_OWNER_MENTEE_ID                    // page_owner_user.mentee.account.id
            mentor = SIGNED_IN_MENTOR_ID                     // "{{signed_in_user.mentor.account.id}}"
        } else {
            mentee = SIGNED_IN_MENTEE_ID                     // "{{signed_in_user.mentee.account.id}}" 
            mentor = PAGE_OWNER_MENTOR_ID                    // "{{page_owner_user.mentor.account.id}}"
            
        }
        // Hi logan :)
        // Hi Adam :D
        attempt_mentorship_request(mentee, mentor)
    })
})



function changeEditToSave(event) {
    event.preventDefault()

    const attr_none = 'none';
    const attr_flex = 'flex';
    const attr_block = 'block'
    const attr_inline_block = 'inline-block';

    //Save button bullshit and shananiganz
    let editBtn = document.getElementById("button-edit")
    let saveBtn = document.getElementById("button-save")
    let cancelBtn = document.getElementById("button-cancel")
    let editPfpOverlay = document.getElementById("edit_profile_overlay")

    //Editable field fuckshit
    let bioTextArea = document.getElementById("bio")
    let allInterestsButtons = document.querySelectorAll(".hidden_interests")
    let user_interests = document.querySelectorAll(".user_interests")
    let max_mentees = document.getElementById('select-max-mentees')

    // make name editable
    let headerDisplay = document.querySelector(".header-display");
    let headerEdit = document.querySelector(".header-edit");
    headerDisplay.style.display = attr_none;
    headerEdit.style.display = attr_block;
    // make job title editable
    let jobTitleDisplay = document.querySelector(".job-title-display");
    let jobTitleEdit = document.querySelector(".job-title-edit");
    // phone AHHHH
    let phoneDisplay = document.querySelector(".phone-view");
    let phoneEdit = document.querySelector(".phone-edit");
    
    if(jobTitleDisplay)
        jobTitleDisplay.style.display = attr_none;
    if(jobTitleEdit)
        jobTitleEdit.style.display = attr_block;

    if(phoneDisplay)
        phoneDisplay.style.display = attr_none;
    if(phoneEdit)
        phoneEdit.style.display = attr_block;

    // make pronouns editable
    let pronounDisplay = document.querySelector(".pronoun-display");
    let pronounEdit = document.querySelector(".pronoun-edit");

    pronounDisplay.style.display = attr_none;
    pronounEdit.style.display = attr_flex;
    
    //Make editable elements visible and selectable
    bioTextArea.readOnly = false
    editPfpOverlay.style.display = attr_flex
    if(max_mentees)
        max_mentees.disabled = false

    // Make interests change on hover
    user_interests.forEach(button => button.classList.add('hover_interest'))

    //This makes all available interests visible
    allInterestsButtons.forEach(button => {
        button.style.display = attr_inline_block
        button.getElementsByTagName('input')[0].classList.add('hover_interest')
    })

    //Make edit button invisible
    editBtn.style.display = attr_none
    //Make save and cancel buttons visible
    cancelBtn.style.display = attr_inline_block
    saveBtn.style.display = attr_inline_block
}

// Allow interests to be added/removed during edit mode
function interestClicked(event) {
    event.preventDefault()

    let saveDisplayed = document.getElementById("button-save")

    //Basically, if the profile is not in edit mode, dont allow the interest selection to be changed.
    if (saveDisplayed === null || saveDisplayed.style.display !== "inline-block") {
        event.target.checked = !event.target.checked
    }
}

// Allow profile picture to be changed during edit mode via an overlay
$(document).ready(function () {
    $('#edit_profile_overlay').click(function () {
        $('#profile_image').click(); // Trigger file input click
    })

    $('#profile_image').change(function (event) {
        let file = event.target.files[0] // Get the selected file

        // Check the file size
        if (file.size > 4500000) { // If the file is lrgaer than 4.5 MB
            alert('The file is too large. Please upload a file smaller than 4.5 MB.')
            return // Stop the function
        }
        
        if (
            file.type !== 'image/jpeg' &&
            file.type !== 'image/png' &&
            file.type !== 'image/gif'
        ) {
            alert('Please upload a PNG, JPEG, or GIF image file.');
            return; // Stop the function
        }

        let reader = new FileReader();
        reader.onload = function (e) {
            $('#profile_pic').attr('src', e.target.result) // Set preview image source to selected file
        }
        reader.readAsDataURL(file); // Read the selected file as Data URL
    })
})

// -------------------- ---------------------- -------------------- \\
// -------------------- <<< REPORT PROFILE >>> -------------------- \\
// -------------------- ---------------------- -------------------- \\

const btn_profile_report = document.getElementById('btn_profile_report');

// Assuming button exists
// Display Report Modal when report button is clicked
// This opens an interface to input report details
if (btn_profile_report) {
    console.log('the button exists')
    btn_profile_report.addEventListener('click', () => {
        console.log('please do something')
        document.getElementById('report-modal').showModal();
    });
}

// -------------------- ----------------------------------------- -------------------- \\
// -------------------- <<< EDIT PHONE NUMBER (SPECIAL INPUT) >>> -------------------- \\
// -------------------- ----------------------------------------- -------------------- \\

// Standard phone number regex pattern - no extension
const regex_phone = /^\(\d{3}\) \d{3}-\d{4}$/;
const input_phone = document.getElementById('phone-edit')

// If input element exists (does not exist for mentees)
// Restrict input to numbers
// Display numbers to the form (123) 456-7890
//      No input required for special characters
// Repeated code segment from registration
// Sorry for duplicating...
if(input_phone)
{
    let previous_value = input_phone.value
    input_phone.addEventListener("input", e => {
        let input_value = e.target.value.replace(/\D/g, ""); // Remove non-numeric characters
        // Account for backspaces on non-numeric characters
        if (input_value === previous_value)
            input_value = input_value.slice(0, -1)


        // User backspaces with one number. Remove '('
        if (input_value.length == 0) {
            input_value = ''
            // Format as '( XXX )'
        } else if (input_value.length <= 3) {
            input_value = '(' + input_value + ')'; // Start with (
            // Format as '( XXX ) XXX'
        } else if (input_value.length <= 6) {
            input_value = '(' + input_value.substring(0, 3) + ') ' + input_value.substring(3);
            // Format as '( XXX ) XXX-XXXX'
        } else {
            input_value = '(' + input_value.substring(0, 3) + ') ' + input_value.substring(3, 6) + '-' + input_value.substring(6, 10); // Format as (XXX) XXX-XXXX
        }

        // Record value for next iteration
        previous_value = input_value.replace(/\D/g, "")
        // Set input to new value
        e.target.value = input_value;

        const regex_result = regex_phone.test(e.target.value)
        const RED = 'firebrick'
        const GREEN = 'forestgreen'
        // Visually indicate Regex Success
        if (regex_result){
            input_phone.style.backgroundColor = GREEN
            saveButton.disabled = false
        }
        else{
            input_phone.style.backgroundColor = RED
            //input_phone.focus()
            saveButton.disabled = true
        }
    });
}

    // -------------------- ----------------- -------------------- \\
    // -------------------- <<< NOTE CODE >>> -------------------- \\
    // -------------------- ----------------- -------------------- \\

    // Button for adding new notes
    const btn_add_note = document.getElementById('btn-add-note');

    // Button for adding a note (Mentor)
    const lst_btn_edit_note = document.getElementsByClassName('btn-note-edit');
    // Button for removing a note (Mentor)
    const lst_btn_remove_note = document.getElementsByClassName('btn-note-remove');

    // Button for viewing a note (Mentee)
    const lst_btn_view_note = document.getElementsByClassName('btn-note-view');
    
    // A list of note modals (one modal for each existing note)
    const lst_note_modal = document.getElementsByClassName('note-modal');
    // A list of the 'exit' buttons on the modal
    const lst_modal_exit = document.getElementsByClassName('modal-exit');

    // A list of every fucking note on the goddamn page - even not pertaining to notes
    const every_single_fucking_note_on_the_goddamn_page = document.getElementsByClassName('modal')
    
    // This holds the modal used by a mentor to add new notes
    const add_modal = Array.from(lst_note_modal).pop()

    // Assuming the 'Add Note' button exists...
    // Show the note creation modal when that button is clicked
    // This handles the note submission process as well
    if(btn_add_note)
    {
        // Show add_modal on button press
        btn_add_note.addEventListener('click', () => add_modal.showModal())

        const btn_submit = add_modal.querySelector('#btn-create-note')      // Submit button
        const title = add_modal.querySelector('#note-title-input');         // Note Title (Input)
        const input_public = add_modal.querySelector('#public-notes');      // Public Note Section
        const input_private = add_modal.querySelector('#private-notes');    // Private Note Section
        const note_form = add_modal.querySelector('#note-form');            // Form wrapper inside modal
        
        // When the submit button is pressed...
        // Assuming there is some actual content in the form, submit it.
        // Otherwise, focus on the empty element.
        btn_submit.addEventListener('click', () => {
            if(title.value.length > 0 && (input_public.value.length > 0 || input_private.value.length > 0)) 
                note_form.submit()
            
            else if(title.value.length == 0)
                title.focus()
            
            else if(input_public.value.length == 0 || input_private.value.length == 0)
                input_public.focus()
        })
    }

    // (Mentee) Show existing notes via modals when the view button is clicked
    if(lst_btn_view_note.length > 0)
        for(let i = 0; i < lst_btn_view_note.length; i++) 
            lst_btn_view_note[i].addEventListener('click', () => lst_note_modal[i].showModal())
    
    // (Mentor) Edit existing notes via modals when the edit button is clicked
    if(lst_btn_edit_note.length > 0)
        for(let i = 0; i < lst_btn_edit_note.length; i++) 
            lst_btn_edit_note[i].addEventListener('click', () => lst_note_modal[i].showModal())
    
    // Allows modals to be exited out of.
    // This code should exist in the modal itself but i don't care it's too late to change that
    // I mean just read some of these variable names!
    if(lst_modal_exit.length > 0)
        for(let i = 0; i < lst_modal_exit.length; i++)
            lst_modal_exit[i].addEventListener("click", () => every_single_fucking_note_on_the_goddamn_page[i].close());


    // Haha this is stinky I hate my life because of this
    // Actually its a far deeper rooted issue than just this function
    // All it does is send a post request to remove a note when the remove button is pressed.
    remove_note = note_id => {
        document.getElementById('loading-overlay').style.display = 'block';

        fetch("/remove_note", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
            },
            body: JSON.stringify({
                'note-id': Number(note_id)
            })
        }).then(response => {
            if (!response.ok) 
                throw new Error('Network response was shit');
            if(response.redirected)
                window.location.href = response.url
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    // Regex for entering a name
    // It looks horrible but its just allowing for appropriately-placed hyphens and apostrophes
    const regex_name = /^[a-zA-Z]+([ \-']{0,1}[a-zA-Z]+){0,2}[.]{0,1}$/ 

    const input_first_name = document.getElementById("firstname-edit")
    const input_last_name = document.getElementById("lastname-edit")

    // Visually indicate (green/red) as a user types if a name is valid
    // This code was stolen from validation.js
    input_first_name.addEventListener("input", e => {
        const input_value = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = input_value;
        const regex_result = regex_name.test(e.target.value)

        // Visually indicate Regex Success
        if(regex_result)
            input_first_name.style.backgroundColor = GREEN
        else
            input_first_name.style.backgroundColor = RED
    })

    // Visually indicate (green/red) as a user types if a name is valid
    // This code was stolen from validation.js
    input_last_name.addEventListener("input", e => {
        const inputValue = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = inputValue;
        const regex_result = regex_name.test(e.target.value)

        // Visually indicate Regex Success
        if(regex_result)
            input_last_name.style.backgroundColor = GREEN
        else
            input_last_name.style.backgroundColor = RED
    })
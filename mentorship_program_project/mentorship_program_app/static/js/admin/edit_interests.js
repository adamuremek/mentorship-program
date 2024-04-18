/*********************************************************************/
/* WRITTEN BY: Logan Zipp                                            */
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
/*      aspects of the administrator 'Edit Interests' modal          */
/* This file is included in 'edit_interests_modal.html'              */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Example Usage:                                                    */
/* <script src="{% static 'js/admin/edit_interests.js' %}"></script> */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

// Contains all pre-existing interest elements 
const active_interests_container = document.getElementById('modal_interests')
// Contains the Add Interest button
const btn_add_interest           = document.getElementById('btn-add-interest')
// Contains the input used to detail a new interest
const input_interest             = document.getElementById('input_new_interest')
// Container for any interests to-be-deleted
const deleted_interests          = document.getElementById('modal_deleted_interests')

// Names of all interests in the modal
let list_interest_inputs         = document.getElementsByClassName('interest-input')
// IDs of all interests in the modal
let list_interest_IDs            = document.getElementsByClassName('interest-id')
// Delete buttons which appear next to each active interest
let list_btn_remove_interest     = document.getElementsByClassName('btn-remove-interest')


// Make edited inputs marked as edited
active_interests_container.querySelectorAll('.interest-input').forEach(interest_input => interest_input.addEventListener('input', () => {
    if(!interest_input.classList.contains('interest-edited'))
        interest_input.classList.add('edited')
}))

// Add event listener to active_interests container
active_interests_container.addEventListener('click', (e) => {
    // If remove button was clicked...
    if (e.target.classList.contains('btn-remove-interest') && !e.target.classList.contains('btn-revert') && e.target.parentElement.classList.contains('active_interest')) {
        const idx = Array.from(list_btn_remove_interest).indexOf(e.target)
        const input = list_interest_inputs[idx]
        const button = e.target
        const id = list_interest_IDs[idx]
        
        const new_container = document.createElement('div')
        // Button is complicated. Sue me. This code sucks and I genuinely don't care.
        // I'm overworked and tired as hell
        // The point of this is to make it so the button will re-add a deleted entry to the 'active' list
        const btn_revert = button.cloneNode(true)
        btn_revert.classList.add('btn-revert')
        btn_revert.innerHTML='+' // Make button visually indicate re-entry

        
        new_container.setAttribute('class', 'modal-interest-container active_interest') 
        new_container.appendChild(input.cloneNode(true))
        new_container.appendChild(id.cloneNode(true))
        new_container.appendChild(btn_revert)
// I am very sad that we have to work on this
// me too, im hoping to be done by 5
// everything works besides this and the request/report button on the profile pages. no idea why theese dont work
// Does the edit interest addition visually work?
// no - fuck
        // Allow deleted entries to be re-added
        // Again, I know this is confusing and I'm sorry.
        btn_revert.addEventListener('click', () => {
            const interest_list = document.getElementById('modal_interests')
            // Remove interest from 'deleted' list
            new_container.remove()
            // Restyle button
            btn_revert.innerHTML = '&#10007;'
            btn_revert.classList.remove('btn-revert')
            // Add interest back to container
            interest_list.appendChild(new_container)
        })

        // Add interest to 'Deleted' list
        deleted_interests.appendChild(new_container)
        deleted_interests.style.display = 'block'
    
        // Remove element from list
        button.parentElement.remove()
    }
}); 

// Enter keypress acts as 'Add Interest' button press
input_interest.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault()
        btn_add_interest.click()
    }
});

// Add a new interest to the list
btn_add_interest.addEventListener('click', () => {
    if(input_interest.value.length > 1) {
        const interest_list = document.getElementById('modal_interests')
        const new_container = document.createElement('div')
        new_container.setAttribute('class', 'modal-interest-container new_interest')
        
        // Create new input element
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('class', 'user-input interest-input');
        input.value = input_interest.value // set input value
        input_interest.value = ''
        
        // Create new button element
        const button = document.createElement('button');
        button.setAttribute('type', 'button');
        button.setAttribute('class', 'btn-remove-interest');
        button.innerHTML = '&#10007;'; // 'X' symbol

        // Create readonly ID field for new interests
        const id = document.createElement('input')
        id.setAttribute('type', 'text');
        id.setAttribute('class', 'user-input interest-id');
        id.disabled = true
        id.value = '#'

        // Delete added interest
        button.addEventListener('click', () => 
        {
            button.remove()
            id.remove()
            input.remove()
        })
        
        // Append input and button to the container
        new_container.appendChild(input);
        new_container.appendChild(id);
        new_container.appendChild(button);
        interest_list.appendChild(new_container);
    }
})

// Add an event listener to the submission button 
document.getElementById('btn-update-interests').addEventListener('click', () => {

    // Interests that are new
    const new_list = document.querySelectorAll('#modal_interests .new_interest .interest-input');
    // Interests that were edited, but already exist
    const deleted_list = document.getElementById('modal_deleted_interests').getElementsByClassName('interest-id')
    // Interests that have been deleted
    const edited_list = document.getElementById('modal_interests').getElementsByClassName('active_interest')

    // Prepare data to be sent to the server
    const form_data = {
        added:   [], // str
        deleted: [], // id
        edited:  [],  // [id, str]
    };
    
    // Add new string values to form_data
    new_list.forEach(item => form_data.added.push(item.value));

    // Add deleted interest information to form_data
    for(item of deleted_list)
        form_data.deleted.push(item.value)
    
    // Add edited interest information to form_data
    // A bit more complicated as the ID and Title must be located
    for (item of edited_list) 
    {
        const inputs = Array.from(item.getElementsByTagName('input')).reverse() // List reversed for backend function
        const edited_interest_data = []
        if(inputs[1].classList.contains('edited')) // Should be string input -> HardCode == bad, but i am going crazy!!!
            for (input of inputs)
                edited_interest_data.push(input.value)
        if(edited_interest_data.length > 0)
            form_data.edited.push(edited_interest_data)
    }    

    // Send POST request to update interest information
    fetch('/update_interests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(form_data)
    })
    .then(response => {
        if (response.ok) {
            // Handle successful response
            console.log('Lists submitted successfully');
            //document.getElementById('interests-modal').close()
            window.location.href = '/dashboard'

        } else {
            // Handle error response
            console.error('Failed to submit lists');
        }
    })
})

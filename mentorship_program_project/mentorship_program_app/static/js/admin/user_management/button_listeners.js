// Import save queue class
import { queue } from './event_queue.js';

// Select user bar elements
const mentee_user_bars = document.querySelectorAll(".mentee_management_bar");
const mentor_user_bars = document.querySelectorAll(".mentor_management_bar");

// Create valid mentee user bar storage
let valid_mentor_user_bars = [];
let invalid_mentor_user_bars = [];

// Update valid mentors
update_mentor_lists();

// Get buttons objects from document
const save_button = document.getElementById("save_button");
const cancel_button = document.getElementById("cancel_button");

// Store constants of event titles
const ADD_MENTEE_EVENT_TYPE = "ADD MENTEE";
const ADD_MENTOR_EVENT_TYPE = "ADD MENTOR";
const EDIT_EVENT_TYPE = "EDIT";
const DELETE_EVENT_TYPE = "DELETE";

// Create queue of events to execute when pressed
const event_queue = new queue;

// Set save button listener
save_button.addEventListener('click', save_event);

// Set cancel button listener
cancel_button.addEventListener('click', cancel_event);

// Set mentee button listeners
set_mentee_button_listeners();

// Set mentor button listeners
set_mentor_button_listeners();


// remove_mentor_button_listeners();

// Functions

// Set up mentee user bar's listeners for every mentee
function set_mentee_button_listeners() 
{
    // Set up mentee user bar's listeners
    for (let mentee_bar of mentee_user_bars)
    {
        // // Get hidden user account values
        // let mentee_id = mentee_bar.querySelector("#user_account");
    
        // Set button listener for view
        mentee_bar.querySelector("#eye_button").addEventListener('click', function() { view_event(mentee_bar); });

        // Check if including adding button
        if (mentee_bar.querySelector("#plus_button") != null)
        {
            // Set button listener for add
            mentee_bar.querySelector("#plus_button").addEventListener('click', function() { add_mentee_event(mentee_bar) });
        }
        
        // Check if include edit button
        if (mentee_bar.querySelector("#edit_button") != null)
        {
            // Set button listener for edit
            mentee_bar.querySelector("#edit_button").addEventListener('click', function() { set_edit_mentor_event(mentee_bar) });
        }

        // Set button listener for delete
        mentee_bar.querySelector("#trashcan_button").addEventListener('click', function() { delete_event(mentee_bar) });
    }
}

// Set up mentor user bar's listeners for every mentor
function set_mentor_button_listeners() 
{
    // Set up mentor user bar's listeners
    for (let mentor_bar of mentor_user_bars)
    {
        // // Get hidden user account values
        // let mentor_id = mentor_bar.querySelector("#user_account");

        // Set button listener for view
        mentor_bar.querySelector("#eye_button").addEventListener('click', function() { view_event(mentor_bar); });
        
        // Set button listener for delete
        mentor_bar.querySelector("#trashcan_button").addEventListener('click', function() { delete_event(mentor_bar) });
    }
}

// // Remove mentor user bar's listeners for every mentor
// function remove_mentor_button_listeners()
// {
//     mentor_user_bars.forEach(mentor_bar => {
//         // mentor_bar.querySelector("#eye_button").removeEventListener("click", view_event);
//         // mentor_bar.querySelector("#trashcan_button").removeEventListener('click', delete_event);

//         mentor_bar.removeEventListener('click', mentor_bar.querySelector("#eye_button"));
//         mentor_bar.removeEventListener('click', mentor_bar.querySelector("#trashcan_button"));

//     });
// }



function save_event() 
{
    // event_queue.enqueue("1");
    // attempt_mentorship_request(1,2);

    // Pass through queue FIFO
    while (!event_queue.isEmpty()) 
    {
        // Store acton value
        current_action = event_queue.dequeue();

        // Sending in offical change depending on action type
        switch(current_action.event_type)
        {
            // Add action
            case("add"):
                // Send request to server
                alert(current_action);

                // attempt_mentorship_request();

                break;

            // Edit action
            case("edit"):
                // Send request to server

                break;

            // Delete action
            case("delete"):
                // Send request to server

                break;

            // Error input
            default:

        }
        // Check if valid
            // Create system log 
            // if valid repeate
            // else break queue on invalid
    }

    // Save event
    alert("Save");
}

function cancel_event()
{
    // Deletes queue elements

    // Cancel event
    alert("Cancel");
}

function view_event(user_bar) 
{
    // MAYBE CANCEL PROGESS WHEN SWITCHING TO ANOTHER PAGE

    // Get hidden user account values
    const user_id = user_bar.querySelector("#user_account");

    // View event
    alert("View\n"+user_id);
}

function add_mentee_event(mentee_bar) 
{
    // Get hidden user account values
    const mentee_id = mentee_bar.querySelector("#user_account");

    // Input add mentee event into queue
    event_queue.enqueue({ADD_MENTEE_EVENT_TYPE, mentee_id});

    // Update event listeners and styles
    update_bar_elements(ADD_MENTEE_EVENT_TYPE, mentee_bar);
    
    // Add event
    alert("Add\n"+mentee_id);
}

function add_mentor_event(mentor_bar)
{  
    // Get hidden user account values
    const mentor_id = mentor_bar.querySelector("#user_account");

    // Input add mentor event into queue
    event_queue.enqueue({ADD_MENTOR_EVENT_TYPE, mentor_id});

    // Update event listeners and styles
    update_bar_elements(ADD_MENTOR_EVENT_TYPE, mentor_bar);


    // Reset mentor event listeners and styles

    // Add mentorship request to event queue

    // Add event
    alert("Add\n"+mentor_id);
}

function edit_event(mentee_bar) 
{    
    // Get hidden user account values
    const mentor_id = mentor_bar.querySelector("#user_account");

    // Update mentor event listeners and styles
    update_bar_elements(EDIT_EVENT_TYPE, mentee_id);

    // Edit event
    alert("Edit\n"+mentee_id);
}

// function edit_mentor_event(mentee_id, mentor_id)
// {
//     // Reset mentor event listeners and styles

//     // Remove mentorship request to event queue

//     // Add mentorship request to event queue
// }

function delete_event(mentee_bar) 
{
    // Update action queue to include delete

    // Update to reflex

    // Delete event
    alert("Delete\n"+mentee_id);
}

function update_bar_elements(event_type, user_bar)
{
    // Determine what type of event
    switch (event_type) 
    {
        // Edit event
        case EDIT_EVENT_TYPE:
            // Find and set prev mentor styling


            // Set prev mentor styling (red or grey out)
            //!!!!!



        // Add mentee event
        case ADD_MENTEE_EVENT_TYPE:
            // Update mentee with styling
            //!!!!!

            break;

        // Add mentor event
        case ADD_MENTOR_EVENT_TYPE:
            // Update mentors with styling
            //!!!!!

            break;

        // Delete event
        case DELETE_EVENT_TYPE:
            
            break;
    
        default:
            break;
    }

    // // TODO WILL USE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // // Update valid mentor styling
    // valid_mentor_user_bars.forEach(valid_mentor_user_bar => {
    //     valid_mentor_user_bar.
    // });

    // // Update invalid mentor styling
    // invalid_mentor_user_bars.forEach(invalid_mentor_user_bar => {
    //     invalid_mentor_user_bar.
    // });

    // Set up event listeners for valid mentors

    // Add event listeners for mentee event
    // mentor_user_bars.forEach(element => {
    //     addEventListener('click', function()
    //     {

    //     })
    // });
}

// Updates which mentor bars are valid
function update_mentor_lists() 
{
    // Remove entries of mentors list
    valid_mentor_user_bars = [];
    invalid_mentor_user_bars = [];

    // Loop through mentor user bar
    mentor_user_bars.forEach(mentor_bar => 
    {
        // Determine if mentor is valid for new mentees
        if (mentor_bar.querySelector("#current_mentees") >= mentor_bar.querySelector("#max_mentees"))
        {
            // // Set mentor user bar id to valid 
            // mentor_bar.id = "user_bar_valid";

            // Add mentor bar to valid mentor bars
            valid_mentor_user_bars.push(mentor_bar);
        }
        else
        {
            // Add mentor bar to invalid mentor bars
            invalid_mentor_user_bars.push(mentor_bar);
        }
    })
}

// Add styles mentors depending on if they are valid, invalid, or prev mentors
function add_mentors_style()
{
    mentor_user_bars.forEach(mentor_bar => {

        if (valid_mentor_user_bars.includes(mentor_bar))
        {

        }
        // Check if valid
            // Set valid
        // Else
            // Set invalid
    });
}

// Removes styles from mentors
function remove_mentors_style()
{

}
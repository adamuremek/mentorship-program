// Import classes from event_queue file 
import { save_event, cancel_event, 
    mentee_clicked_event, view_event, add_mentor_mentee_event, remove_mentor_mentee_event, disable_event, reable_event,
    mentor_clicked_event, select_mentee_mentor_event, promote_organization_mentor_event, transfer_role_mentor_event, edit_organization_mentor_event, decouple_mentor_event,
    organization_clicked_event, remove_organization_event } from './event_queue.js';

// Select and store bar elements
const mentee_bars = document.querySelectorAll(".mentee_management_bar");
const mentor_bars = document.querySelectorAll(".mentor_management_bar_container");
const organization_bars = document.querySelectorAll(".organization_management_bar_container");

// Select and store button elements for user management page
const save_button = document.getElementById("save_button");
const cancel_button = document.getElementById("cancel_button");

// Set save button listener
save_button.addEventListener('click', save_event);

// Set cancel button listener
cancel_button.addEventListener('click', cancel_event);

// Set up mentee bar's listeners
for (let mentee_bar of mentee_bars)
{
    // // Get hidden user account values
    // let mentee_id = mentee_bar.querySelector("#user_account");

    // Set button listener for mentee clicked
    mentee_bar.addEventListener('click', function() { mentee_clicked_event(mentee_bar); });

    // // Set button listener for view
    // mentee_bar.querySelector("#eye_button").addEventListener('click', function() { view_event(mentee_bar); });

    // Set button listener for add
    mentee_bar.querySelector("#plus_button").addEventListener('click', function() { add_mentor_mentee_event(mentee_bar) });

    // Set button listener for remove mentor
    mentee_bar.querySelector("#remove_button").addEventListener('click', function() { remove_mentor_mentee_event(mentee_bar) });

    // Check if there deactivate button 
    if (mentee_bar.querySelector("#trashcan_button") != null)
    {
        // Set button listener for deactivate button
        mentee_bar.querySelector("#trashcan_button").addEventListener('click', function() { disable_event(mentee_bar) });
    }

    // Check if there reactivate button 
    if (mentee_bar.querySelector("#trashcan_off_button") != null)
    {
        // Set button listener for reactivate button
        mentee_bar.querySelector("#trashcan_off_button").addEventListener('click', function() { reable_event(mentee_bar) });
    }
}

// Set up mentor bar's listeners
for (let mentor_bar of mentor_bars)
{
    // // Get hidden user account values
    // let mentor_id = mentor_bar.querySelector("#user_account");

    // Set button listener for mentor clicked
    mentor_bar.addEventListener('click', function() { mentor_clicked_event(mentor_bar); });

    // Set button listener for selecting mentees
    mentor_bar.querySelector(".mentee_counter_container").addEventListener('click', function() { select_mentee_mentor_event(mentor_bar) });
    
    // // Set button listener for view button
    // mentor_bar.querySelector("#eye_button").addEventListener('click', function() { view_event(mentor_bar); });
    
    // Check if there deactivate button 
    if (mentor_bar.querySelector("#trashcan_button") != null)
    {
        // Set button listener for deactivate button
        mentor_bar.querySelector("#trashcan_button").addEventListener('click', function() { disable_event(mentor_bar) });
    }

    // Check if there reactivate button 
    if (mentor_bar.querySelector("#trashcan_off_button") != null)
    {
        // Set button listener for reactivate button
        mentor_bar.querySelector("#trashcan_off_button").addEventListener('click', function() { reable_event(mentor_bar) });
    }

    // Check if there super promote button 
    if (mentor_bar.querySelector("#super_promote_button") != null)
    {
        // Set button listner for super promote button
        mentor_bar.querySelector("#super_promote_button").addEventListener('click', function() { promote_super_mentor_event(mentor_bar) });
    }

    // Set button listener for organization promote button
    mentor_bar.querySelector("#organization_promote_button").addEventListener('click', function() { promote_organization_mentor_event(mentor_bar) });

    // Set button listener for edit organization button
    mentor_bar.querySelector("#edit_organization_button").addEventListener('click', function() { edit_organization_mentor_event(mentor_bar) } );

    // Set button listener for transfer role button
    mentor_bar.querySelector("#transfer_role_button").addEventListener('click', function() { transfer_role_mentor_event(mentor_bar) });

    // Set button listener for decouple button
    mentor_bar.querySelector("#decouple_button").addEventListener('click', function() { decouple_mentor_event(mentor_bar) });

}

// Set organization button listeners
for (let organization_bar of organization_bars)
{
    // Set button listener for organization clicked
    organization_bar.addEventListener('click', function() { organization_clicked_event(organization_bar); });

    // Check if there remove button 
    if (organization_bar.querySelector("#remove_organization_button") != null)
    {
        // Set button listner for super promote button
        organization_bar.querySelector("#remove_organization_button").addEventListener('click', function() { remove_organization_event(organization_bar) });

    }
}



alert("JS activatd");
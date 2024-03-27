// Import classes from event_queue file 
import * as event_queue from './event_queue.js';
import * as filters from './filtering.js';

// Select and store bar elements
const mentee_bars = document.querySelectorAll(".mentee_management_bar");
const mentor_bars = document.querySelectorAll(".mentor_management_bar_container");
const organization_bars = document.querySelectorAll(".organization_management_bar_container");

// Select and store button elements for user management page
const save_button = document.getElementById("save_button");
const cancel_button = document.getElementById("cancel_button");
const filter_user_button = document.querySelector("#filter_users_button");
const filter_organization_button = document.querySelector("#filter_organization_button");

// Select and store search bar elements
const user_search_bar = document.querySelector("#user_search_bar");
const organization_search_bar = document.querySelector("#organization_search_bar");





// Set save button listener
save_button.addEventListener('click', event_queue.save_event);

// Set cancel button listener
cancel_button.addEventListener('click', event_queue.cancel_event);

// Set up search bar selection to trigger attempt filter methods for users and organziation
user_search_bar.addEventListener("input", function() { filters.attempt_user_filter(user_search_bar.value); });
organization_search_bar.addEventListener("input", function() { filters.attempt_organziation_filter(organization_search_bar.value); });

// Set button listener for search buttons
filter_user_button.addEventListener('click', function() { filters.toggle_user_filter(user_search_bar.value); });
filter_organization_button.addEventListener('click', function() { filters.toggle_organization_filter(organization_search_bar.value); });


// TODO NEED TO UPDATE ALL QUERY SELECTERS TO DETEREMINERS


// Set up mentee bar's listeners
for (let mentee_bar of mentee_bars)
{
    // Set button listener for mentee clicked
    mentee_bar.addEventListener('click', function() { event_queue.mentee_clicked_event(mentee_bar); });

    // Set button listener for add
    mentee_bar.querySelector("#plus_button").addEventListener('click', function() { event_queue.add_mentor_mentee_event(mentee_bar) });

    // Set button listener for remove mentor
    mentee_bar.querySelector("#remove_button").addEventListener('click', function() { event_queue.remove_mentor_mentee_event(mentee_bar) });

    // Check if there deactivate button 
    if (mentee_bar.querySelector("#trashcan_button") != null)
    {
        // Set button listener for deactivate button
        mentee_bar.querySelector("#trashcan_button").addEventListener('click', function() { event_queue.disable_event(mentee_bar) });
    }

    // Check if there reactivate button 
    if (mentee_bar.querySelector("#trashcan_off_button") != null)
    {
        // Set button listener for reactivate button
        mentee_bar.querySelector("#trashcan_off_button").addEventListener('click', function() { event_queue.reable_event(mentee_bar) });
    }
}

// Set up mentor bar's listeners
for (let mentor_bar of mentor_bars)
{
    // Set button listener for mentor clicked
    mentor_bar.addEventListener('click', function() { event_queue.mentor_clicked_event(mentor_bar); });

    // Set button listener for selecting mentees
    mentor_bar.querySelector(".mentee_counter_container").addEventListener('click', function() { filters.attempt_mentor_mentee_filter(mentor_bar) });

    // Check if there deactivate button 
    if (mentor_bar.querySelector("#trashcan_button") != null)
    {
        // Set button listener for deactivate button
        mentor_bar.querySelector("#trashcan_button").addEventListener('click', function() { event_queue.disable_event(mentor_bar) });
    }

    // Check if there reactivate button 
    if (mentor_bar.querySelector("#trashcan_off_button") != null)
    {
        // Set button listener for reactivate button
        mentor_bar.querySelector("#trashcan_off_button").addEventListener('click', function() { event_queue.reable_event(mentor_bar) });
    }

    // Check if there super promote button 
    if (mentor_bar.querySelector("#super_promote_button") != null)
    {
        // Set button listner for super promote button
        mentor_bar.querySelector("#super_promote_button").addEventListener('click', function() { event_queue.promote_super_mentor_event(mentor_bar) });
    }

    // Set button listener for organization promote button
    mentor_bar.querySelector("#organization_promote_button").addEventListener('click', function() { event_queue.promote_organization_mentor_event(mentor_bar) });

    // Set button listener for edit organization button
    mentor_bar.querySelector("#edit_organization_button").addEventListener('click', function() { event_queue.edit_organization_mentor_event(mentor_bar) } );

    // SET UP FOR MULT TRANISFER ROLES
    // Set button listener for transfer role button
    mentor_bar.querySelector("#transfer_role_button").addEventListener('click', function() { event_queue.transfer_role_super_admin_mentor_event(mentor_bar) });

    // Set button listener for decouple button
    mentor_bar.querySelector("#decouple_button").addEventListener('click', function() { event_queue.decouple_mentor_event(mentor_bar) });

}

// Set organization button listeners
for (let organization_bar of organization_bars)
{
    // Set button listener for organization clicked
    organization_bar.addEventListener('click', function() { event_queue.organization_clicked_event(organization_bar); });

    // Check if there remove button 
    if (organization_bar.querySelector("#remove_organization_button") != null)
    {
        // Set button listner for super promote button
        organization_bar.querySelector("#remove_organization_button").addEventListener('click', function() { event_queue.remove_organization_event(organization_bar) });

    }
}

alert("JS activatd");
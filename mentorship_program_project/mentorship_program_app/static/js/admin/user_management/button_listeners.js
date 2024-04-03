// Import classes from event_queue file 
import * as event_queue from './event_queue.js';
import * as filters from './filtering.js';
import * as detereminers from './determiners.js';

// Determine and store bar elements
const mentee_bars = detereminers.determine_all_mentee_bars();
const mentor_bars = detereminers.determine_all_mentor_bars();
const organization_bars = detereminers.determine_all_organization_bars();

// Determine and store button elements for user management page
const save_button = detereminers.determine_save_button();
const cancel_button = detereminers.determine_camcel_button();
const filter_user_button = detereminers.determine_filter_user_button();
const filter_organization_button = detereminers.determine_filter_organization_button();

// Select and store search bar elements
const user_search_bar = detereminers.determine_user_search_bar();
const organization_search_bar = detereminers.determine_organization_search_bar();





// Set save button listener
save_button.addEventListener('click', event_queue.save_event);

// Set cancel button listener
cancel_button.addEventListener('click', event_queue.cancel_event);

// Set up search bar selection to trigger attempt filter methods for users and organziation
user_search_bar.addEventListener("input", function() { filters.attempt_user_filter(user_search_bar.value); });
organization_search_bar.addEventListener("input", function() { filters.attempt_organziation_filter(organization_search_bar.value); });

// Set up button listener for search buttons
filter_user_button.addEventListener('click', function() { filters.toggle_user_filter(user_search_bar.value); });
filter_organization_button.addEventListener('click', function() { filters.toggle_organization_filter(organization_search_bar.value); });

// Set up button listern for adding organizations
// TODO 


// Set up mentee bar's listeners
for (let mentee_bar of mentee_bars)
{
    // Set button listener for add
    detereminers.determine_add_button(mentee_bar).addEventListener('click', function() { event_queue.add_mentor_mentee_event(mentee_bar) });

    // Set button listener for remove mentor
    detereminers.determine_remove_button(mentee_bar).addEventListener('click', function() { event_queue.remove_mentor_mentee_event(mentee_bar) });

    // Check if there deactivate button 
    if (detereminers.determine_disable_button(mentee_bar).querySelector("#trashcan_button") != null)
    {
        // Set button listener for deactivate button
        detereminers.determine_disable_button(mentee_bar).addEventListener('click', function() { event_queue.disable_event(mentee_bar) });
    }

    // Check if there reactivate button 
    if (detereminers.determine_enable_button(mentee_bar).querySelector("#trashcan_off_button") != null)
    {
        // Set button listener for reactivate button
        detereminers.determine_enable_button(mentee_bar).addEventListener('click', function() { event_queue.reable_event(mentee_bar) });
    }
}

// Set up mentor bar's listeners
for (let mentor_bar of mentor_bars)
{
    // Set button listener for mentor clicked
    mentor_bar.addEventListener('click', function() { event_queue.mentor_clicked_event(mentor_bar); });

    // Set button listener for selecting mentees filter
    detereminers.determine_mentor_mentee(mentor_bar).addEventListener('click', function() { filters.attempt_mentor_mentee_filter(mentor_bar) });

    // Check if there deactivate button 
    if (detereminers.determine_disable_button(mentor_bar) != null)
    {
        // Set button listener for deactivate button
        detereminers.determine_disable_button(mentor_bar).addEventListener('click', function() { event_queue.disable_event(mentor_bar) });
    }

    // Check if there reactivate button 
    if (detereminers.determine_enable_button(mentor_bar) != null)
    {
        // Set button listener for reactivate button
        detereminers.determine_enable_button(mentor_bar).addEventListener('click', function() { event_queue.reable_event(mentor_bar) });
    }

    // // Check if there super promote button 
    // if (detereminers.determine_promote_super_button(mentor_bar) != null)
    // {
    //     // Set button listner for super promote button
    //     detereminers.determine_promote_super_button(mentor_bar).addEventListener('click', function() { event_queue.promote_super_mentor_event(mentor_bar) });
    // }

    // Set button listener for organization promote button
    detereminers.determine_promote_organization_button(mentor_bar).addEventListener('click', function() { event_queue.promote_mentor_organization_admin_event(mentor_bar) });

    // Set button listener for edit organization button
    detereminers.determine_edit_organization_button(mentor_bar).addEventListener('click', function() { event_queue.edit_organization_mentor_event(mentor_bar) } );

    // Check if there is transfer role super admin button
    if (detereminers.determine_transfer_role_super_admin_button(mentor_bar) != null)
    {
        // Set button listener for transfer role super admin button
        detereminers.determine_transfer_role_super_admin_button(mentor_bar).addEventListener('click', function() { event_queue.transfer_role_super_admin_mentor_event(mentor_bar) });
    }

    // Check if there is transfer role organization admin button
    if (detereminers.determine_transfer_role_organization_admin_button(mentor_bar) != null)
    {
        // Set button listener for transfer role organization admin button
        detereminers.determine_transfer_role_organization_admin_button(mentor_bar).addEventListener('click', function() { event_queue.transfer_role_organization_admin_mentor_event(mentor_bar) });

    }

    // // Set button listener for decouple button
    // detereminers.determine_decouple_button(mentor_bar).addEventListener('click', function() { event_queue.decouple_mentor_event(mentor_bar) });

}

// Set organization button listeners
for (let organization_bar of organization_bars)
{
    // Set button listener for organization clicked
    organization_bar.addEventListener('click', function() { event_queue.organization_clicked_event(organization_bar); });

    // Check if there remove button 
    if (detereminers.determine_remove_organization_button(organization_bar) != null)
    {
        // Set button listner for super promote button
        detereminers.determine_remove_organization_button(organization_bar).addEventListener('click', function() { event_queue.remove_organization_event(organization_bar) });

    }
}

alert("JS activatd");
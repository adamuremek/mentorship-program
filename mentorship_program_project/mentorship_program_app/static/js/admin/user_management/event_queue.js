// Import functions from determiners.js and updaters.js
import * as determiners from "./determiners.js";
import * as updaters from "./updaters.js";
import * as sorters from "./sorting.js";
import * as filters from "./filtering.js";

// Enum values for event types
const EVENT_TYPES = {
    ADD_MENTOR_MENTEE: 'ADD_MENTOR_MENTEE',
    ADD_MENTOR_MENTOR: 'ADD_MENTOR_MENTOR',
    REMOVE_MENTOR_MENTEE: 'REMOVE_MENTOR_MENTEE',
    REMOVE_MENTOR_MENTOR: 'REMOVE_MENTOR_MENTOR',
    DISABLE: 'DISABLE',
    REABLE : 'REABLE',
    PROMOTE_SUPER_FIRST: 'PROMOTE_SUPER_FIRST',
    PROMOTE_SUPER_SECOND: 'PROMOTE_SUPER_SECOND',
    EDIT_ORGANIZATION_MENTOR: 'EDIT_ORGANIZATION_MENTOR',
    EDIT_ORGANIZATION_ORGANIZATION: 'EDIT_ORGANIZATION_ORGANIZATION',
    PROMOTE_ORGANIZATION_MENTOR: 'PROMOTE_ORGANIZATION_MENTOR',
    PROMOTE_ORGANIZATION_ORGANIZATION: 'PROMOTE_ORGANIZATION_ORGANIZATION',    
    TRANSFER_ROLE_ORGANIZATION_FIRST: 'TRANSFER_ROLE_ORGANIZATION_FIRST',
    TRANSFER_ROLE_ORGANIZATION_SECOND: 'TRANSFER_ROLE_ORGANIZATION_SECOND',
    TRANSFER_ROLE_SUPER_FIRST: 'TRANSFER_ROLE_SUPER_FIRST',
    TRANSFER_ROLE_SUPER_SECOND: 'TRANSFER_ROLE_SUPER_SECOND',
    DECOUPLE_MENTOR: 'DECOUPLE_MENTOR',
    DECOUPLE_ORGANIZATION: 'DECOUPLE_ORGANIZATION',
    CREATE_ORGANIZATION: 'CREATE_ORGANIZATION',
    REMOVE_ORGANIZATION: 'REMOVE_ORGANIZATION'

}

class queue
{
    constructor()
    {
        this.events = [];

    }

    enqueue(type, data) 
    {   
        // TODO: Convert to localStorage system
        this.events.push({'type': type, 'data': data});

    }

    dequeue()
    {       
        let return_event = undefined;

        // Check if not empty
        if (!this.isEmpty())
        {
            // Shift and return first value
            return_event = this.events.shift();

        }

        return return_event;

    }

    peek()
    {
        return this.events[0];

    }

    peek_end()
    {
        return this.events[this.events.length - 1];

    }

    cancel()
    {
        this.events = this.events.slice(0, -1);

    }

    isEmpty()
    {
        return (this.events.length == 0);

    }
}

// Create flag storage, initlize all flags to false
let add_mentor_flag = 0;
let remove_mentor_flag = 0;
let edit_organization_flag = 0;
let transfer_role_flag = 0;
let execution_flag = 0;

// Create valid mentee user bar storage
let valid_mentor_bars = []

// Style disabled users bars
updaters.update_all_disable_bar_style_on();

// Style admin bars to remove promote to organization admin button
updaters.update_all_organization_admin_bars();

// Update valid and invalid mentors
valid_mentor_bars = determiners.return_updated_mentor_list();

// Create queue events 
const event_queue = new queue;

// Create arrays for request and created organization ids
const execution_queue = new Array;
const new_organization_ids = new Array;

// Sort all bar elements
sorters.sort_all_bar_elements_alphabetically();





async function execute_events()
{
    // Create storage for starting placeholder id
    let starting_placeholder_id;

    // Initlize last event and valid flags
    let last_event_flag = 0;
    let valid_flag = 1;
    let placeholder_found_flag = 0;

    // Initlize temp new organization counter
    let temp_new_organization_counter = 0;

    // Loop through queue while queue is not empty and execution is valid 
    while (!event_queue.isEmpty() && valid_flag) {
        // Remove event from queue
        let current_event = event_queue.dequeue()

        // Check and set flag if last event
        if (event_queue.isEmpty())
        {
            last_event_flag = 1;
        }

        // Check what type of event 
        switch (current_event.type) 
        {
            // Check for add mentor mentee event
            case EVENT_TYPES.ADD_MENTOR_MENTEE:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if the next event in queue is add mentor mentor event
                    if (event_queue.peek().type == EVENT_TYPES.ADD_MENTOR_MENTOR)
                    {
                        // Set mentor id
                        let mentor_id = event_queue.dequeue().data;

                        // Determine id from passed strings and create mentorship
                        execution_queue.push(attempt_create_mentorship(determiners.determine_id_from_string(current_event.data), 
                            determiners.determine_id_from_string(mentor_id)));

                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Create error queue entry
                    event_queue.enqueue(current_event.type, current_event.data);
                }

                break;

            // Check for remove mentor mentee event
            case EVENT_TYPES.REMOVE_MENTOR_MENTEE:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if the next event in queue is remove mentor mentor event
                    if (event_queue.peek().type == EVENT_TYPES.REMOVE_MENTOR_MENTOR)
                    {
                        // Set mentor id
                        let mentor_id = event_queue.dequeue().data;

                        // Determine id from passed string and remove mentorship
                        execution_queue.push(attempt_delete_mentorship(determiners.determine_id_from_string(current_event.data)));

                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Create error queue entry
                    event_queue.enqueue(current_event.type, current_event.data);
                }

                break;
                
            // Check for disable event
            case EVENT_TYPES.DISABLE:
                // Determine id from passed string and disable user
                execution_queue.push(attempt_disable_user(determiners.determine_id_from_string(current_event.data)));

                break;

            // Check for reable event
            case EVENT_TYPES.REABLE:
                // Determine id from passed string and enable user 
                execution_queue.push(attempt_enable_user(determiners.determine_id_from_string(current_event.data)));

                break;

            // Check for promote organization mentor event
            case EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is promote organization organization event
                    if (event_queue.peek().type == EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION)
                    {
                        // Set organization id
                        let organization_id = event_queue.dequeue().data;

                        // Determeine if organization id is a placeholder
                        if (determiners.determine_if_placeholder_organization_id(organization_id))
                        {
                            // Id is a placeholder
                            // Determine and update new organization id from new organization id array 
                            organization_id = new_organization_ids[determiners.determine_new_organization_placeholder_index(organization_id) - 1];

                        }

                        // Promote organization admin
                        // Determine id from passed string and promote mentor to organization admin
                        execution_queue.push(attempt_promote_mentor_to_organization_admin(determiners.determine_id_from_string(current_event.data)));

                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Create error queue entry
                    event_queue.enqueue(current_event.type, current_event.data);
                }

                break;

            // Check for edit organization mentor event
            case EVENT_TYPES.EDIT_ORGANIZATION_MENTOR:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is edit organization organization event
                    if (event_queue.peek().type == EVENT_TYPES.EDIT_ORGANIZATION_ORGANIZATION)
                    {
                        // Set organization id
                        let organization_id = event_queue.dequeue().data;

                        // Determeine if organization id is a placeholder
                        if (determiners.determine_if_placeholder_organization_id(organization_id))
                        {
                            // Id is a placeholder
                            // Determine and update new organization id from new organization id array 
                            organization_id = new_organization_ids[determiners.determine_new_organization_placeholder_index(organization_id) - 1];

                        }

                        // Equivlent to promoting, there is only one organization admin, will be reaplaced by second mentor id
                        // Determine id from passed string and promote mentor to organization admin
                        execution_queue.push(attempt_edit_mentor_organization(determiners.determine_id_from_string(current_event.data),
                            determiners.determine_id_from_string(organization_id)));

                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Create error queue entry
                    event_queue.enqueue(current_event.type, current_event.data);
                }

                break;

            // Check for transfer role organization first event
            case EVENT_TYPES.TRANSFER_ROLE_ORGANIZATION_FIRST:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is transfer role organization second event
                    if (event_queue.peek().type == EVENT_TYPES.TRANSFER_ROLE_ORGANIZATION_SECOND)
                    {
                        // Set second mentor id
                        let mentor_id = event_queue.dequeue().data;
    
                        // TODO NEED TESTING BUT ABOVE WORKS FINE
                        // Equivlent to promoting, there is only one organization admin, will be reaplaced by second mentor id
                        // Determine id from passed string and promote mentor to organization admin
                        execution_queue.push(attempt_promote_mentor_to_organization_admin(determiners.determine_id_from_string(mentor_id)));
                        
                    }
                }

                break;

            // Check for transfer role super first event
            case EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is transfer role super second event
                    if (event_queue.peek().type == EVENT_TYPES.TRANSFER_ROLE_SUPER_SECOND)
                    {
                        // Set second mentor id
                        let mentor_id = event_queue.dequeue().data;

                        // Equivlent to promoting, there is only one organization admin, will be reaplaced by second mentor id
                        // Determine id from passed string and promote mentor to organization admin
                        execution_queue.push(attempt_promote_mentor_to_organization_admin(determiners.determine_id_from_string(mentor_id)));

                    }
                }

                break;

            // Check for decouple mentor event
            case EVENT_TYPES.DECOUPLE_MENTOR:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is decouple organization event
                    if (event_queue.peek().type == EVENT_TYPES.DECOUPLE_ORGANIZATION)
                    {
                        // Set organization id
                        let organization_id = event_queue.dequeue().data;

                        // Determeine if organization id is a placeholder
                        if (determiners.determine_if_placeholder_organization_id(organization_id))
                        {
                            // Id is a placeholder
                            // Determine and update new organization id from new organization id array 
                            organization_id = new_organization_ids[determiners.determine_new_organization_placeholder_index(organization_id) - 1];
                                
                        }

                        // Remove orgaization relationship from mentor
                        execution_queue.push(attempt_remove_mentors_org(determiners.determine_id_from_string(current_event.data),
                            determiners.determine_id_from_string(organization_id)));

                    }
                }

                break;

            // Check for create organization event
            case EVENT_TYPES.CREATE_ORGANIZATION:
                // Check if placeholder organization is not already found
                if (!placeholder_found_flag)
                {
                    // Deteremine starting placeholder id by finding next created organization id then adding 
                    starting_placeholder_id = (Number( determiners.determine_id_from_string( await attempt_get_next_created_organization_id()) ) + 1);

                    // Update placeholder found flag to be true
                    placeholder_found_flag = 1;

                }

                // Store dynamically determeined organziation ids in new organization id array at inverted index 
                new_organization_ids[temp_new_organization_counter] = "Organization object (" + (starting_placeholder_id + temp_new_organization_counter) + ")"
            
                // Update temp new organizatio counter to increase by 1
                temp_new_organization_counter++;

                // Determine id from string and create organization
                execution_queue.push(attempt_create_new_organziation(current_event.data));

                break;

            // Check for remove organization event
            case EVENT_TYPES.REMOVE_ORGANIZATION:
                // Set organization id
                let organization_id = current_event.data;

                // Determeine if organization id is a placeholder
                if (determiners.determine_if_placeholder_organization_id(organization_id))
                {
                    // Id is a placeholder
                    // Determine and update new organization id from new organization id array 
                    organization_id = new_organization_ids[determiners.determine_new_organization_placeholder_index(organization_id) - 1];
                        
                }

                // Determine id from string and remove organization
                execution_queue.push(attempt_remove_organization(determiners.determine_id_from_string(organization_id)));
            
                break;
        
            // Check for invalid ordering of event
            default:
                // Set valid flag to false
                valid_flag = 0;

                if (current_event == undefined)
                {
                    // Create error entry in queue for unknown event
                    event_queue.enqueue("Unknown event", "");

                }
                else
                {
                    // Create error entry in queue for current event
                    event_queue.enqueue(current_event.type, current_event.data);


                }

                break;
            
        }
    }
    
    // Return boolean if exeuection is valid
    return valid_flag;

}

// Function removes all elements within the event queue without executing them
function remove_queue_elements()
{   
    // Loop through event queue till empty
    while (!event_queue.isEmpty()) 
    {
        // Remove event from event queue
        event_queue.dequeue();

    }
}

// Function checks if the queue is not empty and then will check for flag and first events for add mentor, remove mentor, 
// edit organiztion, or transfer role. Else will do nothing
export function check_cancel_event()
{
    // Check if event queue is not empty
    if (!event_queue.isEmpty())
    {
        // Check if add event is in progress and last event is a add mentor mentee event
        if (add_mentor_flag && event_queue.peek_end().type == EVENT_TYPES.ADD_MENTOR_MENTEE)
        {
            // Cancel add mentor event
            cancel_add_mentor_event();

        }
        // Check if remove event is in progress and last event is a remove mentor event
        else if (remove_mentor_flag && event_queue.peek_end().type == EVENT_TYPES.REMOVE_MENTOR_MENTEE)
        {
            cancel_remove_mentor_event();

        }
        // Check if edit organization is in progess and last event is a edit organization mentor event
        else if (edit_organization_flag && event_queue.peek_end().type == EVENT_TYPES.EDIT_ORGANIZATION_MENTOR)
        {
            cancel_edit_organization_event();

        }
        // Check if transfer role is in progress and last event is a transfer role super first event
        else if (transfer_role_flag && event_queue.peek_end().type == EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST)
        {
            cancel_transfer_role_event();

        }
    }
}

// Function remvoes the last queue in the event queue, then resets the add mentor flag, then update buttons
function cancel_add_mentor_event()
{
    // Determine prev user bar
    const mentee_bar = determiners.return_mentee_bar_from_user_id(event_queue.peek_end().data);

    // Remove add mentor mentee event
    event_queue.cancel();

    // Reset add mentor flag
    add_mentor_flag = 0;

    // Reset bar styles
    updaters.update_reset_choice_bar_styles();

    // Determine and reset button style
    updaters.update_off_button_style(determiners.determine_add_button(mentee_bar));

}

// Function remvoes the last queue in the event queue, then resets the remove mentor flag, then update buttons
function cancel_remove_mentor_event()
{
    // Determine prev user bar
    const mentee_bar = determiners.return_mentee_bar_from_user_id(event_queue.peek_end().data);

    // Remove remove mentor mentee event
    event_queue.cancel();

    // Reset remove mentor flag
    remove_mentor_flag = 0;

    // Reset bar styles
    updaters.update_reset_choice_bar_styles();

    // Determine and reset remove button style
    updaters.update_off_button_style(determiners.determine_remove_button(mentee_bar));

}

// Function remvoes the last queue in the event queue, then resets the edit organiztion flag, then update buttons
function cancel_edit_organization_event()
{
    // Determine prev user bar
    const mentor_bar = determiners.return_mentor_bar_from_id(event_queue.peek_end().data);

    // Remove promote organzation event
    event_queue.cancel();

    // Reset promote organzation flag
    edit_organization_flag = 0;

    // Reset bar styles
    updaters.update_reset_choice_bar_styles();

    // Determeine and reset edit organiztion button style
    updaters.update_off_button_style(determiners.determine_edit_organization_button(mentor_bar));

}

// Function remvoes the last queue in the event queue, then resets the transfer role flag, then update buttons
function cancel_transfer_role_event()
{
    // Determine prev user bar
    const mentor_bar = determiners.return_mentor_bar_from_id(event_queue.peek_end().data);

    // Remove promote organzation event
    event_queue.cancel();

    // Reset transfer role flag
    transfer_role_flag = 0;
    
    // Reset bar styles
    updaters.update_reset_choice_bar_styles();

    // Determine and reset transfer role button button style
    updaters.update_off_button_style( determiners.determine_transfer_role_super_admin_button(mentor_bar));

}























// Nonexported event functions
// Takes pased organziation bar will cancel in progress event creation, checks if mentor bar is not undefined, the last event was a edit organization mentor event,
// and mentor bar is valid to be added to current organization bar. If valid will remove mentor from prev organization if included in one, add mentor to current 
// organization bar, update bar and button elements, then create a edit organization organization event and reset edit organization flag. Else will do nothing.
function edit_organization_event(organization_bar)
{
    // Create storage for prev organziation bar
    let prev_organization_bar;

    // Determine organization id from hidden value in passed organization bar
    const organization_id = determiners.determine_organization_id(organization_bar);

    // Store last event
    const prev_event = event_queue.peek_end();

    // Find mentor bar from user id
    const mentor_bar = determiners.return_mentor_bar_from_id(prev_event.data);

    // Check if mentor_bar is not undefined and it is not the same id as prev organitization
    if (mentor_bar != undefined)
    {
        // Determine if user bar is valid to transfer last event is an promote organzation mentor event and last event is an promote organzation mentor event
        if (determiners.determine_if_bars_valid_edit_organzation(organization_bar, mentor_bar) && prev_event.type == EVENT_TYPES.EDIT_ORGANIZATION_MENTOR)
        {
            // Determine parent organization of prev event user
            prev_organization_bar = determiners.determine_parent_organization_bar_element(mentor_bar)
            
            // Check mentor was part of another organization
            if (prev_organization_bar != null)
            {
                // Remove mentor from prev organization bar
                updaters.update_remove_from_organization(prev_organization_bar, mentor_bar);

            }

            // Add mentor bar to organization bar
            updaters.update_add_to_organization(organization_bar, mentor_bar);

            // Determine and pass edit organization button to be set off
            updaters.update_off_button_style(determiners.determine_edit_organization_button(mentor_bar));

            // Determine and pass mentor list from organization to sorting for mentor bar elements
            sorters.sort_mentor_bar_elements_alphabetically(determiners.determine_organization_mentor_list(organization_bar));

            // Sort all organiation bars
            sorters.sort_all_organization_bar_element_alphabetically();

            // Reset bar styles
            updaters.update_reset_choice_bar_styles();

            // Update organization transfer buttons
            updaters.update_organization_transfer_buttons(organization_bar);

            // Create and store promote organzation organization event in queue
            event_queue.enqueue(EVENT_TYPES.EDIT_ORGANIZATION_ORGANIZATION, organization_id);

            // Reset edit event flag
            edit_organization_flag = 0;

        }
    }
}

// Function takes in user bar element, will cancel in progress event creation, attempts to create mentorship between a mentee and 
// mentor. Checks if the last event was a add mentor mentee event and the mentee bar is not undefined, If so will update mentee bar
// to add mentor data from it, update mentor bar to add mentee data from it, update button and bar styles to be updated and off, will 
// create add mentor mentor event with current user id, then reset add flag. Else will do nothing.
function add_mentor_event(user_bar)
{
    // Store last event
    const prev_event = event_queue.peek_end();

    // Determine user id of clicked mentor
    const user_id = determiners.determine_user_id(user_bar);

    // Determine prev user bar from id
    const prev_user_bar = determiners.return_mentee_bar_from_user_id(prev_event.data);

    // Determine add buttons from mentee bar
    const add_mentee_button = determiners.determine_add_button(prev_user_bar);

    // Determine if last event is an add mentor mentee event
    if (prev_event.type == EVENT_TYPES.ADD_MENTOR_MENTEE & prev_user_bar != undefined) 
    {                    
        // Pass mentee bar and mentor id and update mentee bar
        updaters.update_mentee_bar_add(prev_user_bar, user_id);

        // Update mentor bar
        updaters.update_incerment_mentor_mentees(user_bar, prev_event.data);

        // Pass button and reset button to be off
        updaters.update_off_button_style(add_mentee_button)

        // Reset bar styles
        updaters.update_reset_choice_bar_styles();

        // Create and store add mentor mentee event in queue
        event_queue.enqueue(EVENT_TYPES.ADD_MENTOR_MENTOR, user_id);

        // Reset add event flag
        add_mentor_flag = 0;

    }

}

// Function takes in user bar element, will cancel in progress event creation, attempts to remove mentorship between a mentee and 
// mentor. Checks if the last event was a remove mentor mentee event and the mentee is list as having a mentorship with mentor, If so will 
// will update mentee bar to remove mentor data from it, update mentor bar to remove mentee data from it, update button and bar styles 
// to be updated and off, will create remove mentor mentor event with current user id, then reset remove flag. Else will do nothing.
function remove_mentor_event(user_bar)
{
    // Store last event
    const prev_event = event_queue.peek_end();

    // Determine user id of clicked mentor
    const user_id = determiners.determine_user_id(user_bar);

    // Create stroage for temp user bar
    const prev_user_bar = determiners.return_mentee_bar_from_user_id(prev_event.data);

    // Determine user mentee element from user bar
    const user_mentees = determiners.determine_mentees_value(user_bar);

    // Determine remove button from mentee bar
    const remove_mentee_button = determiners.determine_remove_button(prev_user_bar);

    // Create mentee list from mentee list string
    const mentee_id_list = determiners.return_array_from_string(user_mentees);

    // Determine if last event is an remove mentor mentee event and mentee is included in mentee list
    if (prev_event.type == EVENT_TYPES.REMOVE_MENTOR_MENTEE & mentee_id_list.includes(prev_event.data))
    {
        // Update mentee bar
        updaters.update_mentee_bar_remove(prev_user_bar);

        // Update mentor bar to include 1 less mentee and list
        updaters.update_decerment_mentor_mentees(user_bar, prev_event.data);

        // Pass button and reset button to be off
        updaters.update_off_button_style(remove_mentee_button);

        // Reset bar styles
        updaters.update_reset_choice_bar_styles();

        // Create and store remove mentor mentor event in queue
        event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, user_id);

        // Reset remove event flag
        remove_mentor_flag = 0;

    }

}

// Function takes in user bar element, will cancel in progress event creation, attempts to transfer roles between 2 mentor. 
// Checks if the last event was a transfer role super first event and the organization for both mentors is the same, 
// and one is an organization admin and the other is a mentor within the organization. If so will demote the current organization
// admin and then promote either current or prev user based on which is not the organization admin, update button and bar styles 
// to be updated and off, then will remove prev event and add current mentor id as first event data then add the prev event id as second 
// event data if current user is organziation admin, else will create second event with current mentor id, then reset transfer flag. 
// Else will do nothing.
function transfer_role_event(user_bar)
{
    // Create storage for currrent and prev mentor ids
    let current_id, prev_id;

    // Initlize current user org flag to false 
    let current_user_org_admin_flag = false;

    // Store last event
    let prev_event = event_queue.peek_end();

    // Create stroage for temp user bar
    const prev_user_bar = determiners.return_mentor_bar_from_id(prev_event.data);

    // Determine transfer role button from mentor bar
    const transfer_role_button = determiners.determine_transfer_role_super_admin_button(prev_user_bar);

    // Determine prev user bar to determine parent organization bar element
    const prev_organitization_bar = determiners.determine_parent_organization_bar_element(prev_user_bar);

    // Determine organization bar from user bar
    const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

    // Determine if last event is an transfer role event and if mentors are within the same organization
    if (prev_event.type == EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST & prev_organitization_bar == organization_bar)
    {
        // Determine if prev user bar is organization admin and current user bar is not organization admin or if prev user bar is not organization admin and current user bar is organization admin
        if (determiners.determine_if_bars_valid_transfer(organization_bar, prev_user_bar, user_bar)) 
        {
            // Set current user mentor id 
            current_id = determiners.determine_id(user_bar);

            // Determine if current user bar is a organization admin
            if (determiners.determine_if_bar_organization_admin(organization_bar, user_bar))
            {
                // Set current user org flag to true
                current_user_org_admin_flag = true;

            }

            // Remove mentor bars from admin list to mentor list
            updaters.update_demote_organization_admin(organization_bar);

            // Check if current user is the organization admin
            if (current_user_org_admin_flag)
            {
                // Current user is organization admin
                // Prmote prev mentor to organization admin 
                updaters.update_promote_organization_admin(organization_bar, prev_user_bar);

            }
            else 
            {
                // Current user is not organization admin
                // Prmote current mentor to organization admin
                updaters.update_promote_organization_admin(organization_bar, user_bar);

            }

            // Pass button and reset button to be off
            updaters.update_off_button_style(transfer_role_button);

            // Determine and pass mentor list mentor list and refresh sorting for mentor bar elements
            sorters.sort_mentor_bar_elements_alphabetically(determiners.determine_organization_mentor_list(organization_bar));

            // Reset bar styles
            updaters.update_reset_choice_bar_styles();

            // Update organization transfer buttons
            updaters.update_organization_transfer_buttons(organization_bar);

            // Check if current user is the organization admin
            if (current_user_org_admin_flag)
            {
                // Current user is organization admin
                // Setting prev mentor id while removing prev event in queue
                prev_id = event_queue.dequeue().data;

                // Create and store transfer role event in queue 
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST, current_id);
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_SUPER_SECOND, prev_id);

            }
            else 
            {
                // Current user is not organization admin                
                // Determine mentor id, then create and store transfer role events in queue
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_SUPER_SECOND, current_id);


            }

            // Reset transfer role flag
            transfer_role_flag = 0;

        }
    }

}





// Exported event functions
// Function will cancel in progress event creation, attempt to execute events in event queue, if valid then will update user management page
// message to successful save message, else will update user management message to unsucessful save message and remove and queue elements.
export async function save_event()
{
    // Check execution flag is not true
    if (!execution_flag)
    {
        // Intintlize valid flag to false
        let valid_flag = false;

        // Set execution flag to be true
        execution_flag = 1;

        // Determine user mangement message element
        const user_management_message = determiners.determine_user_management_message();

        // Set loading overlay to show 
        updaters.update_loading();

        // Check and cancel last event if needed
        check_cancel_event();

        // Deteremine if event queue is valid
        valid_flag = await execute_events();

        // Check valid flag
        if (valid_flag)
        {
            // Set valid flag execute request queue value
            valid_flag = await execute_request(execution_queue);

            // Check if not valid reponse
            if (!valid_flag)
            {
                // Create and store error event in queue
                event_queue.enqueue("Database error", "Invalid request to database");

            }
        }

        // Check if valid execution
        if (valid_flag)
        {
            // Update user management message with successful message
            user_management_message.innerHTML = "Save Successful";

            // Update user management to be visable
            updaters.update_show(user_management_message);

            // Refresh page
            location.reload();
            
        }
        // Else save was unsuccessful
        else
        {
            // Store current event in queue
            const current_event = event_queue.dequeue();

            // Update user management message with unsucessful message
            user_management_message.innerHTML = "Error: type = " + current_event.type + ", data = " + current_event.data;

            // Update user management to be visable
            updaters.update_show(user_management_message);

            // Remove queue elements
            remove_queue_elements();

            // Set loading overlay to not show
            updaters.update_not_loading();

        }

        // Set exectuon flag to be off
        execution_flag = 0;

    }
}

// Function will remove and user mangement message being displayed if queue is empty, else will update message to display a cancel
// message, remove all queue elements, then refresh the page to reset elements if not empty.
export function cancel_event()
{
    // Determine user mangemenet message element
    const user_management_message = determiners.determine_user_management_message();

    // Check if event queue is empty
    if (event_queue.isEmpty())
    {
        // Queue is empty
        // Update user management to be hidden
        updaters.update_not_show(user_management_message);

    }
    else
    {
        // Queue is not empty
        // Update user mangement message to show canceled events
        user_management_message.innerHTML = "Canceled queue of events";

        // Update user management to be visable
        updaters.update_show(user_management_message);

        // Cancel queue
        remove_queue_elements();

        // Refresh page
        location.reload();

    }
}

export function mentee_clicked_event(mentee_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(mentee_bar))
    {
        alert("mentee clicked");

    }
}

export function view_event(user_bar)
{
    // Determeine user account value
    const user_id = determiners.determine_user_id(user_bar);

    // Check and cancel last event if needed
    check_cancel_event();

    // Check that user id is not null
    if (user_id != null)
    {
        // Attempt to view user profile page
        view_profile(determiners.determine_id_from_string(user_id));
        
    }
}

export function view_mentee_event(user_bar)
{
    // Check and cancel last event if needed
    check_cancel_event(); 

    // Attempt to filter mentee bars by clicked user bar
    filters.attempt_mentor_mentee_filter(user_bar);

}

// Function will takes in user bar, checks it is not disabled or toggled and has a mentor, cancel in progress event creation. If disabled will do
// nothing, else if toggled will update button style to remove active, else will update and style button then create a add mentor mentee event using 
// current user id.
export function add_mentor_mentee_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Intitlize toggle flag to 0
        let toggle_flag = 0;

        // Determine id from hidden value in passed user bar
        // const user_id = determiners.determine_id(user_bar);
        const user_id = determiners.determine_user_id(user_bar);

        // Determine add button from user bar
        const add_mentor_button = determiners.determine_add_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = determiners.deteremine_if_event_toggle(event_queue.peek_end(), EVENT_TYPES.ADD_MENTOR_MENTEE, user_id);

        }

        // Check and cancel last event if needed
        check_cancel_event();

        // Check if button was toggled
        if (!toggle_flag)
        {
            // Last event was different, cont. exeuction normally 
            // Set add mentor flag on
            add_mentor_flag = 1;

            // Pass button and style button to be on
            updaters.update_on_button_style(add_mentor_button);

            // Style valid mentor bars
            updaters.update_valid_choice_bar_styles(valid_mentor_bars);

            // Create and store add mentor mentee event in queue
            event_queue.enqueue(EVENT_TYPES.ADD_MENTOR_MENTEE, user_id);

        }
        else 
        {
            // Last event was the same cancel without attempting to create event
            // Pass button and reset button to be off 
            updaters.update_off_button_style(add_mentor_button);

        }
    }
}

// Function will takes in user bar, checks it is not disabled or toggled and has a mentor, cancel in progress event creation. If disabled will do
// nothing, else if toggled will update button style to remove active, else will update and style button then create a remove mentor mentee event using 
// current user id.
export function remove_mentor_mentee_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Intitlize toggle flag to 0
        let toggle_flag = 0;

        // Determine id and mentor from hidden value in passed user bar
        // const user_id = determiners.determine_id(user_bar);
        const user_id = determiners.determine_user_id(user_bar);
        const mentor_id = determiners.determine_mentor_id(user_bar);

        // Determine remove button from user bar
        const remove_mentor_button = determiners.determine_remove_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = determiners.deteremine_if_event_toggle(event_queue.peek_end(), EVENT_TYPES.REMOVE_MENTOR_MENTEE, user_id);

        }

        // Check and cancel last event if needed
        check_cancel_event();

        // Check if button was toggled
        if (!toggle_flag)
        {   
            // Last event was different, cont. exeuction normally
            // Set remove flag
            remove_mentor_flag = 1;

            // Find mentor bar using mentor id
            // const mentor_bar = determiners.return_mentor_bar_from_id(mentor_id);
            const mentor_bar = determiners.return_mentor_bar_from_user_id(mentor_id);

            // Check if mentor_bar is not undefined
            if (mentor_bar != undefined)
            {
                // Pass button and style button to be on
                updaters.update_on_button_style(remove_mentor_button)

                // Style mentee's mentor bar
                updaters.update_remove_choice_bar_style(mentor_bar);

                // Create and store remove mentor mentee event in queue
                event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, user_id);

            }
        }
        else
        {
            // Last event was the same cancel without attempting to create event
            // Pass button and reset button to be off 
            updaters.update_off_button_style(remove_mentor_button);

        }
    }
}

// Function takes in user_bar, checks it is not disabled, updates bar styling to be be disabled, updates valid mentor list,
// then creates disable event with current user id.
export function disable_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Create storage for mentee id, mentor bar, and selected mentee bars
        let mentee_id, mentor_bar, selected_mentee_bars;

        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Check and cancel last event if needed
        check_cancel_event();

        // Check if there is hidden mentor element 
        if (determiners.determine_if_bar_mentee(user_bar))
        {
            // User bar is a mentee
            // Determine and set mentor id value 
            mentee_id = determiners.determine_mentor_id(user_bar);

            // Check if there is a mentee_id
            if (mentee_id != "None")
            {
                // Determine and set mentor bar from id
                // const mentor_bar = determiners.return_mentor_bar_from_id(mentee_id);
                mentor_bar = determiners.return_mentor_bar_from_user_id(mentee_id);

                // Update mentee bar to remove mentor and update to have add button
                updaters.update_mentee_bar_remove(user_bar);

                // Check if there is a mentor
                if (mentor_bar != null)
                {
                    // Update mentor bar to remove mentee from mentee list
                    updaters.update_decerment_mentor_mentees(mentor_bar, mentee_id);

                }
            }
        }
        else
        {
            // User bar is a mentor
            // Determine and selected mentee list from determining mentee list string 
            selected_mentee_bars = determiners.return_mentee_bars_from_ids(determiners.return_array_from_string(determiners.determine_mentees_value(user_bar)));

            // Cycle through mentee bars
            selected_mentee_bars.forEach(mentee_bar => {

                // Update mentee bar to remove mentor and update to have add
                updaters.update_mentee_bar_remove(mentee_bar);

                // Determine mentee id from mentee bar
                mentee_id = determiners.determine_id(mentee_bar);

                // Update mentor bar to remove mentee id and decremenent
                updaters.update_decerment_mentor_mentees(user_bar, mentee_id);

            });
        }

        // Update bar to be disabled 
        updaters.update_disable_bar(user_bar);

        // Update valid mentor list
        valid_mentor_bars = determiners.return_updated_mentor_list();

        // Create and store deactivate event in queue
        event_queue.enqueue(EVENT_TYPES.DISABLE, user_id);

    }
}

// Function takes in user_bar, checks it is disabled, updates bar styling to be be reabled, updates valid mentor list,
// then creates reable event with current user id.
export function reable_event(user_bar)
{   
    // Check if account is disabled
    if (determiners.determine_disabled_value(user_bar))
    {
        // Check and cancel last event if needed
        check_cancel_event();

        // Update bar to be reable
        updaters.update_reable_bar(user_bar);

        // Update valid mentor list
        valid_mentor_bars = determiners.return_updated_mentor_list();

        // Determine user if then create and store deactivate event in queue
        event_queue.enqueue(EVENT_TYPES.REABLE, determiners.determine_user_id(user_bar));

    }
}

// Function takes a user bar, checks it is not disabled and the event queue is empty, checks if add, remove, or
// transfer flags are active, if, if any are active will check that ids dont match, pass the user bar element 
// to have the operation preformed, then will update valid mentors bar list in case any updates occured to 
// invalidate or revalidate a user.
export function mentor_clicked_event(user_bar)
{
    // Check if account is not disabled and event queue is not empty 
    if (!determiners.determine_disabled_value(user_bar) & !event_queue.isEmpty())
    {
        // Store last event
        const prev_event = event_queue.peek_end();

        // Check if add or remove flag is on
        if (add_mentor_flag | remove_mentor_flag)
        {
            // Check if prev event user and current user ids are different
            if (prev_event.data !=  determiners.determine_user_id(user_bar))
            {
                // Check for a add event flag and current user bar is valid for adding mentors
                if (add_mentor_flag & determiners.determine_if_mentor_included_in_passed_bars(valid_mentor_bars, user_bar))
                {
                    add_mentor_event(user_bar)

                }
                    
                // Check for a remove event flag
                if (remove_mentor_flag)
                {
                    remove_mentor_event(user_bar)

                }
            }
        }
        // Else check if transfer flag is on
        else if (transfer_role_flag)
        {
            // Check if prev event user and current mentor ids are different and transfer role is active
            if (prev_event.data != determiners.determine_id(user_bar) & transfer_role_flag)
            {
                transfer_role_event(user_bar);

            }
        }

        // Update valid mentors
        valid_mentor_bars = determiners.return_updated_mentor_list();
    
    }
}

// Function takes in user bar element, will cancel in progress event creation, attempts to promote mentor to organization adminn and add promote organization admin event,
// Checks if user bar's organziation bar is valid, if so will demote current organization admin, promote passed user bar organization, update button styling, sort bar mentor elements,
// within organization, then create an promote mentor to organization admin event, else will do nothing.
export function promote_mentor_organization_admin_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_id(user_bar);

        // Determine organization bar from user bar
        const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

        // Check and cancel last event if needed
        check_cancel_event();

        // Check for user bar to be within organization bar
        if (organization_bar != null)
        {
            // Remove mentor bars from admin list to mentor list
            updaters.update_demote_organization_admin(organization_bar);

            // Promote mentor bar from mentor list to admin list
            updaters.update_promote_organization_admin(organization_bar, user_bar);

            // Update organization transfer buttons
            updaters.update_organization_transfer_buttons(organization_bar);

            // Determine and pass mentor list from organziation and refresh sorting for mentor bar elements
            sorters.sort_mentor_bar_elements_alphabetically(determiners.determine_organization_mentor_list(organization_bar));

            // Create and store promote organization mentor event in queue
            event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR, user_id);

            // Determine organziation id from organization bar, then create and store promote organization organzation event in queue
            event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION, determiners.determine_organization_id(organization_bar));

        }
    }
}

// Function takes in user bar element, will cancel in progress event creation, attempts to toggle event and button for editing organization for mentor.
// Checks if event is toggled, if so will turn off button styling and remvoe event in queue else will turn on edit organization flag, button and valid bar styling,
// then add a edit organziaton event.
export function edit_organization_mentor_event(user_bar)
{
    // Intitlize toggle flag to 0
    let toggle_flag = 0; 

    // Determine user id from hidden value in passed user bar
    const user_id = determiners.determine_id(user_bar);

    // Determine edit organization button
    const edit_organization_button = determiners.determine_edit_organization_button(user_bar);

    // Check if queue is not empty
    if (!event_queue.isEmpty())
    {
        // Check if same button was already pressed before
        toggle_flag = determiners.deteremine_if_event_toggle(event_queue.peek_end(), EVENT_TYPES.EDIT_ORGANIZATION_MENTOR, user_id);

    }

    // Check and cancel last event if needed
    check_cancel_event();

    // Check if button was toggled
    if (!toggle_flag)
    {
        // Last event was different, cont. exeuction normally 
        // Set edit organization flag on
        edit_organization_flag = 1;

        // Pass button and style button to be on
        updaters.update_on_button_style(edit_organization_button);

        // Determine organization bar and all but passed organziation bars and style them
        updaters.update_valid_choice_bar_styles(determiners.return_list_all_but_passed_organiztion_bar(determiners.determine_parent_organization_bar_element(user_bar)));
        
        // Create and store add mentor mentee event in queue
        event_queue.enqueue(EVENT_TYPES.EDIT_ORGANIZATION_MENTOR, user_id);

    }
    else
    {
        // Last event was the same cancel without attempting to create event
        // Pass button and reset button to be off 
        updaters.update_off_button_style(edit_organization_button);

        // Remove event from queue
        event_queue.dequeue();

    }
}

// Function takes in user bar element, will cancel in progress event creation, then attempts to transfer roles between the user bar and session user bar and add an transfer role event to queue. 
// Checks if the users are valid for transfer by checking if within the same organization, one is a organization admin and the other a organization mentor, if so will 
// demote organization admin, then promote the user bar to organziation admin, update button styling, sort oraganization mentors, then add transfer role event to queue. 
// Else will do nothing.
export function transfer_role_organization_admin_mentor_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Determine organization bar from user bar
        const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

        // Determine session user bar
        const session_user_bar = determiners.determine_session_user_bar();

        // Check and cancel last event if needed
        check_cancel_event();

        // Check for user bar to be within organization bar
        if (organization_bar != null)
        {
            // Determine session user organization and check if it is the same as the user organization bar, the users are valid for transfer, 
            // and the session user is organization admin for user bar's organization
            if (organization_bar == determiners.determine_parent_organization_bar_element(session_user_bar) && 
                determiners.determine_if_bars_valid_transfer(organization_bar, user_bar, session_user_bar) &&
                determiners.determine_if_bar_organization_admin(organization_bar, session_user_bar))
            {
                // Demote organzation admin 
                updaters.update_demote_organization_admin(organization_bar);

                // Promote user bar to session
                updaters.update_promote_organization_admin(organization_bar, user_bar);

                // Determine and pass mentor list from organziation to refresh sorting for mentor bar elements
                sorters.sort_mentor_bar_elements_alphabetically(determiners.determine_organization_mentor_list(organization_bar));
                    
                // Update organization transfer buttons
                updaters.update_organization_transfer_buttons(organization_bar);

                // Determine session user id and user id from session user bar, then create and store transfer role organzation style event in queue
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_ORGANIZATION_FIRST, determiners.determine_id(session_user_bar));
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_ORGANIZATION_SECOND, determiners.determine_id(user_bar));

            }
        }
    }
}

// Function takes in a user bar element, will cancel in progress event creation, attempts to toggle event and button for transfering roles between user with organization. Checks if account is 
// disabled or event is toggled, if disabled then wont process anything, else if toggled then will turn off button styling and remove event in queue else 
// will turn on transfer role flag, button and valid bar styling, then add a transfer role event. 
export function transfer_role_super_admin_mentor_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Create storage for mentor and admin list
        let valid_organization_mentors;

        // Initlize toggle flag to 0
        let toggle_flag = 0;

        // Create storage for current organization bar
        let organization_bar;

        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_id(user_bar);

        // Determine transfer role button
        const transfer_role_button = determiners.determine_transfer_role_super_admin_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = determiners.deteremine_if_event_toggle(event_queue.peek_end(), EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST, user_id);

        }

        // Check and cancel last event if needed
        check_cancel_event();

        // Check if button was toggled
        if (!toggle_flag)
        {
            // Last event was different, cont. exeuction normally 
            // Determine current organization
            organization_bar = determiners.determine_parent_organization_bar_element(user_bar);
            
            // Check there is a current organization bar
            if (organization_bar != null)
            {
                // Set transfer role flag on
                transfer_role_flag = 1;

                // Pass button and style button to be on
                updaters.update_on_button_style(transfer_role_button);

                // Determine if mentor bar is organization admin
                if (determiners.determine_if_bar_organization_admin(organization_bar, user_bar))
                {
                    // Mentor bar is an organization admin
                    // Determine all mentors in mentor list
                    valid_organization_mentors = determiners.return_mentor_list_all(organization_bar);

                }
                else
                {  
                    // Mentor bar is not a orgnaization admin
                    // Determine all organization admin in organization admin list
                    valid_organization_mentors = determiners.return_admin_list_all(organization_bar);

                }

                // Determine and pass mentor list from organziation to refresh sorting for mentor bar elements
                sorters.sort_mentor_bar_elements_alphabetically(determiners.determine_organization_mentor_list(organization_bar));
                
                // Style valid mentor bars
                updaters.update_valid_choice_bar_styles(valid_organization_mentors);

                // Create and store transfer role event in queue
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_SUPER_FIRST, user_id);

            }
        }
        else
        {
            // Last event was the same cancel without attempting to create event
            // Pass button and reset button to be off 
            updaters.update_off_button_style(transfer_role_button);

            // Remove event from queue
            event_queue.dequeue();

        }

    }
}

export function decouple_mentor_event(user_bar)
{
    // Determine user id from hidden value in passed user bar
    const user_id = determiners.determine_id(user_bar);

    // Determine organization bar from user
    const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

    // Determine orgnization id
    const organization_id = determiners.determine_organization_id(organization_bar);

    // Check and cancel last event if needed
    check_cancel_event();

    // Remove mentor bar from organization to unaffiliated mentors
    updaters.update_remove_from_organization(user_bar);
    
    // Update organization transfer buttons
    updaters.update_organization_transfer_buttons(organization_bar);

    // Sort all organization bar elements to
    sorters.sort_all_organization_bar_element_alphabetically();

    // Create and store decouple organization event in queue
    event_queue.enqueue(EVENT_TYPES.DECOUPLE_MENTOR, user_id);
    event_queue.enqueue(EVENT_TYPES.DECOUPLE_ORGANIZATION, organization_id);

}

// Function takes in organization bar, checks if the edit organization flag is on and the event queue is not empty, if so will pass organziation 
// bar to edit organization event method to edit prev mentors organization. 
export function organization_clicked_event(organization_bar)
{
    // Check if edit organzation flag is on and event queue is not empty
    if (edit_organization_flag && !event_queue.isEmpty())
    {
        // Pass organization bar and edit mentors organization
        edit_organization_event(organization_bar);

    }
}

// Function attempts to crate an organization element and add an create organization event to queue. Checks if name is unique,
// if so will pass name, id, remove organization event, and clicked organizaion event to create new organization and adds new event to queue
// else updates add new organization message bar to include error message.
export function create_orgnization_event()
{
    // Determine organization counter element
    const organization_counter = determiners.determine_organization_counter();

    // Determine error message element
    const message_bar_element = determiners.determine_add_new_organization_message_bar();

    // Determine organization name element
    const new_organization_name_element = determiners.determine_add_new_organization_name();

    // Store then clear name input
    const new_organization_name = new_organization_name_element.value.trim();
    new_organization_name_element.value = "";

    // Check if name input is an empty string
    if (new_organization_name == "")
    {
        // Name is empty
        // Update message to empty string
        message_bar_element.innerHTML = "";

        // Show message is not already
        updaters.update_not_show(message_bar_element);

    }
    // Check if there already an organization with that name
    else if (determiners.determine_if_organization_name_unique(new_organization_name))
    {
        // Name is unique
        // Update organization counter value to increase by 1
        organization_counter.innerHTML = Number( determiners.determine_id_from_string(organization_counter.innerHTML) ) - 1;

        // Pass name, id, and trigger events to create new organization bar 
        updaters.update_create_organization(new_organization_name, "Organization object (" + organization_counter.innerHTML + ")", 
            remove_organization_event, organization_clicked_event);

        // Refresh the organization bar selection
        determiners.deteremine_and_refresh_all_organization_bars();

        // Sort all organiation bars
        sorters.sort_all_organization_bar_element_alphabetically();

        // Update message to creation valid
        message_bar_element.innerHTML = new_organization_name + " creation is valid";

        // Show message if created
        updaters.update_show(message_bar_element);

        // Create and store add organzation organization event in queue
        event_queue.enqueue(EVENT_TYPES.CREATE_ORGANIZATION, new_organization_name);

    }
    else
    {
        // Name is not unique
        // Update message to state non-unique error
        message_bar_element.innerHTML = "Error: " + new_organization_name +" is non-unique";

        // Show message is hidden
        updaters.update_show(message_bar_element);

    }

}

// Function takes organization bar, will cancel in progress event creation, attempts to remove an organization element and add an remove organization event to queue. Checks 
// if an organization is empty, if so then removes the organization and adds event else updates message bar to user to remove mentors 
// included in organization.
export function remove_organization_event(organization_bar)
{
    // Determine organzation id value from hidden value in passed organzation bar
    const organization_id = determiners.determine_organization_id(organization_bar);

    // Determine organization name value from passed organization bar
    const organization_name = determiners.determine_organization_name_value(organization_bar);

    // Determine user management message element
    const message_bar_element = determiners.determine_user_management_message();

    // Check and cancel last event if needed
    check_cancel_event();

    // Check if organization bar is empty
    if (determiners.determine_if_organization_is_empty(organization_bar))
    {
        // Updating organization bar to be removed
        updaters.update_remove_organization(organization_bar);

        // Update user management message to be empty
        message_bar_element.innerHTML = "";

        // Update user management message to hidden
        updaters.update_not_show(message_bar_element);

        // Create and store remove organzation organization event in queue
        event_queue.enqueue(EVENT_TYPES.REMOVE_ORGANIZATION, organization_id);

    }
    else
    {
        // Update user management message to state remove error
        message_bar_element.innerHTML = "Error: " + organization_name + " is not empty";

        // Update user management message to show
        updaters.update_show(message_bar_element);

    }
}
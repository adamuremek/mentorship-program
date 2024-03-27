// Import functions from determiners.js and updaters.js
import * as determiners from "./determiners.js";
import * as updaters from "./updaters.js";

// Enum values for 
const EVENT_TYPES = {
    ADD_MENTOR_MENTEE: 'ADD_MENTOR_MENTEE',
    ADD_MENTOR_MENTOR: 'ADD_MENTOR_MENTOR',
    REMOVE_MENTOR_MENTEE: 'REMOVE_MENTOR_MENTEE',
    REMOVE_MENTOR_MENTOR: 'REMOVE_MENTOR_MENTOR',
    DISABLE: 'DISABLE',
    REABLE : 'REABLE',
    // PROMOTE_SUPER: 'PROMOTE_SUPER',
    EDIT_ORGANIZATION_MENTOR: 'EDIT_ORGANIZATION_MENTOR',
    EDIT_ORGANIZATION_ORGANIZATION: 'EDIT_ORGANIZATION_ORGANIZATION',
    PROMOTE_ORGANIZATION_MENTOR: 'PROMOTE_ORGANIZATION_MENTOR',
    PROMOTE_ORGANIZATION_ORGANIZATION: 'PROMOTE_ORGANIZATION_ORGANIZATION',    
    TRANSFER_ROLE: 'TRANSFER_ROLE',
    TRANSFER_ROLE_DOUBLE_FIRST: 'TRANSFER_ROLE_DOUBLE_FIRST',
    TRANSFER_ROLE_DOUBLE_SECOND: 'TRANSFER_ROLE_DOUBLE_SECOND',
    DECOUPLE_MENTOR: 'DECOUPLE_MENTOR',
    DECOUPLE_ORGANIZATION: 'DECOUPLE_ORGANIZATION',
    REMOVE_ORGANIZATION: 'REMOVE_ORGANIZATION'

}

class queue
{
    constructor()
    {
        this.events = [];

    }

    enqueue(type, user_id) 
    {   
        // TODO: Convert to localStorage system
        this.events.push({'type': type, 'user_id': user_id});

    }

    dequeue()
    {       
        let return_event = undefined;

        // Check if not empty
        if (!this.isEmpty())
        {
            // Decrease back index
            // this.back_index--;

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

    isEmpty()
    {
        return (this.events.length == 0);

    }
}

// Select and store bar elements
const mentee_bar_container = document.querySelector("#mentee_bar_container");
const mentor_bar_container = document.querySelector("#mentor_bar_container");

const mentee_bars = mentee_bar_container.querySelectorAll(".mentee_management_bar");
const mentor_bars = mentor_bar_container.querySelectorAll(".mentor_management_bar_container");
const organization_bars = mentor_bar_container.querySelectorAll(".organization_management_bar_container");

// Create flag storage, initlize all flags to false
let add_mentor_flag = 0;
let remove_mentor_flag = 0;
let edit_organization_flag = 0;
let transfer_role_flag = 0;

let select_mentee_flag = 0;
let decouple_mentor_flag = 0;

// Create valid mentee user bar storage
let valid_mentor_bars = []

// Update valid and invalid mentors
valid_mentor_bars = determiners.return_updated_mentor_list()

// Create queue of events to be executed
const event_queue = new queue;

function execute_events()
{
    // Initlize last event and valid flags
    let last_event_flag = 0;
    let valid_flag = 1;

    // Check and cancel last event if needed
    check_cancel_event();

    // Loop through event queue till empty
    while (!event_queue.isEmpty()) {
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
                        let mentor_id = event_queue.dequeue().user_id;

                        // Remove add mentor mentor event and create a mentorship between mentee and mentor
                        alert("Create mentorship between mentee=" + current_event.user_id + " & mentor=" + mentor_id);

                        // TODO ADD MENTORSHIP
                        // under_development.py - create_mentorship(req : HttpRequest, mentee_user_account_id : int, mentor_user_account_id : int )->HttpResponse
                    
                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Error in queue input will need to cancel rest of queue
                    queue_input_error();
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
                        let mentor_id = event_queue.dequeue().user_id;

                        // Remove remove mentor mentor event and remove mentorship between mentee and mentor
                        alert("Remove mentorship between mentee=" + current_event.user_id + " & mentor=" + mentor_id);

                        // TODO REMOVE MENTORSHIP
                        // under_development.py - delete_mentorship(req: HttpRequest, mentee_user_account_id)
                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Error in queue input will need to cancel rest of queue
                    queue_input_error();
                }

                break;
                
            // Check for disable event
            case EVENT_TYPES.DISABLE:
                alert("disable " + current_event.user_id);

                // TODO DISABLE 
                // under_development.py - disable_user(req:HttpRequest)

                break;

            // Check for reable event
            case EVENT_TYPES.REABLE:
                alert("reable " + current_event.user_id);

                // TODO REABLE
                // under_development.py - enable_user(req:HttpRequest)

                break;

            // Check for promote super event
            case EVENT_TYPES.PROMOTE_SUPER:
                alert("promote super " + current_event.user_id);

                // TODO PROMOTE SUPER 

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
                        let organization_id = event_queue.dequeue().user_id;

                        // Remove promte organization organization event and promote mentor to organzation admin
                        alert("Promote mentor=" + current_event.user_id + " to org admin of org=" + organization_id);

                        // TODO PROMOTE ORGANZATION 

                    }
                }
                else
                {
                    // Set valid flag to false
                    valid_flag = 0;

                    // Error in queue input will need to cancel rest of queue
                    queue_input_error();
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
                        let organization_id = event_queue.dequeue().user_id;

                        // Remove edit organization organization event and edit organization
                        alert("Edit org for mentor=" + current_event.user_id + " to org=" + organization_id);

                        // TODO EDIT ORGANZATION
                    }
                }

                break;

            // Check for transfer role event
            case EVENT_TYPES.TRANSFER_ROLE:
                alert("transfer role " + current_event.user_id);

                // TODO TRANSFER ROLE

                break;

            case EVENT_TYPES.TRANSFER_ROLE_DOUBLE_FIRST:
                // Last event check
                if (!last_event_flag)
                {
                    // Check if next event in queue is 
                    if (event_queue.peek().type == EVENT_TYPES.TRANSFER_ROLE_DOUBLE_SECOND)
                    {
                        // Set second mentor id
                        let mentor_id = event_queue.dequeue().user_id;

                        // Remove role from first mentor and
                        alert("Transfer role from " + current_event.user_id + " to " + mentor_id);

                        // TODO TRANSFER ROLE
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
                        let organization_id = event_queue.dequeue().user_id;

                        // Remove decouple organziation event and decouple mentor from organization
                        alert("decouple mentor=" + current_event.user_id + " from organization= " + organization_id);

                        // TODO DECOUPLE MENTOR FROM ORGANIZATION

                    }
                }

                break;

            // Check for remove organization event
            case EVENT_TYPES.REMOVE_ORGANIZATION:
                alert("remove organization=" + current_event.user_id);

                // TODO REMOVE ORGANIZATION

                break;

            // case EVENT_TYPES.ADD_MENTOR_MENTOR:
            // case EVENT_TYPES.REMOVE_MENTOR_MENTOR:
            // case EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION:
            // case EVENT_TYPES.DECOUPLE_ORGANIZATION:
            //     // Error in queue input will need to cancel rest of queue
            //     queue_input_error();
        
            // Check for invalid ordering of event
            default:
                // Set valid flag to false
                valid_flag = 0;

                // Error in queue input will need to cancel rest of queue
                queue_input_error();

                break;
            
        }
    }

    // Return boolean if exeuection is valid
    return valid_flag;

}

// Will alert and cancel events in queue to keep from intended outcomes
function queue_input_error()
{
    alert("invalid ordering of events for mentee then mentor");
    cancel_events();

}

// Empty queue of eventes without exeucting 
function cancel_events()
{
    // Loop through event queue till empty
    while (!event_queue.isEmpty()) 
    {
        // Remove event from queue
        event_queue.dequeue();

    }
}

// Check for actions that require 2 events, toggled flag, cancel the prev event in queue, and reset bar and button styles
function check_cancel_event()
{
    // Check if event queue is not empty
    if (!event_queue.isEmpty())
    {
        // Check if add event is in progress
        if (add_mentor_flag)
        {
            // Check last event and if add event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.ADD_MENTOR_MENTEE)
            {
                // Determine prev user bar
                const mentee_bar = determiners.return_mentee_bar_from_id(event_queue.peek_end().user_id);

                // Determine prev user bar's add button
                const add_button = determiners.determine_add_button(mentee_bar);

                // Remove add mentor mentee event
                event_queue.dequeue();
                
                // Reset add mentor flag
                add_mentor_flag = 0;

                // Reset bar styles
                updaters.update_reset_choice_bar_styles();

                // Reset button style
                updaters.update_off_button_style(add_button);

            }
        }

        // Check if remove event is in progress
        if (remove_mentor_flag)
        {
            // Check last event and if remove event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.REMOVE_MENTOR_MENTEE)
            {
                // Determine prev user bar
                const mentee_bar = determiners.return_mentee_bar_from_id(event_queue.peek_end().user_id);

                // Determine prev user bar's add button
                const remove_button = determiners.determine_remove_button(mentee_bar);

                // Remove remove mentor mentee event
                event_queue.dequeue();

                // Reset remove mentor flag
                remove_mentor_flag = 0;

                // Reset bar styles
                updaters.update_reset_choice_bar_styles();

                // Reset button style
                updaters.update_off_button_style(remove_button);

            }
        }

        // Check if edit organization is in progess
        if (edit_organization_flag)
        {
            // Check last event if promote organzation event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.EDIT_ORGANIZATION_MENTOR)
            {
                // Determine prev user bar
                const mentor_bar = determiners.return_mentor_bar_from_id(event_queue.peek_end().user_id);

                // Determine prev user bar's add button
                const edit_button = determiners.determine_edit_organization_button(mentor_bar);

                // Remove promote organzation event
                event_queue.dequeue();

                // Reset promote organzation flag
                edit_organization_flag = 0;

                // Reset bar styles
                updaters.update_reset_choice_bar_styles();

                // Reset button style
                updaters.update_off_button_style(edit_button);

            }
        }

        // Check if transfer role is in progress
        if (transfer_role_flag)
        {
            // Check last event if transfer role double first event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.TRANSFER_ROLE_DOUBLE_FIRST)
            {
                // Determine prev user bar
                const mentor_bar = determiners.return_mentor_bar_from_id(event_queue.peek_end().user_id);

                // Determine prev user bar's add button
                const transfer_role_button = determiners.determine_transfer_role_button(mentor_bar);

                // Remove promote organzation event
                event_queue.dequeue();

                // Reset promote organzation flag
                edit_organization_flag = 0;

                // Reset bar styles
                updaters.update_reset_choice_bar_styles();

                // Reset button style
                updaters.update_off_button_style(transfer_role_button);

            }
        }
    }
}





// Updates passed user bar is be styled as disabled 
function update_disable_bar(user_bar)
{
    // Find and set disable element
    determiners.determine_disabled(user_bar).innerHTML = "1";

    // Determine buttons
    const disable_button = determiners.determine_disable_button(user_bar);
    const enable_button = determiners.determine_enable_button(user_bar);

    // Determine user id
    const user_id = determiners.determine_user_id(user_bar);

    // Switch disable button to enable
    updaters.update_bar_disable_button(disable_button, enable_button);

    // Change background color to disabled (grey)
    user_bar.style.background = "darkgray";

    // Check if there is hidden mentor element 
    if (determiners.determine_if_bar_mentee(user_bar))
    {
        // User bar is a mentee
        // Determine mentor id value 
        const mentee_id = determiners.determine_mentor_id(user_bar);

        // Check if there is a mentee_id
        if (mentee_id != "None")
        {
            // Find mentor bar from id
            const mentor_bar = determiners.return_mentor_bar_from_id(mentee_id);

            // Update mentee bar to remove mentor and update to have add button
            updaters.update_mentee_bar_remove(user_bar);

            // Check if there is a mentor
            if (mentor_bar != null)
            {
                // Create and store remove mentor events to remove mentor in queue
                event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, mentee_id);
                event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, user_id);

                // Update mentor bar to remove mentee from mentee list
                decerment_mentor_mentees(mentor_bar, mentee_id);

            }
        }
    }
    else
    {
        // User bar is a mentor
        // Find mentees
        const user_mentees = determiners.determine_mentees_value(user_bar);

        // Create mentee list from mentee list string
        const mentee_id_list = determiners.return_array_from_string(user_mentees);

        // Create list of mentee bars from mentee id list
        const selected_mentees_bars = determiners.return_mentee_bars_from_ids(mentee_id_list);

        // Cycle through mentee bars
        selected_mentees_bars.forEach(mentee_bar => {

            // Update mentee bar to remove mentor and update to have add
            updaters.update_mentee_bar_remove(mentee_bar);

            // Determine mentee id from mentee bar
            let mentee_id = determiners.determine_user_id(mentee_bar);

            // Create and store remove mentor events to remove mentor in queue
            event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, mentee_id);
            event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, user_id);

            // Update mentor bar to remove mentee id and decremenent
            decerment_mentor_mentees(user_bar, mentee_id);

        });
    }
}

// Updates passed user bar is be styled as disabled 
function update_reable_bar(user_bar)
{
    // Find and set disable element
    determiners.determine_disabled(user_bar).innerHTML = "0";
    
    // Determine buttons
    const disable_button = determiners.determine_disable_button(user_bar);
    const enable_button = determiners.determine_enable_button(user_bar);

    // Switch disable button to enable
    updaters.update_bar_enable_button(disable_button, enable_button);

    // Change background color to disabled
    user_bar.style.background = "none";

}

// Updates current mentee value by 1 and add passed mentee id to mentee list of passed user bar
function incerment_mentor_mentees(user_bar, mentee_id)
{
    // Find current mentees element
    const current_mentees = determiners.determine_current_mentees(user_bar);
    
    // Increase and set current value by 1
    current_mentees.innerHTML = determiners.determine_current_mentees_value(user_bar) + 1;

    // Find mentees element
    const mentees_list = determiners.determine_mentees(user_bar);

    // Determine mentee values
    let mentee_values = determiners.determine_mentees_value(user_bar);

    // Get array from string
    let updated_mentee_values = determiners.return_array_from_string(mentee_values);

    // Push new value into updated mentee values
    updated_mentee_values.push(mentee_id);

    // Split mentee values by commas into a array and push new mentee id into it then update mentee list element
    mentees_list.innerHTML = updated_mentee_values.toString();

}

// Updates current mentee value by -1 and removes mentee id from mentee list of passed user bar
function decerment_mentor_mentees(user_bar, mentee_id)
{
    // Find current mentees element
    const current_mentees = determiners.determine_current_mentees(user_bar);

    // Decrease and set current value by 1
    current_mentees.innerHTML = determiners.determine_current_mentees_value(user_bar) - 1;

    // Find mentees element
    const mentees_list = determiners.determine_mentees(user_bar);

    // Determine mentee values
    let mentee_values = determiners.determine_mentees_value(user_bar);

    // Get array from string
    let updated_mentee_values = determiners.return_array_from_string(mentee_values);

    // Determine passed mentee id index
    let remove_index;
    for (let index = 0; index < updated_mentee_values.length; index++) 
    {
        if (updated_mentee_values[index] == mentee_id)
        {
            // Set remove index
            remove_index = index;

            break;

        }    
    }

    // Remove mentee id at remove index
    updated_mentee_values.splice(remove_index, 1);

    // Remove and set mentee value by replacing mentee id value with an empty string
    mentees_list.innerHTML = updated_mentee_values;

}

// Removes and adds passed mentor bar from organziation bar to unaffiliated mentors
function remove_from_organization(mentor_bar)
{
    // Removing mentor bar from organization
    mentor_bar.remove();

    // Add mentor bar to unaffiliated mentors
    mentor_bar_container.appendChild(mentor_bar);

}

// Removes organization admins from admin list and adds them to mentor list
function demote_organization_admins(organization_bar)
{
    // Determine admin list in organization bar
    const admin_list = determiners.determine_organization_admin_list(organization_bar);

    // Determine mentor list in organization bar
    const mentor_list = determiners.determine_organization_mentor_list(organization_bar);

    // Remove mentor from admin list and add to mentor list
    const current_admins = determiners.determine_mentor_bars(admin_list);

    // Check if admin list is not empty
    if (current_admins != null)
    {
        // Cycle through mentors included in admin list adding them mentor list
        current_admins.forEach(current_admin => {
            // Remove mentor from admin list
            current_admin.remove();

            // Add mentor to mentor list
            mentor_list.appendChild(current_admin);

        });
    }
}

// Adds pass passed mentor bar to admin list within organization bar
function promote_organization_admin(organization_bar, mentor_bar)
{
    // Determine admin list in organization bar
    const admin_list = determiners.determine_organization_admin_list(organization_bar);

    // Remove mentor from mentee list
    mentor_bar.remove();

    // Add mentor to admin list
    admin_list.appendChild(mentor_bar);

}

// TODO NEED TESTING
// Removes and adds passed mentor bar from unfailiated mentors to passed organization bar
function add_to_organization(organization_bar, mentor_bar)
{
    // Remove mentor bar from unaffiliated mentors
    mentor_bar.remove();

    // Deteremine mentor list
    const mentor_list = determiners.determine_organization_mentor_list(organization_bar);

    // Add mentor bar to orgnization mentee list
    mentor_list.appendChild(mentor_bar);

}

// TODO NEED TESTING
// Removes and adds mentor bars included in organization bar to unaffiliated mentors, then removes the organization bar
function remove_organization(organization_bar)
{
    // Determine mentors in organization
    const mentor_bars = determiners.determine_mentor_bars(organization_bar);    

    // Cycle thorugh mentors
    mentor_bars.forEach(mentor_bar => {
        // Removing mentor bar from organization
        // Add mentor bar to unaffiliated mentors
        remove_from_organization(mentor_bar);

    });

    // Remove organization bar
    organization_bar.remove();

}





// Check and return if mentor is included in valid mentor bars
function check_mentor_valid(user_bar)
{
    // Initilize found flag to 0
    let found_flag = 0;

    // Cycle through valid mentor bars
    for (let index = 0; index < valid_mentor_bars.length; index++) 
    {
        // Check if passed user bar is same as the valid mentor bar
        if (user_bar == valid_mentor_bars[index])
        {
            // Set found flag to 1
            found_flag = 1;

            break;
        }
    }

    return found_flag;
}

// Check and return 1 if prev_event is the same event type and user id and 0 if not
function check_toggle_event(prev_event, new_event_type, new_event_id)
{
    // Initlize return number value to 0
    let return_flag = 0;

    // Check and set if prev event is the same as the new event
    if (prev_event.type == new_event_type & prev_event.user_id == new_event_id)
    {
        return_flag = 1;
    }

    return return_flag;
}





// Exported functions
export function save_event()
{
    // Exuecute queue
    if (execute_events())
    {
        // Exeucution was successful
        alert("save good")

    }
    else 
    {
        // Exeucution was unsuccessful
        alert("save bad")

    }
}

export function cancel_event()
{
    // Cancel queue
    cancel_events();

    // Remove queue
    alert("cancel")
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
    // Redirects to user page using the id in the user_bar
    alert("view");
}

export function add_mentor_mentee_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Intitlize toggle flag to 0
        let toggle_flag = 0;

        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Determine add button from user bar
        const add_mentor_button = determiners.determine_add_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = check_toggle_event(event_queue.peek_end(), EVENT_TYPES.ADD_MENTOR_MENTEE, user_id);

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

            // Filter mentors to just include valid mentor bars
            // TODO TODO

            // Create and store add mentor mentee event in queue
            event_queue.enqueue(EVENT_TYPES.ADD_MENTOR_MENTEE, user_id);

        }
        else 
        {
            // Last event was the same cancel without attempting to create event
            // Pass button and reset button to be off 
            updaters.update_off_button_style(add_mentor_button);

            // Remove event from queue
            event_queue.dequeue();

        }

        // Creates part 1/2 in queue for adding mentorship
        alert("1/2 add mentor")


    }

}

export function remove_mentor_mentee_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Intitlize toggle flag to 0
        let toggle_flag = 0;

        // Determine user id and mentor from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);
        const mentor_id = determiners.determine_mentor_id(user_bar);

        // Determine remove button from user bar
        const remove_mentor_button = determiners.determine_remove_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = check_toggle_event(event_queue.peek_end(), EVENT_TYPES.REMOVE_MENTOR_MENTEE, user_id);

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
            const mentor_bar = determiners.return_mentor_bar_from_id(mentor_id);

            // Check if mentor_bar is not undefined
            if (mentor_bar != undefined)
            {
                // Pass button and style button to be on
                updaters.update_on_button_style(remove_mentor_button)

                // Style mentee's mentor bar
                updaters.update_remove_choice_bar_style(mentor_bar);

                // Filter mentors to just include remove mentor bars
                // TODO TODO

                // Create and store remove mentor mentee event in queue
                event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, user_id);

            }
        }
        else
        {
            // Last event was the same cancel without attempting to create event
            // Pass button and reset button to be off 
            updaters.update_off_button_style(remove_mentor_button);

            // Remove event from queue
            event_queue.dequeue();

        }

        // Create part 1/2 in queue for removing mentorship 
        alert("1/2 remove mentor");

    }
}

export function disable_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Check and cancel last event if needed
        check_cancel_event();

        // Update bar to be disabled 
        update_disable_bar(user_bar)

        // Create and store deactivate event in queue
        event_queue.enqueue(EVENT_TYPES.DISABLE, user_id);

        // Create in queue for deactiving a user
        alert("disable");
    }
}

export function reable_event(user_bar)
{   
    // Check if account is disabled
    if (determiners.determine_disabled_value(user_bar))
    {
        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Check and cancel last event if needed
        check_cancel_event();

        // Update bar to be reable
        update_reable_bar(user_bar);

        // Create and store deactivate event in queue
        event_queue.enqueue(EVENT_TYPES.REABLE, user_id);

        // Creates in queue for reactiving a user
        alert("reactivte");

    }
}


// TODO NEED TO ADD TRANFURE LOGIC transfer_role_flag
export function mentor_clicked_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Check if there any flags on
        if (add_mentor_flag | remove_mentor_flag | transfer_role_flag)
        {
            // Check if mentor is valid and event queue is not empty
            if (check_mentor_valid(user_bar) & !event_queue.isEmpty())
            {
                // Store last event
                let prev_event = event_queue.peek_end();

                // Create stroage for temp user bar
                let prev_user_bar = determiners.return_mentee_bar_from_id(prev_event.user_id);

                // Determine user id and mentees from hidden value in passed user bar
                const user_id = determiners.determine_user_id(user_bar);

                // Check if prev event user and current user are different
                if (prev_event.user_id != user_id)
                {
                    // Check for a add event flag
                    if (add_mentor_flag)
                    {
                        // Determine prev user bar from id
                        prev_user_bar = determiners.return_mentee_bar_from_id(prev_event.user_id);

                        // Determine add buttons from mentee bar
                        const add_mentee_button = determiners.determine_add_button(prev_user_bar);

                        // Determine if last event is an add mentor mentee event
                        if (prev_event.type == EVENT_TYPES.ADD_MENTOR_MENTEE & prev_user_bar != undefined) 
                        {                    
                            // Pass mentee bar and mentor id and update mentee bar
                            updaters.update_mentee_bar_add(prev_user_bar, user_id);

                            // Update mentor bar
                            incerment_mentor_mentees(user_bar, prev_event.user_id);

                            // Pass button and reset button to be off
                            updaters.update_off_button_style(add_mentee_button)

                            // Reset bar styles
                            updaters.update_reset_choice_bar_styles();

                            // Create and store add mentor mentee event in queue
                            event_queue.enqueue(EVENT_TYPES.ADD_MENTOR_MENTOR, user_id);

                            // Reset add event flag
                            add_mentor_flag = 0;

                            alert("mentor add mentor")

                        }
                    }
                        
                    // Check for a remove event flag
                    if (remove_mentor_flag)
                    {
                        // Determine prev user bar from id
                        prev_user_bar = determiners.return_mentee_bar_from_id(prev_event.user_id);

                        // Determine user mentee element from user bar
                        const user_mentees = determiners.determine_mentees_value(user_bar);

                        // Determine remove button from mentee bar
                        const remove_mentee_button = determiners.determine_remove_button(prev_user_bar);

                        // Create mentee list from mentee list string
                        const mentee_id_list = return_array_from_string(user_mentees);

                        // // Get mentee id is inlcuded in mentor mentees
                        // mentee_id = prev_event.user_id

                        // Determine if last event is an remove mentor mentee event and mentee is included in mentee list
                        if (prev_event.type == EVENT_TYPES.REMOVE_MENTOR_MENTEE & mentee_id_list.includes(prev_event.user_id))
                        {
                            // Update mentee bar
                            updaters.update_mentee_bar_remove(prev_user_bar);

                            // Update mentor bar to include 1 less mentee and list
                            decerment_mentor_mentees(user_bar, prev_event.user_id);

                            // Pass button and reset button to be off
                            updaters.update_off_button_style(remove_mentee_button);

                            // Reset bar styles
                            updaters.update_reset_choice_bar_styles();

                            // Create and store remove mentor mentor event in queue
                            event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, user_id);

                            // Reset remove event flag
                            remove_mentor_flag = 0;

                            alert("mentor remove mentor");

                        }
                    }

                    // Check for a transfer role event flag
                    if (transfer_role_flag)
                    {
                        // Determine prev user bar from id
                        prev_user_bar = determiners.return_mentor_bar_from_id(prev_event.user_id);

                        // Determine transfer role button from mentor bar
                        const transfer_role_button = determiners.determine_transfer_role_button(prev_user_bar);

                        // Determine prev user bar to determine parent organization bar element
                        const prev_organitization_bar = determiners.determine_parent_organization_bar_element(prev_user_bar);

                        // Determine organization bar from user bar
                        const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

                        // Determine if last event is an transfer role event and if mentors are within the same organization
                        if (prev_event.type == EVENT_TYPES.TRANSFER_ROLE_DOUBLE_FIRST & prev_organitization_bar == organization_bar)
                        {
                            // Determine if prev user bar is organization admin and current user bar is not organization admin or if prev user bar is not organization admin and current user bar is organization admin
                            if ((determiners.determine_if_bar_organization_admin(organization_bar, prev_user_bar) && !determiners.determine_if_bar_organization_admin(organization_bar, user_bar)) ||
                                (!determiners.determine_if_bar_organization_admin(organization_bar, prev_event) & determiners.determine_if_bar_organization_admin(organization_bar, user_bar)) ) 
                            {
                                // Remove mentor bars from admin list to mentor list
                                demote_organization_admins(organization_bar);

                                // Prmote mentor bar from mentor list to admin list 
                                promote_organization_admin(organization_bar, prev_user_bar);

                                // Pass button and reset button to be off
                                updaters.update_off_button_style(transfer_role_button);

                                // Reset bar styles
                                updaters.update_reset_choice_bar_styles();

                                // Create and store transfer role event in queue
                                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_DOUBLE_SECOND, user_id);

                                // Reset transfer role flag
                                transfer_role_flag = 0;
                                
                                alert("transfer role")

                            }
                        }
                    }
                }

                // Update valid mentors
                valid_mentor_bars = determiners.return_updated_mentor_list();

                // Reset filter for mentors
                // TODO TODO

            }
        }
    }
}

export function promote_organization_mentor_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Determine organization bar from user bar
        const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

        // Determine organization id of organization bar is included in
        const organization_id = determiners.determine_organization_id(organization_bar);

        // Check and cancel last event if needed
        check_cancel_event();

        // // Determine current organization bar
        // const current_organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

        // Check for user bar to be within organization bar
        if (organization_bar != null)
        {
            // Remove mentor bars from admin list to mentor list
            demote_organization_admins(organization_bar);

            // Promote mentor bar from mentor list to admin list
            promote_organization_admin(organization_bar, user_bar);

            // Create and store promote organization mentor event in queue
            event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR, user_id);

            // Create and store promote organization organzation event in queue
            event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION, organization_id);
            
            // Promotes user to organization admin status
            alert("promote org");

        }
    }
}

export function edit_organization_mentor_event(user_bar)
{
    // CHECK IF SHOULD KEEP OR NOT

    // // Check if account is not disabled
    // if (!determiners.determine_disabled_value(user_bar))
    // {
        // Intitlize toggle flag to 0
        let toggle_flag = 0; 

        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Determine edit organization button
        const edit_organization_button = determiners.determine_edit_organization_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = check_toggle_event(event_queue.peek_end(), EVENT_TYPES.EDIT_ORGANIZATION_MENTOR, user_id);

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

            // Determine current organization bar
            const current_organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

            // Get a list of all but passed organization bars
            const all_but_own_organization_bars = determiners.return_list_all_but_passed_organiztion_bar(current_organization_bar);

            // Style organization bars
            updaters.update_valid_choice_bar_styles(all_but_own_organization_bars);
            
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

        alert("edit org");

    // }
}

// TODO NEED TO SET UP ALONG WITH BUTTONS
export function transfer_role_organization_admin_mentor_event(user_bar)
{
    // Create and store remove mentor mentor event in queue
    event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE, user_id);
}

// SET UP FOR SUPER ADMINS WHERE IS 2 CLICKS BUT WILL NEED ORG ADMIN WHERE IS 1 CLICK
// TODO NEED TESTING
export function transfer_role_super_admin_mentor_event(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Create storage for mentor and admin list
        let valid_organization_admins, valid_organization_mentors;

        // Initlize toggle flag to 0
        let toggle_flag = 0;

        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Determine transfer role button
        const transfer_role_button = determiners.determine_transfer_role_button(user_bar);

        // Check if queue is not empty
        if (!event_queue.isEmpty())
        {
            // Check if same button was already pressed before
            toggle_flag = check_toggle_event(event_queue.peek_end(), EVENT_TYPES.TRANSFER_ROLE_DOUBLE_FIRST, user_id);

        }

        // Check and cancel last event if needed
        check_cancel_event();

        // Check if button was toggled
        if (!toggle_flag)
        {
            // Last event was different, cont. exeuction normally 
            // Determine current organization
            const current_organization_bar = determiners.determine_parent_organization_bar_element(user_bar);
            
            // Check there is a current organization bar
            if (current_organization_bar != null)
            {
            
                // Set transfer role flag on
                transfer_role_flag = 1;

                // Pass button and style button to be on
                updaters.update_on_button_style(transfer_role_button);

                // Determine if mentor bar is organization admin
                if (determiners.determine_if_bar_organization_admin(current_organization_bar, user_bar))
                {
                    // Mentor bar is an organization admin
                    // Set valid admin bars to empty list
                    valid_organization_admins = [];

                    // Determine all mentors in mentor list
                    valid_organization_mentors = determiners.return_mentor_list_all(current_organization_bar);

                }
                else
                {  
                    // Mentor bar is not a orgnaization admin
                    // Determine all organization admin in organization admin list
                    valid_organization_mentors = determiners.return_admin_list_all(current_organization_bar);

                    // // Determine all but current user bar in organization mentor list
                    // valid_organization_mentors = determiners.return_mentor_list_all_but_passed_mentor_bars(current_organization_bar, user_bar);
                }
                
                // Style valid mentor bars
                updaters.update_valid_choice_bar_styles(valid_organization_mentors);
                // updaters.update_valid_choice_bar_styles(valid_organization_admins);

                // Create and store transfer role event in queue
                event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE_DOUBLE_FIRST, user_id);

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

        // Transfers user account role to user
        alert("transfer role");

    }
}

// TODO NEED TESTING
export function decouple_mentor_event(user_bar)
{
    // // Check if account is not disabled
    // if (!determiners.determine_disabled_value(user_bar))
    // {
        // Determine user id from hidden value in passed user bar
        const user_id = determiners.determine_user_id(user_bar);

        // Determine organization bar from user
        const organization_bar = determiners.determine_parent_organization_bar_element(user_bar);

        // Determine orgnization id
        const organization_id = determiners.determine_organization_id(organization_bar);

        // Create and store decouple organization event in queue
        event_queue.enqueue(EVENT_TYPES.DECOUPLE_MENTOR, user_id);
        event_queue.enqueue(EVENT_TYPES.DECOUPLE_ORGANIZATION, organization_id);

        // Check and cancel last event if needed
        check_cancel_event();

        // Remove mentor bar from organization to unaffiliated mentors
        remove_from_organization(user_bar);

        // Removes mentor from organization
        alert("decouple");

    // }
}

// TODO NEED TESTING
export function organization_clicked_event(organization_bar)
{
    // Check if edit organzation flag is on
    if (edit_organization_flag)
    {
        // Check if mentor is valid and event queue is not empty
        if (!event_queue.isEmpty())
        {
            // Determine organization id from hidden value in passed organization bar
            const organization_id = determiners.determine_organization_id(organization_bar);

            // Store last event
            let prev_event = event_queue.peek_end();

            // Find mentor bar from user id
            const mentor_bar = determiners.return_mentor_bar_from_id(prev_event.user_id);

            // Determine prev organitization bar from mentor bar
            const prev_organitization_bar = determiners.determine_parent_organization_bar_element(mentor_bar);

            // Check if mentor_bar is not undefined and it is not the same id as prev organitization
            if (mentor_bar != undefined && determiners.determine_organization_id(prev_organitization_bar) != organization_id)
            {
                // Determine edit organization button
                const edit_organization_button = determiners.determine_edit_organization_button(mentor_bar);

                // Determine if last event is an promote organzation mentor event
                if (prev_event.type == EVENT_TYPES.EDIT_ORGANIZATION_MENTOR) 
                {
                    // Determine parent organization if mentor is apart of another organization
                    const prev_organization_bar = determiners.determine_parent_organization_bar_element(mentor_bar)
                    
                    // Check mentor was part of another organization
                    if (prev_organization_bar != null)
                    {
                        // Remove mentor from prev organization bar
                        remove_from_organization(prev_organization_bar, mentor_bar);

                    }

                    // Add mentor bar to organization bar
                    add_to_organization(organization_bar, mentor_bar);

                    // Pass button and reset button to be off
                    updaters.update_off_button_style(edit_organization_button);

                    // Reset bar styles
                    updaters.update_reset_choice_bar_styles();

                    // Create and store promote organzation organization event in queue
                    event_queue.enqueue(EVENT_TYPES.EDIT_ORGANIZATION_ORGANIZATION, organization_id);

                    // Reset edit event flag
                    edit_organization_flag = 0;

                    alert("org clicked");

                }
            }
        }
    }

    alert("org clicked");
}

export function remove_organization_event(organization_bar)
{
    // Determine user id from hidden value in passed user bar
    const organization_id = determiners.determine_organization_id(organization_bar);

    // Check and cancel last event if needed
    check_cancel_event();

    // Updating mentors and organization bar for organization
    remove_organization(organization_bar);

    // Create and store remove organzation organization event in queue
    event_queue.enqueue(EVENT_TYPES.REMOVE_ORGANIZATION, organization_id);

    // Removes organization
    alert("remove");
}
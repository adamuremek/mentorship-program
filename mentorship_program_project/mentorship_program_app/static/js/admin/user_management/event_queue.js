// Enum values for 
const EVENT_TYPES = {
    ADD_MENTOR_MENTEE: 'ADD_MENTOR_MENTEE',
    ADD_MENTOR_MENTOR: 'ADD_MENTOR_MENTOR',
    REMOVE_MENTOR_MENTEE: 'REMOVE_MENTOR_MENTEE',
    REMOVE_MENTOR_MENTOR: 'REMOVE_MENTOR_MENTOR',
    DISABLE: 'DISABLE',
    REABLE : 'REABLE',
    PROMOTE_SUPER: 'PROMOTE_SUPER',
    PROMOTE_ORGANIZATION_MENTOR: 'PROMOTE_ORGANIZATION_MENTOR',
    PROMOTE_ORGANIZATION_ORGANIZATION: 'PROMOTE_ORGANIZATION_ORGANIZATION',    
    TRANSFER_ROLE: 'TRANSFER_ROLE',
    DECOUPLE: 'DECOUPLE',
    REMOVE_ORGANIZATION: 'REMOVE_ORGANIZATION'
}

class queue
{
    constructor()
    {
        this.events = [];
        // this.front_index = 0;
        // this.back_index = 0;
    }

    enqueue(type, user_id) 
    {
        // this.events[this.back_index] = {'type': type, 'user_id': user_id};
        
        // TODO: Convert to localStorage system
        this.events.push({'type': type, 'user_id': user_id});
        
        // this.back_index++;
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
        // return (this.events == []);
    }
}

// Select and store bar elements
const mentee_bars = document.querySelectorAll(".mentee_management_bar");
const mentor_bars = document.querySelectorAll(".mentor_management_bar_container");
const organization_bars = document.querySelectorAll(".organization_management_bar");

// Create flag storage, initlize all flags to false
let add_mentor_flag = 0;
let remove_mentor_flag = 0;
let select_mentee_flag = 0;
let promote_organization_flag = 0;

// Create valid mentee user bar storage
let valid_mentor_bars = []

// Update valid and invalid mentors
valid_mentor_bars = get_update_mentor_list()

// Create queue of events to be executed
const event_queue = new queue;


// TESTING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, 1);
// remove_mentor_flag = 1;
// check_cancel_event();
// event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, 2);
// cancel_events();
// execute_events();


function execute_events()
{
    // Initlize last event flag to 0
    let last_event_flag = 0;

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
                        // Remove add mentor mentor event and create a mentorship between mentee and mentor
                        alert("Create mentorship between mentor=" + current_event.user_id + " & mentee=" + event_queue.dequeue().user_id);

                        // TODO ADD MENTORSHIP
                    
                    }
                }
                else
                {
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
                        // Remove remove mentor mentor event and remove mentorship between mentee and mentor
                        alert("Remove mentorship between mentor=" + current_event.user_id + " & mentee=" + event_queue.dequeue().user_id);

                        // TODO REMOVE MENTORSHIP
                    }
                }
                else
                {
                    // Error in queue input will need to cancel rest of queue
                    queue_input_error();
                }

                break;
                
            // Check for disable event
            case EVENT_TYPES.DISABLE:
                alert("disable " + current_event.user_id);

                // TODO DISABLE 

                break;

            // Check for reable event
            case EVENT_TYPES.REABLE:
                alert("reable " + current_event.user_id);

                // TODO REABLE

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
                        // Remove promte organization organization event and promote mentor to organzation admin
                        alert("Promote mentor=" + current_event.user_id + " to org admin of org=" + event_queue.dequeue().user_id);

                        // TODO PROMOTE ORGANZATION 

                    }
                }
                else
                {
                    // Error in queue input will need to cancel rest of queue
                    queue_input_error();
                }

                break;

            // Check for transfer role event
            case EVENT_TYPES.TRANSFER_ROLE:
                alert("transfer role " + current_event.user_id);

                // TODO TRANSFER ROLE

                break;

            // Check for decouple 
            case EVENT_TYPES.DECOUPLE:
                alert("decouple " + current_event.user_id);

                // TODO DECOUPLE MENTOR

                break;

            // Check for remove organization event
            case EVENT_TYPES.REMOVE_ORGANIZATION:
                alert("decouple " + current_event.user_id);

                // TODO REMOVE ORGANIZATION

                break;

            // Check for invalid ordering of event
            case EVENT_TYPES.ADD_MENTOR_MENTOR:
            case EVENT_TYPES.REMOVE_MENTOR_MENTOR:
            case EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION:
                // Error in queue input will need to cancel rest of queue
                queue_input_error();
        
            default:
                // Error in queue input will need to cancel rest of queue
                queue_input_error();

                break;
            
        }
    }
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

// Check for actions that require 2 events, toggled flag, cancel the prev event in queue, and reset bar styles
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
                // Remove add mentor mentee event
                event_queue.dequeue();
                
                // Reset add mentor flag
                add_mentor_flag = 0;

            }

            // Reset bar styles
            reset_bar_styles();

        }

        // Check if remove event is in progress
        if (remove_mentor_flag)
        {
            // Check last event and if remove event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.REMOVE_MENTOR_MENTEE)
            {
                // Remove remove mentor mentee event
                event_queue.dequeue();

                // Reset remove mentor flag
                remove_mentor_flag = 0;

            }

            // Reset bar styles
            reset_bar_styles();

        }

        // Check if promote organization is in progess
        if (promote_organization_flag)
        {
            // Check last event and if promote organzation event then remove it
            if (event_queue.peek_end().type == EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR)
            {
                // Remove promote organzation event
                event_queue.dequeue();

                // Reset promote organzation flag
                promote_organization_flag = 0;

            }

            // Reset bar styles
            reset_bar_styles();

        }
    }
}

// Cycle through passed bar's styles to include white borders
function update_choice_bar_styles(passed_bars)
{
    valid_mentor_bars.forEach(valid_mentor_bar => {
        valid_mentor_bar.style.border = "2.5px solid white";
        
    });
}

// Updates bar's style to include red borders
function update_choice_remove_bar_style(user_bar)
{
    user_bar.style.border = "2.5px solid red";
}

// Set all bars to their default border styles
function reset_bar_styles()
{
    // Check last event type in queue and reset only need bars
    // TODO

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        mentee_bar.style.border = "none";

    });

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        mentor_bar.style.border = "none";

    });

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        organization_bar.style.border = "none";

    });
}

// Updates button's style to include darkgrey background
function update_button_style(button)
{
    button.style.background = "darkgray";

}

// Set button to default button backround
function reset_button_style(button)
{
    button.style.background = "none";
    
}

// Updates passed user bar is be styled as disabled 
function update_disable_bar(user_bar)
{
    // Find and set account disable value
    const account_disable = Number(user_bar.querySelector("#user_account_disabled").textContent.trim());

    // Check if account is not disabled
    if (account_disable)
    {
        // Set deactivated value
        account_disable.innerHTML = "1";

        // Check if there is hidden mentor element 
        if (user_bar.querySelector("#user_mentor") != null)
        {
            // User bar is a mentee
            // Find and update mentor bar
    

            // return_mentee_bars_from_ids()



        }
        else
        {
            // User bar is a mentor
            // Find mentees
            const user_mentees = user_bar.querySelector("#user_mentees").textContent.trim();

            // Create mentee list from mentee list string
            const mentee_id_list = create_mentee_list(user_mentees);

            // Create list of mentee bars from mentee id list
            selected_mentees_bars = return_mentee_bars_from_ids(mentee_id_list);

            // Cycle through mentee bars
            selected_mentees_bars.forEach(mentee_bar => {
                update_mentee_bar_remove(mentee_bar);
            });
        }

        // Change background color to disabled
        // TODO NEED TO UPDATE
        // user_bar.style.background = "";

        // Switch disable button to enable

    }
}

// Updates passed user bar is be styled as disabled 
function update_reable_bar(user_bar)
{
    // Find and set account disable value
    const account_disable = Number(user_bar.querySelector("#user_account_disabled").textContent.trim());

    // Check if account is disabled
    if (!account_disable)
    {
        // Set deactivated value
        account_disable.innerHTML = "0";

        // Change background color to disabled
        // TODO NEED TO UPDATE
        // user_bar.style.background = "";

        // Switch disable button to enable

    }
}

function update_mentee_bar_add(user_bar, mentor_id)
{
    // Updates mentee bar to show the remove button and update mentor value to new mentor id

}

function update_mentee_bar_remove(user_bar)
{
    // Updates mentee bar to show the add button and update mentor value to None

}

function incerment_mentor_mentees(user_bar, mentee_id)
{
    // Increase and updates the current mentee value of passed user bar
    // Add mentee id value to passed user bar

}

function decerment_mentor_mentees(user_bar)
{
    // Decrease and updates the current mentee value of passed user bar
    // Remove mentee id value from passed user bar

}

function get_update_mentor_list()
{
    // Remove entries of mentors list
    let valid_mentor_bars = [];

    // Cycles through mentor list determining and storing valid mentors in valid_mentor_bars
    mentor_bars.forEach(mentor_bar => { 
        // Set current and max mentee values
        current_mentees = Number(mentor_bar.querySelector("#current_mentees").textContent);
        max_mentees = Number(mentor_bar.querySelector("#max_mentees").textContent);

        // Determine if mentor is valid for new mentees
        if (current_mentees < max_mentees)
        {
            // Add mentor bar to valid mentor bars
            valid_mentor_bars.push(mentor_bar);

        }
    });

    return valid_mentor_bars;
}

// Check and return if mentor is included in valid mentor bars
function check_mentor_valid(user_bar)
{
    // Initilize found flag to 0
    let found_flag = 0;

    // Cycle through valid mentor bars
    valid_mentor_bars.forEach(valid_mentor_bar => {
        // Check if passed user bar is same as the valid mentor bar
        if (user_bar == valid_mentor_bar)
        {
            // Set found flag to 1
            found_flag = 1;
        }
    });

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

// Cycle through mentee bars and return bar matching mentee id
function return_mentee_bar_from_id(user_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Cycle through mentee bars
    for (let index = 0; index < mentee_bars.length; index++)
    {
        // Determine user id and mentor from hidden value in passed user bar
        const mentee_id = mentee_bars[index].querySelector("#user_account").textContent.trim();

        // Check if user id field is the same as passed id
        if (user_id == mentee_id)
        {
            // Set return bar
            return_bar = mentee_bars[index];

            // Break loop
            break;

        }
    }

    return return_bar;

}

// Cycle through mentor bars and return bars matching mentor id
function return_mentor_bar_from_id(mentor_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Cycle through mentee bars
    for (let index = 0; index < mentor_bars.length; index++)
    {
        // Determine user id and mentor from hidden value in passed user bar
        const mentor_id = mentor_bars[index].querySelector("#user_account").textContent.trim();

        // Check if user id field is the same as passed id
        if (user_id == mentor_id)
        {
            // Set return bar
            return_bar = mentor_id;

            // Break loop
            break;

        }
    }

    return return_bar;

}

// Cycle thorugh bars searching for bars matching one of the passed ids
function return_mentee_bars_from_ids(user_ids)
{
    // Initlize return value as undefined and flag as false 
    let return_bars = [];
    // let found_flag = 0;

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Determine user id and mentor from hidden value in passed user bar
        const mentor_id = user_bar.querySelector("#user_account").textContent.trim();

        // Cycle through all passed user ids
        for (let index = 0; index < user_ids.length; index++)
        {
            // Check all user ids against mentor id
            if (user_ids[index] == mentor_id)
            {
                // Push mentor bar into returned list
                return_bars.push(mentee_bar);

                break;

            }
        }
    });

    return return_bars;

}

function create_mentee_list(passed_list_string)
{
    // Initlize mentee list to empty list
    let mentee_list = [];

    // Check if passed list is not None
        // Cycles through passed string seperating mentee out and pushing into list

    return mentee_list;
}

function remove_organization(organization_bar)
{
    // Remove mentors included in organization admin list and add them to unfailitated mentor list

    // Remove organization bar
}

function promote_prganzation_admin(organization_bar, mentor_bar)
{
    // Remvove mentor bar from unfilated section

    // Place mentor bar in organzation bar
}






// Exported functions
export function save_event()
{
    // Exuecute queue
    execute_events();

    // Refresh page?
    alert("save")    
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
    alert("mentee clicked")
}



export function view_event(user_bar)
{
    // Redirects to user page using the id in the user_bar
    alert("view");
}

export function add_mentor_mentee_event(user_bar)
{
    // Intitlize toggle flag to 0
    let toggle_flag = 0;

    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Determine add button from user bar
    const add_mentor_button = user_bar.querySelector("#plus_button");

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
        update_button_style(add_mentor_button);

        // Style valid mentor bars
        update_choice_bar_styles(valid_mentor_bars);

        // Create and store add mentor mentee event in queue
        event_queue.enqueue(EVENT_TYPES.ADD_MENTOR_MENTEE, user_id);

    }
    else 
    {
        // Last event was the same cancel without attempting to create event
        // Pass button and reset button to be off 
        reset_button_style(add_mentor_button);

        // Remove event from queue
        event_queue.dequeue();

    }

    // Creates part 1/2 in queue for adding mentorship
    alert("1/2 add mentor")
}

export function remove_mentor_mentee_event(user_bar)
{
    // Intitlize toggle flag to 0
    let toggle_flag = 0;

    // Determine user id and mentor from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();
    const mentor_id = user_bar.querySelector("#user_mentor").textContent.trim();

    // Determine remove button from user bar
    const remove_mentor_button = user_bar.querySelector("#remove_button");

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
        // Find mentor bar using mentor id
        const mentor_bar = return_mentor_bar_from_id(mentor_id);

        // Check if mentor_bar is not undefined
        if (mentor_bar != undefined)
        {
            // Pass button and style button to be on
            update_button_style(remove_mentor_button)

            // Style mentee's mentor bar
            update_choice_remove_bar_style(mentor_bar);

            // Create and store remove mentor mentee event in queue
            event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTEE, user_id);

        }
    }
    else
    {
        // Last event was the same cancel without attempting to create event
        // Pass button and reset button to be off 
        reset_button_style(remove_mentor_button);

        // Remove event from queue
        event_queue.dequeue();

    }

    // Create part 1/2 in queue for removing mentorship 
    alert("1/2 remove mentor")
}

export function disable_event(user_bar)
{
    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // Update bar to be disabled 
    update_disable_bar(user_bar)

    // Create and store deactivate event in queue
    event_queue.enqueue(EVENT_TYPES.DISABLE, user_id);

    // Create in queue for deactiving a user
    alert("disable")
}

export function reable_event(user_bar)
{   
    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // Update bar to be reable
    update_reable_bar(user_bar)

    // Create and store deactivate event in queue
    event_queue.enqueue(EVENT_TYPES.REABLE, user_id);

    // Creates in queue for reactiving a user
    alert("reactivte")
}

export function mentor_clicked_event(user_bar)
{
    // Check if any flag are on
    if (add_mentor_flag | remove_mentor_flag)
    {
        // Check if mentor is valid and event queue is not empty
        if (check_mentor_valid(user_bar) & !event_queue.isEmpty())
        {
            // Determine user id and mentees from hidden value in passed user bar
            const user_id = user_bar.querySelector("#user_account").textContent.trim();
            const user_mentees = user_bar.querySelector("#user_mentees").textContent.trim();

            // Store last event
            let prev_event = event_queue.peek_end();

            // Find mentee bar from user id
            const mentee_bar = return_mentee_bar_from_id(prev_event.user_id);

            // Check if mentor_bar is not undefined
            if (mentee_bar != undefined)
            {
                // Determine buttons from mentee bar
                const add_mentee_button = mentee_bar.querySelector("#plus_button");
                const remove_mentee_button = mentee_bar.querySelector("#remove_button");

                // Check for a add event flag
                if (add_mentor_flag)
                {
                    // Determine if last event is an add mentor mentee event
                    if (prev_event.type == EVENT_TYPES.ADD_MENTOR_MENTEE) 
                    {                    
                        // Pass mentee bar and mentor id and update mentee bar
                        update_mentee_bar_add(mentee_bar, user_id);

                        // Update mentor bar
                        incerment_mentor_mentees(user_bar, prev_event.user_id);

                        // Pass button and reset button to be off
                        reset_button_style(add_mentee_button)

                        // Reset bar styles
                        reset_bar_styles();

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
                    // Create mentee list from mentee list string
                    const mentee_id_list = create_mentee_list(user_mentees);

                    // Get mentee id is inlcuded in mentor mentees
                    mentee_id = prev_event.user_id

                    // Determine if last event is an remove mentor mentee event and mentee is included in mentee list
                    if (prev_event.type == EVENT_TYPES.REMOVE_MENTOR_MENTEE & mentee_id_list.includes(mentee_id))
                    {
                        // Update mentee bar
                        update_mentee_bar_remove(mentee_bar)

                        // Update mentor bar to include 1 less mentee and list
                        decerment_mentor_mentees(user_bar);

                        // Pass button and reset button to be off
                        reset_button_style(remove_mentee_button)

                        // Reset bar styles
                        reset_bar_styles();

                        // Create and store remove mentor mentor event in queue
                        event_queue.enqueue(EVENT_TYPES.REMOVE_MENTOR_MENTOR, user_id);

                        // Reset remove event flag
                        remove_mentor_flag = 0;

                        alert("mentor remove mentor");

                    }
                }
            }
        }
    }
}

export function select_mentee_mentor_event(user_bar)
{
    // NEED TO SET UP TOGGLE FOR THIS SO CLICKING THE SAME BUTTON WILL CANCEL WITHOUT START ELSE JUST CANCEL AND START NEW ONE
    // NEED TO UPDATE CHECK CANCEL TO INCLUDE THIS <---

    // // Check if this or 

    // // Set select mentee flag
    // select_mentee_flag = 1;

    // Initlize selected mentee bars as empty list
    let selected_mentees_bars = []

    // Updates to display mentees included in mentee list of passed user bar
    const user_mentees = user_bar.querySelector("#user_mentees").textContent.trim();

    // Create mentee list from mentee list string
    const mentee_id_list = create_mentee_list(user_mentees);

    // Create list of mentee bars from mentee id list
    selected_mentees_bars = return_mentee_bars_from_ids(mentee_id_list);

    // Update mentee bars styles from list
    update_choice_bar_styles(selected_mentees_bars);

    alert("select mentor's mentees")
}

// REMOVING FUNCTIONALLTY 
// export function promote_super_mentor_event(user_bar)
// {
//     // Determine user id from hidden value in passed user bar
//     const user_id = user_bar.querySelector("#user_account").textContent.trim();

//     // Check and cancel last event if needed
//     check_cancel_event();

//     // Create and store remove mentor mentor event in queue
//     event_queue.enqueue(EVENT_TYPES.PROMOTE_SUPER, user_id);

//     // Promotes user to super admin status
//     alert("promote super");
// }

export function promote_organization_mentor_event(user_bar)
{
    // Intitlize toggle flag to 0
    let toggle_flag = 0;

    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Determine organization promote button from user bar
    const organization_promote_button = user_bar.querySelector("#organization_promote_button");

    // Check if queue is not empty
    if (!event_queue.isEmpty())
    {
        // Check if same button was already pressed before
        toggle_flag = check_toggle_event(event_queue.peek_end(), EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR, user_id);

    }

    // Check and cancel last event if needed
    check_cancel_event();

    // Check if button was toggled
    if (!toggle_flag)
    {
        // Last event was different, cont. exeuction normally
        // Set promote organization flag
        promote_organization_flag = 1;

        // Pass button and style button to be on
        update_button_style(organization_promote_button);

        // Style organization bars
        update_choice_bar_styles(organization_bars);

        // Create and store remove mentor mentor event in queue
        event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR, user_id);

    }
    else
    {
        // Last event was the same cancel without attempting to create event
        // Pass button and reset button to be off 
        reset_button_style(organization_promote_button);

        // Remove event from queue
        event_queue.dequeue();
    }
    
    // Promotes user to organization admin status
    alert("promote org")

}

export function edit_organization_mentor_event(user_bar)
{
    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // TODO NEED LOGIC

    alert("edit org")
}

export function transfer_role_mentor_event(user_bar)
{
    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // Create and store remove mentor mentor event in queue
    event_queue.enqueue(EVENT_TYPES.TRANSFER_ROLE, user_id);    

    // Transfers user account role to user
    alert("transfer role")
}

export function decouple_mentor_event(user_bar)
{
    // Determine user id from hidden value in passed user bar
    const user_id = user_bar.querySelector("#user_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // Create and store remove mentor mentor event in queue
    event_queue.enqueue(EVENT_TYPES.DECOUPLE, user_id);

    // Removes mentor from organization
    alert("decouple")
}

export function organization_clicked_event(organization_bar)
{
    // Check if promote organzation flag
    if (promote_organization_flag)
    {
        // Check if mentor is valid and event queue is not empty
        if (!event_queue.isEmpty())
        {
            // Determine organization id from hidden value in passed organization bar
            const organization_id = organization_bar.querySelector("#organization_account").textContent.trim();

            // Store last event
            let prev_event = event_queue.peek_end();

            // Find mentor bar from user id
            const mentor_bar = return_mentor_bar_from_id(prev_event.user_id);

            // Check if mentor_bar is not undefined
            if (mentor_bar != undefined)
            {
                // Determine organization promote button from mentor bar
                const organization_promote_button = mentor_bar.querySelector("#organization_promote_button");

                // Determine if last event is an promote organzation mentor event
                if (prev_event.type == EVENT_TYPES.PROMOTE_ORGANIZATION_MENTOR) 
                {
                    // Pass organization bar and promote mentor to admin of organzation
                    promote_prganzation_admin(organization_bar, mentor_bar);

                    // Pass button and reset button to be off
                    reset_button_style(organization_promote_button);

                    // Reset bar styles
                    reset_bar_styles();

                    // Create and store promote organzation organization event in queue
                    event_queue.enqueue(EVENT_TYPES.PROMOTE_ORGANIZATION_ORGANIZATION, organization_id);

                    // Reset remove event flag
                    remove_mentor_flag = 0;

                    alert("mentor remove mentor");

                }
            }
        }
    }

    alert("org clicked");
}

export function remove_organization_event(organization_bar)
{
    // Determine user id from hidden value in passed user bar
    const organization_id = organization_bar.querySelector("#organization_account").textContent.trim();

    // Check and cancel last event if needed
    check_cancel_event();

    // Updating mentors and organization bar for organization
    remove_organization(organization_bar);

    // Create and store remove organzation organization event in queue
    event_queue.enqueue(EVENT_TYPES.REMOVE_ORGANIZATION, organization_id);

    // Removes organization
    alert("remove");
}
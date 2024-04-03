// Import classes from event_queue file 
import * as updaters from './updaters.js';
import * as determiners from './determiners.js';

// Intitlize filter flags to false
let user_filter_flag = 0;
let organization_filter_flag = 0;
let bar_filter_flag = 0;

// Create filtering bar element
let current_filter_bar;

// Function to check and cancel any filtering occuring
function check_cancel_filter()
{
    // Check if user filter is in progess
    if (user_filter_flag)
    {
        // Detemine user filter button
        const filter_user_button = determiners.determine_filter_user_button();

        // Update user filter button to be off
        updaters.update_off_button_style(filter_user_button);

        // Reset filters
        updaters.update_reset_filter();

        // Update flag value
        user_filter_flag = 0;

    }

    // Check if orgnaizatiton filter is in progess
    if (organization_filter_flag)
    {
        // Determine filter orgnization button 
        const filter_organization_button = determiners.determine_filter_organization_button();

        // Update organization filter button to be off
        updaters.update_off_button_style(filter_organization_button);

        // Reset filters
        updaters.update_reset_filter();

        // Update flag value
        organization_filter_flag = 0;

    }

    // Check if bar filter is in progess
    if (bar_filter_flag)
    {
        // Update all filter buttons included in bars to be off
        updaters.update_reset_bar_filter_buttons();

        // Reset filters
        updaters.update_reset_filter();

        // Reset current filter bar to passed user bar
        current_filter_bar = null;

        // Update flag value
        bar_filter_flag = 0;

    }
}

// Function to toggle the user button between on and off state
export function toggle_user_filter(user_input) 
{
    // Check if user filter is active
    if (user_filter_flag)
    {
        // Filter is active
        // Cancel filter
        check_cancel_filter();

    }
    else
    {
        // Filter is invactive
        // Attempt to filter by user input
        attempt_user_filter(user_input);

    }   
}

// Function to toggle the organization button between on and off state
export function toggle_organization_filter(user_input) 
{
    // Check if organization is active
    if (organization_filter_flag)
    {
        // Filter is active
        // Cancel filter
        check_cancel_filter();

    }
    else
    {
        // Filter is inactive
        // Attempt to filter by user input
        attempt_organziation_filter(user_input);

    }
}

// Function to filter user bars for passed input
export function attempt_user_filter(user_input)
{
    // Check and cancel last filter if needed
    check_cancel_filter();

    // Determine filter user button
    const filter_user_button = determiners.determine_filter_user_button();

    // Update button to be on
    updaters.update_on_button_style(filter_user_button);

    // Set user filter flag to active
    user_filter_flag = 1;

    // Check if the input is empty
    if (user_input != "")
    {
        // If not empty than filter by string
        updaters.update_filter_user_bars(user_input);
    }
    else
    {
        // Reset filter
        updaters.update_reset_filter();
    }
}

// Function to filter organization bars for passed input
export function attempt_organziation_filter(user_input)
{
    // Check and cancel last filter if needed
    check_cancel_filter();

    // Determine filter orgnaization button
    const filter_organization_button = determiners.determine_filter_organization_button();

    // Update button to be on
    updaters.update_on_button_style(filter_organization_button);

    // Set user filter flag to active
    organization_filter_flag = 1;

    // Check if input is empty
    if (user_input != "")
    {
        // If not empty than filter by string
        updaters.update_filter_organization_bars(user_input);
    }
    else
    {
        // Reset filter
        updaters.update_reset_filter();

    }
}


// PRESSSING A MENTOR MENTEE BUTTON AND BAR FLAG ALREADY IS ACTIVE SHOULD RESET FILTERS

// Function to filter mentee bars for mentee value from passed bar
export function attempt_mentor_mentee_filter(user_bar)
{
    // Check if account is not disabled
    if (!determiners.determine_disabled_value(user_bar))
    {
        // Check if passed user bar is the same as the currrent filter bar
        if (user_bar != current_filter_bar)
        {
            // Bar element is different
            // Check and cancel last filter if needed
            check_cancel_filter();

            // Update mentor mentee button
            updaters.update_on_button_style(determiners.determine_mentor_mentee(user_bar));

            // Updates to display mentees included in mentee list of passed user bar
            const user_mentees = determiners.determine_mentees_value(user_bar);

            // Create mentee list from mentee list string
            const mentee_id_list = determiners.return_array_from_string(user_mentees);

            // Create list of mentee bars from mentee id list
            const selected_mentees_bars = determiners.return_mentee_bars_from_ids(mentee_id_list);

            // Update all but passed mentee bars to be hidden
            updaters.update_filter_all_mentee_bars_but_passed(selected_mentees_bars);

            // Set current filter bar to passed user bar
            current_filter_bar = user_bar

            // Set bar filter to active
            bar_filter_flag = 1;

        }
        else
        {
            // Bar element is the same
            // Reset current filter bar to nothing
            check_cancel_filter(); 

        }
    }
}
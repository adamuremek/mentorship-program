// Select and store bar elements
const mentee_bars = mentee_bar_container.querySelectorAll(".mentee_management_bar");
const mentor_bars = mentor_bar_container.querySelectorAll(".mentor_management_bar_container");
const organization_bars = mentor_bar_container.querySelectorAll(".organization_management_bar_container");

// Return disable value from passed bar
export function determine_disabled_value(passed_bar)
{
    return Number(passed_bar.querySelector("#user_account_disabled").textContent.trim());

}

// Determine current mentees value from passed bar
export function determine_current_mentees_value(passed_bar)
{
    return Number(passed_bar.querySelector("#current_mentees").textContent);

}

// Determine max mentees value from passed bar
export function determine_max_mentees_value(passed_bar)
{
    return Number(passed_bar.querySelector("#max_mentees").textContent);

}

// Return disable element from passed bar
export function determine_disabled(passed_bar)
{
    return passed_bar.querySelector("#user_account_disabled");

}

// Returns current mentees element from passed bar
export function determine_current_mentees(passed_bar)
{
    return passed_bar.querySelector("#current_mentees");
}

// Returns disable button from passed bar
export function determine_disable_button(passed_bar)
{
    return passed_bar.querySelector("#trashcan_button");

}

// Returns enable button from passed bar
export function determine_enable_button(passed_bar)
{
    return passed_bar.querySelector("#trashcan_off_button");

}

// Returns mentor element from passed bar
export function determine_mentor(passed_bar)
{
    return passed_bar.querySelector("#user_mentor");

}

// Returns add button element from passed bar
export function determine_add_button(passed_bar)
{
    return passed_bar.querySelector("#plus_button");

}

// Returns remove button element from passed bar
export function determine_remove_button(passed_bar)
{
    return passed_bar.querySelector("#remove_button");

}

export function determine_transfer_role_button(passed_bar)
{
    return passed_bar.querySelector("#transfer_role_button");

}

// Returns user id value from passed bar
export function determine_user_id(passed_bar)
{
    return passed_bar.querySelector("#user_account").textContent.trim();

}

// Return mentees value from passed bar
export function determine_mentees_value(passed_bar)
{
    return passed_bar.querySelector("#user_mentees").textContent.trim();

}

// Return mentees element from passed bar
export function determine_mentees(passed_bar)
{
    return passed_bar.querySelector("#user_mentees");
}

// Return mentor value from passed bar
export function determine_mentor_id(passed_bar)
{
    return passed_bar.querySelector("#user_mentor").textContent.trim();

}

// Returns organization id from passed bar
export function determine_organization_id(passed_bar)
{
    return passed_bar.querySelector("#organization_account").textContent.trim();

}

// Return parent organization bar element from passed bar
export function determine_parent_organization_bar_element(passed_bar)
{
    return passed_bar.parentElement.parentElement;

}

// Returns all mentor bars from passed bar
export function determine_mentor_bars(passed_bar)
{
    return passed_bar.querySelectorAll(".mentor_management_bar_container");

}

// Returns edit organizition button from passed bar
export function determine_edit_organization_button(passed_bar)
{
    return passed_bar.querySelector("#edit_organization_button");

}

// Returns mentee list element from passed bar
export function determine_organization_mentor_list(passed_bar)
{
    return passed_bar.querySelector("#mentor_list");

}

// Returns admin list element from passed bar
export function determine_organization_admin_list(passed_bar)
{
    return passed_bar.querySelector("#admin_list");

}

// Returns value based on if passed bar is mentee
export function determine_if_bar_mentee(passed_bar)
{
    return passed_bar.querySelector("#user_mentor") != null;

}

// Returns value based on if passed bar is
export function determine_if_bar_organization_admin(organitization_bar, user_bar)
{
    // Initlize return value to 0
    let return_value = 0;

    // Determine organization admin list
    const organitization_admin_list = determine_organization_admin_list(organitization_bar)

    // Determine mentors of mentor list
    const current_mentors = determine_mentor_bars(organitization_admin_list);

    // Check if current list is not empty
    if (current_mentors != null)
    {
        // Cycle through current mentors
        for (let index = 0; index < current_mentors.length; index++) 
        {
            // Check if current mentor matches passed user bar
            if (current_mentors[index] == user_bar)
            {
                // Set return value to 1
                return_value = 1;

                // Break cycle
                break;

            }
        }
    }

    return return_value;
}

// Returns organization value from passed bar
export function determine_organization_name(passed_bar)
{
    return passed_bar.querySelector(".organization_management_bar_name");

}

// Returns user name value from passed bar
export function determine_user_name(passed_bar)
{
    return passed_bar.querySelector(".user_management_bar_name");

}

// Returns mentee counter counter from passed bar
export function determine_mentor_mentee(passed_bar)
{
    return passed_bar.querySelector(".mentee_counter_container");

}

// Returns filter buttons from bars
export function determine_bar_filter_buttons() 
{
    // Initltize list for filter buttons
    let filter_buttons = [];

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Determine mentee filter button
        filter_buttons.push(determine_mentor_mentee(mentor_bar));

    });

    return filter_buttons;

}





// Then cycles through list of mentor bars checking if they have reached their limit of mentees
export function return_updated_mentor_list()
{
    // Inititlize return value to an empty list
    let valid_mentor_bars = [];

    // Cycles through mentor list determining and storing valid mentors in valid_mentor_bars
    mentor_bars.forEach(mentor_bar => { 
        // Set current and max mentee values
        let current_mentees = determine_current_mentees_value(mentor_bar);
        let max_mentees = determine_max_mentees_value(mentor_bar);

        // Determine if mentor is valid for new mentees
        if (current_mentees < max_mentees)
        {
            // Add mentor bar to valid mentor bars
            valid_mentor_bars.push(mentor_bar);

        }
    });

    return valid_mentor_bars;
}

// Cycles through organization bars pushing to return list if they are not passed bar, then return it 
export function return_list_all_but_passed_organiztion_bar(passed_bar)
{
    // Inititlize return list to an empty list
    let return_organization_list = [];

    // Cycle through organization bars checking if they are the passed bar
    for (let index = 0; index < organization_bars.length; index++) {
        // Check if organization is not passed_bar
        if (organization_bars[index] != passed_bar)
        {
            // Push organization bar to return list
            return_organization_list.push(organization_bars[index]);

        }
    }

    return return_organization_list;

} 

// Returns list of all mentors in mentor list of passed organization
export function return_mentor_list_all(organization_bar)
{
    // Determine mentor list in organization bar
    const mentor_list = determine_organization_mentor_list(organization_bar);

    // Determine mentors of mentor list
    return determine_mentor_bars(mentor_list);

}

// Returns list of all mentors in admin list of passed organization
export function return_admin_list_all(organitization_bar)
{
    // Determine admin list in organization bar
    const admin_list = determine_organization_admin_list(organitization_bar);

    // Determine mentors of admin list
    return determine_mentor_bars(admin_list);
}

// // Returns list of mentors within admin list of expept for passed user_bar
// export function return_mentor_list_all_but_passed_mentor_bars(organization_bar, user_bar)
// {
//     // Initlize return list to an empty list
//     let return_mentor_list = [];

//     // Determine mentor list in organization bar
//     const mentor_list = determine_organization_mentor_list(organization_bar);

//     // Determine mentors of mentor list
//     const current_mentors = determine_mentor_bars(mentor_list);

//     // Check if current list is not empty
//     if (current_mentors != null)
//     {
//         // Cycle through current mentors
//         current_mentors.forEach(current_mentor => {
//             // Check if current admin is the same as user id
//             if (current_mentor != user_bar)
//             {
//                 // Push current mentor into return mentor list
//                 return_mentor_list.push(current_mentor);

//             }
//         });
//     }

//     return return_mentor_list;
// }

// Cycle through mentee bars and return bar matching mentee id
export function return_mentee_bar_from_id(user_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Cycle through mentee bars
    for (let index = 0; index < mentee_bars.length; index++)
    {
        // Determine user id and mentor from hidden value in passed user bar
        const mentee_id = determine_user_id(mentee_bars[index]);

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
export function return_mentor_bar_from_id(user_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Check if passed id doesn't equal None
    if (user_id != "None")
    {
        // Cycle through mentee bars
        for (let index = 0; index < mentor_bars.length; index++)
        {
            // Determine user id and mentor from hidden value in passed user bar
            const mentor_id = determine_user_id(mentor_bars[index])

            // Check if user id field is the same as passed id
            if (user_id == mentor_id)
            {
                // Set return bar
                return_bar = mentor_bars[index];

                // Break loop
                break;

            }
        }
    }

    return return_bar;

}

// Cycle thorugh bars searching for bars matching one of the passed ids
export function return_mentee_bars_from_ids(user_ids)
{
    // Initlize return value as undefined and flag as false 
    let return_bars = [];

    // Check if passed array is empty
    if (user_ids.length > 0)
    {
        // Cycle through mentee bars
        mentee_bars.forEach(mentee_bar => {
            // Determine user id and mentor from hidden value in passed user bar
            const mentor_id = determine_user_id(mentee_bar);

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
    }

    return return_bars;

}

// Takes in passed string, creates and returns array
export function return_array_from_string(passed_list_string)
{
    // Intitlize to empty array
    let return_array = []

    // Check if passed string is empty
    if (passed_list_string != "")
    {
        // Split by commas
        return_array = passed_list_string.split(",");

    }

    return return_array

}
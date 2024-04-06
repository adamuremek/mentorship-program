// Determnine and store mentee bar elements and container elements
const mentee_bar_container = document.querySelector("#mentee_bar_container");
const mentor_bar_container = document.querySelector("#mentor_bar_container");
const mentee_bars = mentee_bar_container.querySelectorAll(".mentee_management_bar_container");
const mentor_bars = mentor_bar_container.querySelectorAll(".mentor_management_bar_container");

// Determine static page elements
const save_button = document.getElementById("save_button");
const cancel_button = document.getElementById("cancel_button");
const add_new_organization_button = document.getElementById("add_new_organization_button");
const filter_user_button = document.querySelector("#filter_users_button");
const filter_organization_button = document.querySelector("#filter_organization_button");
const user_search_bar = document.querySelector("#user_search_bar");
const organization_search_bar = document.querySelector("#organization_search_bar");
const session_user_admin_flag = document.querySelector("#session_user_admin_flag");
const user_management_message = document.querySelector(".user_management_message_bar");

// Determine and store organzition elements
let organization_bars = mentor_bar_container.querySelectorAll(".organization_management_bar_container");
const create_organization_button = document.getElementById("create_organization_button");
const exit_add_new_organization_button = document.getElementById("exit_add_new_organization_button");
const add_new_organization_modal = document.querySelector("#organization-modal");
const add_new_organization_message_bar = add_new_organization_modal.querySelector(".create_organization_message_bar");
const add_new_organization_name = add_new_organization_modal.querySelector(".user-input");
let organization_counter = document.querySelector("#organization_counter");

// From page elements
// Return mentee bar element container from document
export function determine_mentee_bar_container()
{
    return mentee_bar_container;

}

// Return mentor bar element container from document
export function determine_mentor_bar_container()
{
    return mentor_bar_container;
    
}

// Return all mentee bar elements from document
export function determine_all_mentee_bars()
{
    return mentee_bars;

}

// Return all mentor bar elements from document
export function determine_all_mentor_bars()
{
    return mentor_bars;

}

// Return all organization bar elements from document
export function determine_all_organization_bars()
{
    return organization_bars;

}

// Returns save button element from document
export function determine_save_button()
{
    return save_button; 

}

// Returns camcel button element from document
export function determine_camcel_button()
{
    return cancel_button;

}

// Returns add new orgnization button element from document
export function determine_add_new_organization_button()
{
    return add_new_organization_button;

}

// Returns create organization button element from document
export function determine_create_organization_button()
{
    return create_organization_button;

}

// Returns exit add new orgnization button element from document
export function determine_exit_add_new_organization_button()
{
    return exit_add_new_organization_button;

}

// Returns filter user button element from document
export function determine_filter_user_button()
{
    return filter_user_button;

}

// Returns filter organization button element from document
export function determine_filter_organization_button()
{
    return filter_organization_button;

}

// Returns user search bar element from document
export function determine_user_search_bar()
{
    return user_search_bar;

}

// Returns organization search bar element from document
export function determine_organization_search_bar()
{
    return organization_search_bar;

}

// Returns add new organization modal element from document
export function determine_add_new_organization_modal()
{
    return add_new_organization_modal;

}

// Returns organization counter element from document
export function determine_organization_counter()
{
    return organization_counter;

}

// Find and returns name element within add new organizaition modal
export function determine_add_new_organization_name()
{
    return add_new_organization_name;

}

// Find and return error message element within add new organization modal
export function determine_add_new_organization_message_bar()
{
    return add_new_organization_message_bar;

}

// Return 
export function determine_user_management_message()
{
    return user_management_message;

}





// From page elements
// Returns values
// Returns session user organization flag value
export function determine_session_user_admin_flag()
{
    return session_user_admin_flag.textContent.trim();

}





// From bar elements
// Return elements
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

// Returns transfer role super admin button from passed bar
export function determine_transfer_role_super_admin_button(passed_bar)
{
    return passed_bar.querySelector("#transfer_role_super_admin_button");

}

// Returns transfer role organization admin button from passed bar
export function determine_transfer_role_organization_admin_button(passed_bar)
{
    return passed_bar.querySelector("#transfer_role_organization_admin_button");

}

// Returns promote super button form passed bar
export function determine_promote_super_button(passed_bar)
{
    return passed_bar.querySelector("#super_promote_button");

}

// Returns promote organization button from passed bar
export function determine_promote_organization_button(passed_bar)
{
    return passed_bar.querySelector("#organization_promote_button");

}

// Return mentees element from passed bar
export function determine_mentees(passed_bar)
{
    return passed_bar.querySelector("#user_mentees");
}


// Returns all mentor bars from passed bar
export function determine_mentor_bars(passed_bar)
{
    return passed_bar.querySelectorAll(".mentor_management_bar_container");

}

// Returns all mentee bars from passed bar
export function determine_mentee_bars(passed_bar)
{
    return passed_bar.querySelectorAll(".mentee_management_bar_container");

}

// Returns edit organizition button from passed bar
export function determine_edit_organization_button(passed_bar)
{
    return passed_bar.querySelector("#edit_organization_button");

}

// Returns decouple mentor button from passed bar
export function determine_decouple_button(passed_bar)
{
    return passed_bar.querySelector("#decouple_button");

}

// Returns organization account element from passed bar
export function determine_organization_account(passed_bar)
{
    return passed_bar.querySelector("#organization_account");

}

// Return organization name element from passed bar
export function determine_organization_name(passed_bar)
{
    return passed_bar.querySelector(".organization_management_bar_name");

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

// Returns orgnzation remove button from passed bar
export function determine_remove_organization_button(passed_bar)
{
    return passed_bar.querySelector("#remove_organization_button");

}

// Returns mentee counter counter from passed bar
export function determine_mentor_mentee(passed_bar)
{
    return passed_bar.querySelector(".mentee_counter_container");

}







// From bar elements
// Return values
// Returns user name value from passed bar
export function determine_user_name(passed_bar)
{
    return passed_bar.querySelector(".user_management_bar_name").innerHTML.trim().toLowerCase();

}

// Returns organization value from passed bar
export function determine_organization_name_value(passed_bar)
{
    return passed_bar.querySelector(".organization_management_bar_name").innerHTML.trim();

}

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

// Returns account id value from passed bar
export function determine_id(passed_bar)
{
    return passed_bar.querySelector("#account").textContent.trim();

}

// Returns user id vlaue from passed bar
export function determine_user_id(passed_bar)
{
    return passed_bar.querySelector("#user_account").textContent.trim();

}

// Return mentees value from passed bar
export function determine_mentees_value(passed_bar)
{
    return passed_bar.querySelector("#user_mentees").textContent.trim();

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

// Returns session user flag value from passed bar
export function determine_session_user_flag_value(passed_bar)
{
    return passed_bar.querySelector("#session_user_flag").textContent.trim();

}





// Determiners
// Determines the parent organization bar element from all organization bar based on passed bar element
export function determine_parent_organization_bar_element(passed_bar)
{
    // Initltize parent organization bar to undefined and found flag to false
    let parent_organization_bar_element = undefined; 
    let found_flag = false;

    // Determine organization all bar elements
    const organization_bars = determine_all_organization_bars();

    // Cycle through organization elements
    for (let organiation_index = 0; organiation_index < organization_bars.length; organiation_index++) {
        // Check if found flag is true
        if (found_flag)
        {
            // Break loop
            break;

        }

        // Determine admin list and mentor list of organization
        let admin_list = determine_organization_admin_list(organization_bars[organiation_index]);
        let mentor_list = determine_organization_mentor_list(organization_bars[organiation_index]);

        // Determine mentors from list
        let admins = determine_mentor_bars(admin_list);
        let mentors = determine_mentor_bars(mentor_list);

        // Loop through admins
        for (let index = 0; index < admins.length; index++) {
            // Check if admin bar is the same as passed bar
            if (passed_bar == admins[index])
            {
                // Store parent organization bar 
                parent_organization_bar_element = organization_bars[organiation_index];

                // Set found flag to true
                found_flag = true;

            }   
        }

        // Loop through mentors
        for (let index = 0; index < mentors.length; index++) {
            // Check if mentor bar is the same as passed bar
            if (passed_bar == mentors[index])
            {
                // Store parent organization bar 
                parent_organization_bar_element = organization_bars[organiation_index];

                // Set found flag to true
                found_flag = true;
            }
        }
    }

    return parent_organization_bar_element;

}

// Searches first mentors then mentee bars for session user bar
export function determine_session_user_bar()
{
    // Initltize session user bar to null
    let session_user_bar = undefined 

    // Determine mentee and mentor bar elements
    const mentor_bars = determine_all_mentor_bars();
    const mentee_bars = determine_all_mentee_bars();

    // Cycle through mentor bars
    for (let index = 0; index < mentor_bars.length; index++) 
    {
        // Determine session user flag value is true
        if (1 == determine_session_user_flag_value(mentor_bars[index]))
        {
            // Set session user bar to currernt mentor bar
            session_user_bar = mentor_bars[index];

            // Break loop
            break;

        }
    }

    // Check if session user bar is not found
    if (!session_user_bar == undefined)
    {
        // Cycle through mentee bars
        for (let index = 0; index < mentee_bars.length; index++) 
        {
            // Determine session user flag value is true
            if (1 == determine_session_user_flag_value(mentee_bars[index]))
            {
                // Set seesion user bar to current mentee bar
                session_user_bar = mentee_bars[index];

                // Break loop
                break;

            }
        }

    }

    return session_user_bar;

}

// Then cycles through list of mentor bars checking if they have reached their limit of mentees
export function return_updated_mentor_list()
{
    // Inititlize return value to an empty list
    let valid_mentor_bars = [];

    // Determine all mentor bar elements
    const mentor_bars = determine_all_mentor_bars();

    // Cycles through mentor list determining and storing valid mentors in valid_mentor_bars
    mentor_bars.forEach(mentor_bar => { 
        // Set current and max mentee values
        let current_mentees = determine_current_mentees_value(mentor_bar);
        let max_mentees = determine_max_mentees_value(mentor_bar);

        // Determine if mentor is valid for new mentees and mentor is not disabled
        if (current_mentees < max_mentees && !determine_disabled_value(mentor_bar))
        {
            // Add mentor bar to valid mentor bars
            valid_mentor_bars.push(mentor_bar);

        }
    });

    return valid_mentor_bars;
}

// Returns value based on if passed user bar is an admin for passed organization bar 
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

// Return value based on if the 2 passed bars are valid for tranfering roles
export function determine_if_bars_valid_transfer(organization_bar, passed_bar_1, passed_bar_2)
{
    // Determine if passed bar 1 is organization admin and passed bar 2 is not organization admin or if passed bar 1 is not organization admin and passed bar 2 is organization admin
    return ((determine_if_bar_organization_admin(organization_bar, passed_bar_1) && !determine_if_bar_organization_admin(organization_bar, passed_bar_2)) ||
    (!determine_if_bar_organization_admin(organization_bar, passed_bar_1) && determine_if_bar_organization_admin(organization_bar, passed_bar_2)) );

}

// Returns value based on if the passed mentor bar's organization bar and the passed organization bars match
export function determine_if_bars_valid_edit_organzation(organitization_bar, mentor_bar)
{
    // Inintlize return value to false
    let return_value = false;

    // Determine prev organitization bar from mentor bar
    const prev_organitization_bar = determine_parent_organization_bar_element(mentor_bar);

    // Determine if mentor is within a organization
    if ((prev_organitization_bar != null))
    {
        // Mentor has organization
        // Check if mentor is within the same organization already
        if (determine_organization_id(prev_organitization_bar) != determine_organization_id(organitization_bar))
        {
            return_value = true;
        }
    }
    else
    {
        // Mentor do not have organization
        return_value = true;

    }

    return return_value;

}

// Returns value based on if passed bar is mentee
export function determine_if_bar_mentee(passed_bar)
{
    return passed_bar.querySelector("#user_mentor") != null;

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

// Cycle through mentee bars and return bar matching mentee id
export function return_mentee_bar_from_user_id(user_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Determine mentee bars elements
    const mentee_bars = determine_all_mentee_bars();

    // Cycle through mentee bars
    for (let index = 0; index < mentee_bars.length; index++)
    {
        // Determine id and mentor from hidden value in passed user bar
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
            // Determine id and mentor from hidden value in passed user bar
            const mentor_id = determine_id(mentor_bars[index])

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


// Cycle through mentor bars and return bars matching user id
export function return_mentor_bar_from_user_id(user_id)
{
    // Initlize return value as undefined
    let return_bar = undefined;

    // Check if passed id doesn't equal None
    if (user_id != "None")
    {
        // Cycle through mentee bars
        for (let index = 0; index < mentor_bars.length; index++)
        {
            // Determine id and mentor from hidden value in passed user bar
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

    // Detemine mentee bar elements
    const mentee_bars = determine_all_mentee_bars();

    // Check if passed array is empty
    if (user_ids.length > 0)
    {
        // Cycle through mentee bars
        mentee_bars.forEach(mentee_bar => {
            // Determine id and mentor from hidden value in passed user bar
            // const mentor_id = determine_id(mentee_bar);
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

// Will search through organization names and return value based on if passed name unqiue 
export function determine_if_organization_name_unique(new_organization_name)
{
    // Initlize unique flag to true
    let unique_flag = true;

    // Determine all organization bars
    const all_roganization_bars = determine_all_organization_bars();

    // Cycle through organization bars
    for (let index = 0; index < all_roganization_bars.length; index++)
    {
        // Determine current organization name value
        let current_organization_name = determine_organization_name_value(all_roganization_bars[index]).toLowerCase();

        // Check if current organization is the same as passed new organization name
        if (current_organization_name == new_organization_name)
        {
            // Set unique flag value to false
            unique_flag = false;

            // Break loop
            break;

        }
        
    }

    return unique_flag;

}

// Refresh the determiner variable for all organization bars 
export function deteremine_and_refresh_all_organization_bars()
{
    organization_bars = mentor_bar_container.querySelectorAll(".organization_management_bar_container");

}

// Returns value based on if there are any users in passed organization
export function determine_if_organization_is_empty(passed_organiation)
{
    // Determine organization admin list
    const admin_list = determine_organization_admin_list(passed_organiation);

    // Determine admin bars
    const admin_bars = determine_mentor_bars(admin_list);

    // Determine organization mentor list
    const mentor_list = determine_organization_mentor_list(passed_organiation);

    // Determine mentor bars
    const mentor_bars = determine_mentor_bars(mentor_list);

    // Return value based on if either admin or mentor bars have any bars
    return !(admin_bars.length > 0 || mentor_bars.length > 0);

}

// Returns value based on if passed button element is a word
export function determine_if_word_button(passsed_button)
{
    // Checks passed button's class list and check if it has an active or inactive class for word buttons
    return (passsed_button.classList.contains("admin_user_management_word_button_active") || passsed_button.classList.contains("admin_user_management_word_button_inactive"))

}

// Returns id value based on numbers within id string
export function determine_id_from_string(id_string)
{
    // Replace all letters, spaces, and () char
    return id_string.replaceAll(/[a-zA-Z ()]*/g,"");
    
}

// Return value based on if prev_event is the same event type and user id, Else will return 0
export function deteremine_if_event_toggle(prev_event, new_event_type, new_event_id)
{
    // Initlize return number value to 0
    let return_flag = 0;

    // Check and set if prev event is the same as the new event
    if (prev_event.type == new_event_type & prev_event.data == new_event_id)
    {
        return_flag = 1;
    }

    return return_flag;
}

// Function returns values based on if passed mentor is included in passed mentor bars
export function determine_if_mentor_included_in_passed_bars(valid_mentor_bars, mentor_bar)
{
    // Initilize found flag to 0
    let found_flag = 0;

    // Cycle through valid mentor bars
    for (let index = 0; index < valid_mentor_bars.length; index++) 
    {
        // Check if passed user bar is same as the valid mentor bar
        if (mentor_bar == valid_mentor_bars[index])
        {
            // Set found flag to 1
            found_flag = 1;

            break;
        }
    }

    return found_flag;
}

// Function returns filter buttons from bars
export function determine_bar_filter_buttons() 
{
    // Initltize list for filter buttons
    let filter_buttons = [];

    // Determine all mentor bars
    const mentor_bars = determine_all_mentor_bars();

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Determine mentee filter button
        filter_buttons.push(determine_mentor_mentee(mentor_bar));

    });

    return filter_buttons;

}



// // Returns value based on if there is not unaffiliated mentors in the mentor bar container
// export function determine_if_no_unaffiliated_mentors()
// { 
//     // Initlize no unaffiliated mentors flag to true
//     let no_unaffiliated_mentors_flag = true;

//     // Detrmine mentor bars within mentor bar container
//     const mentor_bars = determine_mentor_bars(mentor_bar_container);

//     // Cycle through mentor bars
//     for (let index = 0; index < mentor_bars.length; index++) {
//     // mentor_bars.forEach(mentor_bar => {
//         // Check if mentor bars bar's parent element class list if it is a oragnization bar
//         if (mentor_bars[index].parentNode.parentNode.classList.contains("organization_management_bar_container"))
//         {
//             // Set no unaffiliated mentors flag to true
//             no_unaffiliated_mentors_flag = true;

//         }
//         else 
//         {
//             // Set no unaffiliated mentors flag to false
//             no_unaffiliated_mentors_flag = false;

//             // Break loop
//             break;

//         }
//     };

//     return no_unaffiliated_mentors_flag;

// }








// // Returns elements from any bar
// // Returns organization management bar container from any organization bar
// export function determine_organization_management_bar_container()
// {
//     // Determine mentor bar container 
//     const mentor_bar_container = determine_mentor_bar_container();

//     return mentor_bar_container.querySelector(".organization_management_bar_container");

// }


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
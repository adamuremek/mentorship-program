// Import functions from determiners.js
import * as determiners from "./determiners.js";

// Updates display elements
// Function updates modal class list to make it visable
export function show_add_new_organization_modal()
{
    // Determine add new organization modal
    const add_new_organization_modal = determiners.determine_add_new_organization_modal();

    // Update modal style to visable
    add_new_organization_modal.style.display = "block";

}

// Function updates modal class list to make it not visable
export function hide_add_new_organization_modal()
{
    // Determine add new organization modal
    const add_new_organization_modal = determiners.determine_add_new_organization_modal();

    // Update modal style to not visable
    add_new_organization_modal.style.display = "none";
}

// Function updates orgaization bar element to be removed
export function update_remove_organization(organization_bar)
{
    // Remove organization bar
    organization_bar.remove();

}

// Function updates passed organization bar to include passed mentor bar and update passed mentor bar to include a promote 
// organization button.
export function update_add_to_organization(organization_bar, mentor_bar)
{
    // Remove mentor bar from unaffiliated mentors
    mentor_bar.remove();

    // Determine mentor list, add mentor bar to orgnization mentee list
    determiners.determine_organization_mentor_list(organization_bar).appendChild(mentor_bar);

    // Determine and update to have promote organization admin button
    update_show(determiners.determine_promote_organization_button(mentor_bar));

}

// Function updates passed mentor bar to be passed organization bar 
export function update_promote_organization_admin(organization_bar, mentor_bar)
{
    // Remove mentor from mentee list
    mentor_bar.remove();

    // Determine and add admin list and add mentor to admin list
    determiners.determine_organization_admin_list(organization_bar).appendChild(mentor_bar);

    // Determine and update to have promote organization admin button
    update_not_show(determiners.determine_promote_organization_button(mentor_bar));

}

// Function removes current organization admin of passed organization bar and adds them to mentor list of passed organization
export function update_demote_organization_admin(organization_bar)
{
    // Determine admin list and remove mentor from admin list and add to mentor list
    const current_admins = determiners.determine_mentor_bars(determiners.determine_organization_admin_list(organization_bar));

    // Check if admin list is not empty
    if (current_admins != null)
    {
        // Cycle through mentors included in admin list adding them mentor list
        current_admins.forEach(current_admin => {
            // Remove mentor from admin list
            current_admin.remove();

            // Determine mentor list and add mentor to mentor list
            determiners.determine_organization_mentor_list(organization_bar).appendChild(current_admin);

            // Determine and update to have promote organization admin button
            update_show(determiners.determine_promote_organization_button(current_admin));

        });
    }
}

// Function removes passed mentor bar element from organization and adds it to unailifated mentors 
export function update_remove_from_organization(mentor_bar)
{
    // Removing mentor bar from organization
    mentor_bar.remove();

    // Determine mentor bar continer, then add mentor bar to unaffiliated mentors
    determiners.determine_mentor_bar_container().appendChild(mentor_bar);

    //Determine and update to remove promote organization admin button
    update_not_show(determiners.determine_promote_organization_button(mentor_bar));

}

// Function will remove passed mentee id from mentee values in passed user bar, and decrement mentee value in passed user bar
export function update_decerment_mentor_mentees(user_bar, mentee_id)
{
    // Deteremine current mentees element, decrease and set current value by 1
    determiners.determine_current_mentees(user_bar).innerHTML = determiners.determine_current_mentees_value(user_bar) - 1;

    // Determine mentee values and create array of mentee values from the string
    let updated_mentee_values = determiners.return_array_from_string(determiners.determine_mentees_value(user_bar));

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

    // Determine mentee list, remove and set mentee value by replacing mentee id value with an empty string
    determiners.determine_mentees(user_bar).innerHTML = updated_mentee_values;

}

// Updates current mentee value by 1 and add passed mentee id to mentee list of passed user bar
// Function will add passed mentee id to mentee values in passed user bar, and increment mentee value in passed user bar
export function update_incerment_mentor_mentees(user_bar, mentee_id)
{   
    // Deteremine mentee value and store array from string
    const updated_mentee_values = determiners.return_array_from_string(determiners.determine_mentees_value(user_bar));

    //Deteremine current mentees element, increase and set current value by 1
    determiners.determine_current_mentees(user_bar).innerHTML = determiners.determine_current_mentees_value(user_bar) + 1;

    // Push new value into updated mentee values
    updated_mentee_values.push(mentee_id);

    // Determine mentee list, add to it updated mentee values
    determiners.determine_mentees(user_bar).innerHTML = updated_mentee_values.toString();

}

// Function will update passed bar disabled value, show its enable button, and update its backround to be default
export function update_reable_bar(user_bar)
{
    // Find and set disable element
    determiners.determine_disabled(user_bar).innerHTML = "0";

    // Determine disable and enable button, switch disable button to enable button
    update_buttons_toggle_on(determiners.determine_disable_button(user_bar),
        determiners.determine_enable_button(user_bar));

    // Change background color to disabled
    // -=-=-;
    user_bar.style.background = "none";

}

// Updates passed user bar is be styled as disabled 
// Function will update passed bars disable value, show its disable button, and update its backround to grey
export function update_disable_bar(user_bar)
{
    // Find and set disable element
    determiners.determine_disabled(user_bar).innerHTML = "1";

    // Determine disable and enable button, switch enable button to disable button
    update_buttons_toggle_off(determiners.determine_disable_button(user_bar),
        determiners.determine_enable_button(user_bar));

    // Change background color to disabled (grey)
    // -=-=--;
    update_on_button_style(user_bar);
}

// Cycle through passed bar's styles to include white borders
export function update_valid_choice_bar_styles(passed_bars)
{
    passed_bars.forEach(passed_bar => {
        passed_bar.style.border = "2.5px solid white";
        
    });
}

// Updates bar's style to include red borders
export function update_remove_choice_bar_style(passed_bar)
{
    passed_bar.style.border = "2.5px solid red";
}

// Set all bars to their default border styles
export function update_reset_choice_bar_styles()
{
    // Determine mentee, mentor, and orgnaiztion bar elements
    const mentor_bars = determiners.determine_all_mentor_bars();
    const mentee_bars = determiners.determine_all_mentee_bars();
    const organization_bars = determiners.determine_all_organization_bars();

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
export function update_on_button_style(button)
{
    button.style.background = "darkgray";
    // -=-=-=;

}

// Set button to default button backround
export function update_off_button_style(button)
{
    button.style.background = "rgba(128, 128, 128, 0.25)";
    // -=-=-=-;
    
}

// Set all filter buttons to on
export function update_reset_bar_filter_buttons()
{
    // Inintlize filter buttons to empty list
    const filter_buttons = []

    // Determine mentee and  mentor bar elements
    const mentor_bars = determiners.determine_all_mentor_bars();
    const mentee_bars = determiners.determine_all_mentee_bars()

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Determine add and remove button and add them to filter buttons
        filter_buttons.push(determiners.determine_add_button(mentee_bar));
        filter_buttons.push(determiners.determine_remove_button(mentee_bar));

    });

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Determine and add mentor mentee button to filter buttons 
        filter_buttons.push(determiners.determine_mentor_mentee(mentor_bar));

    });
    
    // Cycle through filter buttons 
    filter_buttons.forEach(filter_button => {
        // Update button styles to be off
        update_off_button_style(filter_button);

    });
}

// Updates mentee bar to show the add button and update mentor value to None
export function update_mentee_bar_remove(user_bar)
{
    // Check if passed bar is undefinfed
    if (user_bar != null)
    {
        // Find and set mentor value to None
        determiners.determine_mentor(user_bar).innerHTML = "None";

        // Find add and remove buttons
        const add_button = determiners.determine_add_button(user_bar);
        const remove_button = determiners.determine_remove_button(user_bar);

        // Switch remove and add buttons
        update_buttons_toggle_off(remove_button, add_button);

    }
}

// Updates mentee bar to show the remove button and update mentor value to new mentor id
export function update_mentee_bar_add(user_bar, mentor_id)
{
    // Find and set mentor value to passed mentor_id
    determiners.determine_mentor(user_bar).innerHTML = mentor_id;

    // Find add and remove buttons
    const add_button = determiners.determine_add_button(user_bar);
    const remove_button = determiners.determine_remove_button(user_bar);

    // Switch add and remove buttons
    update_buttons_toggle_on(remove_button, add_button);

}

// Updates passed organization bar user's transfer button to reflect new postitons
export function update_organization_transfer_buttons(organitization_bar)
{
    // Determine organization admin and mentor list from organization bar
    const organitization_admins = determiners.return_admin_list_all(organitization_bar);
    const organitization_mentors = determiners.return_mentor_list_all(organitization_bar);
    
    // Determine session user bar
    const session_user_bar = determiners.determine_session_user_bar();

    // Cycle through admin list
    organitization_admins.forEach(organitization_admin => {
        // Determine transfer button for admin bar
        let transfer_own_role_button = determiners.determine_transfer_role_organization_admin_button(organitization_admin);

        // Check if organitization admin has transfer own role button
        if (transfer_own_role_button != null)
        {
            // Update to not have transfer own role button
            update_not_show(transfer_own_role_button);

        }
    });

    //Cycle through mentor list
    organitization_mentors.forEach(organitization_mentor => {
        // Determine transfer button for admin bar
        let transfer_own_role_button = determiners.determine_transfer_role_organization_admin_button(organitization_mentor);

        // Check if organitization admin has transfer own role button
        if (transfer_own_role_button != null)
        {
            // Checking if mentor is session user bar
            if (organitization_mentor == session_user_bar)
            {
                // Update to not have transfer own role button
                update_not_show(transfer_own_role_button);

            } 
            else
            {
                // Update to have transfer own role button
                update_show(transfer_own_role_button);

            }
        }
    });
}

// Updates loading overlay to show
export function update_loading()
{
    // Deteremine and set loading overlay to show
    determiners.deteremine_loading_overlay().style.display = "block";

}

// Updates loading overlay to now show
export function update_not_loading()
{
    // Deteremine and set loading overlay to not show
    determiners.deteremine_loading_overlay().style.display = "none";

}

// Updates passed element to show. Remove input inactive class and add active class to input
export function update_show(input)
{
    // Check if input is a word button
    if (determiners.determine_if_word_button(input))
    {
        // Input is word button
        input.classList.remove("admin_user_management_word_button_inactive");
        input.classList.add("admin_user_management_word_button_active");

    }
    // Check if input is a button
    else if (determiners.deteremine_if_button(input))
    {
        // Input is button
        input.classList.remove("admin_user_management_button_clear_inactive");
        input.classList.add("admin_user_management_button_clear_active");

    }
    // Check if input is mentee user bar
    else if (determiners.determine_if_user_mentee_bar(input))
    {
        // Input is mentee user bar
        input.classList.remove("mentee_management_bar_container_inactive");
        input.classList.add("mentee_management_bar_container_active");

    }
    // Check if input is mentor user bar
    else if (determiners.determine_if_user_mentor_bar(input))
    {
        // Input is mentor user bar
        input.classList.remove("mentee_management_bar_container_inactive");
        input.classList.add("mentee_management_bar_container_active");

    }
    // Check if input is a organization bar
    else if (determiners.deteremine_if_organization(input))
    {
        // Input is organzation bar
        input.classList.remove("organization_management_bar_container_inactive");
        input.classList.add("organization_management_bar_container_active");

    }
    // Check if input is create organziation message bar
    else if (determiners.deteremine_if_create_organization_message_bar(input))
    {
        // Input is create organization message bar
        input.classList.remove("create_organization_message_bar_inactive");
        input.classList.add("create_organization_message_bar_active");

    }
    // Check if input is user managment message bar
    else if (determiners.deteremine_if_user_maanagement_message_bar(input))
    {
        input.classList.remove("user_management_message_bar_inactive");
        input.classList.add("user_management_message_bar_active");

    }
}

// Updates passed element to show. Remove input inactive class and add active class to input
export function update_not_show(input)
{
    // Check if input is a word button
    if (determiners.determine_if_word_button(input))
    {
        // Input is word button
        input.classList.remove("admin_user_management_word_button_active");
        input.classList.add("admin_user_management_word_button_inactive");

    }
    // Check if input is a button
    else if (determiners.deteremine_if_button(input))
    {
        // Input is button
        input.classList.remove("admin_user_management_button_clear_active");
        input.classList.add("admin_user_management_button_clear_inactive");

    }
    // Check if input is mentee user bar
    else if (determiners.determine_if_user_mentee_bar(input))
    {
        // Input is mentee user bar
        input.classList.remove("mentee_management_bar_container_active");
        input.classList.add("mentee_management_bar_container_inactive");

    }
    // Check if input is mentor user bar
    else if (determiners.determine_if_user_mentor_bar(input))
    {
        // Input is mentor user bar
        input.classList.remove("mentee_management_bar_container_active");
        input.classList.add("mentee_management_bar_container_inactive");

    }
    // Check if input is a organization bar
    else if (determiners.deteremine_if_organization(input))
    {
        // Input is organzation bar
        input.classList.remove("organization_management_bar_container_active");
        input.classList.add("organization_management_bar_container_inactive");

    }    
    // Check if input is create organziation message bar
    else if (determiners.deteremine_if_create_organization_message_bar(input))
    {
        // Input is create organization message bar
        input.classList.remove("create_organization_message_bar_active");
        input.classList.add("create_organization_message_bar_inactive");

    }
    // Check if input is user managment message bar
    else if (determiners.deteremine_if_user_maanagement_message_bar(input))
    {
        input.classList.remove("user_management_message_bar_active");
        input.classList.add("user_management_message_bar_inactive");

    }
}

// Updates the first passed button class list to hide and the second passed button class list to show
export function update_buttons_toggle_on(passed_button_1, passed_button_2)
{
    // Show passed button 1
    passed_button_1.classList.remove("admin_user_management_button_clear_inactive");
    passed_button_1.classList.add("admin_user_management_button_clear_active");

    // Hide passed button 2
    passed_button_2.classList.remove("admin_user_management_button_clear_active");
    passed_button_2.classList.add("admin_user_management_button_clear_inactive");

}

// Updates the first passed button class list to show and the second passed button class list to hide
export function update_buttons_toggle_off(passed_button_1, passed_button_2)
{
    // Hide passed button 1
    passed_button_1.classList.remove("admin_user_management_button_clear_active");
    passed_button_1.classList.add("admin_user_management_button_clear_inactive");

    // Show passed button 2
    passed_button_2.classList.remove("admin_user_management_button_clear_inactive");
    passed_button_2.classList.add("admin_user_management_button_clear_active");
    
}

// Function updates all disabled user bars with disabled styling and button
export function update_all_disable_bar_style_on()
{
    // Create storage for button elements
    let disable_button, enable_button;

    // Determine all mentor or mentee bars 
    const mentor_bars = determiners.determine_all_mentor_bars();
    const mentee_bars = determiners.determine_all_mentee_bars();

    // Cycle through mentor bars
    for (let index = 0; index < mentor_bars.length; index++) {
        // Check if user bar is disable
        if (determiners.determine_disabled_value(mentor_bars[index]))
        {
            // Determine disable and enable button
            disable_button = determiners.determine_disable_button(mentor_bars[index]);
            enable_button = determiners.determine_enable_button(mentor_bars[index]);

            // Check if disable and enable button are null
            if (disable_button != null & enable_button != null)
            {
                // Switch disable button to enable
                update_buttons_toggle_off(disable_button, enable_button);

            }

            // Change background color to disabled (grey)
            // .style.background = "darkgray";
            update_on_button_style(mentor_bars[index]);

        }
    }

    // Cycle through mentee bars
    for (let index = 0; index < mentee_bars.length; index++) {
        // Check if user bar is disable
        if (determiners.determine_disabled_value(mentee_bars[index]))
        {
            disable_button = determiners.determine_disable_button(mentee_bars[index]);
            enable_button = determiners.determine_enable_button(mentee_bars[index]);

            // Switch disable button to enable
            update_buttons_toggle_off(disable_button, enable_button);

            // Change background color to disabled (grey)
            // .style.background = "darkgray";
            update_on_button_style(mentee_bars[index]);

        }
    }
    
}

// Function will cycle through all organization admin
export function update_all_organization_admin_bars()
{
    // Determine all organization bars
    const organization_bars = determiners.determine_all_organization_bars();

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        // Determine mentors within admin list
        determiners.determine_mentor_bars(determiners.determine_organization_admin_list(organization_bar)).forEach(admin_bar => {
            // Determine and hide promote organization button
            update_not_show(determiners.determine_promote_organization_button(admin_bar));

        });
    });
}





// Filtering methods
// Set all bars elements to visible
export function update_reset_filter()
{

    // Determine mentee, mentor, and orgnaiztion bar elements
    const mentor_bars = determiners.determine_all_mentor_bars();
    const mentee_bars = determiners.determine_all_mentee_bars();
    const organization_bars = determiners.determine_all_organization_bars();

    // Cycles through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Update bar styles to be visible
        update_show(mentee_bar);

    });

    // Cycles through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Update bar styles to be visible
        update_show(mentor_bar);

    });

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        // Update bar styles to be visible
        update_show(organization_bar);

    });
}

// Updates user bars to hide bars that don't match filter
export function update_filter_user_bars(user_input)
{
    // Create storage for temp user name
    let current_user_name;

    // Determine mentee and mentor orgnaiztion bar elements
    const mentor_bars = determiners.determine_all_mentor_bars();
    const mentee_bars = determiners.determine_all_mentee_bars();

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Determine mentee bar name
        current_user_name = determiners.determine_user_name(mentee_bar);

        // Check if mentee bar name dosesn't matche input
        if (!current_user_name.includes(user_input.toLowerCase()))
        {
            // Update mentee bar to be hidden
            update_not_show(mentee_bar);

        }
    });

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Determine mentor bar name
        current_user_name = determiners.determine_user_name(mentor_bar);

        // Check if mentor bar name doesn't matche input
        if (!current_user_name.includes(user_input.trim().toLowerCase()))
        {
            // Update mentor bar to be hiddem
            update_not_show(mentor_bar);

        }
    });
}

// Updates organization bars to hide bars that don't match filter
export function update_filter_organization_bars(user_input)
{
    // Create storage for temp user name
    let current_organization_name;

    // Determine orgnaiztion bar elements
    const organization_bars = determiners.determine_all_organization_bars();

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        // Determine orgnaization bar name
        current_organization_name = determiners.determine_organization_name_value(organization_bar).toLowerCase();

        // Check if orgnaization bar name doesn't match input
        if (!current_organization_name.includes(user_input.trim().toLowerCase()))
        {
            // Update orgnaization bar to be hidden
            update_not_show(organization_bar);

        }
    });
}

// Updates mentee bars to filter all bars not included in passed bars
export function update_filter_all_mentee_bars_but_passed(passed_bars)
{
    // Determine mentee bar elements
    const mentee_bars = determiners.determine_all_mentee_bars();

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Update mentee bar to be hidden
        update_not_show(mentee_bar);

        // Cycle through passed bars
        for (let index = 0; index < passed_bars.length; index++) {
            // Check if mentee bar is the same as passed bar
            if (mentee_bar == passed_bars[index])
            { 
                // Update bar to be visible
                update_show(mentee_bar);

                // Break of passed bar loop
                break;
            }
        }
    });
}





// Creating html element functions
// Creates an organziation bar using the passed name, account, remove and clicked event methods, then attaches it to mentor bar container
export function update_create_organization(organitization_name, organization_account_string, remove_organization_event, organization_clicked_event)
{
    // Determine mentor bar container
    const mentor_bar_container = determiners.determine_mentor_bar_container();

    // Determine if session user is an organization admin
    const session_user_admin_flag = determiners.determine_session_user_admin_flag();

    // Create organization management bar container element
    const organization_management_bar_container_active = document.createElement("div");
    organization_management_bar_container_active.classList.add("organization_management_bar_container_active");

    // Create organization management bar element
    const organization_management_bar = document.createElement("div");
    organization_management_bar.classList.add("organization_management_bar");

    // Attach managment bar to management bar container
    organization_management_bar_container_active.appendChild(organization_management_bar);

    // Create organization bar account element
    const organization_account = document.createElement("div");
    organization_account.id = ("organization_account");
    organization_account.innerHTML = organization_account_string;

    // Attach organization bar account to management bar container
    organization_management_bar_container_active.appendChild(organization_account);

    // Create organization bar name element
    const organization_management_bar_name = document.createElement("div");
    organization_management_bar_name.classList.add("organization_management_bar_name");
    organization_management_bar_name.id = "admin_user_management_medium_text";
    organization_management_bar_name.innerHTML = organitization_name;

    // Attach managment bar name to organization mangement bar
    organization_management_bar.appendChild(organization_management_bar_name);

    // Check if session user is an admin
    if (session_user_admin_flag)
    {
        // Create remove organiation button element
        const remove_organization_button = document.createElement("button");
        remove_organization_button.classList.add("admin_user_management_word_button_active");
        remove_organization_button.id = "remove_organization_button";

        // Create remove organiation button text element
        const remove_button_text = document.createElement("p");
        remove_button_text.id = "admin_user_management_small_text";
        remove_button_text.innerHTML = "REMOVE";

        // Attach remove organization button text to remove organization button
        remove_organization_button.appendChild(remove_button_text);

        // Attach remove organization button to organization mangement bar
        organization_management_bar.appendChild(remove_organization_button);

        // Attach button listner for remove organization button
        remove_organization_button.addEventListener('click', function() { remove_organization_event(organization_management_bar_container_active) });
        
    }

    // Attach organization mangement bar to mentor bar container
    organization_management_bar_container_active.appendChild(organization_management_bar);

    // Craete admin list element
    const admin_list = document.createElement("div");
    admin_list.id = "admin_list";

    // Create admin list title element
    const admin_list_title = document.createElement("p");
    admin_list_title.id = "admin_user_management_small_text";
    admin_list_title.innerHTML = "Admins";

    // Attach admin list title to admin list
    admin_list.appendChild(admin_list_title);

    // Create line break element
    const admin_list_line_break = document.createElement("hr");

    // Attach line break element to admin list
    admin_list.appendChild(admin_list_line_break);

    // Attach admin list to mentor bar container
    organization_management_bar_container_active.appendChild(admin_list);

    // Create mentor list element
    const mentor_list = document.createElement("div");
    mentor_list.id = "mentor_list";

    // Create mentor list title element
    const mentor_list_title = document.createElement("p");
    mentor_list_title.id = "admin_user_management_small_text";
    mentor_list_title.innerHTML = "Mentors"

    // Attach mentor list title to mentor list
    mentor_list.appendChild(mentor_list_title);

    // Create line break element
    const mentor_list_line_break = document.createElement("hr");

    // Attach line break element to admin list
    mentor_list.appendChild(mentor_list_line_break);

    // Attach mentor list to mentor bar container
    organization_management_bar_container_active.appendChild(mentor_list);

    // Create line break element
    const organization_line_break = document.createElement("hr");

    // Attach line break element to mentor bar container
    organization_management_bar_container_active.appendChild(organization_line_break);

    // Attach organization mangement bar to mentor bar container
    mentor_bar_container.appendChild(organization_management_bar_container_active);

    // Attach listener for organization clicked
    organization_management_bar_container_active.addEventListener('click', function() { organization_clicked_event(organization_management_bar_container_active); });

}
// Import functions from determiners.js
import * as determiners from "./determiners.js";

// Select and store bar elements
const mentee_bars = mentee_bar_container.querySelectorAll(".mentee_management_bar");
const mentor_bars = mentor_bar_container.querySelectorAll(".mentor_management_bar_container");
const organization_bars = mentor_bar_container.querySelectorAll(".organization_management_bar_container");

const filter_user_button = document.querySelector("#filter_users_button");
const filter_organization_button = document.querySelector("#filter_organization_button");




// Styling methods 

// Updates bar style to visible
export function update_bar_visible(bar)
{
    bar.style.display = "flex";

}

// Updates bar style to invisible
export function update_bar_hidden(bar)
{
    bar.style.display = "none";

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

}

// Set button to default button backround
export function update_off_button_style(button)
{
    button.style.background = "rgba(128, 128, 128, 0.25)";
    
}

// Set all filter buttons to on
export function update_reset_bar_filter_buttons()
{
    // Inintlize filter buttons to empty list
    const filter_buttons = []

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

// Updates passed buttons class lists to hide enable button and show disable button
export function update_bar_disable_button(disable_button, enable_button)
{
    // Remove disable button active class and add inactive class
    disable_button.classList.remove("admin_user_management_button_clear_active");
    disable_button.classList.add("admin_user_management_button_clear_inactive");
    
    // Remove enable button inactive class and add active class
    enable_button.classList.remove("admin_user_management_button_clear_inactive");
    enable_button.classList.add("admin_user_management_button_clear_active");
}

// Updates passed buttons class lists to hide disable button and show enable button
export function update_bar_enable_button(disable_button, enable_button)
{
    // Remove disable button inactive class and add active class
    disable_button.classList.remove("admin_user_management_button_clear_inactive");
    disable_button.classList.add("admin_user_management_button_clear_active");

    // Remove enable button active class and add inactive class
    enable_button.classList.remove("admin_user_management_button_clear_active");
    enable_button.classList.add("admin_user_management_button_clear_inactive");

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
        update_mentee_bar_show_add_button(remove_button, add_button);

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
    update_mentee_bar_remove_button(remove_button, add_button);

}

// Updates passed button class lists to hide add button and show remove button
export function update_mentee_bar_remove_button(remove_button, add_button)
{
    // Remove remove button inactive class and add active class
    remove_button.classList.remove("admin_user_management_button_clear_inactive");
    remove_button.classList.add("admin_user_management_button_clear_active");

    // Remove add button active class and add inactive class
    add_button.classList.remove("admin_user_management_button_clear_active");
    add_button.classList.add("admin_user_management_button_clear_inactive");
}

// Updates passed button class lists to hide remove button and show add button
export function update_mentee_bar_show_add_button(remove_button, add_button)
{
    // Remove remove button active class and add inactive class
    remove_button.classList.remove("admin_user_management_button_clear_active");
    remove_button.classList.add("admin_user_management_button_clear_inactive");

    // Remove add button inactive class and add active class
    add_button.classList.remove("admin_user_management_button_clear_inactive");
    add_button.classList.add("admin_user_management_button_clear_active");
    
}




// Filtering methods

// Set all bars elements to visible
export function update_reset_filter()
{
    // Cycles through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Update bar styles to be visible
        update_bar_visible(mentee_bar);

    });

    // Cycles through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Update bar styles to be visible
        update_bar_visible(mentor_bar);

    });

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        // Update bar styles to be visible
        update_bar_visible(organization_bar);

    });
}

// Updates user bars to hide bars that don't match filter
export function update_filter_user_bars(user_input)
{
    // Create storage for temp user name
    let current_user_name;

    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Determine mentee bar name
        current_user_name = determiners.determine_user_name(mentee_bar).innerHTML.trim().toLowerCase();

        // Check if mentee bar name dosesn't matche input
        if (!current_user_name.includes(user_input.toLowerCase()))
        {
            // Update mentee bar to be hidden
            update_bar_hidden(mentee_bar);

        }
    });

    // Cycle through mentor bars
    mentor_bars.forEach(mentor_bar => {
        // Determine mentor bar name
        current_user_name = determiners.determine_user_name(mentor_bar).innerHTML.trim().toLowerCase();

        // Check if mentor bar name doesn't matche input
        if (!current_user_name.includes(user_input.trim().toLowerCase()))
        {
            // Update mentor bar to be hiddem
            update_bar_hidden(mentor_bar);

        }
    });
}

// Updates organization bars to hide bars that don't match filter
export function update_filter_organization_bars(user_input)
{
    // Create storage for temp user name
    let current_organization_name;

    // Cycle through organization bars
    organization_bars.forEach(organization_bar => {
        // Determine orgnaization bar name
        current_organization_name = determiners.determine_organization_name(organization_bar).innerHTML.trim().toLowerCase();

        // Check if orgnaization bar name doesn't match input
        if (!current_organization_name.includes(user_input.trim().toLowerCase()))
        {
            // Update orgnaization bar to be hidden
            update_bar_hidden(organization_bar);

        }
    });
}

// Updates filter user button to be on
export function update_filter_user_button_on()
{
    update_on_button_style(filter_user_button);

}

// Update filter user button to be off
export function update_filter_user_button_off()
{
    update_off_button_style(filter_user_button);

}

// Updates filter orgnization button to be on
export function update_filter_organization_button_on()
{
    update_on_button_style(filter_organization_button);

}

// Updates filter orgnization button to be off
export function update_filter_organization_button_off()
{
    update_off_button_style(filter_organization_button);

}

// Updates mentee bars to filter all bars not included in passed bars
export function update_filter_all_mentee_bars_but_passed(passed_bars)
{
    // Cycle through mentee bars
    mentee_bars.forEach(mentee_bar => {
        // Update mentee bar to be hidden
        update_bar_hidden(mentee_bar);

        // Cycle through passed bars
        for (let index = 0; index < passed_bars.length; index++) {
            // Check if mentee bar is the same as passed bar
            if (mentee_bar == passed_bars[index])
            { 
                // Update bar to be visible
                update_bar_visible(mentee_bar);

                // Break of passed bar loop
                break;
            }
        }
    });
}
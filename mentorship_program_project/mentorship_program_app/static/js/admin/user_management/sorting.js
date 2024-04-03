import * as detereminers from "./determiners.js";

// Define alphabetical order comparator, will return 1 if name1 is greater than name2, 
// else -1 if name2 is greater than name1, else 0 if equal 
function alphabetical_user_name_order_comparator(bar1, bar2)
{
    // Determine user name values of bars
    const name1 = detereminers.determine_user_name(bar1);
    const name2 = detereminers.determine_user_name(bar2);

    // Compare name values and return value based on if bar1 name is higher alphabetical order than bar2
    return name1.localeCompare(name2)
}

// Define alphabetical order comparator, will return 1 if name1 is greater than name2, 
// else -1 if name2 is greater than name1, else 0 if equal 
function alphabetical_organization_name_order_comparator(bar1, bar2)
{
    // Determine organization name values of bars
    const name1 = detereminers.determine_organization_name_value(bar1);
    const name2 = detereminers.determine_organization_name_value(bar2);

    // Compare name values and return value based on if bar1 name is higher alphabetical order than bar2
    return name1.localeCompare(name2)
}

// Function removes, sorts, adds passed user bars to passed container based on passed comparer
function sort_bars_by_passed_compare(bar_elements, container, comparator)
{
    // Create sorted array from passed bar element based on comparator
    let sorted_array = Array.from(bar_elements).sort(comparator);

    // Append sorted array in order to passed container
    sorted_array.forEach(user_bar => {
        container.appendChild(user_bar)
    });

}

// Function takes in container, determines mentor bars, then sorts them alphabetically
export function sort_mentor_bar_elements_alphabetically(container)
{
    // Determine all mentor bar elemetns within container
    const mentor_bars = detereminers.determine_mentor_bars(container);

    // Pass elements to sort
    sort_bars_by_passed_compare(mentor_bars, container, alphabetical_user_name_order_comparator);

}

// Function determines organization bars, then sorts them alphabetically
export function sort_all_organization_bar_element_alphabetically()
{
    // Determine mentor bar container
    const mentor_bar_container = detereminers.determine_mentor_bar_container();

    // Determine all organization bar bar elements within container
    const organization_bars = detereminers.determine_all_organization_bars();

    // Sort organizations bar elemenets
    sort_bars_by_passed_compare(organization_bars, mentor_bar_container, alphabetical_organization_name_order_comparator);
}

// Function sorts all bar elemenets on the user management page, it will first do mentee bars, 
// then organizations, then each organization's mentee list
export function sort_all_bar_elements_alphabetically()
{
    // Determine mentee bar container 
    const mentee_bar_container = detereminers.determine_mentee_bar_container();

    // Determine all mentee bar elements within container
    const mentee_bars = detereminers.determine_mentee_bars(mentee_bar_container);

    // // Determine mentor bar container
    // const mentor_bar_container = detereminers.determine_mentor_bar_container();

    // Determine all organization bar bar elements within container
    const organization_bars = detereminers.determine_all_organization_bars();

    // Sort mentee bars elements alphabetically
    sort_bars_by_passed_compare(mentee_bars, mentee_bar_container, alphabetical_user_name_order_comparator);
    
    // // Sort organizations bar elemenets
    // sort_bars_by_passed_compare(organization_bars, mentor_bar_container, alphabetical_organization_name_order_comparator);

    // Sort all organization bar elements
    sort_all_organization_bar_element_alphabetically();

    // For loop organization bars
    organization_bars.forEach(organization_bar => {
        // Determine mentor list from orgnization bar
        let organitization_mentor_list = detereminers.determine_organization_mentor_list(organization_bar);

        // Determine mentor bar elements within container
        const mentor_bars = detereminers.determine_mentor_bars(organitization_mentor_list);

        // Sort mentor bar elements alphabetically
        sort_bars_by_passed_compare(mentor_bars, organitization_mentor_list, alphabetical_user_name_order_comparator);

    });

}
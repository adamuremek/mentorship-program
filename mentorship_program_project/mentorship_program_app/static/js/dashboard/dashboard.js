/*********************************************************************/
/* WRITTEN BY: Logan Z, Matt, Adam C, Jason S                        */
/* (OFFICIAL) DATE CREATED: April 14, 2024                           */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the JavaScript necessary to use functional     */
/*      aspects of the Dashboard                                     */
/* This file is included in 'dashboard.html'                         */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Example Usage:                                                    */
/* <script src="{% static 'js/dashboard/dashboard.js' %}"></script>  */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

/* These event listeners show/hide the Interests popup when it is clicked on */
// I am confident you can figure it out if you read it
// I believe in you bestie :)
var popupRoot = document.getElementById('popup-root')
var popup = document.getElementById('popup')
var popupContent = document.getElementById('inner-popup-content')
popupRoot.addEventListener("mouseup", event => {
    if (event.target != popupContent && (event.target == popupRoot || event.target.parentNode == popup))
        popup.classList.toggle('show')
})


/**
* Returns an array of the currently selected interests
*/
function getInterestFilters() {

    // Get list of filters selected by user
    const filter_tags = document.getElementsByClassName('popup-checkbox-item')
    const selected_filters = []
    // Add string values of interests to an array 
    for(const interest_filter of filter_tags)
        if(interest_filter.querySelector('input').checked) 
        {
            const class_of_interest = Array.from(interest_filter.classList).pop(0)
            selected_filters.push(class_of_interest)
        }
    // Return values of selected interests
    return selected_filters;
}


/**
* Filters the displayed user cards based on selected interests and 
* Username. User fields must match both criteria in order to be 
* shown.
*/
function filterInterests() {
    const users = document.getElementsByClassName('available-card')
    const search_bar = document.getElementById('searchByNameField')
    
    // params
    const search_query = search_bar.value.toLowerCase()
    const selected_filters = getInterestFilters();

    for(const user of users) {

        const username = user.getElementsByClassName('card-name')[0].innerHTML.toLowerCase();

        const does_username_match = username.includes(search_query);
        // i.e. User interests are a subset of selected interests
        const do_interests_match = Array.from(selected_filters).every(filter => Array.from(user.classList).includes(filter));
        if(!does_username_match || !do_interests_match) {
            user.style.display = 'none';
        } else {
            user.style.display = 'block';
        }
    }
}

/**
 * Filters the displayed user cards based on selected companies and 
* Username. User fields must match both criteria in order to be 
* shown. Only available for mentees viewing mentors.
 */
function filterInterestsWithCompany() {
    const users = document.getElementsByClassName('available-card')
    const search_bar = document.getElementById('searchByNameField')
    const search_by_company = document.getElementById('searchByCompanyField')
    
    // params
    const search_query = search_bar.value.toLowerCase()
    const selected_filters = getInterestFilters();
    const search_company_query = search_by_company.value.toLowerCase()

    for(const user of users) {

        const username = user.getElementsByClassName('card-name')[0].innerHTML.toLowerCase();
        const company = user.getElementsByClassName('card-organization')[0].innerHTML.toLowerCase();

        const does_username_match = username.includes(search_query);
        const does_company_match = company.includes(search_company_query)
        // i.e. User interests are a subset of selected interests
        const do_interests_match = Array.from(selected_filters).every(filter => Array.from(user.classList).includes(filter));
        if(!does_username_match || !does_company_match || !do_interests_match) {
            user.style.display = 'none';
        } else {
            user.style.display = 'block';
        }
    }
}


// -------------------- <<< MAKE CARDS CLICKABLE >>> -------------------- \\

// Loading sometimes takes a lot of time so this code waits to execute until page load
document.addEventListener('DOMContentLoaded', () => {
    // Get all user cards
    const cards = document.getElementsByClassName('card')
    // Assuming users exist...
    if(cards)
        for (card of cards)
        {
            // Fun Fact: Cards are forms!
            // So we make them clickable, where clicking submits the form -> loads their profile
            const profile_form = card.getElementsByTagName('form')[0]
            card.getElementsByClassName('profile-view-zone')[0].addEventListener('click', () => profile_form.submit())
        }
})




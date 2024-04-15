/*********************************************************************/
/* FILE NAME: admin_dashboard.js                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp & Jason S                                  */
/* (OFFICIAL) DATE CREATED: April 15, 2024                           */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the JavaScript necessary to use functional     */
/*      aspects of the Administrator Dashboard                       */
/* This file is included in 'admin_dashboard.html'                    */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

// Super basic string matching on report user's name to show/hide their cards
//  Added in filtering by user type (ie. mentor, mentee, or all)
// Created By Jason
function filterUsers() {
    const searchByNameField = document.getElementById('searchByNameField');
    const reportedUserCards = document.querySelectorAll('.card');

    //params
    const searchString = searchByNameField.value.toLowerCase();
    const userType = document.getElementById('selectUserType').value.toLowerCase();

    // Return early and unhide all cards if there is nothing to search for.
    if (searchString === '' && userType === 'all') {
        const hiddenCards = document.querySelectorAll('.hidden');
        hiddenCards.forEach(card => card.classList.remove('hidden'));
        return;
    }

    // For each reported user elemet on the page...
    reportedUserCards.forEach(card => {
        // Get the value of the h2, which should be first.
        // It should contain the name of the card user.
        const cardName = card.children[0].innerText.toLowerCase();
        const cardUserType = card.getElementsByClassName('reported-user-role')[0].innerHTML.toLowerCase();

        const doesUserTypeMatch = userType === 'all' || cardUserType.includes(userType);
        const doesNameMatch = cardName.includes(searchString);

        if (!doesUserTypeMatch || !doesNameMatch) {
            card.classList.add('hidden');
        } else {
            card.classList.remove('hidden');
        }
    });
}

// -------------------- -------------------------------- -------------------- \\
// -------------------- <<< REPORT RESOLUTION MODALS >>> -------------------- \\
// -------------------- -------------------------------- -------------------- \\

document.addEventListener('DOMContentLoaded', function() {

    // List of all "Resolve" buttons - Each has its own modal for resolving the report
    const resolveButtons = document.querySelectorAll('.resolve-report');
    // List of all Modals on the page - One for each "Resolve" option
    const modals = document.querySelectorAll('.resolve-report-modal');

    // Add event listeners to each "Resolve" button
    // Show the related modal when the button is clicked
    resolveButtons.forEach((button, index) => {
        button.addEventListener("click", function() {
            // Assuming there's a direct mapping between the index of the resolve button and the modal
            const modal = modals[index];
            if (modal) {
                modal.showModal();
                // Assuming there's an element with id 'modal-exit' in each modal for closing it
                modal.querySelector('#modal-exit').addEventListener('click', () => modal.close());
            }
        });
    });

    // -------------------- -------------------------------- -------------------- \\
    // -------------------- <<< REPORT RESOLUTION MODALS >>> -------------------- \\
    // -------------------- -------------------------------- -------------------- \\    

    const showAllCheckbox = document.getElementById('showAllCheckbox')
    const unresolvedReports = document.getElementById('unresolvedReports');
    const allReports = document.getElementById('allReports');

    // A Checkbox exists in the header of this page
    // This checkbox allows 2 filtering options:
    //  - People w/ pending reports
    //  - All reports, pending AND resolved
    showAllCheckbox.addEventListener('change', function() {
      if (this.checked) {
        unresolvedReports.style.display = 'none';
        allReports.style.display = '';  
      } else {
        unresolvedReports.style.display = '';
        allReports.style.display = 'none';
      }
    });
});
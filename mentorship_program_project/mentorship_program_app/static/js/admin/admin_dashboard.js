/*********************************************************************/
/* FILE NAME: admin_dashboard.js                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew Pyscher, Logan Zipp & Others                   */
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

// under development has been purged
// WOOOOOOOOOOOOOO! *pops champagne*
// its deleted from existence ^-^
// no more
// never to been seen again
// now its just development - yeeeeeaaaaaaaaahhhhh baby
// Shits developed, finally B)
document.addEventListener('DOMContentLoaded', () => {
    const userManagementBtn = document.getElementById('user-management');
    const viewReportedUsersBtn = document.getElementById('view-reported-users');
    const buttonDiv = document.getElementById('mentorApplications');
    const editInterestsBtn = document.getElementById('btn-edit-interests');
    const interests_modal = document.getElementById('interests-modal')
    const load_overlay = document.getElementById('loading-overlay')
    const processFile = document.getElementById('btn-process-file')
    
    // Various reroutes to different pages on button clicks
    userManagementBtn.addEventListener('click', () => window.location.href = '/admin_user_management');
    processFile.addEventListener('click', () => window.location.href = '/process_file');
    viewReportedUsersBtn.addEventListener('click', () => window.location.href = '/admin_reported_users');
    buttonDiv.addEventListener('click', () => window.location.href = '/view_pending');

    // -------------------- <<< EDIT INTERESTS MODAL >>> -------------------- \\

    // Open modal w/ appropriate button
    editInterestsBtn.addEventListener('click', () => interests_modal.showModal());

    // Locate exit_modal button
    const modal_exit = document.getElementById('modal-exit') 
    // Make exit_modal refresh page to eradicate changes
    modal_exit.addEventListener('click', () => {
        interests_modal.close()
        window.location.href = '/dashboard'
    })

    // Override default 'Escape' behavior to ensure page refresh
    modal_exit.addEventListener('keydown', (e) => {
        if(e.key === 'Escape') {
            e.preventDefault()
            interests_modal.close()
            window.location.href = '/dashboard'
        }
    })

    // -------------------- <<< REPORT GENERATION >>> -------------------- \\
    
    // Elements pertaining to report generation
    var generateButton = document.getElementById("generate-reports-button");
    var generateForm = document.getElementById("generate-reports-form");

    // Fixes a bug where the loading overlay appears when report is downloaded.
    // It was unnecessary and would never go away :(
    generateButton.addEventListener("click", () => {
        if(load_overlay)
            load_overlay.remove()

        generateForm.submit()
    });


    // -------------------- <<< VERIFY MENTEE UNDERGRAD STATUS >>> -------------------- \\

    var validateMenteeUGStatusButton = document.getElementById("verify-mentee-ug-status-button");
    var validateMenteeUGStatusForm = document.getElementById("verify-mentee-ug-status-form");

    validateMenteeUGStatusButton.addEventListener("click", () => validateMenteeUGStatusForm.submit());
});
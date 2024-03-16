/*********************************************************************/
/* FILE NAME: nav_logic.js                                           */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Tanner Koth                                           */
/* DATE CREATED: March 15, 2024                                      */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the javascript necessary to control different  */
/* navigation elements within the applications navigation bar.       */
/*********************************************************************/
/* COMMAND LINE PARAMETER LIST (In Parameter Order):                 */
/* (NONE)                                                            */
/*********************************************************************/
/* ENVIRONMENTAL RETURNS:                                            */
/* (NOTHING)                                                         */
/*********************************************************************/
/* GLOBAL VARIABLE LIST (Alphabetically):                            */
/* (none)                                                            */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/* -created (03/15/2024) by Tanner Koth                              */
/*********************************************************************/

// This routine is responsible for controlling the sidebar element of the sites
// primary navigation. It contains logic checking if the sidebar is displayed,
// and updates it's style.display property to either 'flex' or 'none'. It also
// contains an eventListener that checks if the users mouse leaves the sidebar,
// and updates the style property accordingly.
function sidebarController() {
    // Obtains DOM element sidebar (ul element)
    const sidebar = document.querySelector('.sidebar');
    // Obtain sidebar styles
    const sidebarComputedStyle = window.getComputedStyle(sidebar);

    // Display sidebar if not displayed, else hide sidebar
    if (sidebarComputedStyle.display === 'none') {
        sidebar.style.display = 'flex'
    }
    else {
        sidebar.style.display = 'none'
    }

    // EventListener listening for mouse to leave sidebar, then hide sidebar.
    sidebar.addEventListener('mouseleave', () => {
        sidebar.style.display = 'none';
    });
}

// This routine is invoked to display the mobile sidebar. It is invoked when the
// user-profile icon is clicked on the mobile navigation bar.
function openMobileSidebar() {
    const sidebar = document.querySelector('.mobile-sidebar');
    sidebar.style.display = 'flex';
}

// This routine is invoked to hide the mobile sidebar. It is invoked when the
// close icon is clicked on the mobile navigation sidebar.
function closeMobileSidebar() {
    const sidebar = document.querySelector('.mobile-sidebar');
    sidebar.style.display = 'none';
}

// This routine checks the screen width, checking if it exceeds 800px. If true
// close the mobile navigation sidebar.
function checkScreenWidth() {
    // Check if the screen width is 800px or more
    if (window.matchMedia("(min-width: 800px)").matches) {
        closeMobileSidebar();
    };
}

// Event listener for window resize. Invokes checkScreenWidth to close the
// mobile navigation sidebar if the screen width is too large.
window.addEventListener('resize', checkScreenWidth);
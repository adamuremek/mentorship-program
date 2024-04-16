/*********************************************************************/
/* FILE NAME: index.js                                             */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp                                            */
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
/*      aspects of the base index template. Used in every page       */
/* This file is included in 'index.html'                    */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

// Show current year on bottom of the page
document.addEventListener('DOMContentLoaded', ()=>{
    const currentYear = new Date().getFullYear();
    document.getElementById('current-year').textContent = currentYear;
});


// -------------------- ----------------------- -------------------- \\
// -------------------- <<< LOADING OVERLAY >>> -------------------- \\
// -------------------- ----------------------- -------------------- \\

const load_overlay = document.getElementById('loading-overlay')

// Assuming overlay exists...
if(load_overlay)
{
    // Show overlay when navigating away from current page
    window.onbeforeunload = () => {
        load_overlay.style.display = 'block'
        return undefined
    };

    // Remove overlay when a new page is being shown
    window.onload = () => {
        load_overlay.style.display = 'none'
        return undefined
    }

    // If a page data was cached, ensure overlay is removed when reloaded
    window.addEventListener('pageshow', () => {
        load_overlay.style.display = 'none'
        return undefined
    });

    
}
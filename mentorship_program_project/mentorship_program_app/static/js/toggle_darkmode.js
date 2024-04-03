/*********************************************************************/
/* FILE NAME: toggle_darkmode.js                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Ben Swaffer                                           */
/* DATE CREATED: March 15, 2024                                      */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the javascript to toggle light mode on or off  */
/*********************************************************************/
/* COMMAND LINE PARAMETER LIST (In Parameter Order):                 */
/* (NONE)                                                            */
/*********************************************************************/
/* ENVIRONMENTAL RETURNS:                                            */
/* (NOTHING)                                                         */
/*********************************************************************/
/* SAMPLE INVOCATION:                                                */
/*                                                                   */
/* This is ran whenever a user toggles on or off light mode settings */
/*********************************************************************/
/* GLOBAL VARIABLE LIST (Alphabetically):                            */
/* (input_email): HTMLElement of email input field                   */
/* (theme): class set on body of html if lightmode is turned on      */
/* (togglebox): hidden checkbox associated with lightmode span       */
/*********************************************************************/
/* COMPILATION NOTES:                                                */
/*                                                                   */
/* This project compiles normally under Visual Studio Code 2022.     */
/* No special compile options or optimizations were used.            */
/* 0 unresolved warnings & 0 errors exist under these conditions     */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/

//get access to checkbox
const togglebox = document.getElementById('toggler');

//check localstorage for a theme
if(localStorage.getItem('theme')) 
{
    const theme = localStorage.getItem('theme');

    if (theme)
        document.body.classList.add(theme);

    //when checkbox is changed, update values
    togglebox.addEventListener('change', (event)=>{
        if (event.currentTarget.checked) {
            localStorage.setItem('theme','light-mode');
            document.body.classList.add('light-mode');
        } else {
            localStorage.removeItem('theme');
            document.body.classList.remove('light-mode');
        }
    });
}
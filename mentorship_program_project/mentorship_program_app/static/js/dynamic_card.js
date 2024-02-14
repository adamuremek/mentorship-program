/*********************************************************************/
/* FILE NAME: dynamic-card.js                                        */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp                                            */
/* DATE CREATED: February 14, 2024                                   */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project is responsible for connecting SVSU CSIS students to  */
/* experienced mentors in the industry.                              */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the javascript to make one page *look* like    */
/* several individual pages.                                         */
/*********************************************************************/
/* COMMAND LINE PARAMETER LIST (In Parameter Order):                 */
/* (NONE)                                                            */
/*********************************************************************/
/* ENVIRONMENTAL RETURNS:                                            */
/* (NOTHING)                                                         */
/*********************************************************************/
/* SAMPLE INVOCATION:                                                */
/*                                                                   */
/* This program is launched from (1) the Windows Start Menu, (2)     */
/* clicking on the PROJECT.EXE program icon or (3) entering the path */
/* and PROJECT.EXE name in the Run box on the Windows Start Menu.    */
/*********************************************************************/
/* GLOBAL VARIABLE LIST (Alphabetically):                            */
/*                                                                   */
/*********************************************************************/
/* COMPILATION NOTES:                                                */
/*                                                                   */
/* This project compiles normally under Visual Studio Code 2022.     */
/* No special compile options or optimizations were used.            */
/* 0 unresolved warnings & 0 errors exist under these conditions     */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/

// Get all snippets being rendered
const snippets = document.getElementsByClassName('sign-in-card-content')
    
// Hide all code snippets by default
for (i of snippets) 
    i.style = 'display: none;'

// Display first snippet
let curID = 0
snippets[0].style = 'display: flex'

// Get progression buttons
const buttons = document.getElementsByClassName('sign-in-card-option-button')

// Assign event listener to each button
for(button of buttons) 
{
    button.addEventListener('click', e => {
        snippets[curID].style = 'display: none;'

        // When button is clicked, progress displayed card
        curID += 1
        if(curID >= snippets.length)
            curID = 0
        snippets[curID].style = 'display: flex;'
        console.log(`Current ID: ${curID}`)
    })
}
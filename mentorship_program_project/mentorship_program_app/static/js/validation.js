/*********************************************************************/
/* FILE NAME: Validation.js                                          */
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
/* This file contains the javascript to autocomplete/validate forms  */
/*  in the service's registration process.                           */
/* This file is used for both mentee AND mentor field validation     */
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
/* (input_email): HTMLElement of email input field                   */
/* (input_phone): HTMLElement of phone input field                   */
/* (regex_email): Regex used for validating email input              */
/* (regex_phone): Regex used for validating phone input              */
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


const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // Validates <{string}@{string}.{string}>
const regex_phone = /^\(\d{3}\) \d{3}-\d{4}$/;

const input_email = document.getElementById('email')
const input_phone = document.getElementById("phone");

input_email.addEventListener('input', e => {
    const regex_result = regex_email.test(e.target.value)

    // Visually indicate Regex Success
    if(regex_result)
        input_email.style.backgroundColor = 'green'
    else
        input_email.style.backgroundColor = 'red'
}) 


// -------------------- <<< COMPLETED REGEX PATTERNS >>> -------------------- \\


let previousValue = input_phone.value.replace(/\D/g, "")

input_phone.addEventListener("input", e => {
    let inputValue = e.target.value.replace(/\D/g, ""); // Remove non-numeric characters
    console.log(`inputValue: ${inputValue}`)
    console.log(`previous: ${previousValue}`)
    // Account for backspaces on non-numeric characters
    if(inputValue === previousValue){
        console.log('fuck you')
        inputValue = inputValue.slice(0, -1)
    }

    // User backspaces with one number. Remove '('
    if (inputValue.length == 0) {
        inputValue = ''
    // Format as '( XXX )'
    } else if(inputValue.length <= 3) {
        inputValue = '(' + inputValue + ')'; // Start with (
    // Format as '( XXX ) XXX'
    } else if (inputValue.length <= 6) {
        inputValue = '(' + inputValue.substring(0, 3) + ') ' + inputValue.substring(3);
    // Format as '( XXX ) XXX-XXXX'
    } else {
        inputValue = '(' + inputValue.substring(0, 3) + ') ' + inputValue.substring(3, 6) + '-' + inputValue.substring(6, 10); // Format as (XXX) XXX-XXXX
    }
    
    // Record value for next iteration
    previousValue = inputValue.replace(/\D/g, "")
    // Set input to new value
    e.target.value = inputValue;

    const regex_result = regex_phone.test(e.target.value)
    // Visually indicate Regex Success
    if(regex_result)
        input_phone.style.backgroundColor = 'green'
    else
        input_phone.style.backgroundColor = 'red'
});

// Ensure keyboard inputs are only numbers or backspace
input_phone.addEventListener("keypress", e => {
    const keyCode = e.keyCode || e.which;
    const keyValue = String.fromCharCode(keyCode);
    if (!/\d/.test(keyValue)) { // Allow only numeric input
        e.preventDefault();
    }
});
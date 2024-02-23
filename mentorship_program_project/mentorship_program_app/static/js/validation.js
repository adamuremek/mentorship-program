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
document.addEventListener('DOMContentLoaded', winloaded => {


console.log('why are you not working :(')
const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // Validates <{string}@{string}.{string}>
const regex_svsu = /^[^\s@]+@svsu[.]edu$/ // Validates <{string}@{svsu}.{edu}>
const regex_phone = /^\(\d{3}\) \d{3}-\d{4}$/;

// const is_student = document.getElementById('register-form-mentee')


const input_email = document.getElementById('email');
const input_phone = document.getElementById('phone');
const input_first_name  = document.getElementById('fname');
const input_last_name  = document.getElementById('lname');

var regex_custom = /^/

const RED = 'firebrick'
const GREEN = 'forestgreen'

console.log(`Student: ${is_student}`)

input_email.addEventListener("input", e => {
    if(is_student)
        regex_custom = regex_svsu
    else
        regex_custom = regex_email

    const regex_result = regex_custom.test(e.target.value)

    // Visually indicate Regex Success
    if(regex_result)
        input_email.style.backgroundColor = GREEN
    else
        input_email.style.backgroundColor = RED
}) 

input_first_name.addEventListener("input", e => {
    let inputValue = e.target.value.replace(/\d/g, ""); // Remove numeric characters
    // Set input to new value
    e.target.value = inputValue;
})

input_last_name.addEventListener("input", e => {
    let inputValue = e.target.value.replace(/\d/g, ""); // Remove numeric characters
    // Set input to new value
    e.target.value = inputValue;
})


// -------------------- <<< COMPLETED REGEX PATTERNS >>> -------------------- \\


// let previousValue = input_phone.value.replace(/\D/g, "")
let previousValue

input_phone.addEventListener("input", e => {
    let inputValue = e.target.value.replace(/\D/g, ""); // Remove non-numeric characters
    console.log(`inputValue: ${inputValue}`)
    console.log(`previous: ${previousValue}`)
    // Account for backspaces on non-numeric characters
    if(inputValue === previousValue)
        inputValue = inputValue.slice(0, -1)


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
        input_phone.style.backgroundColor = GREEN
    else
        input_phone.style.backgroundColor = RED
});

// Ensure keyboard inputs are only numbers or backspace
input_phone.addEventListener("keypress", e => {
    const keyCode = e.keyCode || e.which;
    const keyValue = String.fromCharCode(keyCode);
    if (!/\d/.test(keyValue)) { // Allow only numeric input
        e.preventDefault();
    }
});

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

    const page_count = buttons.length

    // Get Header Corner Element list
    const corner_guy = document.getElementsByClassName('sign_in_top_left_element')[0]
    console.log('corner guy')
    console.log(corner_guy)

    corner_guy.innerText = `<- Step ${(curID+1)} of ${page_count}`

    corner_guy.addEventListener('click', e => {
        snippets[curID].style = 'display: none;'
        
        curID -= 1

        if(curID == -1)
            window.location.href = "http://localhost:8000/landing";
        else {
            snippets[curID].style = 'display: flex;'

            corner_guy.innerText = `<- Step ${(curID+1)} of ${page_count}`
        }
        
    })

    // Assign event listener to each button
    for(button of buttons) 
    {
        button.addEventListener('click', e => {
            snippets[curID].style = 'display: none;'

            // When button is clicked, progress displayed card
            curID += 1

            // Submit at the end
            if(curID >= snippets.length) {
                form_submit()
            }
            else {
                 snippets[curID].style = 'display: flex;'

                corner_guy.innerText = `<- Step ${(curID+1)} of ${page_count}`

                console.log(`Current ID: ${curID}`)
            }
        })
    }



// -------------------- <<< FORM SUBMIT >>> -------------------- \\

// function form_submit() {
//     const good_form = regex_custom.test(input_email.value) && regex_phone.test(input_phone.value)

//     if(good_form)
//         console.log('this form is good!')
//     else
//         console.log('this form sux you fucking idiot')
// }


}) // DOM listener

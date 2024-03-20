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

    const regex_email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // Validates <{string}@{string}.{string}>
    const regex_svsu = /^[^\s@]+@svsu[.]edu$/ // Validates <{string}@{svsu}.{edu}>
    const regex_phone = /^\(\d{3}\) \d{3}-\d{4}$/;

    // const is_student = document.getElementById('register-form-mentee')

    const input_first_name = document.getElementById('fname');
    const input_last_name = document.getElementById('lname');

    const input_email = document.getElementById('email');
    const input_phone = document.getElementById('phone');
    const input_password = document.getElementById('password')

    const input_company = document.getElementById('organization')
    // const input_company_type = document.getElementById('company-type')
    // const input_experience = document.getElementById('experience')
    const input_job_title = document.getElementById('jobTitle')

    const input_interests = document.getElementById('interests')

    const btn_user_agree = document.getElementById('btnUserAgree')

    let warning_message = document.getElementById('must-accept-agreement-error')

    var regex_custom = /^/

    // ID of current 'page'
    let cur_id = 0

    const RED = 'firebrick'
    const GREEN = 'forestgreen'

    console.log(`Student: ${is_student}`)

    // PREVENT SENDING FORM ON 'ENTER
    // Reassign to simply go to next page
    document.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            buttons[cur_id].click()
        }
    });


    input_email.addEventListener("input", e => {
        if (is_student)
            regex_custom = regex_svsu
        else
            regex_custom = regex_email

        const regex_result = regex_custom.test(e.target.value)

        // Visually indicate Regex Success
        if (regex_result)
            input_email.style.backgroundColor = GREEN
        else
            input_email.style.backgroundColor = RED
    })

    input_first_name.addEventListener("input", e => {
        const input_value = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = input_value;
    })

    input_last_name.addEventListener("input", e => {
        const inputValue = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = inputValue;
    })


    // -------------------- <<< COMPLETED REGEX PATTERNS >>> -------------------- \\

    // Record value for deletions on special characters
    let previous_value

    input_phone.addEventListener("input", e => {
        let input_value = e.target.value.replace(/\D/g, ""); // Remove non-numeric characters
        console.log(`inputValue: ${input_value}`)
        console.log(`previous: ${previous_value}`)
        // Account for backspaces on non-numeric characters
        if (input_value === previous_value)
            input_value = input_value.slice(0, -1)


        // User backspaces with one number. Remove '('
        if (input_value.length == 0) {
            input_value = ''
            // Format as '( XXX )'
        } else if (input_value.length <= 3) {
            input_value = '(' + input_value + ')'; // Start with (
            // Format as '( XXX ) XXX'
        } else if (input_value.length <= 6) {
            input_value = '(' + input_value.substring(0, 3) + ') ' + input_value.substring(3);
            // Format as '( XXX ) XXX-XXXX'
        } else {
            input_value = '(' + input_value.substring(0, 3) + ') ' + input_value.substring(3, 6) + '-' + input_value.substring(6, 10); // Format as (XXX) XXX-XXXX
        }

        // Record value for next iteration
        previous_value = input_value.replace(/\D/g, "")
        // Set input to new value
        e.target.value = input_value;

        const regex_result = regex_phone.test(e.target.value)
        // Visually indicate Regex Success
        if (regex_result)
            input_phone.style.backgroundColor = GREEN
        else
            input_phone.style.backgroundColor = RED
    });

    // Ensure keyboard inputs are only numbers or backspace
    input_phone.addEventListener("keypress", e => {
        const key_code = e.keyCode || e.which;
        const key_value = String.fromCharCode(key_code);
        if (!/\d/.test(key_value)) { // Allow only numeric input
            e.preventDefault();
        }
    });

    

    // Get all snippets being rendered
    const snippets = document.getElementsByClassName('sign-in-card-content')

    // Hide all code snippets by default
    for (i of snippets)
        i.style = 'display: none;'

    // Display first snippet
    snippets[0].style = 'display: flex'
    snippets[cur_id].getElementsByTagName('input')[0].focus()

    // Get progression buttons
    const buttons = document.getElementsByClassName('sign-in-card-option-button')

    const page_count = buttons.length

    // Get Header Corner Element list
    const corner_guy = document.getElementsByClassName('sign_in_top_left_element')[0]
    corner_guy.onclick = null

    corner_guy.innerText = `<- Step ${(cur_id + 1)} of ${page_count}`

    corner_guy.addEventListener('click', e => {
        snippets[cur_id].style = 'display: none;'

        cur_id -= 1
        console.log('corner guy')
        console.log(cur_id)

        if (cur_id === -1)
            window.location.href = "/role_selection";
        else {
            snippets[cur_id].style = 'display: flex;'
            snippets[cur_id].getElementsByTagName('input')[0].focus()

            corner_guy.innerText = `<- Step ${(cur_id + 1)} of ${page_count}`
        }

    })

    // Assign event listener to each button
    for (button of buttons) {
        button.addEventListener('click', e => {
            if (!is_page_valid(cur_id + 1))
                return
            snippets[cur_id].style = 'display: none;'

            // When button is clicked, progress displayed card
            cur_id += 1
            console.log('corner guy')
            console.log(cur_id)

            // Submit at the end
            if (cur_id >= snippets.length) {
                // Do nothing?
                // form_submit()
            }
            else {
                snippets[cur_id].style = 'display: flex;'
                snippets[cur_id].getElementsByTagName('input')[0].focus()
                console.log(snippets[cur_id].getElementsByTagName('input'))

                corner_guy.innerText = `<- Step ${(cur_id + 1)} of ${page_count}`

                console.log(`Current ID: ${cur_id}`)
            }
        })
    }

    btn_user_agree.style.visibility = 'Hidden'
    document.getElementById('useragreement').addEventListener('change', e => {
        if (e.target.checked) 
            btn_user_agree.style.visibility = 'Visible'
        else 
            btn_user_agree.style.visibility = 'Hidden'
    })

    // -------------------- <<< FORM SUBMIT >>> -------------------- \\

    /**
     * @param {int} form_idx Index of current page of registration form
     * @returns Status of form component ( true=completed )
     */
    function is_page_valid(form_idx) {
        // Use form validation for ? mentee | mentor
        const form_function = is_student ? is_mentee_page_valid : is_mentor_page_valid
        console.log(`Form_Index: ${form_idx}`)
        let is_valid = true

        switch (form_idx) {
            case 1: // Name and Pronouns
                is_valid = input_first_name.value.length > 0 &&
                    input_last_name.value.length > 0
                                
                is_valid = input_first_name.value.length > 1 &&
                    input_last_name.value.length > 1
                if(!is_valid)
                    display_error_message_for_name()
                break

            case 2: // Email | Phone | Password
                is_valid = regex_custom.test(input_email.value) &&
                    regex_phone.test(input_phone.value) &&
                    input_password.value.length > 1
                if(!is_valid)
                    display_error_message_for_email_phone_password()
                break

            default:
                is_valid = form_function(form_idx)
        }

        return is_valid
    }


    function is_mentee_page_valid(form_idx) {
        // If flag becomes false, a form component failed validation
        let is_valid = true
        switch (form_idx) {
    
            case 3: // Interests
                is_valid = true
                break

            case 4: // User Agreement
                const chk_agree = document.getElementById('useragreement')
                is_valid = chk_agree.checked
                if (is_valid)
                    document.getElementById('register-form-mentee').submit()
                else 
                {
                    warning_message.innerText = "You must accept the user agreement\
                    in order to register."
                } 
                break
        }

        return is_valid
    }

    function is_mentor_page_valid(form_idx) {
        // If flag becomes false, a form component failed validation
        let is_valid = true
        switch (form_idx) {
           
            case 3: // company information
                is_valid = input_company.value.length > 0 &&
                    input_job_title.value.length > 0
                //input_company-type.value != none ??
                //input_expeience.value != none    ??
                if(!is_valid)
                    display_error_message_for_mentor()
                break

            case 4: // Interests
                is_valid = true
                break

            case 5: // User Agreement
                const chk_agree = document.getElementById('useragreement')
                is_valid = chk_agree.checked
                if (is_valid)
                    document.getElementById('register-form-mentor').submit()
                else
                {
                    warning_message.innerText = "You must accept the user agreement\
                    in order to register."
                } 
                break
        }

        return is_valid
    }

    function display_error_message_for_name(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data
        let first_name_warning_message = document.getElementById('frm-first-name-warning-message')
        let last_name_warning_message = document.getElementById('frm-last-name-warning-message')

        if(input_first_name.value.length == 0)
            first_name_warning_message.innerText = "First name cannot be blank!"
        else if(input_first_name.value.length == 1)
            first_name_warning_message.innerText = "First name must be longer than one character."
        else
            first_name_warning_message.innerText = ""
        
        if(input_last_name.value.length == 0)
            last_name_warning_message.innerText = "Last name cannot be blank!"
        else if(input_last_name.value.length == 1)
            last_name_warning_message.innerText = "Last name must be longer than one character."
        else
            last_name_warning_message.innerText = ""
    }

    function display_error_message_for_email_phone_password(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data
        let email_warning_message = document.getElementById('frm-email-warning-message')
        let phone_warning_message = document.getElementById('frm-phone-warning-message')
        let password_warning_message = document.getElementById('frm-password-warning-message')
        
        if(input_password.value.length == 0)
            password_warning_message.innerText = "Password cannot be blank!"
        else if(input_password.value.length == 1)
            password_warning_message.innerText = "Password must be longer than one character."
        else
            password_warning_message.innerText = ""
        
        if(input_phone.value.length == 0)
            phone_warning_message.innerText = "Phone number cannot be blank!"
        else if(!regex_phone.test(input_phone.value))
            phone_warning_message.innerText = "You must enter a valid phone number."
        else
            phone_warning_message.innerText = ""

        if(input_email.value.length == 0)
            email_warning_message.innerText = "Email cannot be blank!"
        else if(!regex_custom.test(input_email.value))
            email_warning_message.innerText = "You must enter a valid email address."
        else
            email_warning_message.innerText = ""
    }

    function display_error_message_for_mentor(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data
        let company_warning_message = document.getElementById('frm-company-warning-message')
        //let company_type_warning_message = document.getElementById('frm-company-type-warning-message')
        //let experience_warning_message = document.getElementById('frm-experience-warning-message')
        let job_title_warning_message = document.getElementById('frm-job-title-warning-message')

        if(input_company.value.length == 0)
            company_warning_message.innerText = "Company cannot be blank!"
        else if(input_company.value.length == 1)
        company_warning_message.innerText = "Company name must be longer than one character."
        else
            company_warning_message.innerText = ""

        if(input_job_title.value.length == 0)
            job_title_warning_message.innerText = "Job Title cannot be blank!"
        else if(input_job_title.value.length == 1)
            job_title_warning_message.innerText = "Job Title must be longer than one character."
        else
            job_title_warning_message.innerText = ""
        
    }

}) // DOM listener
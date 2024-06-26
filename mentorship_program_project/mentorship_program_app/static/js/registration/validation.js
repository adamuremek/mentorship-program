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
    //const new_regex_email = /^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$/ 
    const regex_email_name = /[!#$%^&*()+\[\]{}|\\;:'",<>\/?=~`]/;
    const regex_svsu = /^[^\s@]+@svsu[.]edu$/ // Validates <{string}@{svsu}.{edu}>
    const regex_phone = /^\(\d{3}\) \d{3}-\d{4}$/;
    const regex_name = /^[a-zA-Z]+([ \-']{0,1}[a-zA-Z]+){0,2}[.]{0,1}$/ 
    //Validates name including hyphens, apostrophies, and suffix (with period)

    // const is_student = document.getElementById('register-form-mentee')

    const input_first_name = document.getElementById('fname');
    const input_last_name = document.getElementById('lname');

    const input_email = document.getElementById('email');
    const input_phone = document.getElementById('phone');
    const input_password = document.getElementById('password')
    const input_confirm_password = document.getElementById('confirm-password')

    const input_companyDropD = document.getElementById('select-company-name')
    const input_companyTextF = document.getElementById('organization')
    // const input_company_type = document.getElementById('company-type')
    // const input_experience = document.getElementById('experience')
    const input_job_title = document.getElementById('jobTitle')

    const input_interests = document.getElementById('interests')

    const btn_user_agree = document.getElementById('btnUserAgree')

    const agreement_warning_message = document.getElementById('must-accept-agreement-error')
    const first_name_warning_message = document.getElementById('frm-first-name-warning-message')
    const last_name_warning_message = document.getElementById('frm-last-name-warning-message')
    const email_warning_message = document.getElementById('frm-email-warning-message')
    const phone_warning_message = document.getElementById('frm-phone-warning-message')
    const password_warning_message = document.getElementById('frm-password-warning-message')
    const company_warning_message = document.getElementById('frm-company-warning-message')
    const job_title_warning_message = document.getElementById('frm-job-title-warning-message')

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
        const regex_email_name_result = regex_email_name.test(e.target.value)

        // Visually indicate Regex Success
        if (regex_result && !regex_email_name_result)
            input_email.style.backgroundColor = GREEN
        else
            input_email.style.backgroundColor = RED
    })

    input_first_name.addEventListener("input", e => {
        const input_value = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = input_value;
        const regex_result = regex_name.test(e.target.value)

        // Visually indicate Regex Success
        if(regex_result)
            input_first_name.style.backgroundColor = GREEN
        else
            input_first_name.style.backgroundColor = RED
    })

    input_last_name.addEventListener("input", e => {
        const inputValue = e.target.value.replace(/\d/g, ""); // Remove numeric characters
        // Set input to new value
        e.target.value = inputValue;
        const regex_result = regex_name.test(e.target.value)

        // Visually indicate Regex Success
        if(regex_result)
            input_last_name.style.backgroundColor = GREEN
        else
            input_last_name.style.backgroundColor = RED
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

    function is_all_white_space(string){
        // Returns true if the string contains only white spaces.
        const ALL_WHITE_SPACE = /^\s*$/
        return ALL_WHITE_SPACE.test(string);
    }

    // -------------------- --------------------------------------- -------------------- \\
    // -------------------- <<< VISUAL CARD PROGRESSION SECTION >>> -------------------- \\
    // -------------------- --------------------------------------- -------------------- \\
    
    // Get all snippets being rendered
    const snippets = document.getElementsByClassName('sign-in-card-content')

    // Get progression buttons
    const buttons = document.getElementsByClassName('sign-in-card-option-button')
    const page_count = buttons.length

    // Get Header Corner Element list
    const corner_guy = document.getElementsByClassName('sign_in_top_left_element')[0]
    corner_guy.onclick = null

    // Hide all code snippets by default
    for (i of snippets)
        i.style = 'display: none;'

    // Display first snippet
    display_snippets_at_idx(cur_id)

    corner_guy.addEventListener('click', e => {
        snippets[cur_id].style = 'display: none;'

        cur_id -= 1

        if (cur_id === -1)
            window.location.href = "/role_selection";
        else 
            display_snippets_at_idx(cur_id)

    })

    // Assign event listener to each button
    for (button of buttons) {
        button.addEventListener('click', async e => {
            
            let valid = await is_page_valid(cur_id + 1)
     
            if (!valid )
                return
            snippets[cur_id].style = 'display: none;'

            // When button is clicked, progress displayed card
            cur_id += 1

            // Submit at the end
            if (cur_id >= snippets.length) {
                // Do nothing?
                // form_submit()
            }
            else 
                display_snippets_at_idx(cur_id)
        })
    }

    btn_user_agree.style.visibility = 'Hidden'
    document.getElementById('useragreement').addEventListener('change', e => {
        if (e.target.checked) 
            btn_user_agree.style.visibility = 'Visible'
        else 
            btn_user_agree.style.visibility = 'Hidden'
    })

    // -------------------- ------------------- -------------------- \\
    // -------------------- <<< FORM SUBMIT >>> -------------------- \\
    // -------------------- ------------------- -------------------- \\


    /**
     * @param {int} form_idx Index of current page of registration form
     * @returns Status of form component ( true=completed )
     */
    async function  is_page_valid(form_idx) {
        // Use form validation for ? mentee | mentor
        const form_function = is_student ? is_mentee_page_valid : is_mentor_page_valid
        let is_valid = true

        switch (form_idx) {
            case 1: // Name and Pronouns
                is_valid = input_first_name.value.length > 0 &&
                    input_last_name.value.length > 0 && regex_name.test(input_first_name.value)
                    && regex_name.test(input_last_name.value)
                
                                
                if(!is_valid)
                    display_error_message_for_name()
                else
                    reset_error_messages(form_idx)
                break
                

            case 2: // Email | Phone | Password
                is_valid = regex_custom.test(input_email.value) &&
                    regex_phone.test(input_phone.value) &&
                    ! await email_already_exist(input_email.value) &&
                    is_password_valid()
                 
                if(!is_valid)
                    display_error_message_for_email_phone_password()
                else
                    reset_error_messages(form_idx)
                break

            default:
                is_valid = form_function(form_idx)
        }
 

        return is_valid
    }


    function is_password_valid(){
       
            // Requirement 1: Password should contain 12 or more characters
            if (input_password.value.length < 12)
              return false;
          
            // Requirement 2: Password should contain 36 or less characters
            if (input_password.value.length > 36)
              return false;
          
            // Requirement 3: Password should contain a combination of uppercase letters, lowercase letters, at least one number, and at least one symbol
            const uppercaseRegex = /[A-Z]/;
            const lowercaseRegex = /[a-z]/;
            const numberRegex = /[0-9]/;
            const symbolRegex = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/;
            const emojiRegex = /([\u{1F600}-\u{1F64F}|\u{1F300}-\u{1F5FF}|\u{1F680}-\u{1F6FF}|\u{1F700}-\u{1F77F}|\u{1F780}-\u{1F7FF}|\u{1F800}-\u{1F8FF}|\u{1F900}-\u{1F9FF}|\u{1FA00}-\u{1FA6F}|\u{1FA70}-\u{1FAFF}|\u{2600}-\u{26FF}|\u{2700}-\u{27BF}|\u{231A}-\u{231B}|\u{23E9}-\u{23EC}|\u{23F0}|\u{23F3}|\u{25FD}-\u{25FE}|\u{2614}-\u{2615}|\u{2648}-\u{2653}|\u{267F}|\u{2693}|\u{26A1}|\u{26AA}-\u{26AB}|\u{26BD}-\u{26BE}|\u{26C4}-\u{26C5}|\u{26CE}|\u{26D4}|\u{26EA}-\u{26EB}|\u{26F2}-\u{26F3}|\u{26F5}|\u{26FA}|\u{26FD}|\u{2705}|\u{270A}-\u{270B}|\u{2728}|\u{274C}|\u{274E}|\u{2753}-\u{2755}|\u{2757}|\u{2795}-\u{2797}|\u{27B0}|\u{27BF}|\u{2934}-\u{2935}|\u{2B05}-\u{2B07}|\u{2B1B}-\u{2B1C}|\u{2B50}|\u{2B55}|\u{3030}|\u{303D}|\u{3297}|\u{3299}|\u{FE0F}|\u{200D}|\u{20E3}|\u{E0020}-\u{E007F}]+|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]|\uD83D[\uDE80-\uDEFF])/gu;
            if (
              !uppercaseRegex.test(input_password.value) ||
              !lowercaseRegex.test(input_password.value) ||
              !numberRegex.test(input_password.value) ||
              !symbolRegex.test(input_password.value) ||
              emojiRegex.test(input_password.value)
            ) {
              return false;
            }

            // Ensure passwords match
            if(input_password.value != input_confirm_password.value)
                return false;
          
            return true;
    }

     async function email_already_exist(email){
        try {
            
            const response = await fetch('/check-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                    
                },
                body: JSON.stringify({ email })
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();
            
            return data.exists; // Assuming the response contains a boolean indicating if the email exists
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            return false; // Return false in case of error
        }
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
                    agreement_warning_message.innerText = "You must accept the user agreement\
                    in order to register."
                } 
                break
        }

        return is_valid
    }

    function is_mentor_page_valid(form_idx) {
        // If flag becomes false, a form component failed validation
        let is_valid = true

        //  Take the current selections/entered input for the user's information..... 
        //  the user's interests, and their response to the user agreement
        var selected_orgName = input_companyDropD.options[input_companyDropD.selectedIndex].text
        var selected_OtherText = "Other"
        var selected_OtherOrgName = (input_companyTextF.value).trim()

        switch (form_idx) {
            case 3:     //  Company information
                if(selected_orgName == selected_OtherText)
                {
                    //  Take info from textfield for the organization name
                    //  if "Other" was selected from the dropdown
                    //  (Check if selection is valid).
                    is_valid = selected_OtherOrgName != selected_OtherText &&
                        selected_OtherOrgName.length > 0 &&
                        input_job_title.value.length > 0 &&
                        !is_all_white_space(selected_OtherOrgName)
                }
                else
                {
                    //  Otherwise, take the text from what was selected
                    //  from the dropdown
                    //  (Check if selection is valid).
                    is_valid = selected_orgName.length > 0 &&
                        input_job_title.value.length > 0
                }
                //input_companyDropD-type.value != none ??
                //input_expeience.value != none    ??
                if(is_valid)
                    reset_error_messages(form_idx)
                else
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
                    agreement_warning_message.innerText = "You must accept the user agreement\
                    in order to register."
                } 
                break
        }

        return is_valid
    }

    // This is not good but at least removes some redundancy :)
    function display_snippets_at_idx(id) {
        snippets[id].style = 'display: flex;'
        snippets[id].getElementsByTagName('input')[0].focus()

        corner_guy.innerText = `<- Step ${(id + 1)} of ${page_count}`
    }

    function display_error_message_for_name(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data

        if(input_first_name.value.length == 0)
            first_name_warning_message.innerText = "First name cannot be blank!"
        else if(!regex_name.test(input_first_name.value))
            first_name_warning_message.innerText = "Invalid first name."
        else
            first_name_warning_message.innerText = ""
        
        if(input_last_name.value.length == 0)
            last_name_warning_message.innerText = "Last name cannot be blank!"
        else if(!regex_name.test(input_last_name.value))
            last_name_warning_message.innerText = "Invalid last name."
        else
            last_name_warning_message.innerText = ""
    }

    async function display_error_message_for_email_phone_password(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data
        const emojiRegex = /([\u{1F600}-\u{1F64F}|\u{1F300}-\u{1F5FF}|\u{1F680}-\u{1F6FF}|\u{1F700}-\u{1F77F}|\u{1F780}-\u{1F7FF}|\u{1F800}-\u{1F8FF}|\u{1F900}-\u{1F9FF}|\u{1FA00}-\u{1FA6F}|\u{1FA70}-\u{1FAFF}|\u{2600}-\u{26FF}|\u{2700}-\u{27BF}|\u{231A}-\u{231B}|\u{23E9}-\u{23EC}|\u{23F0}|\u{23F3}|\u{25FD}-\u{25FE}|\u{2614}-\u{2615}|\u{2648}-\u{2653}|\u{267F}|\u{2693}|\u{26A1}|\u{26AA}-\u{26AB}|\u{26BD}-\u{26BE}|\u{26C4}-\u{26C5}|\u{26CE}|\u{26D4}|\u{26EA}-\u{26EB}|\u{26F2}-\u{26F3}|\u{26F5}|\u{26FA}|\u{26FD}|\u{2705}|\u{270A}-\u{270B}|\u{2728}|\u{274C}|\u{274E}|\u{2753}-\u{2755}|\u{2757}|\u{2795}-\u{2797}|\u{27B0}|\u{27BF}|\u{2934}-\u{2935}|\u{2B05}-\u{2B07}|\u{2B1B}-\u{2B1C}|\u{2B50}|\u{2B55}|\u{3030}|\u{303D}|\u{3297}|\u{3299}|\u{FE0F}|\u{200D}|\u{20E3}|\u{E0020}-\u{E007F}]+|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]|\uD83D[\uDE80-\uDEFF])/gu;

        if (input_password.value.length == 0) {
            password_warning_message.innerText = "Password cannot be blank!";
        } else if (input_password.value.length < 12) {
            password_warning_message.innerText = "Password must be 12 or more characters.";
        } else if (input_password.value.length > 36) {
            password_warning_message.innerText = "Password must be 36 or fewer characters.";
        } else if (!/[A-Z]/.test(input_password.value) || !/[a-z]/.test(input_password.value) || !/[0-9]/.test(input_password.value) || !/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(input_password.value) || emojiRegex.test(input_password.value)) {
            password_warning_message.innerText = "Password must contain at least one uppercase letter, one lowercase letter, one number, and one symbol.";
        } else if(input_password.value != input_confirm_password.value) {
            password_warning_message.innerText = "Passwords must match"
        } else {
            password_warning_message.innerText = "";
        }
        
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
        else if(await email_already_exist(input_email.value))
            email_warning_message.innerText = "Account with this email already exist"
        else
            email_warning_message.innerText = ""
    }

    function display_error_message_for_mentor(){
        //Descriptive errors will be displayed to the user depending on what is wrong with their data
        var selected_orgName = input_companyDropD.options[input_companyDropD.selectedIndex].text
        var selected_OtherText = "Other"
        var selected_OtherOrgName = input_companyTextF.value
        

        //  If 'Other' has been selected from the dropdown...
        if(selected_orgName == selected_OtherText)
        {
            //  If nothing has been typed for the organization's name...
            if(selected_OtherOrgName.length == 0)
                company_warning_message.innerText = "Company cannot be blank!"
            //  If only 1 character has been typed for the organization's name...
            else if(selected_OtherOrgName.length == 1)
                company_warning_message.innerText = "Company name must be longer than one character."
            //  (Users cannot enter in 'Other' for their company name!)
            else if(selected_OtherOrgName == selected_OtherText)
                company_warning_message.innerText = "Company name is invalid. Please enter in another name."
            else if(is_all_white_space(selected_OtherOrgName))
                company_warning_message.innerText = "Company name is all white space. Please enter another name."
            //  If nothing has been typed for the organization's name...
            else
                company_warning_message.innerText = ""
        }
        //  If anything else has been selected from the dropdown...
        else
        {
            //  If an empty space has been selected.....
            if(selected_orgName.length == 0)
                company_warning_message.innerText = "Company cannot be blank!"
            //  If a company name has been selected.....
            else
                company_warning_message.innerText = ""
        }
            
        //  If nothing has been typed for the the job title.....
        if(input_job_title.value.length == 0)
            job_title_warning_message.innerText = "Job Title cannot be blank!"
        //  If only 1 character has been typed for the the job title.....
        else if(input_job_title.value.length == 1)
            job_title_warning_message.innerText = "Job Title must be longer than one character."
        //  Otherwise, if a valid string of characters has been typed for the the job title.....
        else
            job_title_warning_message.innerText = ""
    }

    function reset_error_messages(form_idx){
        //Resets the innerText values of the error messages based on the form index 
        //(so that if you go back, the error messages do not continue to show)
        switch (form_idx){
            case 1:
                first_name_warning_message.innerText = ""
                last_name_warning_message.innerText = ""
                break;
            case 2:
                password_warning_message.innerText = ""
                phone_warning_message.innerText = ""
                email_warning_message.innerText = ""
                break;
            case 3:
                company_warning_message.innerText = ""
                job_title_warning_message.innerText = ""
                break;
            default:
                break;
        }
    }

}) // DOM listener
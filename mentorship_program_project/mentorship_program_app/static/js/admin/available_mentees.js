/*********************************************************************/
/* FILE NAME: available_mentees.js                                   */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Logan Zipp & Andrew Pyscher (???)                     */
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
/*      aspects of the Available Mentees page                        */
/* This file is included in 'available_mentees.html'                 */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/


// -------------------- -------------------------- -------------------- \\
// -------------------- <<< GENERAL PAGE LOGIC >>> -------------------- \\
// -------------------- -------------------------- -------------------- \\

// I can't comment this rn i just dont get what is even happening in here

const added = document.getElementById('check-all-added')
const removed = document.getElementById('check-all-removed')
const cancel_button = document.getElementById('cancel_button')
const save_button = document.getElementById('save_button')
const added_checks = document.getElementById('added_bar_container').getElementsByTagName('input')
const removed_checks = document.getElementById('removed_bar_container').getElementsByTagName('input')

added.addEventListener('change', (e) => {
    if(e.target.checked) 
        for(chk of added_checks)
            chk.checked = true
    
    else
        for(chk of added_checks)
            chk.checked = false
    
})
removed.addEventListener('change', (e) => {
    if(e.target.checked) 
        for(chk of document.getElementById('removed_bar_container').getElementsByTagName('input'))
            chk.checked = true
    else
        for(chk of removed_checks)
            chk.checked = false
})

cancel_button.addEventListener('click', e =>{
    window.location.href = "/available_mentees"
})

save_button.addEventListener('click', async function(e){
    let added_string = ""
    for(let i=0; i<added_checks.length; i++){
        if(added_checks[i].checked)
            added_string += "," + added_checks[i].id
    }
    added_string += ";"
    for(let i=0; i<removed_checks.length; i++){
        if(removed_checks[i].checked)
            added_string += "," + removed_checks[i].id
    }
    const response = await update_mentee_list(added_string)
    if (!response.ok) 
            throw new Error('Network response was shit')
    if(response.redirected)
        window.location.href = response.url

})  
    

async function update_mentee_list(list_of_mentees) {
    console.log(list_of_mentees);
    const req = new Request("add_remove_mentees_from_file", {
        method: "POST", 
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        // Convert your data into a JSON string
        body: JSON.stringify({list_of_mentees: list_of_mentees})
    });

    let response = await fetch(req);
    return response;
}

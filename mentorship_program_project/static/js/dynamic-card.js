/* These event listeners show/hide the Interests popup when it is clicked on */
const snippets = document.getElementsByClassName('sign-in-card-content')
    
for (i of snippets) 
{
    i.style = 'display: none;'
}

let curID = 0

snippets[0].style = 'display: flex'

const TEMPORARY_LENGTH = snippets.length

const buttons = document.getElementsByClassName('sign-in-card-button-option')

for(button of buttons) 
{
    button.addEventListener('click', e => {
        snippets[curID].style = 'display: none;'

        curID += 1
        if(curID >= TEMPORARY_LENGTH)
            curID = 0
        snippets[curID].style = 'display: flex;'
        console.log(`Current ID: ${curID}`)
    })
}
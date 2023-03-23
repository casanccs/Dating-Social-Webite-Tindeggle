const choices = document.querySelectorAll('.choice')
const checkboxes = document.querySelectorAll('.choice .checkbox')
const chosen = document.querySelector('.chosen')
const choicesDiv = document.querySelector('.choices')
for (let i = 0; i < choices.length; i++) {
    choices[i].addEventListener("click", function(e) {
        let checkbox = e.target.parentNode.getElementsByTagName('input')[0];
        checkbox.click();
    })
}

for (let i = 0; i < checkboxes.length; i++){
    checkboxes[i].addEventListener('click', function(e) {
        if (choices[i].parentNode == choicesDiv){
            choicesDiv.removeChild(choices[i]);
            chosen.appendChild(choices[i]);
        }
        else{
            chosen.removeChild(choices[i]);
            choicesDiv.appendChild(choices[i]);
        }
    })
}


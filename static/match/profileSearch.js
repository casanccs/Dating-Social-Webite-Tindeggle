let likes = document.querySelectorAll('.like');
let unlikes = document.querySelectorAll('.unlike');
let likeDivs = document.querySelectorAll('.likeDiv');
let unlikeDivs = document.querySelectorAll('.unlikeDiv');
let undoLikes = document.querySelectorAll('.undoLike');
let undoNotLikes = document.querySelectorAll('.undoNotLike');
let usernames = document.querySelectorAll('.username');
console.log(likes);

for (let i = 0; i < likes.length; i++){
    //When the person clicks on the "like" button
    likes[i].addEventListener('click', (e) =>{

        likeDivs[i].setAttribute('hidden','true');
        unlikeDivs[i].setAttribute('hidden','true');
        undoLikes[i].removeAttribute('hidden');

        const formData = new FormData();
        let username = usernames[i].textContent; //to know which profile we are trying to like
        formData.append('username', username);
        formData.append('relationship', 'like'); //tells us we "like"ed "username"'s profile
        formData.append('csrfmiddlewaretoken', csrf_token); //csrf_token is from base.html script
        console.log(formData);
        fetch(profileSearchUrl, { //profileSearchUrl is from base.html script
            method: 'POST',
            body: formData
        })
        
        .then(response => console.log(response))
        .then(data => {
            console.log('Success: ', data)

        })
        .catch(error => {
            console.error('Error: ', error);
        });
    })
}

for (let i = 0; i < likes.length; i++){
    unlikes[i].addEventListener('click', (e) =>{
        likeDivs[i].setAttribute('hidden','true');
        unlikeDivs[i].setAttribute('hidden','true');
        undoNotLikes[i].removeAttribute('hidden');
        
        const formData = new FormData();
        let username = usernames[i].textContent; //to know which profile we are trying to like
        formData.append('username', username);
        formData.append('relationship', 'unlike'); //tells us we "like"ed "username"'s profile
        formData.append('csrfmiddlewaretoken', csrf_token); //csrf_token is from base.html script
        console.log(formData);
        fetch(profileSearchUrl, { //profileSearchUrl is from base.html script
            method: 'POST',
            body: formData
        })
        
        .then(response => console.log(response))
        .then(data => {
            console.log('Success: ', data)

        })
        .catch(error => {
            console.error('Error: ', error);
        });
    })
}

for (let i = 0; i < likes.length; i++){
    likeDivs[i].addEventListener('click', (e) =>{
        e.target.parentNode.getElementsByTagName('input')[0].click();
        e.target.getElementsByTagName('input')[0].click();
    })
}

for (let i = 0; i < likes.length; i++){
    unlikeDivs[i].addEventListener('click', (e) =>{
        e.target.parentNode.getElementsByTagName('input')[0].click();
        e.target.getElementsByTagName('input')[0].click();
    })
}

for (let i = 0; i < likes.length; i++){
    undoLikes[i].addEventListener('click', (e) =>{
        undoLikes[i].setAttribute('hidden', '');
        likeDivs[i].removeAttribute('hidden');
        unlikeDivs[i].removeAttribute('hidden');
        likes[i].checked = false;


        const formData = new FormData();
        let username = usernames[i].textContent; //to know which profile we are trying to like
        formData.append('username', username);
        formData.append('relationship', 'delete'); //tells us we "like"ed "username"'s profile
        formData.append('csrfmiddlewaretoken', csrf_token); //csrf_token is from base.html script
        console.log(formData);
        fetch(profileSearchUrl, { //profileSearchUrl is from base.html script
            method: 'POST',
            body: formData
        })
        
        .then(response => console.log(response))
        .then(data => {
            console.log('Success: ', data)

        })
        .catch(error => {
            console.error('Error: ', error);
        });

    })
}

for (let i = 0; i < likes.length; i++){
    undoNotLikes[i].addEventListener('click', (e) =>{
        undoNotLikes[i].setAttribute('hidden', '');
        likeDivs[i].removeAttribute('hidden');
        unlikeDivs[i].removeAttribute('hidden');
        unlikes[i].checked = false;

        const formData = new FormData();
        let username = usernames[i].textContent; //to know which profile we are trying to like
        formData.append('username', username);
        formData.append('relationship', 'delete'); //tells us we "like"ed "username"'s profile
        formData.append('csrfmiddlewaretoken', csrf_token); //csrf_token is from base.html script
        console.log(formData);
        fetch(profileSearchUrl, { //profileSearchUrl is from base.html script
            method: 'POST',
            body: formData
        })
        
        .then(response => console.log(response))
        .then(data => {
            console.log('Success: ', data)

        })
        .catch(error => {
            console.error('Error: ', error);
        });
    })
}
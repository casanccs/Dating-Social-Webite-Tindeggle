const loginHeader = document.querySelector('.loginHeader');
const loginBox = document.querySelector('.loginBox');
const form = document.querySelector('.form');
const bottom = document.querySelector('#bottom');

function boxEnter(e) {
    loginHeader.style.fontSize = "45px";
    loginHeader.style.marginTop = "50px";
    loginHeader.style.marginBottom = "35px";
    loginBox.style.width = "800px";
    loginBox.style.cursor = 'pointer';
    loginBox.style.backgroundColor = 'rgba(255, 255, 255, 0.25)';
}

function boxLeave(e) {
    loginHeader.style.fontSize = "40px";
    loginHeader.style.marginTop = "40px";
    loginHeader.style.marginBottom = "25px";
    loginBox.style.width = "700px";
    loginBox.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
}

loginBox.addEventListener('pointerenter', boxEnter)

loginBox.addEventListener('pointerleave', boxLeave)

loginBox.addEventListener('click', function boxClick(e) {
    loginBox.removeEventListener('pointerenter', boxEnter);
    loginBox.removeEventListener('pointerleave', boxLeave);
    loginBox.style.cursor = 'context-menu';
    loginBox.style.backgroundColor = 'rgba(50, 50, 50, 0.5)';
    loginBox.style.width = "800px";
    form.toggleAttribute('hidden');
    loginHeader.toggleAttribute('hidden');
    bottom.toggleAttribute('hidden');
    bottom.style.display = 'inline-block';
    loginBox.removeEventListener('click', boxClick);
})
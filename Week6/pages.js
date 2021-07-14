
function ShowPage(page) { 
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none';
    });

    document.querySelector(`#${page}`).style.display = 'block';

}

document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            ShowPage(this.dataset.page);
        }
    })

})
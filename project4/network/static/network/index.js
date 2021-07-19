document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit_post').forEach(element => {
        element.style.display = "none";
    });

    document.querySelectorAll('.editbutton').forEach(button => {
        button.addEventListener('click', () => {
            const id = parseInt(button.id.substring(11)); // should probably use regex instead of hardcoding
            
            document.querySelector(`#post_${id}`).style.display = "none";
            document.querySelector(`#edit_${id}`).style.display = "inherit";
            button.style.display = "none";

            const csrftoken = getCookie('csrftoken');

            document.querySelector(`#saveedit_${id}`).onclick = function() {

                const request = new Request(
                    `post/edit/${id}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );

                fetch(request, {
                    method: "POST",
                    mode: "same-origin",
                    body: JSON.stringify({
                        "text": document.querySelector(`#posttext_${id}`).value
                    })
                })
                .then(response=> response.json())
                .then(post => {
                    document.querySelector(`#edit_${id}`).style.display = "none";
                    document.querySelector(`#post_${id}`).style.display = "inherit";
                    button.style.display = "inherit";

                    console.log(post["postUpdate"]);
                    const updatedpost = document.querySelector(`#postbody_${id}`)
                    updatedpost.innerHTML = post["postUpdate"];

                    
                });

            }
 
        })
        })
    

    document.querySelectorAll('.likebutton').forEach(button => {
        button.addEventListener('click', function() {
            console.log("like button clicked")
            if (button.innerHTML === 'Like') {
                button.innerHTML = 'Liked';
            } else {
                button.innerHTML = 'Like';
            }
        })
    
        
    });

});

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
}

    


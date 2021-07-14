document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit_post').forEach(element => {
        element.style.display = "none";
    });

    document.querySelectorAll('.editbutton').forEach(button => {
        button.addEventListener('click', () => {
            id = parseInt(button.id.substring(11)); // should probably use regex instead of hardcoding
           
            document.querySelector(`#post_${id}`).style.display = "none";
            document.querySelector(`#edit_${id}`).style.display = "inherit";
            button.style.display = "none";

            document.querySelector(`#form_${id}`).onsubmit = function() {
                fetch("{% url 'edit' id %}", {
                    method: "POST"
                })
                .then(response => response.json())
                .then(post => {
                    const updatedpost = document.querySelector(`#post_${id}`)
                    updatedpost.innerHTML = post.postUpdate;

                    updatedpost.style.display = "inherit";
                    document.querySelector(`#edit_${id}`).style.display = "none";
                    button.style.display = "inherit";
                })
                }
            
        })

        })
    });

    document.querySelectorAll('.likebutton').forEach(button => {
        button.addEventListener('click', function() {
            if (button.innerHTML === 'Like') {
                button.innerHTML = 'Liked';
            } else {
                button.innerHTML = 'Like';
            }
        })
    });


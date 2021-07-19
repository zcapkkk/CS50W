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

            document.querySelector(`#saveedit_${id}`).onclick = function() {

                fetch(`post/edit/${id}`, {
                    method: "POST",
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


    


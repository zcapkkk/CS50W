document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.editbutton').forEach(button => {
        this.onclick = editPage;

    }

    );
})

function editPage() {
    alert(`clicked on button`);
}
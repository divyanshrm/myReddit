
const deleteButtons = document.querySelectorAll('.delete-comment');

deleteButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        const confirmation = confirm("Are you sure you want to delete this comment?");
        
        if (!confirmation) {
            event.preventDefault();
        }
    });
});

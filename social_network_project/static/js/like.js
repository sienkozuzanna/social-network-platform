document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            const isLiked = this.getAttribute('data-liked') === 'true';

            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                    } else {
                        this.setAttribute('data-liked', data.is_liked);
                        this.innerHTML = data.is_liked ? '❤️ Unlike' : '🤍 Like';
                        this.nextElementSibling.textContent = `${data.likes_count} likes`;
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
});

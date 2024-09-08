const addComment = async (id) => {
    try {
        const content = document.getElementById('content').value
        const res = await fetch('/api/comments/', {
            method: 'POST',
            body: JSON.stringify({
                content: content,
                id: id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await res.json();
        document.getElementById('amount').innerText = `${data.count}`
        const element = data.data
        const comment = document.createElement('div')
        comment.className = 'card my-3';
        comment.innerHTML = `
                    <div class="card-header d-flex align-items-center">
                            <img
                                src="${element.user.avatar}"
                                class="rounded-circle me-2"
                                alt="${element.user.username}"
                                width="50"
                                height="50" />
						<div>
							<h6 class="mb-0">
								${element.user.full_name}
							</h6>
							<small class="text-muted"
								>${moment(element.date_created).startOf('hour').fromNow()}</small
							>
						</div>
					</div>

					<div class="card-body">
						<p class="card-text">${element.content}</p>
					</div>

					<div class="card-footer text-end">
						<button class="btn btn-sm btn-outline-primary">
							Reply
						</button>
						<button class="btn btn-sm btn-outline-secondary">
							Like
						</button>
					</div>
        `

        const container = document.getElementById('comments');
        container.prepend(comment)
    } catch (error) {
        console.error('Error adding comment:', error);
    }
}
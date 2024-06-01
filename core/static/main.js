"use strict";

document.addEventListener("DOMContentLoaded", (e) => {
  const msg = document.getElementById("messages");

  if (msg.innerText !== "") {
    setTimeout(() => {
      msg.remove();
    }, 2000);
  }
});

function submitComment(e, blogId) {
  e.preventDefault();
  let commentText = document.getElementById("commentText").value;
  const allComments = document.querySelector(".blog-comments-target");
  const listComments = document.querySelector(".all-comments");

  if (!commentText) return;

  const formData = new FormData();

  formData.append("comment", commentText);
  formData.append("id", blogId);

  fetch(`/comment/${blogId}`, {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      listComments.classList.add("show");

      allComments.innerHTML = `
     <a href="url_for('users.profile',username=cmt.user.username)">
              <img
                src="/static/profiles/${data.comment.user.image}"
                class="border rounded-circle me-2"
                alt="Avatar"
                style="height: 40px"
              />
            </a>
            <div>
              <div class="bg-body-tertiary rounded-3 px-3 py-1">
                <a
                  href="{{ url_for('users.profile',username=cmt.user.username) }}"
                  class="text-dark mb-0"
                >
                  <strong>${data.comment.user.username}</strong>
                </a>

                <span class="comment-text py-1 text-muted d-block"
                  >${data.comment.comment}</span
                >
              </div>
              <a href="" class="text-muted small ms-3 me-2"
                ><strong>Like</strong></a
              >
              <a href="" class="text-muted small me-2"
                ><strong>Reply</strong></a
              >
            </div>
      `;
    })
    .catch((error) => error);
}

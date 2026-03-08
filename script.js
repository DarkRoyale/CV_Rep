const systemInfo = navigator.userAgent;
console.log("Інформація про систему:", systemInfo);
localStorage.setItem("system_info", systemInfo);

const footer = document.getElementById("footer");
const savedInfo = localStorage.getItem("system_info");
footer.innerHTML += "<br><strong>Система:</strong>" + savedInfo;

const variantNumber = 10;
const apiUrl = `https://jsonplaceholder.typicode.com/posts/${variantNumber}/comments`;
const commentsContainer = document.getElementById("comments-container");

async function fetchComments() {
  try {
    commentsContainer.innerHTML = "<p>Loading comments...</p>";

    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const comments = await response.json();

    commentsContainer.innerHTML = "";

    comments.forEach((comment) => {
      const commentDiv = document.createElement("div");
      commentDiv.classList.add("comment-card");
      commentDiv.innerHTML = `
                <p><strong>Name:</strong> ${comment.name}</p>
                <p><strong>Email:</strong> <a href="mailto:${comment.email}">${comment.email}</a></p>
                <p><strong>Feedback:</strong> ${comment.body}</p>
                <hr>
            `;
      commentsContainer.appendChild(commentDiv);
    });
  } catch (error) {
    console.error("Comments getting error", error);
    commentsContainer.innerHTML = `<p style="color: red;">Try Laterp>`;
  }
}
fetchComments();

function createAndShowModal() {
  const modal = document.createElement("div");
  modal.id = "contact-modal";
  modal.classList.add("modal");

  modal.innerHTML = `
        <div class="modal-content">
            <span class="close-button" id="close-modal">&times;</span>
            <h2>Feedback</h2>
            <form action="https://formspree.io/f/xvzbnyka" method="POST">
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone:</label>
                    <input type="tel" id="phone" name="phone">
                </div>
                <div class="form-group">
                    <label for="message">Message:</label>
                    <textarea id="message" name="message" rows="4" required></textarea>
                </div>
                <button type="submit" class="submit-btn">Submit</button>
            </form>
        </div>
    `;
  document.body.appendChild(modal);

  const closeBtn = document.getElementById("close-modal");

  modal.style.display = "block";

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
}

setTimeout(createAndShowModal, 10);

const themeToggleBtn = document.getElementById("theme-toggle");
const body = document.body;
function setInitialTheme() {
  const currentHour = new Date().getHours();
  if (currentHour >= 7 && currentHour < 21) {
    body.classList.remove("dark-mode");
    themeToggleBtn.innerText = "Dark Mode";
  } else {
    body.classList.add("dark-mode");
    themeToggleBtn.innerText = "Light Mode";
  }
}

setInitialTheme();

themeToggleBtn.addEventListener("click", () => {
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    themeToggleBtn.innerText = "Light Mode";
  } else {
    themeToggleBtn.innerText = "Dark Mode";
  }
});

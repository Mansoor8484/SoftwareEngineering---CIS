// logout.js
function openPopup() {
  const modal = document.getElementById("logoutModal");
  modal.style.display = "block";
}

function closePopup() {
  const modal = document.getElementById("logoutModal");
  modal.style.display = "none";
}

function logout() {
  // Clear user session or token from localStorage
  localStorage.removeItem("token");
  localStorage.removeItem("user_id");

  // Redirect to the login page
  window.location.href = "/api/auth/login";
}

// Close the modal if clicked outside the content
window.onclick = function(event) {
  const modal = document.getElementById("logoutModal");
  if (event.target === modal) {
    closePopup();
  }
};

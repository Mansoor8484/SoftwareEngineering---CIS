
function openPopup() {
    document.getElementById("popup").style.display = "block";
  }

  function logout() {
    // Remove stored user session/token
    localStorage.removeItem('user_id');
    localStorage.removeItem('token');
    window.location.href = '/api/auth/login'; // Redirect to login page
  }

  // Attach logout functionality to the logout button
  document.getElementById('logout-button').addEventListener('click', logout);

  // Close the popup without any action
  function cancelLogout() {
    document.getElementById("popup").style.display = "none";
  }
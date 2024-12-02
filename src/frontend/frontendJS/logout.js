
function openPopup() {
    document.getElementById("popup").style.display = "block";
  }
  
  // Redirect to login page
  function logout() {
    window.location.href = "login.html"; // Change to your login page URL
  }
  
  // Close the popup without any action
  function cancelLogout() {
    document.getElementById("popup").style.display = "none";
  }
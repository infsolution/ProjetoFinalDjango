 //Modal Reaction
var modalR = document.getElementById('modalR');
var btnR = document.getElementById("btnR");
var spanR = document.getElementsByClassName("close")[0];
btnR.onclick = function() {
  modalR.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanR.onclick = function() {
  modalR.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalR) {
    modalR.style.display = "none";
  }
}
var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

//Comentarios
function show_comment(element){
	if(document.getElementById(element).style.display == "none"){
		document.getElementById(element).style.display = "block";
	}else{
		document.getElementById(element).style.display = "none";	
	}
	
}



function post_comment(comment, event)
{
	if(event.keyCode == 13){
		document.getElementById(comment).submit();
	}
}

function show_react(element){
	if(document.getElementById(element).style.display == "none"){
		document.getElementById(element).style.display = "block";
	}else{
		document.getElementById(element).style.display = "none";	
	}
	
}

function to_react(reaction){
	document.getElementById(reaction).submit();
}
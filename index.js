// var modal = document.getElementById("boxModal");
        
// var btn = document.getElementById("popbtn");

// var span = document.getElementsByClassName("close")[0];

// btn.onclick = function() {
//   modal.style.display = "block";
// }

// span.onclick = function() {
//   modal.style.display = "none";
// }

// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }



var modal = document.getElementsByClassName('boxModal');

var btn = document.getElementsByClassName("popbtn");

var span = document.getElementsByClassName("close");


btn[0].onclick = function() {
    modal[0].style.display = "block";
}

btn[1].onclick = function() {
    modal[1].style.display = "block";
}

btn[2].onclick = function() {
  modal[2].style.display = "block";
}

span[0].onclick = function() {
    modal[0].style.display = "none";
}

span[1].onclick = function() {
    modal[1].style.display = "none";
}

span[2].onclick = function() {
  modal[2].style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal[0]) {
         modal[0].style.display = "none";
     }
    if (event.target == modal[1]) {
         modal[1].style.display = "none";
     } 
     if (event.target == modal[2]) {
      modal[2].style.display = "none";
  }  
}

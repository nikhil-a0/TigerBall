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

for (let i = 0; i < btn.length; i++) {
    btn[i].onclick = function() {
        modal[i].style.display = "block";
    }
}

for (let i = 0; i < span.length; i++) {
    span[i].onclick = function() {
        modal[i].style.display = "none";
    }
}


window.onclick = function(event) {
    for (let i = 0; i < modal.length; i++) {
        if (event.target == modal[i]) {
            modal[i].style.display = "none";
        }
    }
}

// window.onscroll = function() {myFunction()};

// var header = document.getElementById('myheader');
// var sticky = header.offsetTop;

// function myFunction() {
//   if (window.pageYOffset > sticky) {
//     header.classList.add("sticky");
//   } else {
//     header.classList.remove("sticky");
//   }
// }


$(window).scroll(function () {
    console.log($(window).scrollTop())
    if ($(window).scrollTop() > 63) {
      $('#myheader').addClass('navbar-fixed');
    }
    if ($(window).scrollTop() < 64) {
      $('#myheader').removeClass('navbar-fixed');
    }
  });

// ----------------------- Scroll to top button ----------------------- //
let topbutton = document.getElementById("goToTopBtn");

window.onscroll = function () { scrollPage(); };

function scrollPage() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    topbutton.style.display = "block";
  } else {
    topbutton.style.display = "none";
  }
}

function goToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

$(document).ready(function () {
  var url = window.location.pathname;
  $('nav a[href="' + url + '"]').addClass('active');
});

// ----------------------- Menu hover ----------------------- //
$(document).ready(function () {
  $('.nav-item.dropdown').hover(function () {
    $(this).find('.dropdown-menu').addClass('show');
  }, function () {
    $(this).find('.dropdown-menu').removeClass('show');
  });

  $('.dropdown-menu').hover(function () {
    $(this).addClass('show');
  }, function () {
    $(this).removeClass('show');
  });
});

// ------------- Bootstrap tooltips activeren --------------- //
document.addEventListener('DOMContentLoaded', function () {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );

  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

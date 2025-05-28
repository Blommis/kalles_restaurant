/* jshint esversion: 6 */
/* global google, bootstrap */ // Declaring google and bootstrap as global since they are loaded via external scripts in the HTML
document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-images");
    const images = document.querySelectorAll(".carousel-image");
    const btnLeft = document.querySelector(".carousel-btn.left");
    const btnRight = document.querySelector(".carousel-btn.right");

    let currentIndex = 0;
    const totalImages = images.length;

    function updateCarousel() {
      const translateX = -currentIndex * 100;
      carousel.style.transform = `translateX(${translateX}%)`;
    }

    btnLeft.addEventListener("click", function () {
      currentIndex = (currentIndex - 1 + totalImages) % totalImages;
      updateCarousel();
    });

    btnRight.addEventListener("click", function () {
      currentIndex = (currentIndex + 1) % totalImages;
      updateCarousel();
    });
  });

  
async function initMap() {
      const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

      const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 8,
        center: { lat: 42.3601, lng: -71.0589 },
        mapId: "9c695404f34e7d4bb115f515"
      });

      const marker = new AdvancedMarkerElement({
        map: map,
        position: { lat: 42.4668, lng: -70.9495 },
        title: "Kalle's",
        });
      }

// to make sure Navbar collapses in mobile device
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".navbar-collapse .nav-link").forEach((link) => {
        link.addEventListener("click", function () {
            let navbarCollapse = document.querySelector(".navbar-collapse");

            // 'bootstrap' is a global object provided by the Bootstrap JS script
            let bsCollapse = new bootstrap.Collapse(navbarCollapse); 
            bsCollapse.hide(); 
        });
    });
});

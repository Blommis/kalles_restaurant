/* jshint esversion: 6 */
/* global google, bootstrap */

document.addEventListener("DOMContentLoaded", function () {
  //  CAROUSEL LOGIK
  const carousel = document.querySelector(".carousel-images");
  const images = document.querySelectorAll(".carousel-image");
  const btnLeft = document.querySelector(".carousel-btn.left");
  const btnRight = document.querySelector(".carousel-btn.right");

  if (carousel && images.length && btnLeft && btnRight) {
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
  }

  //  NAVBAR COLLAPSE
  const navLinks = document.querySelectorAll(".navbar-collapse .nav-link");
  if (navLinks.length) {
    navLinks.forEach((link) => {
      link.addEventListener("click", function () {
        let navbarCollapse = document.querySelector(".navbar-collapse");
        let bsCollapse = new bootstrap.Collapse(navbarCollapse);
        bsCollapse.hide();
      });
    });
  }
});


async function initMap() {
  const mapElement = document.getElementById("map");
  if (!mapElement) return;

  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  const map = new google.maps.Map(mapElement, {
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
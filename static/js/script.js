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

  // Initiera kartan när API-laddningen är klar
   function initMap() { 
    let options ={ 
        zoom:8, 
        center:{lat: 42.3601, lng:-71.0589}
     }

    let map = new google.maps.Map(document.getElementById('map'), options);

    const marker = new google.maps.AdvancedMarkerElement({
        position: { lat: 42.4668, lng: -70.9495 },
        map,
        title: "Restaurant"
    });
};
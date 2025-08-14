/**
* Template Name: AgriCulture
* Template URL: https://bootstrapmade.com/agriculture-bootstrap-website-template/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Scroll up sticky header to headers with .scroll-up-sticky class
   */
  let lastScrollTop = 0;
  window.addEventListener('scroll', function() {
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky')) return;

    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = `-${header.offsetHeight + 50}px`;
    } else if (scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = "0";
    } else {
      selectHeader.style.removeProperty('top');
      selectHeader.style.removeProperty('position');
    }
    lastScrollTop = scrollTop;
  });

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Auto generate the carousel indicators
   */
  document.querySelectorAll('.carousel-indicators').forEach((carouselIndicator) => {
    carouselIndicator.closest('.carousel').querySelectorAll('.carousel-item').forEach((carouselItem, index) => {
      if (index === 0) {
        carouselIndicator.innerHTML += `<li data-bs-target="#${carouselIndicator.closest('.carousel').id}" data-bs-slide-to="${index}" class="active"></li>`;
      } else {
        carouselIndicator.innerHTML += `<li data-bs-target="#${carouselIndicator.closest('.carousel').id}" data-bs-slide-to="${index}"></li>`;
      }
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

})();

document.addEventListener("DOMContentLoaded", function() {
  const openBtn = document.getElementById("open-form-btn");
  const closeBtn = document.getElementById("close-form-btn");
  const overlay = document.getElementById("form-overlay");

  openBtn.addEventListener("click", () => {
    overlay.style.display = "flex";
    document.body.style.overflow = "hidden"; // Bloquea scroll
  });

  closeBtn.addEventListener("click", () => {
    overlay.style.display = "none";
    document.body.style.overflow = ""; // Restaura scroll
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      overlay.style.display = "none";
      document.body.style.overflow = "";
    }
  });
});

/*
document.addEventListener("DOMContentLoaded", function() {
  const openUpdateBtns = document.querySelectorAll(".open-update-form-btn");
  const closeUpdateBtn = document.getElementById("close-update-form-btn");
  const updateOverlay = document.getElementById("update-form-overlay");

  openUpdateBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      updateOverlay.style.display = "flex";
      document.body.style.overflow = "hidden";
    });
  });

  closeUpdateBtn.addEventListener("click", () => {
    updateOverlay.style.display = "none";
    document.body.style.overflow = "";
  });

  updateOverlay.addEventListener("click", (e) => {
    if (e.target === updateOverlay) {
      updateOverlay.style.display = "none";
      document.body.style.overflow = "";
    }
  });
});
*/



// document.addEventListener("DOMContentLoaded", function() {
//   const updateOverlay = document.getElementById("update-form-overlay");
//   const updateContent = document.getElementById("update-form-content");
//   const closeUpdateBtn = document.getElementById("close-update-form-btn");

//   // Abrir modal y cargar el form
//   document.querySelectorAll(".open-update-form-btn").forEach(btn => {
//     btn.addEventListener("click", () => {
//       const url = btn.getAttribute("data-url");
//       fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
//         .then(res => res.text())
//         .then(html => {
//           updateContent.innerHTML = html;
//           updateOverlay.style.display = "flex";
//           document.body.style.overflow = "hidden";

//           // Cerrar con el botón "Cancel" dentro del form
//           const cancelBtn = document.getElementById("cancel-update-btn");
//           if (cancelBtn) {
//             cancelBtn.addEventListener("click", () => {
//               updateOverlay.style.display = "none";
//               document.body.style.overflow = "";
//             });
//           }
//         });
//     });
//   });

//   // Cerrar con la X del modal
//   closeUpdateBtn.addEventListener("click", () => {
//     updateOverlay.style.display = "none";
//     document.body.style.overflow = "";
//   });

//   // Cerrar haciendo click fuera del form
//   updateOverlay.addEventListener("click", e => {
//     if (e.target === updateOverlay) {
//       updateOverlay.style.display = "none";
//       document.body.style.overflow = "";
//     }
//   });
// });



document.addEventListener("DOMContentLoaded", function() {
  // ------- CREATE overlay (por si no lo tienes con null-checks) -------
  const openCreateBtn = document.getElementById("open-form-btn");
  const createOverlay = document.getElementById("form-overlay");
  const closeCreateBtn = document.getElementById("close-form-btn");

  if (openCreateBtn && createOverlay) {
    openCreateBtn.addEventListener("click", () => {
      createOverlay.style.display = "flex";
      document.body.style.overflow = "hidden";
    });
  }
  if (closeCreateBtn && createOverlay) {
    closeCreateBtn.addEventListener("click", () => {
      createOverlay.style.display = "none";
      document.body.style.overflow = "";
    });
    createOverlay.addEventListener("click", (e) => {
      if (e.target === createOverlay) {
        createOverlay.style.display = "none";
        document.body.style.overflow = "";
      }
    });
  }

  // ------- UPDATE overlay (AJAX) -------
  const updateOverlay = document.getElementById("update-form-overlay");
  const updateContent = document.getElementById("update-form-content");
  const closeUpdateBtn = document.getElementById("close-update-form-btn");

  // Abrir modal y cargar el form por AJAX
  document.querySelectorAll(".open-update-form-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-url");
      if (!updateOverlay || !updateContent || !url) return;

      fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(res => res.text())
        .then(html => {
          updateContent.innerHTML = html;
          updateOverlay.style.display = "flex";
          document.body.style.overflow = "hidden";

          // Cerrar con el botón "Cancel" dentro del formulario inyectado
          const cancelBtn = updateContent.querySelector("#cancel-update-btn");
          if (cancelBtn) {
            cancelBtn.addEventListener("click", () => {
              updateOverlay.style.display = "none";
              document.body.style.overflow = "";
            });
          }
        })
        .catch(err => {
          console.error("Error cargando el formulario de update:", err);
        });
    });
  });

  // Cerrar con la X del modal
  if (closeUpdateBtn && updateOverlay) {
    closeUpdateBtn.addEventListener("click", () => {
      updateOverlay.style.display = "none";
      document.body.style.overflow = "";
    });
  }

  // Cerrar haciendo click fuera del contenido
  if (updateOverlay) {
    updateOverlay.addEventListener("click", e => {
      if (e.target === updateOverlay) {
        updateOverlay.style.display = "none";
        document.body.style.overflow = "";
      }
    });
  }
});


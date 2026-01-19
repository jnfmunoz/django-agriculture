document.addEventListener("DOMContentLoaded", function () {

  /* =====================================================
     CREATE POST MODAL
  ===================================================== */
  const openCreateBtn = document.getElementById("open-form-btn");
  const createOverlay = document.getElementById("form-overlay");
  const closeCreateBtn = document.getElementById("close-form-btn");

  if (openCreateBtn && createOverlay && closeCreateBtn) {
    openCreateBtn.addEventListener("click", () => {
      createOverlay.style.display = "flex";
      document.body.style.overflow = "hidden";
    });

    closeCreateBtn.addEventListener("click", () => {
      createOverlay.style.display = "none";
      document.body.style.overflow = "";
    });
  }

  /* =====================================================
     UPDATE POST MODAL (AJAX)
  ===================================================== */
  const updateOverlay = document.getElementById("update-form-overlay");
  const updateContent = document.getElementById("update-form-content");
  const closeUpdateBtn = document.getElementById("close-update-form-btn");

  document.querySelectorAll(".open-update-form-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;
      if (!url || !updateOverlay || !updateContent) return;

      fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
        .then(res => res.text())
        .then(html => {
          updateContent.innerHTML = html;
          updateOverlay.style.display = "flex";
          document.body.style.overflow = "hidden";
        })
        .catch(err => {
          console.error("Error cargando formulario update:", err);
        });
    });
  });

  if (closeUpdateBtn && updateOverlay) {
    closeUpdateBtn.addEventListener("click", () => {
      updateOverlay.style.display = "none";
      document.body.style.overflow = "";
    });
  }

});

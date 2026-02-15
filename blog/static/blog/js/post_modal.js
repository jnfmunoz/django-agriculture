console.log("POST MODAL JS LOADED");

document.addEventListener("DOMContentLoaded", function () {

  /* ===============================
     MODAL CORE
  =============================== */
  function openModal(overlay) {
    overlay.style.display = "flex";
    document.body.style.overflow = "hidden";
  }

  function closeModal(overlay) {
    overlay.style.display = "none";
    document.body.style.overflow = "";
  }

  /* ===============================
     CREATE MODAL (AJAX BLOQUEADO)
  =============================== */
  const openCreateBtn = document.getElementById("open-form-btn");
  const createOverlay = document.getElementById("form-overlay");
  const createContainer = createOverlay?.querySelector(".form-container");

  if (openCreateBtn && createOverlay && createContainer) {
    openCreateBtn.addEventListener("click", () => {
      const url = openCreateBtn.dataset.url;
      if (!url) return;

      fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
        .then(res => res.text())
        .then(html => {
          createContainer.innerHTML = `
            <span class="close-btn" id="close-form-btn">&times;</span>
            ${html}
          `;

          openModal(createOverlay);
          bindAjaxForm(createOverlay);

          // Botón X
          createContainer.querySelector("#close-form-btn")
            .addEventListener("click", () => closeModal(createOverlay));
        });
    });

    // ❌ NO cerrar al hacer click fuera
    createOverlay.addEventListener("click", e => {
      e.stopPropagation(); // solo bloquea, no cierra
    });

    createContainer.addEventListener("click", e => e.stopPropagation());
  }

  /* ===============================
     UPDATE MODAL (AJAX BLOQUEADO)
  =============================== */
  const updateOverlay = document.getElementById("update-form-overlay");
  const updateContent = document.getElementById("update-form-content");

  document.querySelectorAll(".open-update-form-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;
      if (!url || !updateOverlay || !updateContent) return;

      fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
        .then(res => res.text())
        .then(html => {
          updateContent.innerHTML = `
            <span class="close-btn" id="close-update-form-btn">&times;</span>
            ${html}
          `;

          openModal(updateOverlay);
          bindAjaxForm(updateOverlay);

          updateContent.querySelector("#close-update-form-btn")
            .addEventListener("click", () => closeModal(updateOverlay));
        });
    });
  });

  // ❌ No cerrar al click fuera
  updateOverlay?.addEventListener("click", e => e.stopPropagation());
  updateContent?.addEventListener("click", e => e.stopPropagation());

  /* ===============================
     AJAX FORM HANDLER
  =============================== */
  function bindAjaxForm(overlay) {
    const form = overlay.querySelector("form");
    if (!form) return;

    bindRealtimeValidation(form);

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const isUpdate = form.dataset.isUpdate === "true";

    Swal.fire({
      title: isUpdate ? "¿Actualizar post?" : "¿Crear post?",
      text: isUpdate
        ? "Se actualizará el contenido del post"
        : "Se creará un nuevo post",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#198754",
      cancelButtonColor: "#dc3545",
      confirmButtonText: isUpdate ? "Sí, actualizar" : "Sí, crear",
      cancelButtonText: "Cancelar",
      customClass: {
        popup: "swal-above-modal"
      },
      backdrop: true,
      allowOutsideClick: false,
      allowEscapeKey: false
    }).then((result) => {
      if (!result.isConfirmed) return;

        const formData = new FormData(form);

        fetch(form.action, {
          method: "POST",
          body: formData,
          headers: { "X-Requested-With": "XMLHttpRequest" }
        })
          .then(async res => {
            const data = await res.json();
            if (!res.ok) throw data;
            return data;
          })
          .then(data => {        
            Swal.fire({
              icon: "success",
              title: "Éxito",
              text: data.message || "Operación realizada correctamente",
              confirmButtonColor: "#198754",
              confirmButtonText: "OK"
            }).then(() => {
              window.location.reload();
            });
          })
          .catch(err => {
            Swal.fire({
              icon: "error",
              title: "Error al crear post",
              text: "Revisa los campos marcados en rojo",
              confirmButtonText: "OK"
            });

            if (err.errors) {
              renderFormErrors(form, err.errors);
            }
          });
      });
    });

    overlay.querySelectorAll(".cancel-modal-btn").forEach(btn => {
      btn.addEventListener("click", () => closeModal(overlay));
    });
  }
});

function clearFormErrors(form) {
  form.querySelectorAll(".error-container").forEach(container => {
    container.innerHTML = "";
  });

  form.querySelectorAll(".is-invalid").forEach(input => {
    input.classList.remove("is-invalid");
  });
}


function renderFormErrors(form, errors){
  clearFormErrors(form);

  Object.entries(errors).forEach(([field, messages]) => {
    const container = form.querySelector(
      `.error-container[data-error-for="${field}"]`
    );

    if (!container) return;

    container.innerHTML = messages.join("<br>");
    
    const input = form.querySelector(`[name="${field}"]`);
    if (input) {
      input.classList.add("is-invalid");
    }
  });
}

function bindRealtimeValidation(form){
  form.querySelectorAll("input, textarea, select").forEach(input => {
    input.addEventListener("input", () => {
      const fieldName = input.name;
      if (!fieldName) return;

      const container = form.querySelector(
        `.error-container[data-error-for="${fieldName}"]`
      );      
      if(container) {
        container.innerHTML = "";
      }

      input.classList.remove("is-invalid");
    });
  });
}
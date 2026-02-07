document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".delete-post-form").forEach(form => {

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      Swal.fire({
        title: "¿Eliminar post?",
        text: "Esta acción no se puede deshacer",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        customClass: {
          popup: "swal-above-modal"
        },
        allowOutsideClick: false,
        allowEscapeKey: false
      }).then((result) => {
        if (!result.isConfirmed) return;

        const formData = new FormData(form);

        fetch(form.action, {
          method: "POST",
          body: formData,
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
          }
        })
          .then(res => res.json())
          .then(data => {
            if (!data.success) throw data;

            Swal.fire({
              icon: "success",
              title: "Éxito",
              text: data.message,
              confirmButtonColor: "#198754",
              confirmButtonText: "OK",
              customClass: {
                popup: "swal-above-modal"
              }
            }).then(() => {
              window.location.reload();
            });
          })
          .catch(() => {
            Swal.fire({
              icon: "error",
              title: "Error",
              text: "No se pudo eliminar el post"
            });
          });
      });
    });

  });
});

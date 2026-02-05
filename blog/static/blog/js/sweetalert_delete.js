document.addEventListener("DOMContentLoaded", function () {
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
        backdrop: true,
        allowOutsideClick: false,
        allowEscapeKey: false
      }).then((result) => {
        if (result.isConfirmed) {
          form.submit();
        }
      });

    });

  });
});

document.addEventListener("DOMContentLoaded", function () {
  if (!window.DJANGO_MESSAGES) return;

  window.DJANGO_MESSAGES.forEach(msg => {
    Swal.fire({
      icon: msg.tag,
      title: msg.tag.charAt(0).toUpperCase() + msg.tag.slice(1),
      text: msg.text,
      confirmButtonColor: "#198754",
      confirmButtonText: "OK",
      customClass: {
        popup: "swal-above-modal"
      },
      backdrop: true,
      allowOutsideClick: false,
      allowEscapeKey: false
    });
  });
});

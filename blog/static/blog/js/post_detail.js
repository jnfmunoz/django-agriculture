/** CRUD Comentarios */
document.addEventListener("DOMContentLoaded", () => {

  /* ---------- helper: get cookie CSRF (si lo necesitas) ---------- */
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  /* ---------- 1) submit del form principal de comentarios ---------- */
  const commentForm = document.getElementById("commentForm"); 
  if (commentForm) {
    commentForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = new FormData(this);

      const response = await fetch(window.location.pathname, {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        body: formData
      });

      if (response.ok) {
        const text = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        const newComment = doc.querySelector("#comments-section .comment:first-child");

        if (newComment) {
          document.getElementById("comments-section").insertAdjacentHTML("afterbegin", newComment.outerHTML);
        } else {
          try {
            const json = JSON.parse(text);
            if (json.html)
              document.getElementById("comments-section").insertAdjacentHTML("afterbegin", json.html);
          } catch (err) { /* ignore */ }
        }

        this.reset();

        const countElem = document.querySelector(".comments-count");
        if (countElem) {
          const currentCount = parseInt(countElem.textContent) || 0;
          countElem.textContent = (currentCount + 1) + " Comments";
        }
      } else {
        console.error("Error al crear comentario principal:", response.status, await response.text());
      }
    });
  }

  /* ---------- 2) event delegation para mostrar/ocultar formularios reply ---------- */
  document.body.addEventListener("click", (e) => {
    const replyBtn = e.target.closest(".reply");
    if (!replyBtn) return;
    e.preventDefault();

    const commentId = replyBtn.dataset.commentId;
    if (!commentId) return;

    // 🔹 Cierra cualquier otro formulario abierto
    document.querySelectorAll(".reply-form").forEach(f => {
      if (f.id !== `reply-form-${commentId}`) {
        f.style.display = "none";
      }
    });

    // 🔹 Alterna el formulario actual (abre/cierra)
    const form = document.getElementById(`reply-form-${commentId}`);
    if (form) {
      form.style.display = form.style.display === "none" || form.style.display === "" ? "block" : "none";
    } else {
      console.warn(`No se encontró el formulario con id reply-form-${commentId}`);
    }
  });

  /* ---------- 3) event delegation para submit de cualquier .ajax-reply-form ---------- */
  document.body.addEventListener("submit", async (e) => {
    const form = e.target.closest(".ajax-reply-form");
    if (!form) return;
    e.preventDefault();

    const parentId = form.dataset.parentId || form.querySelector("[name=parent_id]")?.value;
    const formData = new FormData(form);
    if (parentId) formData.set("parent_id", parentId);

    const response = await fetch(form.action, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: formData
    });

    if (response.ok) {
      const data = await response.json();

      if (data.html) {
        // 🔹 Buscamos el contenedor .replies del comentario padre
        const parentComment = form.closest(".comment");
        const repliesContainer = parentComment?.querySelector(".replies");

        if (repliesContainer) {
          repliesContainer.insertAdjacentHTML("beforeend", data.html);
        } else {
          // Si no existe .replies, insertamos antes del formulario
          form.insertAdjacentHTML("beforebegin", data.html);
        }
      } else {
        console.warn("AJAX reply: response ok pero no vino data.html");
      }

      // 🔹 Limpiar y cerrar el formulario
      form.reset();
      form.style.display = "none";

    } else {
      console.error("Error al enviar reply:", response.status, await response.text());
    }
  });

  /* ---------- 4) cancelar reply ---------- */
  document.body.addEventListener("click", (e) => {
    const btn = e.target.closest(".cancel-reply");
    if (!btn) return;
    e.preventDefault();

    const wrapper = btn.closest(".reply-form");
    if (wrapper) wrapper.style.display = "none";
  });

});

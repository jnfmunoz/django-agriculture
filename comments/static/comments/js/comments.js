/** CRUD Comentarios */
document.addEventListener("DOMContentLoaded", () => {

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

      if (!response.ok) {
        console.error(
          "Error al crear comentario:",
          response.status,
          await response.text()
        );
        return;
      }

      const text = await response.text();

      // 🔹 Elimina el mensaje "No comments yet..." si existe
      const emptyMessage = document.getElementById("no-comments-message");
      if (emptyMessage) {
        emptyMessage.remove();
      }

      // 🔹 Insertar nuevo comentario
      try {
        const json = JSON.parse(text);
        if (json.html) {
          document
            .getElementById("comments-section")
            .insertAdjacentHTML("afterbegin", json.html);
        }
      } catch {
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        const newComment = doc.querySelector(".comment");

        if (newComment) {
          document
            .getElementById("comments-section")
            .insertAdjacentHTML("afterbegin", newComment.outerHTML);
        }
      }

      // 🔹 Reset del formulario
      this.reset();

      // 🔹 Actualizar contador
      const countElem = document.querySelector(".comments-count");
      if (countElem) {
        const current = parseInt(countElem.textContent) || 0;
        countElem.textContent = `${current + 1} Comments`;
      }
    });
  }

  /* ---------- 2) mostrar / ocultar reply forms ---------- */
  document.body.addEventListener("click", (e) => {
    const replyBtn = e.target.closest(".reply");
    if (!replyBtn) return;
    e.preventDefault();

    const commentId = replyBtn.dataset.commentId;
    if (!commentId) return;

    document.querySelectorAll(".reply-form").forEach(f => {
      if (f.id !== `reply-form-${commentId}`) {
        f.style.display = "none";
      }
    });

    const form = document.getElementById(`reply-form-${commentId}`);
    if (form) {
      form.style.display =
        form.style.display === "block" ? "none" : "block";
    }
  });

  /* ---------- 3) submit de replies (AJAX) ---------- */
  document.body.addEventListener("submit", async (e) => {
    const form = e.target.closest(".ajax-reply-form");
    if (!form) return;

    e.preventDefault();

    const parentId = form.dataset.parentId;
    const formData = new FormData(form);
    if (parentId) formData.set("parent_id", parentId);

    const response = await fetch(form.action, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: formData
    });

    if (!response.ok) {
      console.error(
        "Error al enviar reply:",
        response.status,
        await response.text()
      );
      return;
    }

    const data = await response.json();

    if (data.html) {
      const parentComment = form.closest(".comment");
      let repliesContainer = parentComment.querySelector(".replies");

      if (!repliesContainer) {
        repliesContainer = document.createElement("div");
        repliesContainer.className = "replies ms-5 mt-3 ps-3";
        form.before(repliesContainer);
      }

      repliesContainer.insertAdjacentHTML("beforeend", data.html);
    }

    form.reset();
    form.style.display = "none";
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

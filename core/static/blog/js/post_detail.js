document.getElementById("commentForm")?.addEventListener("submit", async function(e){
e.preventDefault();

const formData = new FormData(this);

const response = await fetch("", {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
    body: formData
});

if(response.ok){
    const parser = new DOMParser();
    const html = await response.text();
    const doc = parser.parseFromString(html, "text/html");
    
    // Tomamos solo el comentario recién agregado (último en la lista)
    const newComment = doc.querySelector("#comments-section .comment:first-child");
    document.getElementById("comments-section").insertAdjacentHTML("afterbegin", newComment.outerHTML);

    // Limpiamos el formulario
    this.reset();

    // Actualizamos el contador
    const countElem = document.querySelector(".comments-count");
    const currentCount = parseInt(countElem.textContent) || 0;
    countElem.textContent = (currentCount + 1) + " Comments";
}
});

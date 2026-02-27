const app = document.getElementById("app");
const grid = document.getElementById("moviesGrid");

if (app && grid) {
    let page = parseInt(app.dataset.page || 1);
    const query = app.dataset.query;
    let loading = false;

    window.addEventListener("scroll", () => {
        const nearBottom =
            window.innerHeight + window.scrollY >=
            document.body.offsetHeight - 200;

        if (nearBottom && !loading) {
            loading = true;
            page++;

            let url = `/?page=${page}`;
            if (query) {
                url += `&q=${query}`;
            }

            fetch(url)
                .then(res => res.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, "text/html");
                    const newCards = doc.querySelectorAll(".movie-card");

                    newCards.forEach(card => grid.appendChild(card));
                    loading = false;
                })
                .catch(() => {
                    loading = false;
                });
        }
    });
}
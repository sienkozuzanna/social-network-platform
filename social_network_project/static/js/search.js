document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    searchInput.addEventListener("input", function () {
        const query = this.value.trim(); // Usuń białe znaki

        if (query.length > 1) {
            fetch(`/search-users/?search=${query}`)
                .then((response) => response.json())
                .then((data) => {
                    searchResults.innerHTML = ""; // Wyczyść listę wyników

                    if (data.results.length === 0) {
                        // Jeśli brak wyników, pokaż komunikat
                        const noResultsLi = document.createElement("li");
                        noResultsLi.textContent = "No results found.";
                        noResultsLi.className = "no-results";
                        searchResults.appendChild(noResultsLi);
                    } else {
                        // Wyświetl wyniki
                        data.results.forEach((user) => {
                            const li = document.createElement("li");
                            li.innerHTML = `
                                <img src="${user.profile_picture}" alt="Profile Picture">
                                <span>${user.username}</span>
                            `;
                            li.addEventListener("click", function () {
                                window.location.href = `/profile/${user.username}/`;
                            });
                            searchResults.appendChild(li);
                        });
                    }
                })
                .catch((error) => {
                    console.error("Error fetching search results:", error);
                });
        } else {
            searchResults.innerHTML = ""; // Wyczyść listę wyników, jeśli zapytanie jest zbyt krótkie
        }
    });

    // Ukryj dropdown, gdy klikniesz poza wyszukiwarkę
    document.addEventListener("click", function (event) {
        if (!searchResults.contains(event.target) && event.target !== searchInput) {
            searchResults.innerHTML = "";
        }
    });
});

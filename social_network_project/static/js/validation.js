document.addEventListener("DOMContentLoaded", () => {
    /**
     * Funkcja do wyświetlania błędów w formularzu
     */
    const showError = (form, message) => {
        let errorDiv = form.querySelector(".form-error");
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.classList.add("form-error");
            form.prepend(errorDiv);
        }
        errorDiv.innerText = message;
        errorDiv.style.display = "block";
    };

    /**
     * Funkcja do walidacji długości pola tekstowego
     */
    const validateContentLength = (content, maxLength) => {
        if (content.trim().length > maxLength) {
            return `Content must be less than ${maxLength} characters.`;
        }
        if (content.trim() === "") {
            return "Content cannot be empty.";
        }
        return null;
    };

    /**
     * Walidacja dla dodawania posta
     */
    const addPostForm = document.getElementById("addPostForm");
    if (addPostForm) {
        addPostForm.addEventListener("submit", (event) => {
            const content = document.getElementById("content").value;
            const errorMessage = validateContentLength(content, 500);
            if (errorMessage) {
                showError(addPostForm, errorMessage);
                event.preventDefault();
            }
        });
    }

    /**
     * Walidacja dla edycji posta
     */
    const editPostForm = document.getElementById("editPostForm");
    if (editPostForm) {
        editPostForm.addEventListener("submit", (event) => {
            const content = document.getElementById("content").value;
            const errorMessage = validateContentLength(content, 500);
            if (errorMessage) {
                showError(editPostForm, errorMessage);
                event.preventDefault();
            }
        });
    }

    /**
     * Walidacja dla usuwania posta
     */
    const deletePostForm = document.getElementById("deletePostForm");
    if (deletePostForm) {
        deletePostForm.addEventListener("submit", (event) => {
            const confirmDelete = confirm("Are you sure you want to delete this post?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    }

    /**
     * Walidacja dla formularza rejestracji
     */
    const registrationForm = document.getElementById("registrationForm");
    if (registrationForm) {
        registrationForm.addEventListener("submit", (event) => {
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;

            if (password !== confirmPassword) {
                showError(registrationForm, "Passwords do not match.");
                event.preventDefault();
            }
        });
    }

    /**
     * Walidacja dla edycji profilu
     */
    const editProfileForm = document.getElementById("editProfileForm");
    if (editProfileForm) {
        editProfileForm.addEventListener("submit", (event) => {
            const bio = document.getElementById("bio").value;
            const errorMessage = validateContentLength(bio, 500);
            if (errorMessage) {
                showError(editProfileForm, errorMessage);
                event.preventDefault();
            }
        });
    }
});

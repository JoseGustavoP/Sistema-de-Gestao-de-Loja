document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("#registerForm"); // Certifique-se de que este seletor corresponde ao seu formulário
    const password1 = document.querySelector("#id_password1");
    const password2 = document.querySelector("#id_password2");
    const errorMessage = document.querySelector("#error-message"); // Certifique-se de que este elemento existe

    function isPasswordStrong(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumber;
    }

    form.addEventListener("submit", function(e) {
        errorMessage.textContent = ''; // Limpa a mensagem de erro

        // Verifica se as senhas coincidem
        if (password1.value !== password2.value) {
            e.preventDefault();
            errorMessage.textContent = "As senhas não coincidem. Por favor, insira senhas iguais.";
            console.log("Senhas não coincidem"); // Debugging
            return;
        }

        // Verifica a força da senha
        if (!isPasswordStrong(password1.value)) {
            e.preventDefault();
            errorMessage.innerHTML += "A senha não é segura o suficiente. Use uma senha com pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números.<br>"; // Alterado para refletir a nova política de senha
            console.log("Senha fraca"); // Debugging
            return;
        }

        console.log("Formulário válido, enviando..."); // Mensagem de debug para indicar que o formulário deve ser enviado
        // O formulário será enviado se não entrar em nenhum dos if's acima
    });
});

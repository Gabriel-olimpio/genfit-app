document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.notification .delete').forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});

// Fetch para o backend

document.getElementById("exercise-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Evita o reload da página

    // Coleta os dados do formulário
    const formData = {
        objetivo: document.getElementById("objetivo").value,
        dias: document.getElementById("dias").value,
        peso: document.getElementById("peso").value,
        altura: document.getElementById("altura").value,
        duracao: document.getElementById("duracao").value

    };

    try {
        // Faz a requisição ao backend
        const response = await fetch('/generate_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        // Exibe o plano gerado no frontend
        const resultDiv = document.getElementById("result");
        if (data.plan) {
            resultDiv.innerHTML = `<h2>Plano de Treino Gerado:</h2><pre>${data.plan}</pre>`;
        } else {
            resultDiv.innerHTML = `<p>Erro ao gerar o plano: ${data.error}</p>`;
        }
    } catch (error) {
        console.error("Erro:", error);
    }
});

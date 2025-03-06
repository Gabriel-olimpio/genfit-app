document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.notification .delete').forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});


document.getElementById('generate-plan-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const generateButton = document.getElementById('generate-button');
    generateButton.classList.add('is-loading');

    
    const formData = new FormData(this);

    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok){
            return response.text();

        } else {
            throw new Error('Erro ao gerar o plano');
        }
    })
    .then(html => {
        document.open();
        document.write(html);
        document.close();

    })
    .catch(error => {
        console.error('Error:', error);
        alert('Erro ao gerar o plano');
    })
    .finally(() => {
        generateButton.classList.remove('is-loading');
    });
});


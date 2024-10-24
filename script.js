document.getElementById('checkDate').addEventListener('click', async function() {
    const username = document.getElementById('user').value;
    const projectCode = document.getElementById('code').value;

    if (!username || !projectCode) {
        document.getElementById('result').textContent = "Please enter both username and project code.";
        return;
    }

    const url = `https://editor.p5js.org/${username}/sketches`;

    try {
        const response = await fetch(url);
        const htmlText = await response.text();

        // Criar um elemento DOM para processar o HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, 'text/html');

        // Selecionar todas as linhas da tabela
        const rows = doc.querySelectorAll('.sketches-table__row');

        let found = false;
        rows.forEach(row => {
            const sketchLink = row.querySelector('a').getAttribute('href');
            const sketchCode = sketchLink.split('/').pop(); // Pega o código do projeto no final da URL

            if (sketchCode === projectCode) {
                const lastUpdated = row.querySelector('td:nth-child(3)').textContent;
                document.getElementById('result').textContent = `Project was last updated on: ${lastUpdated}`;
                found = true;
            }
        });

        if (!found) {
            document.getElementById('result').textContent = "Project not found.";
        }

    } catch (error) {
        document.getElementById('result').textContent = "Error fetching the data. Please check the username and project code.";
        console.error('Error:', error);
    }
});

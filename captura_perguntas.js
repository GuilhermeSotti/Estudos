    function scr() {
        let resumo = [];
        
        let testes = document.querySelectorAll("#on-container-fast-test > form > div.on-fast-test-item");

        testes.forEach((teste, index) => {
            let titulo = teste.querySelector("h3");
            let enunciado = teste.querySelector("p");
            let exemplo = teste.querySelector("pre");
            let alternativas = teste.querySelectorAll("label");

            let questaoTexto = `Questão ${index + 1}:\n`;

            if (titulo) questaoTexto += `**${titulo.innerText.trim()}**\n`;
            if (enunciado) questaoTexto += `${enunciado.innerText.replace(/\s+/g, " ").trim()}\n\n`;
            if (exemplo) questaoTexto += `\n${exemplo.innerText.replace(/\s+/g, " ").trim()}\n\n`;

            alternativas.forEach((alternativa, altIndex) => {
                let letra = String.fromCharCode(65 + altIndex); // Converte índice para A, B, C...
                questaoTexto += `${letra}) ${alternativa.innerText.replace(/\s+/g, " ").trim()}\n`;
            });

            resumo.push(questaoTexto);
        });

        return resumo.join("\n\n--------------------\n\n");
    }
function scr() {
    let resumo = [];
    let testes = document.querySelectorAll("#responseform");

    testes.forEach((teste, index) => {
        let titulo = teste.querySelector("div > div.col-md-12.my-3 > div > div.col-md-6.pr-3.d-flex.flex-column.justify-content-between > h3");
        let enunciado = teste.querySelectorAll("div:nth-child(2) > div.content-question.tipo-multichoice.d-flex.flex-wrap > div > div > p");
        let exemplo = teste.querySelector("pre");
        let alternativas = teste.querySelectorAll("div:nth-child(2) > div.content-question.tipo-multichoice.d-flex.flex-wrap > ul > li > label");

        let questaoTexto = `Questão ${index + 1}:\n`;

        if (titulo) questaoTexto += `**${titulo.innerText.trim()}**\n`;
        if (exemplo) questaoTexto += `\n${exemplo.innerText.replace(/\s+/g, " ").trim()}\n\n`;

        enunciado.forEach((enunciado) => {
            questaoTexto += `) ${enunciado.innerText.replace(/\s+/g, " ").trim()}\n`;
        });

        alternativas.forEach((alternativa, altIndex) => {
            let letra = String.fromCharCode(65 + altIndex); // Converte índice para A, B, C...
            questaoTexto += `${letra}) ${alternativa.innerText.replace(/\s+/g, " ").trim()}\n`;
        });

        resumo.push(questaoTexto);
    });

    return resumo.join("\n\n--------------------\n\n");
}
//----------------------------------------------------------------------------------------
// Busca todos os alunos via API e preenche um dropdown (<select>)
function getAllStudents(){
    // Faz requisição GET para a rota '/alunos'
    fetch('/alunos')
    .then(response => {
       return response.json()  // Converte resposta para JSON
    })
    .then(data => {
        // Cria option padrão (desabilitada)
        let html = '<option selected disabled> Selecione um aluno </option>'
        
        // Itera sobre os dados recebidos
        for(let i = 0; i < data.length; i++){
            // Adiciona cada aluno como uma opção no dropdown
            html += `<option value="${data[i].id}"> ${data[i].nome} </option>`
        }
        
        // Insere as options no elemento <select> com ID 'aluno'
        document.getElementById('aluno').innerHTML = html
    })    
    .catch(error => console.error('Erro ao carregar alunos:', error)); // Adicionei tratamento de erro
}
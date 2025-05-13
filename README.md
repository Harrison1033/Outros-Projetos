# Outros-Projetos
Projetos usando linguagens diversas aprendidos durante meus estudos.

## 📚 GenericSchool
Projeto escolar genérico desenvolvido com Flask (Python) para gerenciamento de alunos, cursos e matrículas.

🛠️ Tecnologias
Backend: Python + Flask

Frontend: HTML, CSS (arquivos estáticos), JavaScript

Templates: Jinja2 (integrado ao Flask)

📂 **Estrutura do Projeto**  
- 📁 `GenericSchool/`  
  - 📄 `app.py` *(Aplicação principal)*  
  - 📁 `static/`  
    - 📁 `css/` → `style.css`  
    - 📁 `img/` *(Imagens)*  
    - 📁 `js/` → `script.js`  
  - 📁 `templates/`  
    - 📄 `createAluno.html`  
    - 📄 `createCurso.html`  
    - 📄 `index.html`  
    - 📄 `matriculas.html`  
    - 📄 `registerUser.html`

🚀 Como Executar
Clone o repositório:

bash
git clone https://github.com/Harrison1033/GenericSchool.git
cd GenericSchool
Configure o ambiente virtual (Python):

bash
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate # Linux/Mac
Instale as dependências:

bash
pip install flask
Execute a aplicação:

bash
flask --app app run
Acesse: http://localhost:5000

✨ Funcionalidades
Cadastro de alunos, cursos e usuários.

Páginas HTML interativas com CSS e JavaScript.

Roteamento via Flask (ver app.py).

🤝 Contribuição
Contribuições são bem-vindas! Siga os passos:

Faça um fork do projeto.

Crie uma branch: git checkout -b minha-feature.

Envie um Pull Request.

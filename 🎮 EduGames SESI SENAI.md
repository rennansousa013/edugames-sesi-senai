# 🎮 EduGames SESI SENAI

> Aplicativo educacional com IA adaptativa para estudantes do SESI SENAI Maracanaú-CE

## 🚀 Visão Geral

O **EduGames SESI SENAI** é uma plataforma educacional inovadora que utiliza inteligência artificial para personalizar a experiência de aprendizagem de cada aluno. O sistema inclui um quiz inicial para identificar o perfil de aprendizagem e oferece jogos educacionais adaptativos baseados na metodologia STEAM.

## ✨ Principais Funcionalidades

- 🧠 **IA Adaptativa**: Ajusta automaticamente a dificuldade baseada no desempenho
- 📝 **Quiz de Perfil**: Identifica o estilo de aprendizagem e interesses do aluno
- 🎯 **Metodologia STEAM**: Integra Ciência, Tecnologia, Engenharia, Arte e Matemática
- 🎮 **Jogos Educacionais**: 6 categorias de jogos alinhados ao currículo SESI SENAI
- 📊 **Gamificação**: Sistema de pontos, progresso e conquistas
- 📱 **Interface Responsiva**: Funciona em desktop e dispositivos móveis

## 🛠️ Tecnologias Utilizadas

### Frontend
- ⚛️ React 18 + Vite
- 🎨 Tailwind CSS
- 🧩 Shadcn/UI Components
- 🔗 React Router
- 🎯 Lucide Icons

### Backend
- 🐍 Python Flask
- 🤖 Scikit-learn (IA)
- 🗄️ SQLAlchemy (ORM)
- 🌐 Flask-CORS

## 🚀 Como Executar

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- Git

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd edugames-sesi-senai
```

### 2. Configure o Backend
```bash
cd adaptive_learning_system
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python src/main.py
```

### 3. Configure o Frontend
```bash
cd adaptive-learning-frontend
npm install
npm run dev
```

### 4. Acesse o sistema
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:5000

## 🎯 Jogos Disponíveis

| Jogo | Foco | Metodologia STEAM |
|------|------|-------------------|
| 🧮 **Aventura Matemática** | Lógica e Cálculo | Investigar |
| 🤖 **Laboratório de Robótica** | Programação | Criar |
| 🧩 **Desafios de Lógica** | Raciocínio | Refletir |
| 💻 **Código Criativo** | Algoritmos | Criar |
| 🌍 **Comunicação Global** | Idiomas | Conectar |
| 🔬 **Laboratório Virtual** | Ciências | Descobrir |

## 📊 Quiz de Perfil

O quiz inicial identifica:
- 🎨 Estilo de aprendizagem (visual, auditivo, cinestésico)
- ⭐ Atividades preferidas
- 📚 Matérias favoritas
- 🎯 Preferência de desafio
- 🏆 Fontes de motivação
- 🔬 Atividades STEAM preferidas
- 💼 Interesses profissionais

## 🏗️ Arquitetura do Sistema

```
📁 Projeto/
├── 🌐 adaptive-learning-frontend/    # React Frontend
│   ├── 📦 src/components/           # Componentes React
│   ├── 🖼️ src/assets/              # Imagens e recursos
│   └── ⚛️ src/App.jsx              # App principal
├── 🔧 adaptive_learning_system/     # Flask Backend
│   ├── 📊 src/models/              # Modelos de dados
│   ├── 🛣️ src/routes/              # Rotas da API
│   ├── 🤖 src/ai_engine.py         # Motor de IA
│   └── 🐍 src/main.py              # App principal
└── 📚 documentacao/                # Documentação
```

## 🧪 Status dos Testes

| Componente | Status | Descrição |
|------------|--------|-----------|
| ✅ Frontend | Aprovado | Interface responsiva e funcional |
| ✅ Backend | Aprovado | API REST completa |
| ✅ IA Adaptativa | Aprovado | Algoritmos implementados |
| ✅ Quiz | Aprovado | 7 perguntas funcionais |
| ✅ Integração | Aprovado | Frontend-Backend conectados |

## 🎓 Metodologia STEAM

O sistema implementa os 5 pilares:

- 🔬 **Investigar** (Science): Pesquisa e descoberta
- 💻 **Descobrir** (Technology): Exploração tecnológica  
- 🔧 **Conectar** (Engineering): Colaboração e integração
- 🎨 **Criar** (Arts): Projetos criativos
- 📐 **Refletir** (Mathematics): Análise e metacognição

## 🚀 Próximos Passos

- 🎮 Implementar jogos interativos completos
- 👨‍🏫 Dashboard para professores
- 🏆 Sistema de gamificação avançado
- 🤝 Funcionalidades colaborativas
- ☁️ Deploy em produção

## 📞 Contato

**Escola SESI SENAI Maracanaú**
- 📍 Av. Senador Virgílio Távora, 1103
- 🏢 Distrito Industrial - Maracanaú/CE
- ☎️ (85) 4009-6300

---

*Desenvolvido para transformar a educação através da tecnologia e inovação pedagógica* 🚀


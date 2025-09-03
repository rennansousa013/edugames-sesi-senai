import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Brain, Gamepad2, Trophy, Star, BookOpen, Zap, Target, Users } from 'lucide-react'
import QuizComponent from './components/QuizComponent.jsx'
import logoEduGames from './assets/logo-edugames.png'
import heroBackground from './assets/hero-background.png'
import gameMath from './assets/game-math.png'
import gameRobotics from './assets/game-robotics.png'
import gameLogic from './assets/game-logic.png'
import './App.css'

// Componente de Header
function Header({ currentUser, onLogin, onLogout }) {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <img src={logoEduGames} alt="EduGames SESI SENAI" className="h-10 w-10" />
            <div>
              <h1 className="text-xl font-bold text-gray-900">EduGames</h1>
              <p className="text-sm text-gray-500">SESI SENAI</p>
            </div>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="text-gray-700 hover:text-blue-600 font-medium">Início</a>
            <a href="#games" className="text-gray-700 hover:text-blue-600 font-medium">Jogos</a>
            <a href="#progress" className="text-gray-700 hover:text-blue-600 font-medium">Progresso</a>
            <a href="#about" className="text-gray-700 hover:text-blue-600 font-medium">Sobre</a>
          </nav>
          
          <div className="flex items-center space-x-4">
            {currentUser ? (
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{currentUser.name}</p>
                  <p className="text-xs text-gray-500">{currentUser.grade_level}</p>
                </div>
                <Button variant="outline" size="sm" onClick={onLogout}>
                  Sair
                </Button>
              </div>
            ) : (
              <Button onClick={onLogin}>
                Entrar
              </Button>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

// Componente de Hero Section
function HeroSection({ onStartQuiz }) {
  return (
    <section 
      className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-orange-500 text-white py-20"
      style={{
        backgroundImage: `url(${heroBackground})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundBlendMode: 'overlay'
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Aprendizagem que se
            <span className="block text-yellow-300">Adapta a Você!</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
            Descubra jogos educacionais que evoluem com seu progresso, 
            baseados na metodologia STEAM do SESI SENAI
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold"
              onClick={onStartQuiz}
            >
              <Brain className="mr-2 h-5 w-5" />
              Começar Quiz de Perfil
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-white text-white hover:bg-white hover:text-gray-900"
            >
              <Gamepad2 className="mr-2 h-5 w-5" />
              Explorar Jogos
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}

// Componente de Game Card
function GameCard({ game, onPlayGame }) {
  const gameImages = {
    math: gameMath,
    robotics: gameRobotics,
    logic: gameLogic,
    programming: gameRobotics,
    language: gameLogic,
    science: gameMath
  }

  const gameIcons = {
    math: Target,
    robotics: Zap,
    logic: Brain,
    programming: BookOpen,
    language: Users,
    science: Star
  }

  const Icon = gameIcons[game.type] || Gamepad2

  return (
    <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => onPlayGame(game)}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <Icon className="h-6 w-6 text-blue-600" />
          <Badge variant="secondary">Nível {game.difficulty}</Badge>
        </div>
        <CardTitle className="text-lg">{game.title}</CardTitle>
        <CardDescription>{game.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <img 
          src={gameImages[game.type]} 
          alt={game.title}
          className="w-full h-32 object-cover rounded-lg mb-4"
        />
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Progresso</span>
            <span>{game.progress}%</span>
          </div>
          <Progress value={game.progress} className="h-2" />
        </div>
        <div className="flex flex-wrap gap-1 mt-3">
          {game.skills.map((skill, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {skill}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

// Componente de Games Section
function GamesSection({ games, onPlayGame }) {
  return (
    <section id="games" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Jogos Adaptativos
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Nossa IA analisa seu desempenho e ajusta a dificuldade para manter você sempre desafiado
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {games.map((game, index) => (
            <GameCard key={index} game={game} onPlayGame={onPlayGame} />
          ))}
        </div>
      </div>
    </section>
  )
}

// Componente de Features Section
function FeaturesSection() {
  const features = [
    {
      icon: Brain,
      title: "IA Adaptativa",
      description: "Sistema inteligente que ajusta a dificuldade baseado no seu progresso"
    },
    {
      icon: Target,
      title: "Metodologia STEAM",
      description: "Investigar, Descobrir, Conectar, Criar e Refletir em cada atividade"
    },
    {
      icon: Trophy,
      title: "Gamificação",
      description: "Pontos, medalhas e rankings para manter você motivado"
    },
    {
      icon: BookOpen,
      title: "Currículo SESI SENAI",
      description: "Alinhado com as competências e habilidades da sua escola"
    }
  ]

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Por que escolher o EduGames?
          </h2>
          <p className="text-lg text-gray-600">
            Tecnologia de ponta para uma educação personalizada
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <feature.icon className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

// Componente principal do App
function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [showQuiz, setShowQuiz] = useState(false)
  
  // Dados de exemplo para jogos
  const [games] = useState([
    {
      type: 'math',
      title: 'Aventura Matemática',
      description: 'Resolva problemas matemáticos em aventuras emocionantes',
      difficulty: 3,
      progress: 65,
      skills: ['Lógica', 'Cálculo', 'Resolução de Problemas']
    },
    {
      type: 'robotics',
      title: 'Laboratório de Robótica',
      description: 'Programe robôs virtuais para completar missões',
      difficulty: 4,
      progress: 40,
      skills: ['Programação', 'Lógica', 'Criatividade']
    },
    {
      type: 'logic',
      title: 'Desafios de Lógica',
      description: 'Quebra-cabeças que exercitam seu raciocínio',
      difficulty: 2,
      progress: 80,
      skills: ['Raciocínio', 'Padrões', 'Análise']
    },
    {
      type: 'programming',
      title: 'Código Criativo',
      description: 'Aprenda programação criando projetos divertidos',
      difficulty: 5,
      progress: 25,
      skills: ['Programação', 'Algoritmos', 'Criatividade']
    },
    {
      type: 'language',
      title: 'Comunicação Global',
      description: 'Desenvolva habilidades de comunicação e idiomas',
      difficulty: 3,
      progress: 55,
      skills: ['Comunicação', 'Idiomas', 'Cultura']
    },
    {
      type: 'science',
      title: 'Laboratório Virtual',
      description: 'Experimentos científicos em ambiente virtual',
      difficulty: 4,
      progress: 35,
      skills: ['Ciências', 'Experimentação', 'Observação']
    }
  ])

  const handleLogin = () => {
    // Simulação de login
    setCurrentUser({
      id: 1,
      name: 'João Silva',
      email: 'joao.silva@sesisenai.edu.br',
      grade_level: '8º ano'
    })
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setShowQuiz(false)
  }

  const handleStartQuiz = () => {
    if (!currentUser) {
      handleLogin()
    }
    setShowQuiz(true)
  }

  const handlePlayGame = (game) => {
    if (!currentUser) {
      handleLogin()
      return
    }
    
    // Aqui seria implementada a lógica para iniciar o jogo
    alert(`Iniciando ${game.title}! (Em desenvolvimento)`)
  }

  const handleQuizComplete = async (answers, profile) => {
    try {
      // Aqui seria feita a chamada para a API para salvar o perfil
      console.log('Quiz answers:', answers)
      console.log('Generated profile:', profile)
      
      // Simular salvamento do perfil
      setCurrentUser(prev => ({
        ...prev,
        learningProfile: profile
      }))
      
      setShowQuiz(false)
      alert('Perfil de aprendizagem criado com sucesso! Agora os jogos serão personalizados para você.')
    } catch (error) {
      console.error('Erro ao salvar perfil:', error)
      alert('Erro ao salvar seu perfil. Tente novamente.')
    }
  }

  if (showQuiz) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header currentUser={currentUser} onLogin={handleLogin} onLogout={handleLogout} />
        <QuizComponent 
          onQuizComplete={handleQuizComplete}
          onBack={() => setShowQuiz(false)}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      <Header currentUser={currentUser} onLogin={handleLogin} onLogout={handleLogout} />
      <HeroSection onStartQuiz={handleStartQuiz} />
      <GamesSection games={games} onPlayGame={handlePlayGame} />
      <FeaturesSection />
      
      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <img src={logoEduGames} alt="EduGames" className="h-8 w-8" />
                <span className="text-xl font-bold">EduGames SESI SENAI</span>
              </div>
              <p className="text-gray-400">
                Plataforma de aprendizagem adaptativa para estudantes do SESI SENAI
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Links Úteis</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Sobre o SESI SENAI</a></li>
                <li><a href="#" className="hover:text-white">Metodologia STEAM</a></li>
                <li><a href="#" className="hover:text-white">Suporte</a></li>
                <li><a href="#" className="hover:text-white">Contato</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Contato</h3>
              <div className="text-gray-400 space-y-2">
                <p>Escola SESI SENAI Maracanaú</p>
                <p>Av. Senador Virgílio Távora, 1103</p>
                <p>Distrito Industrial - Maracanaú/CE</p>
                <p>(85) 4009-6300</p>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 SESI SENAI Ceará. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App


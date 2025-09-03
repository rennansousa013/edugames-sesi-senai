import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { CheckCircle, ArrowRight, ArrowLeft, Brain } from 'lucide-react'

const QuizComponent = ({ onQuizComplete, onBack }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({})
  const [isCompleted, setIsCompleted] = useState(false)

  const questions = [
    {
      id: 'learning_preference',
      title: 'Como você prefere aprender?',
      description: 'Escolha a opção que mais se identifica com você',
      type: 'single',
      options: [
        { value: 'visual', label: 'Vendo imagens, diagramas e vídeos', description: 'Aprendo melhor com recursos visuais' },
        { value: 'auditory', label: 'Ouvindo explicações e discussões', description: 'Prefiro escutar para entender' },
        { value: 'kinesthetic', label: 'Fazendo atividades práticas', description: 'Gosto de colocar a mão na massa' },
        { value: 'reading_writing', label: 'Lendo textos e fazendo anotações', description: 'Aprendo melhor lendo e escrevendo' }
      ]
    },
    {
      id: 'favorite_activities',
      title: 'Quais atividades você mais gosta?',
      description: 'Selecione até 3 opções',
      type: 'multiple',
      maxSelections: 3,
      options: [
        { value: 'drawing', label: 'Desenhar e criar arte' },
        { value: 'building', label: 'Construir e montar coisas' },
        { value: 'reading', label: 'Ler livros e histórias' },
        { value: 'music', label: 'Ouvir música e tocar instrumentos' },
        { value: 'sports', label: 'Praticar esportes' },
        { value: 'experimenting', label: 'Fazer experimentos' },
        { value: 'programming', label: 'Programar computadores' },
        { value: 'talking', label: 'Conversar com amigos' }
      ]
    },
    {
      id: 'subject_preferences',
      title: 'Quais matérias você mais gosta na escola?',
      description: 'Selecione até 4 opções',
      type: 'multiple',
      maxSelections: 4,
      options: [
        { value: 'math', label: 'Matemática' },
        { value: 'science', label: 'Ciências' },
        { value: 'portuguese', label: 'Português' },
        { value: 'english', label: 'Inglês' },
        { value: 'history', label: 'História' },
        { value: 'geography', label: 'Geografia' },
        { value: 'art', label: 'Arte' },
        { value: 'physical_education', label: 'Educação Física' },
        { value: 'robotics', label: 'Robótica' },
        { value: 'programming', label: 'Programação' }
      ]
    },
    {
      id: 'challenge_preference',
      title: 'Como você gosta dos seus desafios?',
      description: 'Escolha o nível de dificuldade que mais te motiva',
      type: 'single',
      options: [
        { value: 'easy', label: 'Fáceis e relaxantes', description: 'Prefiro começar devagar' },
        { value: 'medium', label: 'Equilibrados', description: 'Nem muito fácil, nem muito difícil' },
        { value: 'hard', label: 'Difíceis e desafiadores', description: 'Gosto de desafios que me fazem pensar muito' }
      ]
    },
    {
      id: 'motivation_sources',
      title: 'O que mais te motiva a aprender?',
      description: 'Selecione até 3 opções',
      type: 'multiple',
      maxSelections: 3,
      options: [
        { value: 'points', label: 'Ganhar pontos e recompensas' },
        { value: 'competition', label: 'Competir com outros alunos' },
        { value: 'collaboration', label: 'Trabalhar em equipe' },
        { value: 'discovery', label: 'Descobrir coisas novas' },
        { value: 'creation', label: 'Criar projetos próprios' },
        { value: 'recognition', label: 'Ser reconhecido pelo progresso' },
        { value: 'fun', label: 'Se divertir enquanto aprende' },
        { value: 'achievement', label: 'Conquistar objetivos' }
      ]
    },
    {
      id: 'steam_activities',
      title: 'Qual dessas atividades STEAM mais te interessa?',
      description: 'STEAM = Ciência, Tecnologia, Engenharia, Arte e Matemática',
      type: 'single',
      options: [
        { value: 'investigate', label: 'Investigar e pesquisar', description: 'Descobrir como as coisas funcionam' },
        { value: 'discover', label: 'Explorar e descobrir', description: 'Encontrar coisas novas e interessantes' },
        { value: 'connect', label: 'Conectar e colaborar', description: 'Trabalhar com outros e fazer conexões' },
        { value: 'create', label: 'Criar e construir', description: 'Fazer projetos e inventar coisas' },
        { value: 'reflect', label: 'Analisar e refletir', description: 'Pensar sobre o que aprendi' }
      ]
    },
    {
      id: 'career_interests',
      title: 'Que profissão te interessa mais?',
      description: 'Pense no que você gostaria de fazer no futuro',
      type: 'single',
      options: [
        { value: 'engineer', label: 'Engenheiro(a)', description: 'Projetar e construir coisas' },
        { value: 'programmer', label: 'Programador(a)', description: 'Criar aplicativos e jogos' },
        { value: 'scientist', label: 'Cientista', description: 'Fazer descobertas e experimentos' },
        { value: 'artist', label: 'Artista', description: 'Criar arte e design' },
        { value: 'teacher', label: 'Professor(a)', description: 'Ensinar e ajudar outros a aprender' },
        { value: 'entrepreneur', label: 'Empreendedor(a)', description: 'Criar meu próprio negócio' }
      ]
    }
  ]

  const handleAnswerChange = (questionId, value, isMultiple = false) => {
    if (isMultiple) {
      const currentAnswers = answers[questionId] || []
      const question = questions.find(q => q.id === questionId)
      const maxSelections = question.maxSelections || 999
      
      if (currentAnswers.includes(value)) {
        // Remove if already selected
        setAnswers(prev => ({
          ...prev,
          [questionId]: currentAnswers.filter(answer => answer !== value)
        }))
      } else if (currentAnswers.length < maxSelections) {
        // Add if under limit
        setAnswers(prev => ({
          ...prev,
          [questionId]: [...currentAnswers, value]
        }))
      }
    } else {
      setAnswers(prev => ({
        ...prev,
        [questionId]: value
      }))
    }
  }

  const canProceed = () => {
    const question = questions[currentQuestion]
    const answer = answers[question.id]
    
    if (question.type === 'multiple') {
      return answer && answer.length > 0
    }
    return answer !== undefined
  }

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      handleComplete()
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const handleComplete = async () => {
    setIsCompleted(true)
    
    // Simular processamento
    setTimeout(() => {
      const profile = processAnswers(answers)
      onQuizComplete(answers, profile)
    }, 2000)
  }

  const processAnswers = (answers) => {
    // Processar respostas para criar perfil de aprendizagem
    const profile = {
      learning_style: answers.learning_preference || 'visual',
      interests: answers.subject_preferences || [],
      steam_preference: answers.steam_activities || 'investigate',
      difficulty_preference: answers.challenge_preference || 'medium',
      motivation_factors: answers.motivation_sources || [],
      career_interest: answers.career_interests || 'engineer',
      favorite_activities: answers.favorite_activities || []
    }

    return profile
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100

  if (isCompleted) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center space-y-6">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Quiz Concluído!
                </h2>
                <p className="text-gray-600">
                  Estamos processando suas respostas para criar seu perfil personalizado...
                </p>
              </div>
              <div className="flex justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const question = questions[currentQuestion]
  const currentAnswer = answers[question.id]

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-gray-900">Quiz de Perfil de Aprendizagem</h1>
          <span className="text-sm text-gray-500">
            {currentQuestion + 1} de {questions.length}
          </span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-xl">{question.title}</CardTitle>
          <CardDescription>{question.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {question.type === 'single' ? (
            <RadioGroup
              value={currentAnswer || ''}
              onValueChange={(value) => handleAnswerChange(question.id, value)}
            >
              {question.options.map((option) => (
                <div key={option.value} className="flex items-start space-x-3 p-4 border rounded-lg hover:bg-gray-50">
                  <RadioGroupItem value={option.value} id={option.value} className="mt-1" />
                  <div className="flex-1">
                    <Label htmlFor={option.value} className="text-base font-medium cursor-pointer">
                      {option.label}
                    </Label>
                    {option.description && (
                      <p className="text-sm text-gray-600 mt-1">{option.description}</p>
                    )}
                  </div>
                </div>
              ))}
            </RadioGroup>
          ) : (
            <div className="space-y-3">
              {question.maxSelections && (
                <p className="text-sm text-gray-600">
                  Selecione até {question.maxSelections} opções
                  {currentAnswer && ` (${currentAnswer.length}/${question.maxSelections} selecionadas)`}
                </p>
              )}
              {question.options.map((option) => (
                <div
                  key={option.value}
                  className={`flex items-center space-x-3 p-4 border rounded-lg cursor-pointer transition-colors ${
                    currentAnswer && currentAnswer.includes(option.value)
                      ? 'bg-blue-50 border-blue-200'
                      : 'hover:bg-gray-50'
                  }`}
                  onClick={() => handleAnswerChange(question.id, option.value, true)}
                >
                  <div className={`w-5 h-5 border-2 rounded flex items-center justify-center ${
                    currentAnswer && currentAnswer.includes(option.value)
                      ? 'bg-blue-600 border-blue-600'
                      : 'border-gray-300'
                  }`}>
                    {currentAnswer && currentAnswer.includes(option.value) && (
                      <CheckCircle className="w-3 h-3 text-white" />
                    )}
                  </div>
                  <Label className="text-base font-medium cursor-pointer flex-1">
                    {option.label}
                  </Label>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="flex justify-between mt-8">
        <Button
          variant="outline"
          onClick={currentQuestion === 0 ? onBack : handlePrevious}
          className="flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{currentQuestion === 0 ? 'Voltar' : 'Anterior'}</span>
        </Button>

        <Button
          onClick={handleNext}
          disabled={!canProceed()}
          className="flex items-center space-x-2"
        >
          <span>{currentQuestion === questions.length - 1 ? 'Finalizar' : 'Próxima'}</span>
          {currentQuestion === questions.length - 1 ? (
            <CheckCircle className="w-4 h-4" />
          ) : (
            <ArrowRight className="w-4 h-4" />
          )}
        </Button>
      </div>
    </div>
  )
}

export default QuizComponent


import numpy as np
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
from src.models.student import Student, GameSession, QuizResult

class AdaptiveLearningEngine:
    """
    Motor de IA adaptativa para personalizar a experiência de aprendizagem
    baseado no desempenho e perfil do estudante.
    """
    
    def __init__(self):
        # Pesos para diferentes fatores na adaptação
        self.performance_weight = 0.4
        self.time_weight = 0.3
        self.learning_style_weight = 0.2
        self.difficulty_progression_weight = 0.1
        
        # Configurações de dificuldade
        self.min_difficulty = 1
        self.max_difficulty = 10
        self.difficulty_step = 0.5
        
        # Tipos de jogos e suas características
        self.game_types = {
            'math': {
                'steam_elements': ['investigar', 'conectar', 'refletir'],
                'skills': ['logical_thinking', 'problem_solving', 'numerical_reasoning']
            },
            'logic': {
                'steam_elements': ['investigar', 'descobrir', 'refletir'],
                'skills': ['logical_thinking', 'pattern_recognition', 'critical_thinking']
            },
            'robotics': {
                'steam_elements': ['criar', 'conectar', 'investigar'],
                'skills': ['technical_skills', 'creativity', 'problem_solving']
            },
            'programming': {
                'steam_elements': ['criar', 'conectar', 'refletir'],
                'skills': ['technical_skills', 'logical_thinking', 'creativity']
            },
            'language': {
                'steam_elements': ['descobrir', 'conectar', 'refletir'],
                'skills': ['communication', 'creativity', 'cultural_awareness']
            },
            'science': {
                'steam_elements': ['investigar', 'descobrir', 'conectar'],
                'skills': ['scientific_thinking', 'observation', 'hypothesis_testing']
            }
        }
    
    def analyze_learning_profile(self, quiz_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa as respostas do quiz inicial para criar um perfil de aprendizagem.
        
        Args:
            quiz_answers: Dicionário com as respostas do quiz inicial
            
        Returns:
            Perfil de aprendizagem do estudante
        """
        profile = {
            'learning_style': self._determine_learning_style(quiz_answers),
            'interests': self._identify_interests(quiz_answers),
            'steam_preferences': self._analyze_steam_preferences(quiz_answers),
            'difficulty_preference': self._determine_difficulty_preference(quiz_answers),
            'motivation_factors': self._identify_motivation_factors(quiz_answers)
        }
        
        return profile
    
    def _determine_learning_style(self, answers: Dict[str, Any]) -> str:
        """Determina o estilo de aprendizagem predominante"""
        styles = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
            'reading_writing': 0
        }
        
        # Análise baseada nas respostas sobre preferências de aprendizagem
        if 'learning_preference' in answers:
            pref = answers['learning_preference']
            if 'visual' in pref or 'images' in pref or 'diagrams' in pref:
                styles['visual'] += 2
            if 'audio' in pref or 'listening' in pref or 'music' in pref:
                styles['auditory'] += 2
            if 'hands_on' in pref or 'practice' in pref or 'movement' in pref:
                styles['kinesthetic'] += 2
            if 'reading' in pref or 'writing' in pref or 'text' in pref:
                styles['reading_writing'] += 2
        
        # Análise baseada em atividades preferidas
        if 'favorite_activities' in answers:
            activities = answers['favorite_activities']
            if any(act in activities for act in ['drawing', 'watching', 'observing']):
                styles['visual'] += 1
            if any(act in activities for act in ['music', 'talking', 'listening']):
                styles['auditory'] += 1
            if any(act in activities for act in ['sports', 'building', 'experimenting']):
                styles['kinesthetic'] += 1
            if any(act in activities for act in ['reading', 'writing', 'researching']):
                styles['reading_writing'] += 1
        
        return max(styles, key=styles.get)
    
    def _identify_interests(self, answers: Dict[str, Any]) -> List[str]:
        """Identifica os principais interesses do estudante"""
        interests = []
        
        if 'subject_preferences' in answers:
            interests.extend(answers['subject_preferences'])
        
        if 'career_interests' in answers:
            career_mapping = {
                'engineer': ['math', 'science', 'robotics'],
                'artist': ['art', 'creativity', 'design'],
                'programmer': ['programming', 'logic', 'technology'],
                'teacher': ['communication', 'language', 'social'],
                'scientist': ['science', 'research', 'investigation']
            }
            
            for career in answers['career_interests']:
                if career in career_mapping:
                    interests.extend(career_mapping[career])
        
        return list(set(interests))
    
    def _analyze_steam_preferences(self, answers: Dict[str, Any]) -> Dict[str, float]:
        """Analisa as preferências relacionadas aos elementos STEAM"""
        steam_scores = {
            'investigar': 0.0,
            'descobrir': 0.0,
            'conectar': 0.0,
            'criar': 0.0,
            'refletir': 0.0
        }
        
        # Mapeamento de atividades para elementos STEAM
        activity_mapping = {
            'research': 'investigar',
            'explore': 'descobrir',
            'collaborate': 'conectar',
            'build': 'criar',
            'analyze': 'refletir',
            'experiment': 'investigar',
            'discover': 'descobrir',
            'connect': 'conectar',
            'create': 'criar',
            'think': 'refletir'
        }
        
        if 'preferred_activities' in answers:
            for activity in answers['preferred_activities']:
                for key, steam_element in activity_mapping.items():
                    if key in activity.lower():
                        steam_scores[steam_element] += 1.0
        
        # Normalizar scores
        total = sum(steam_scores.values())
        if total > 0:
            for element in steam_scores:
                steam_scores[element] /= total
        else:
            # Valores padrão se não houver dados suficientes
            for element in steam_scores:
                steam_scores[element] = 0.2
        
        return steam_scores
    
    def _determine_difficulty_preference(self, answers: Dict[str, Any]) -> str:
        """Determina a preferência de dificuldade inicial"""
        if 'challenge_preference' in answers:
            pref = answers['challenge_preference'].lower()
            if 'easy' in pref or 'simple' in pref:
                return 'low'
            elif 'hard' in pref or 'difficult' in pref or 'challenge' in pref:
                return 'high'
            else:
                return 'medium'
        return 'medium'
    
    def _identify_motivation_factors(self, answers: Dict[str, Any]) -> List[str]:
        """Identifica os fatores de motivação do estudante"""
        factors = []
        
        if 'motivation_sources' in answers:
            factors.extend(answers['motivation_sources'])
        
        # Fatores padrão baseados em gamificação
        default_factors = ['points', 'badges', 'progress', 'competition', 'collaboration']
        
        return list(set(factors + default_factors))
    
    def calculate_next_difficulty(self, student_id: int, game_type: str) -> float:
        """
        Calcula o próximo nível de dificuldade para um estudante em um tipo específico de jogo.
        
        Args:
            student_id: ID do estudante
            game_type: Tipo do jogo
            
        Returns:
            Nível de dificuldade recomendado (1.0 - 10.0)
        """
        # Buscar histórico de sessões do estudante
        recent_sessions = self._get_recent_sessions(student_id, game_type, limit=5)
        
        if not recent_sessions:
            # Primeira vez jogando - usar preferência do perfil
            student = Student.query.get(student_id)
            if student:
                profile = student.get_learning_profile()
                difficulty_pref = profile.get('difficulty_preference', 'medium')
                
                difficulty_map = {
                    'low': 2.0,
                    'medium': 4.0,
                    'high': 6.0
                }
                return difficulty_map.get(difficulty_pref, 4.0)
            return 4.0  # Dificuldade padrão
        
        # Analisar desempenho recente
        performance_score = self._calculate_performance_score(recent_sessions)
        time_efficiency = self._calculate_time_efficiency(recent_sessions)
        progression_rate = self._calculate_progression_rate(recent_sessions)
        
        # Calcular ajuste de dificuldade
        current_difficulty = recent_sessions[0].difficulty_level
        
        # Fator de ajuste baseado no desempenho
        performance_factor = (performance_score - 0.7) * 2  # -1.4 a 0.6
        time_factor = (time_efficiency - 0.5) * 1  # -0.5 a 0.5
        progression_factor = progression_rate * 0.5  # 0 a 0.5
        
        total_adjustment = (
            performance_factor * self.performance_weight +
            time_factor * self.time_weight +
            progression_factor * self.difficulty_progression_weight
        )
        
        # Aplicar ajuste
        new_difficulty = current_difficulty + (total_adjustment * self.difficulty_step)
        
        # Garantir que está dentro dos limites
        new_difficulty = max(self.min_difficulty, min(self.max_difficulty, new_difficulty))
        
        return round(new_difficulty, 1)
    
    def _get_recent_sessions(self, student_id: int, game_type: str, limit: int = 5) -> List[GameSession]:
        """Busca as sessões mais recentes de um estudante para um tipo de jogo"""
        return GameSession.query.filter_by(
            student_id=student_id,
            game_type=game_type
        ).order_by(GameSession.created_at.desc()).limit(limit).all()
    
    def _calculate_performance_score(self, sessions: List[GameSession]) -> float:
        """Calcula a pontuação média de desempenho"""
        if not sessions:
            return 0.5
        
        scores = [session.score for session in sessions]
        return np.mean(scores)
    
    def _calculate_time_efficiency(self, sessions: List[GameSession]) -> float:
        """Calcula a eficiência de tempo (menor tempo = maior eficiência)"""
        if not sessions:
            return 0.5
        
        times = [session.time_spent for session in sessions]
        avg_time = np.mean(times)
        
        # Normalizar baseado em tempos esperados por dificuldade
        expected_times = {i: 60 + (i * 30) for i in range(1, 11)}  # 60s a 360s
        
        avg_difficulty = np.mean([session.difficulty_level for session in sessions])
        expected_time = expected_times.get(int(avg_difficulty), 180)
        
        efficiency = max(0.1, min(1.0, expected_time / avg_time))
        return efficiency
    
    def _calculate_progression_rate(self, sessions: List[GameSession]) -> float:
        """Calcula a taxa de progressão do estudante"""
        if len(sessions) < 2:
            return 0.0
        
        # Ordenar por data (mais antiga primeiro)
        sorted_sessions = sorted(sessions, key=lambda x: x.created_at)
        
        # Calcular melhoria na pontuação
        first_scores = [s.score for s in sorted_sessions[:len(sorted_sessions)//2]]
        last_scores = [s.score for s in sorted_sessions[len(sorted_sessions)//2:]]
        
        if first_scores and last_scores:
            improvement = np.mean(last_scores) - np.mean(first_scores)
            return max(0.0, improvement)
        
        return 0.0
    
    def recommend_games(self, student_id: int, num_recommendations: int = 3) -> List[Dict[str, Any]]:
        """
        Recomenda jogos para um estudante baseado em seu perfil e desempenho.
        
        Args:
            student_id: ID do estudante
            num_recommendations: Número de recomendações a retornar
            
        Returns:
            Lista de recomendações de jogos
        """
        student = Student.query.get(student_id)
        if not student:
            return []
        
        profile = student.get_learning_profile()
        interests = profile.get('interests', [])
        steam_preferences = profile.get('steam_preferences', {})
        
        recommendations = []
        
        for game_type, game_info in self.game_types.items():
            # Calcular score de compatibilidade
            compatibility_score = self._calculate_game_compatibility(
                game_type, game_info, interests, steam_preferences
            )
            
            # Calcular dificuldade recomendada
            difficulty = self.calculate_next_difficulty(student_id, game_type)
            
            recommendations.append({
                'game_type': game_type,
                'difficulty_level': difficulty,
                'compatibility_score': compatibility_score,
                'steam_elements': game_info['steam_elements'],
                'skills': game_info['skills']
            })
        
        # Ordenar por score de compatibilidade
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return recommendations[:num_recommendations]
    
    def _calculate_game_compatibility(self, game_type: str, game_info: Dict, 
                                    interests: List[str], steam_preferences: Dict[str, float]) -> float:
        """Calcula o score de compatibilidade entre um jogo e o perfil do estudante"""
        score = 0.0
        
        # Score baseado em interesses
        interest_matches = sum(1 for interest in interests if interest in game_info['skills'])
        score += interest_matches * 0.3
        
        # Score baseado em preferências STEAM
        steam_score = sum(steam_preferences.get(element, 0) for element in game_info['steam_elements'])
        score += steam_score * 0.7
        
        return score
    
    def generate_feedback(self, session: GameSession) -> Dict[str, Any]:
        """
        Gera feedback personalizado para uma sessão de jogo.
        
        Args:
            session: Sessão de jogo concluída
            
        Returns:
            Feedback personalizado
        """
        student = Student.query.get(session.student_id)
        profile = student.get_learning_profile() if student else {}
        
        feedback = {
            'performance_level': self._assess_performance_level(session.score),
            'time_assessment': self._assess_time_performance(session.time_spent, session.difficulty_level),
            'strengths': self._identify_strengths(session, profile),
            'improvement_areas': self._identify_improvement_areas(session, profile),
            'next_steps': self._suggest_next_steps(session, profile),
            'motivational_message': self._generate_motivational_message(session, profile)
        }
        
        return feedback
    
    def _assess_performance_level(self, score: float) -> str:
        """Avalia o nível de desempenho baseado na pontuação"""
        if score >= 0.9:
            return 'excellent'
        elif score >= 0.7:
            return 'good'
        elif score >= 0.5:
            return 'satisfactory'
        else:
            return 'needs_improvement'
    
    def _assess_time_performance(self, time_spent: int, difficulty: int) -> str:
        """Avalia o desempenho de tempo"""
        expected_time = 60 + (difficulty * 30)  # Tempo esperado baseado na dificuldade
        
        if time_spent <= expected_time * 0.8:
            return 'fast'
        elif time_spent <= expected_time * 1.2:
            return 'optimal'
        else:
            return 'slow'
    
    def _identify_strengths(self, session: GameSession, profile: Dict) -> List[str]:
        """Identifica pontos fortes baseados na sessão"""
        strengths = []
        
        if session.score >= 0.8:
            strengths.append('high_accuracy')
        
        expected_time = 60 + (session.difficulty_level * 30)
        if session.time_spent <= expected_time * 0.9:
            strengths.append('quick_thinking')
        
        if session.completed:
            strengths.append('persistence')
        
        return strengths
    
    def _identify_improvement_areas(self, session: GameSession, profile: Dict) -> List[str]:
        """Identifica áreas de melhoria"""
        areas = []
        
        if session.score < 0.6:
            areas.append('accuracy')
        
        expected_time = 60 + (session.difficulty_level * 30)
        if session.time_spent > expected_time * 1.5:
            areas.append('speed')
        
        if not session.completed:
            areas.append('persistence')
        
        return areas
    
    def _suggest_next_steps(self, session: GameSession, profile: Dict) -> List[str]:
        """Sugere próximos passos para o estudante"""
        suggestions = []
        
        if session.score >= 0.8:
            suggestions.append('try_harder_level')
        elif session.score < 0.5:
            suggestions.append('practice_fundamentals')
        else:
            suggestions.append('continue_current_level')
        
        # Sugestões baseadas no perfil STEAM
        steam_prefs = profile.get('steam_preferences', {})
        top_steam = max(steam_prefs, key=steam_prefs.get) if steam_prefs else 'investigar'
        
        suggestions.append(f'explore_{top_steam}_activities')
        
        return suggestions
    
    def _generate_motivational_message(self, session: GameSession, profile: Dict) -> str:
        """Gera uma mensagem motivacional personalizada"""
        motivation_factors = profile.get('motivation_factors', ['progress'])
        
        if session.score >= 0.8:
            messages = [
                "Excelente trabalho! Você está dominando este desafio!",
                "Parabéns! Sua dedicação está dando resultados incríveis!",
                "Fantástico! Continue assim e você chegará ainda mais longe!"
            ]
        elif session.score >= 0.6:
            messages = [
                "Bom trabalho! Você está no caminho certo!",
                "Continue praticando, você está melhorando!",
                "Ótimo progresso! Cada tentativa te deixa mais forte!"
            ]
        else:
            messages = [
                "Não desista! Cada erro é uma oportunidade de aprender!",
                "Continue tentando! O sucesso vem com a prática!",
                "Você consegue! Acredite no seu potencial!"
            ]
        
        import random
        return random.choice(messages)


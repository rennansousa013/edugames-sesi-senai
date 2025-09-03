from flask import Blueprint, request, jsonify
from src.models.student import db, Student, GameSession, QuizResult
from src.ai_engine import AdaptiveLearningEngine
from datetime import datetime

ai_bp = Blueprint('ai', __name__)
ai_engine = AdaptiveLearningEngine()

@ai_bp.route('/analyze-quiz', methods=['POST'])
def analyze_quiz():
    """
    Analisa as respostas do quiz inicial e cria o perfil de aprendizagem do estudante.
    """
    try:
        data = request.get_json()
        
        if not data or 'student_id' not in data or 'quiz_answers' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        student_id = data['student_id']
        quiz_answers = data['quiz_answers']
        
        # Buscar o estudante
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Analisar o perfil de aprendizagem
        learning_profile = ai_engine.analyze_learning_profile(quiz_answers)
        
        # Atualizar o perfil do estudante
        student.set_learning_profile(learning_profile)
        
        # Salvar resultado do quiz
        quiz_result = QuizResult(
            student_id=student_id,
            quiz_type='initial_profile',
            answers=quiz_answers,
            results=learning_profile
        )
        quiz_result.set_answers(quiz_answers)
        quiz_result.set_results(learning_profile)
        
        db.session.add(quiz_result)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'learning_profile': learning_profile,
            'message': 'Perfil de aprendizagem criado com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/recommend-difficulty', methods=['POST'])
def recommend_difficulty():
    """
    Recomenda o próximo nível de dificuldade para um estudante em um tipo específico de jogo.
    """
    try:
        data = request.get_json()
        
        if not data or 'student_id' not in data or 'game_type' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        student_id = data['student_id']
        game_type = data['game_type']
        
        # Verificar se o estudante existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Calcular dificuldade recomendada
        recommended_difficulty = ai_engine.calculate_next_difficulty(student_id, game_type)
        
        return jsonify({
            'success': True,
            'recommended_difficulty': recommended_difficulty,
            'game_type': game_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/recommend-games', methods=['POST'])
def recommend_games():
    """
    Recomenda jogos para um estudante baseado em seu perfil e desempenho.
    """
    try:
        data = request.get_json()
        
        if not data or 'student_id' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        student_id = data['student_id']
        num_recommendations = data.get('num_recommendations', 3)
        
        # Verificar se o estudante existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Gerar recomendações
        recommendations = ai_engine.recommend_games(student_id, num_recommendations)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/record-session', methods=['POST'])
def record_session():
    """
    Registra uma sessão de jogo e gera feedback personalizado.
    """
    try:
        data = request.get_json()
        
        required_fields = ['student_id', 'game_type', 'difficulty_level', 'score', 'time_spent']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Criar nova sessão de jogo
        session = GameSession(
            student_id=data['student_id'],
            game_type=data['game_type'],
            difficulty_level=data['difficulty_level'],
            score=data['score'],
            time_spent=data['time_spent'],
            completed=data.get('completed', True),
            session_data=data.get('session_data', {})
        )
        
        if 'session_data' in data:
            session.set_session_data(data['session_data'])
        
        db.session.add(session)
        db.session.commit()
        
        # Gerar feedback personalizado
        feedback = ai_engine.generate_feedback(session)
        
        # Calcular próxima dificuldade recomendada
        next_difficulty = ai_engine.calculate_next_difficulty(
            data['student_id'], 
            data['game_type']
        )
        
        return jsonify({
            'success': True,
            'session_id': session.id,
            'feedback': feedback,
            'next_difficulty': next_difficulty,
            'message': 'Sessão registrada com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/student-progress/<int:student_id>', methods=['GET'])
def get_student_progress(student_id):
    """
    Retorna o progresso detalhado de um estudante.
    """
    try:
        # Verificar se o estudante existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Buscar todas as sessões do estudante
        sessions = GameSession.query.filter_by(student_id=student_id).order_by(
            GameSession.created_at.desc()
        ).all()
        
        # Agrupar sessões por tipo de jogo
        progress_by_game = {}
        for session in sessions:
            game_type = session.game_type
            if game_type not in progress_by_game:
                progress_by_game[game_type] = {
                    'sessions': [],
                    'avg_score': 0,
                    'avg_difficulty': 0,
                    'total_time': 0,
                    'completion_rate': 0
                }
            
            progress_by_game[game_type]['sessions'].append(session.to_dict())
        
        # Calcular estatísticas
        for game_type, data in progress_by_game.items():
            game_sessions = [s for s in sessions if s.game_type == game_type]
            
            if game_sessions:
                data['avg_score'] = sum(s.score for s in game_sessions) / len(game_sessions)
                data['avg_difficulty'] = sum(s.difficulty_level for s in game_sessions) / len(game_sessions)
                data['total_time'] = sum(s.time_spent for s in game_sessions)
                data['completion_rate'] = sum(1 for s in game_sessions if s.completed) / len(game_sessions)
        
        # Buscar perfil de aprendizagem
        learning_profile = student.get_learning_profile()
        
        return jsonify({
            'success': True,
            'student': student.to_dict(),
            'learning_profile': learning_profile,
            'progress_by_game': progress_by_game,
            'total_sessions': len(sessions)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/adaptive-feedback', methods=['POST'])
def get_adaptive_feedback():
    """
    Gera feedback adaptativo baseado no desempenho recente do estudante.
    """
    try:
        data = request.get_json()
        
        if not data or 'student_id' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        student_id = data['student_id']
        game_type = data.get('game_type')
        
        # Verificar se o estudante existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Buscar sessões recentes
        query = GameSession.query.filter_by(student_id=student_id)
        if game_type:
            query = query.filter_by(game_type=game_type)
        
        recent_sessions = query.order_by(GameSession.created_at.desc()).limit(5).all()
        
        if not recent_sessions:
            return jsonify({
                'success': True,
                'feedback': {
                    'message': 'Comece jogando para receber feedback personalizado!',
                    'recommendations': ['Experimente diferentes tipos de jogos', 'Explore suas áreas de interesse']
                }
            })
        
        # Gerar feedback para a sessão mais recente
        latest_session = recent_sessions[0]
        feedback = ai_engine.generate_feedback(latest_session)
        
        # Adicionar recomendações de jogos
        game_recommendations = ai_engine.recommend_games(student_id, 3)
        
        return jsonify({
            'success': True,
            'feedback': feedback,
            'game_recommendations': game_recommendations,
            'recent_performance': {
                'avg_score': sum(s.score for s in recent_sessions) / len(recent_sessions),
                'sessions_count': len(recent_sessions),
                'improvement_trend': 'improving' if len(recent_sessions) > 1 and 
                                   recent_sessions[0].score > recent_sessions[-1].score else 'stable'
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/learning-analytics/<int:student_id>', methods=['GET'])
def get_learning_analytics(student_id):
    """
    Retorna análises detalhadas de aprendizagem para um estudante.
    """
    try:
        # Verificar se o estudante existe
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Estudante não encontrado'}), 404
        
        # Buscar todas as sessões
        sessions = GameSession.query.filter_by(student_id=student_id).order_by(
            GameSession.created_at.asc()
        ).all()
        
        if not sessions:
            return jsonify({
                'success': True,
                'analytics': {
                    'message': 'Nenhuma sessão encontrada para análise',
                    'total_sessions': 0
                }
            })
        
        # Análises por período
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        recent_sessions = [s for s in sessions if s.created_at >= week_ago]
        monthly_sessions = [s for s in sessions if s.created_at >= month_ago]
        
        # Análises de desempenho
        analytics = {
            'total_sessions': len(sessions),
            'recent_sessions': len(recent_sessions),
            'monthly_sessions': len(monthly_sessions),
            'overall_performance': {
                'avg_score': sum(s.score for s in sessions) / len(sessions),
                'avg_difficulty': sum(s.difficulty_level for s in sessions) / len(sessions),
                'total_time_hours': sum(s.time_spent for s in sessions) / 3600,
                'completion_rate': sum(1 for s in sessions if s.completed) / len(sessions)
            },
            'recent_performance': {},
            'game_type_analysis': {},
            'learning_trends': {},
            'steam_engagement': {}
        }
        
        # Análise de desempenho recente
        if recent_sessions:
            analytics['recent_performance'] = {
                'avg_score': sum(s.score for s in recent_sessions) / len(recent_sessions),
                'avg_difficulty': sum(s.difficulty_level for s in recent_sessions) / len(recent_sessions),
                'improvement': 'improving' if len(recent_sessions) > 1 and 
                              recent_sessions[-1].score > recent_sessions[0].score else 'stable'
            }
        
        # Análise por tipo de jogo
        game_types = set(s.game_type for s in sessions)
        for game_type in game_types:
            game_sessions = [s for s in sessions if s.game_type == game_type]
            analytics['game_type_analysis'][game_type] = {
                'sessions_count': len(game_sessions),
                'avg_score': sum(s.score for s in game_sessions) / len(game_sessions),
                'avg_difficulty': sum(s.difficulty_level for s in game_sessions) / len(game_sessions),
                'total_time': sum(s.time_spent for s in game_sessions),
                'last_played': max(s.created_at for s in game_sessions).isoformat()
            }
        
        # Tendências de aprendizagem
        if len(sessions) >= 5:
            # Dividir sessões em grupos para análise de tendência
            mid_point = len(sessions) // 2
            early_sessions = sessions[:mid_point]
            later_sessions = sessions[mid_point:]
            
            early_avg = sum(s.score for s in early_sessions) / len(early_sessions)
            later_avg = sum(s.score for s in later_sessions) / len(later_sessions)
            
            analytics['learning_trends'] = {
                'score_improvement': later_avg - early_avg,
                'trend': 'improving' if later_avg > early_avg else 'declining' if later_avg < early_avg else 'stable',
                'consistency': 'high' if abs(later_avg - early_avg) < 0.1 else 'moderate' if abs(later_avg - early_avg) < 0.3 else 'variable'
            }
        
        # Análise de engajamento STEAM
        profile = student.get_learning_profile()
        steam_prefs = profile.get('steam_preferences', {})
        
        if steam_prefs:
            # Mapear tipos de jogos para elementos STEAM
            steam_mapping = ai_engine.game_types
            steam_engagement = {element: 0 for element in steam_prefs.keys()}
            
            for session in sessions:
                game_info = steam_mapping.get(session.game_type, {})
                steam_elements = game_info.get('steam_elements', [])
                
                for element in steam_elements:
                    if element in steam_engagement:
                        steam_engagement[element] += session.score
            
            # Normalizar por número de sessões
            for element in steam_engagement:
                relevant_sessions = [s for s in sessions 
                                   if element in steam_mapping.get(s.game_type, {}).get('steam_elements', [])]
                if relevant_sessions:
                    steam_engagement[element] /= len(relevant_sessions)
            
            analytics['steam_engagement'] = steam_engagement
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


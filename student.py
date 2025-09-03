from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    grade_level = db.Column(db.String(20), nullable=False)  # Ex: "6º ano", "7º ano", etc.
    learning_profile = db.Column(db.Text)  # JSON string com perfil de aprendizagem
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    game_sessions = db.relationship('GameSession', backref='student', lazy=True)
    quiz_results = db.relationship('QuizResult', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name}>'
    
    def get_learning_profile(self):
        """Retorna o perfil de aprendizagem como dicionário"""
        if self.learning_profile:
            return json.loads(self.learning_profile)
        return {}
    
    def set_learning_profile(self, profile_dict):
        """Define o perfil de aprendizagem a partir de um dicionário"""
        self.learning_profile = json.dumps(profile_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'grade_level': self.grade_level,
            'learning_profile': self.get_learning_profile(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class GameSession(db.Model):
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # Ex: "math", "logic", "robotics"
    difficulty_level = db.Column(db.Integer, nullable=False)  # 1-10
    score = db.Column(db.Float, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)  # em segundos
    completed = db.Column(db.Boolean, default=False)
    session_data = db.Column(db.Text)  # JSON com dados específicos da sessão
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GameSession {self.game_type} - Level {self.difficulty_level}>'
    
    def get_session_data(self):
        """Retorna os dados da sessão como dicionário"""
        if self.session_data:
            return json.loads(self.session_data)
        return {}
    
    def set_session_data(self, data_dict):
        """Define os dados da sessão a partir de um dicionário"""
        self.session_data = json.dumps(data_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'game_type': self.game_type,
            'difficulty_level': self.difficulty_level,
            'score': self.score,
            'time_spent': self.time_spent,
            'completed': self.completed,
            'session_data': self.get_session_data(),
            'created_at': self.created_at.isoformat()
        }

class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    quiz_type = db.Column(db.String(50), nullable=False)  # Ex: "initial_profile", "subject_assessment"
    answers = db.Column(db.Text, nullable=False)  # JSON com respostas
    results = db.Column(db.Text, nullable=False)  # JSON com resultados processados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizResult {self.quiz_type} for Student {self.student_id}>'
    
    def get_answers(self):
        """Retorna as respostas como dicionário"""
        return json.loads(self.answers)
    
    def set_answers(self, answers_dict):
        """Define as respostas a partir de um dicionário"""
        self.answers = json.dumps(answers_dict)
    
    def get_results(self):
        """Retorna os resultados como dicionário"""
        return json.loads(self.results)
    
    def set_results(self, results_dict):
        """Define os resultados a partir de um dicionário"""
        self.results = json.dumps(results_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'quiz_type': self.quiz_type,
            'answers': self.get_answers(),
            'results': self.get_results(),
            'created_at': self.created_at.isoformat()
        }


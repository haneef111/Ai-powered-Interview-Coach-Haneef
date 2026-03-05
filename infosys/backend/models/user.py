from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, email, password_hash, name, job_role=None, industry=None):
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.job_role = job_role
        self.industry = industry
        self.created_at = datetime.utcnow()
        self.interviews = []
    
    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'job_role': self.job_role,
            'industry': self.industry,
            'created_at': self.created_at,
            'interviews': self.interviews
        }
    
    @staticmethod
    def from_dict(data):
        user = User(
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            name=data.get('name'),
            job_role=data.get('job_role'),
            industry=data.get('industry')
        )
        if 'created_at' in data:
            user.created_at = data['created_at']
        if 'interviews' in data:
            user.interviews = data['interviews']
        return user

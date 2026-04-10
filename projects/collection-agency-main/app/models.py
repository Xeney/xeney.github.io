from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
import os

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator')  # admin, manager, operator
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # мягкое удаление

    # Relationships (явные back_populates, чтобы избежать конфликтов)
    interactions = db.relationship('Interaction', back_populates='user', lazy='dynamic')
    uploaded_documents = db.relationship('Document', back_populates='uploader', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can_manage_users(self):
        return self.role == 'admin'
    
    def can_edit_debtors(self):
        return self.role in ['admin', 'manager']
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class Debtor(db.Model):
    __tablename__ = 'debtor'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    passport_data = db.Column(db.String(300), nullable=True)
    contract_number = db.Column(db.String(100), unique=True, nullable=False)
    debt_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    bank_name = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, server_default='active')

    interactions = db.relationship(
        'Interaction',
        back_populates='debtor',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    documents = db.relationship(
        'Document',
        back_populates='debtor',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<Debtor id={self.id} name={self.full_name}>"

class Interaction(db.Model):
    __tablename__ = 'interaction'
    id = db.Column(db.Integer, primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('debtor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interaction_type = db.Column(db.String(20), nullable=False)  # call, sms, email, meeting
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    debtor = db.relationship('Debtor', back_populates='interactions', lazy='joined')
    user = db.relationship('User', back_populates='interactions', lazy='joined')

    def __repr__(self):
        return f'<Interaction {self.interaction_type} with {self.debtor_id} by {self.user_id}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('debtor.id', ondelete='CASCADE'), nullable=False, index=True)
    filename_original = db.Column(db.String(512), nullable=False)
    filename_disk = db.Column(db.String(512), nullable=False)
    content_type = db.Column(db.String(128), nullable=True)
    size = db.Column(db.BigInteger, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # связи (явные back_populates)
    debtor = db.relationship('Debtor', back_populates='documents')
    uploader = db.relationship('User', back_populates='uploaded_documents')

    def file_path(self, upload_folder):
        return os.path.join(upload_folder, f"debtors_{self.debtor_id}", self.filename_disk)

    def __repr__(self):
        return f"<Document id={self.id} debtor={self.debtor_id} original={self.filename_original}>"
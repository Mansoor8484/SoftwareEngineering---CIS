from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import bcrypt

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("ChatbotInteraction", back_populates="user", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")  # Corrected Reminder relationship
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

    # Methods
    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Validates the provided password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        """String representation of the User object."""
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    balance = Column(Float, default=0.00)

    user = relationship("User", back_populates="bank_accounts")

    def __repr__(self):
        return f"<BankAccount(id={self.id}, account_name={self.account_name}, balance={self.balance})>"

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, server_default=func.now())
    transaction_type = Column(String, nullable=False)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return (f"<Transaction(id={self.id}, user_id={self.user_id}, "
                f"amount={self.amount}, transaction_date={self.transaction_date}, "
                f"transaction_type={self.transaction_type})>")

class ChatbotInteraction(db.Model):
    __tablename__ = 'chatbot_interactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    interaction_date = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="interactions")

    def __repr__(self):
        return (f"<ChatbotInteraction(id={self.id}, user_id={self.user_id}, "
                f"message={self.message}, response={self.response}, "
                f"interaction_date={self.interaction_date})>")

class Reminder(db.Model):
    __tablename__ = 'reminders'

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference to the User model
    date = Column(DateTime, nullable=False)  # Store the date and time of the reminder
    text = Column(String(255), nullable=False)  # The reminder text

    # Relationships
    user = relationship("User", back_populates="reminders")  # Matches the User model relationship

    # Methods
    def __repr__(self):
        """String representation of the Reminder object."""
        return f"<Reminder(id={self.id}, date={self.date}, text={self.text})>"

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship('User', back_populates='budgets')  # Updated to match the User relationship

    def __repr__(self):
        return f'<Budget {self.category} for User {self.user_id}>'

class Message(db.Model):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message_type = Column(String(50), nullable=False)  # Type of message: Request, Complaint, etc.
    content = Column(Text, nullable=False)  # The actual message content
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp for when the message was sent

    user = relationship('User', back_populates='messages')  # Relationship to the User model

    def __repr__(self):
        return f'<Message {self.id} from User {self.user_id}>'

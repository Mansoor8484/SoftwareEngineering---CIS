from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import bcrypt

base = declarative_base()

class User(base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_At = Column(DateTime, server_default=func.now())

    transactions = relationship("Transaction", back_populates="user")
    interactions = relationship("Interaction", back_populates="user")
    bank_accounts = relationship("BankAccount", back_populates="user")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class BankAccount(base):

    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    account_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    balance = Column(Float, default=0.00)

    user = relationship("User", back_populates="bank_accounts")

    def __repr__(self):
        return f"<BankAccount(id={self.id}, account_name={self.account_name}, balance={self.balance})>"

class Transactions(base):
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

class ChatbotInteraction(base):
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

# engine = create_engine('sqlite:///your_database.db')
# base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
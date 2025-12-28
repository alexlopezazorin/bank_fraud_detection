"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from .user import User
from bank_system.logging_config import get_logger

logger = get_logger(__name__)

class Bank:
    
    
    def __init__(self,analyst):
        self.users=[]
        self.transactions=[]
        self.analyst=analyst
        
    def create_user(self,name):
        user = User(name,self)
        self.users.append(user.user_id)
        return user
        
    def call_analyst(self,transaction):
        logger.info(f"Sending transaction to analyst | transaction_id={transaction.transaction_id}")
        if (self.analyst.analyze_transaction(transaction)):
            self.process_transaction(transaction)
            self.log_transaction(transaction)
            return 'Transaction was done'
        else:
            return 'Transaction was detected as Fraud'
    
    def process_transaction(self,transaction):
        transaction.sender.balance-=transaction.amount
        transaction.receiver.balance += transaction.amount
    
    
    def log_transaction(self,transaction):
        logger.debug(f"Transaction logged | transaction_id={transaction.transaction_id}")
        self.transactions.append(transaction.transaction_id)
        
    
"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from .transaction import Transaction
from bank_system.logging_config import get_logger

logger = get_logger(__name__)

class User:
    
    _id_counter = 1 
    
    def __init__(self,name,bank):
        
        self.user_id = User._id_counter  #asigna el id único
        User._id_counter += 1 #incrementa el contador
        
        self.name=name
        self.bank=bank
        self.balance=0.0
        self.transaction_history=[]
        logger.info(f"user={self.name} was created")
    
    
    def consult_balance(self):
        return self.balance
    
    
    def deposit(self, amount):
        if amount<=0:
            raise ValueError('Can not deposit a negative amount')
        
        self.balance += amount
        logger.info(f"Deposit | user={self.name} | amount={amount}€ | new_balance={self.balance}€")
        return self.balance
    
    
    
    def withdraw(self, amount):
        if amount<=0:
            raise ValueError('Can not withdraw a negative amount')
        
        if self.balance<amount:
            raise ValueError('Insufficient funds')
        
        self.balance -= amount
        logger.info(f"Withdraw | user={self.name} | amount={amount}€ | new_balance={self.balance}€")
        return self.balance
    
    
    
    def transfer(self, receiver, amount, concept):
        if amount<=0:
            raise ValueError('Can not withdraw a negative amount')
        
        if self.balance<amount:
            raise ValueError('Insufficient funds')
        
        logger.info(
            f"Transfer initiated | from={self.name} | to={receiver.name} "
            f"| amount={amount}€ | concept='{concept}'"
        )
        
        transaction=Transaction(self, receiver, amount, concept, "pending")
        
        x = self.bank.call_analyst(transaction)
        if x =='Transaction was done':
            self.log_transaction(transaction)
            logger.info(f"Transfer completed | from={self.name} | to={receiver.name} | amount={amount}€")
            return True
        else:
            logger.warning(f"Transfer not completed | from={self.name} | to={receiver.name} | amount={amount}€")
            return False

        
    
    def log_transaction(self,transaction):
        self.transaction_history.append(transaction.transaction_id)
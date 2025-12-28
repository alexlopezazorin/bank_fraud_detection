"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from bank_system.logging_config import get_logger
from datetime import datetime

logger = get_logger(__name__)

class Transaction:
    
    _id_counter = 1 
    
    def __init__(self, sender, receiver, amount, concept, status):
        
        self.transaction_id = Transaction._id_counter  #asigna el id único
        Transaction._id_counter += 1 #incrementa el contador
        
        self.sender=sender
        self.receiver=receiver
        self.amount=amount
        self.concept=concept
        self.status=status
        
        self.local_time = datetime.now().time()
        
        
        logger.info(
            f"Transaction created | "
            f"{self.sender.name} → {self.receiver.name} | "
            f"{self.amount}€ | concept='{self.concept}'"
        )

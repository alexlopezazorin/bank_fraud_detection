"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
from ML.predict import model_analyzes_transaction
from bank_system.logging_config import get_logger

logger = get_logger(__name__)

class Analyst:
    
    def __init__(self):
        pass
    
    def model_predict_only(self, amount, concept, local_time):#esta funcion se usa solo para el API, eliminamos el input() para automatizar la respuesta del API
        p_fraud, is_fraud = model_analyzes_transaction(amount, concept, local_time)
        logger.info(
            f"API prediction | amount={amount} | concept='{concept}' "
            f"| p_fraud={p_fraud:.2f} | is_fraud={is_fraud}"
        )
        
        return p_fraud, is_fraud
    
    def analyze_transaction(self, transaction):
        """
        Devuelve True si la transacción es segura, False si es fraude.
        Llama a la función model_analyzes_transaction del pipeline ML.
        """
        
        p_fraud, is_fraud = self.model_predict_only(transaction.amount, transaction.concept, transaction.local_time)

        
        if transaction.status=="pending":
             
            if is_fraud == 1:
                
                logger.warning(
                    f"Manual review required | transaction_id={transaction.transaction_id} "
                    f"| p_fraud={p_fraud:.2f}"
                )
                
                x=str(input('Introduce "SAFE" for allowing the transaction and "FRAUD" for blocking the transaction: '))
                
                if x=="SAFE":
                    transaction.status="approved"
                    logger.info(f"Transaction manually approved | transaction_id={transaction.transaction_id}")
                    return True
                
                else:
                    if x=="FRAUD":
                        transaction.status="blocked"
                        logger.info(f"Transaction manually blocked | transaction_id={transaction.transaction_id}")
                        return False
                    else:
                        raise ValueError('Analyst can only introduce "SAFE" or "FRAUD" for classifying transactions')
            
            else:
                transaction.status = "approved"
                return True
               
            
            


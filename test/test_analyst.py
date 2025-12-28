"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pytest
from bank_system.transaction import Transaction
from bank_system.user import User
from bank_system.bank import Bank
from bank_system.analyst import Analyst

class Test_Analyst():
    
    def test_analyst_approves_safe_transaction(self,monkeypatch):
        analista1 = Analyst()
        Santander = Bank(analista1)
        Pepe = User('Pepe',Santander)
        Manolo = User('Manolo',Santander)
        
        transaction = Transaction(Pepe, Manolo, 500, 'Urgent', 'pending')
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.12, 0) # SAFE
        )
        
        # Simulamos que el analista escribe 'SAFE'
        monkeypatch.setattr('builtins.input', lambda _: 'SAFE')
        
        result = analista1.analyze_transaction(transaction)
        
        assert result is True
        assert transaction.status == 'approved'
    
    
    
    def test_analyst_blocks_fraud_transaction(self,monkeypatch):
        analista1 = Analyst()
        Santander = Bank(analista1)
        Pepe = User('Pepe',Santander)
        Manolo = User('Manolo',Santander)
        
        transaction = Transaction(Pepe, Manolo, 500, 'Urgent crypto', 'pending')
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.95, 1) # FRAUD
        )
        
        # Simulamos que el analista escribe 'FRAUD'
        monkeypatch.setattr('builtins.input', lambda _: 'FRAUD')
        
        result = analista1.analyze_transaction(transaction)
        
        assert result is False
        assert transaction.status == 'blocked'
        
        
        
    def test_analyst_inputs_invalid_classification(self,monkeypatch):
        analista1 = Analyst()
        Santander = Bank(analista1)
        Pepe = User('Pepe',Santander)
        Manolo = User('Manolo',Santander)
        
        transaction = Transaction(Pepe, Manolo, 500, 'Urgent crypto', 'pending')
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.95, 1) # FRAUD
        )
        
        # Simulamos que el analista escribe 'INVALID'
        monkeypatch.setattr('builtins.input', lambda _: 'INVALID')
        
        with pytest.raises(ValueError, match='Analyst can only introduce "SAFE" or "FRAUD" for classifying transactions'):
            analista1.analyze_transaction(transaction)
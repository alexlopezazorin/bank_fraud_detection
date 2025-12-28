"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pytest
from bank_system.transaction import Transaction
from bank_system.user import User
from bank_system.bank import Bank
from bank_system.analyst import Analyst

class Test_Transaction():
    
    def test_transaction_creation(self):
        
        analista1 = Analyst()
        Santander = Bank(analista1)
        Pepe = User('Pepe',Santander)
        Manolo = User('Manolo',Santander)
        
        transaction = Transaction(Pepe, Manolo, 500, 'Rent', 'pending')
        
        assert transaction.sender == Pepe
        assert transaction.receiver == Manolo
        assert transaction.amount == 500
        assert transaction.concept == 'Rent'
        assert transaction.status == 'pending'
        assert isinstance(transaction.transaction_id, int)


    def test_transaction_id_is_unique(self):
        
        analista1 = Analyst()
        Santander = Bank(analista1)
        Pepe = User('Pepe',Santander)
        Manolo = User('Manolo',Santander)
        
        transaction_1 = Transaction(sender=Pepe, receiver=Manolo, amount=500, concept='Rent', status='pending')
        transaction_2 = Transaction(sender=Pepe, receiver=Manolo, amount=500, concept='Rent', status='pending')

        assert transaction_1.transaction_id != transaction_2.transaction_id
        assert transaction_2.transaction_id == transaction_1.transaction_id + 1

"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pytest
from bank_system.user import User
from bank_system.bank import Bank
from bank_system.analyst import Analyst

class Test_Integration_Bank_Flow():

    def test_full_bank_transaction_flow_safe(self,monkeypatch):
        """
        Simula el flujo completo:
        User -> Bank -> Analyst (IA) -> Bank -> User
        """
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.12, 0) # SAFE
        )

        analyst = Analyst()
        bank = Bank(analyst)

        alice = User("Alice", bank)
        bob = User("Bob", bank)

        alice.deposit(1000)

        result = alice.transfer(bob, 200, "Urgent crypto investment")

        assert result is True
        assert alice.balance == 800
        assert bob.balance == 200
        assert len(bank.transactions) == 1
        assert len(alice.transaction_history) == 1


    def test_full_bank_transaction_flow_fraud_blocked(self,monkeypatch):
        """
        Mismo flujo, pero la IA detecta fraude y el anaista la bloquea
        """

        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.95, 1) # FRAUD
        )
        
        # Simulamos que el analista escribe 'FRAUD'
        monkeypatch.setattr('builtins.input', lambda _: 'FRAUD')

        analyst = Analyst()
        bank = Bank(analyst)

        alice = User("Alice", bank)
        bob = User("Bob", bank)

        alice.deposit(1000)

        result = alice.transfer(bob, 200, "Urgent crypto investment")

        assert result is False
        assert alice.balance == 1000
        assert bob.balance == 0
        assert len(bank.transactions) == 0
        assert len(alice.transaction_history) == 0
        
    def test_full_bank_transaction_flow_fraud_approved(self,monkeypatch):
        """
        Mismo flujo, pero la IA detecta fraude y el analista la permite
        """

        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.95, 1) # FRAUD
        )
        
        # Simulamos que el analista escribe 'SAFE'
        monkeypatch.setattr('builtins.input', lambda _: 'SAFE')

        analyst = Analyst()
        bank = Bank(analyst)

        alice = User("Alice", bank)
        bob = User("Bob", bank)

        alice.deposit(1000)

        result = alice.transfer(bob, 200, "Urgent crypto investment")

        assert result is True
        assert alice.balance == 800
        assert bob.balance == 200
        assert len(bank.transactions) == 1
        assert len(alice.transaction_history) == 1

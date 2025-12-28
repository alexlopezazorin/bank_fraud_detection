"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pytest
from bank_system.bank import Bank
from bank_system.user import User
from bank_system.transaction import Transaction
from bank_system.analyst import Analyst

@pytest.fixture
def bank_creation():
    analist = Analyst()
    return Bank(analist)

class Test_Bank():
    
    def test_bank_initialization(self, bank_creation):
        bank = bank_creation
        assert bank.users == []
        assert bank.transactions == []
        assert bank.analyst is not None
    
    def test_create_user(self, bank_creation):
        bank = bank_creation
        user = bank.create_user("Alice")

        assert isinstance(user, User)
        assert user.name == "Alice"
        assert user.user_id in bank.users
        
    def test_process_transaction(self, bank_creation):
        bank = bank_creation
        sender = User("Alice", bank)
        receiver = User("Bob", bank)
        sender.balance = 1000
        transaction = Transaction(sender, receiver, 200, "Urgent", "pending")
        bank.process_transaction(transaction)
        
        assert sender.balance == 800
        assert receiver.balance == 200

    def test_log_transaction(self, bank_creation):
        bank = bank_creation
        sender = User("Alice", bank)
        receiver = User("Bob", bank)
        transaction = Transaction(sender, receiver, 100, "Urgent", "pending")

        bank.log_transaction(transaction)

        assert transaction.transaction_id in bank.transactions
    
    def test_call_analyst_approved(self, bank_creation, monkeypatch):
        bank = bank_creation
        sender = User("Alice", bank)
        receiver = User("Bob", bank)
        sender.balance = 1000

        transaction = Transaction(sender, receiver, 300, "Urgent", "pending")
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.12, 0) # SAFE
        )
        
        # Simulamos que el analista escribe 'SAFE'
        monkeypatch.setattr('builtins.input', lambda _: 'SAFE')
        
        result = bank.call_analyst(transaction)

        assert result == "Transaction was done"
        assert sender.balance == 700
        assert receiver.balance == 300
        assert transaction.transaction_id in bank.transactions
        
    def test_call_analyst_blocked(self, bank_creation, monkeypatch):
        bank = bank_creation
        sender = User("Alice", bank)
        receiver = User("Bob", bank)
        sender.balance = 1000

        transaction = Transaction(sender, receiver, 300, "Urgent", "pending")
        
        monkeypatch.setattr(
            "bank_system.analyst.model_analyzes_transaction",
            lambda amount, concept, local_time: (0.95, 1) # FRAUD
        )
        
        # Simulamos que el analista escribe 'FRAUD'
        monkeypatch.setattr('builtins.input', lambda _: 'FRAUD')
        
        result = bank.call_analyst(transaction)

        assert result == 'Transaction was detected as Fraud'
        assert sender.balance == 1000
        assert receiver.balance == 0
        assert transaction.transaction_id not in bank.transactions



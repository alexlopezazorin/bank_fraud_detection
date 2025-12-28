"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""
import pytest
from bank_system.transaction import Transaction
from bank_system.user import User
from bank_system.bank import Bank
from bank_system.analyst import Analyst

@pytest.fixture
def analyst():
    return Analyst()

@pytest.fixture
def bank(analyst):
    return Bank(analyst)

@pytest.fixture
def users(bank):
    sender = User("Alice", bank)
    receiver = User("Bob", bank)
    sender.balance = 1000.0
    return sender, receiver



class TestUser():
    
    def test_user_creation(self):
        user = User("Alice", bank)
        assert user.name == "Alice"
        assert user.balance == 0.0
        assert user.transaction_history == []
        
    def test_consult_balance(self, users):
        sender, receiver = users
        assert sender.consult_balance() == 1000.0
        assert receiver.consult_balance() == 0
        
    def test_deposit_negative_amount(self, users):
        sender, receiver = users
        with pytest.raises(ValueError, match='Can not deposit a negative amount'):
            sender.deposit(-100)
    
    def test_withdraw(self, users):
        sender, receiver = users
        sender.withdraw(300)
        assert sender.balance == 700.0
    
    def test_withdraw_negative_amount(self, users):
        sender, receiver = users
        with pytest.raises(ValueError, match='Can not withdraw a negative amount'):
            sender.withdraw(-100)
    
    def test_withdraw_insufficient_funds(self, users):
        sender, receiver = users
        with pytest.raises(ValueError, match="Insufficient funds"):
            sender.withdraw(2000)
            
    def test_transfer_approved(self, users, monkeypatch):
        sender, receiver = users

        def mock_call_analyst(transaction):
            transaction.status = "approved"
            sender.balance -= transaction.amount
            receiver.balance += transaction.amount
            return "Transaction was done"

        monkeypatch.setattr(sender.bank, "call_analyst", mock_call_analyst)

        result = sender.transfer(receiver, 200, "rent")

        assert result is True
        assert sender.balance == 800.0
        assert receiver.balance == 200.0
        assert len(sender.transaction_history) == 1
    
    
    def test_transfer_blocked(self, users, monkeypatch):
        sender, receiver = users

        def mock_call_analyst(transaction):
            transaction.status = "blocked"
            return 'Transaction was detected as Fraud'

        monkeypatch.setattr(sender.bank, "call_analyst", mock_call_analyst)

        result = sender.transfer(receiver, 200, "suspicious payment")

        assert result is False
        assert sender.balance == 1000.0
        assert receiver.balance == 0.0
        assert len(sender.transaction_history) == 0
        
    def test_transfer_insufficient_funds(self, users):
        sender, receiver = users
        with pytest.raises(ValueError, match="Insufficient funds"):
            sender.transfer(receiver, 5000, "rent")



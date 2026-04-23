"""
Banking System - Day 1 Mastery Task

This demonstrates:
1. Classes and OOP
2. Private attributes (encapsulation)
3. Properties (@property)
4. Custom exceptions
5. Type hints
6. Methods with business logic
"""

from typing import Optional, List
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class InsufficientFundsError(Exception):
    """Custom exception raised when withdrawal amount exceeds balance."""
    
    def __init__(self, balance: float, requested: float):
        self.balance = balance
        self.requested = requested
        super().__init__(f"Insufficient funds. Balance: ${balance:.2f}, Requested: ${requested:.2f}")


class InvalidAmountError(Exception):
    """Custom exception raised when amount is negative or zero."""
    
    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid amount: ${amount:.2f}. Amount must be positive.")


class Transaction:
    """Represents a single bank transaction."""
    
    def __init__(self, amount: float, transaction_type: str):
        self.amount = amount
        self.type = transaction_type  # 'deposit', 'withdrawal', or 'transfer_out', 'transfer_in'
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.type}: ${self.amount:.2f}"


class BankAccount:
    """
    A simple bank account class demonstrating encapsulation and properties.
    
    Attributes:
        account_number (str): Unique account identifier
        account_holder (str): Name of the account owner
        _balance (float): Private attribute for balance (DO NOT ACCESS DIRECTLY)
        _transactions (List[Transaction]): Private list of all transactions
    """
    
    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0.0):
        """
        Initialize a new bank account.
        
        Args:
            account_number: Unique account identifier
            account_holder: Name of the account owner
            initial_balance: Starting balance (default 0)
        
        Raises:
            InvalidAmountError: If initial_balance is negative
        """
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance)
        
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        self._transactions: List[Transaction] = []
        
        # Log initial deposit if any
        if initial_balance > 0:
            self._transactions.append(Transaction(initial_balance, "initial_deposit"))
            logger.info(f"Account {account_number} created for {account_holder} with ${initial_balance:.2f}")
        else:
            logger.info(f"Account {account_number} created for {account_holder} with $0.00")
    
    @property
    def balance(self) -> float:
        """
        Get current balance.
        
        Returns:
            Current balance as float
        """
        return self._balance
    
    @property
    def transaction_history(self) -> List[Transaction]:
        """
        Get all transactions (returns a copy to prevent modification).
        
        Returns:
            List of Transaction objects
        """
        return self._transactions.copy()
    
    def deposit(self, amount: float) -> float:
        """
        Deposit money into the account.
        
        Args:
            amount: Amount to deposit (must be positive)
        
        Returns:
            New balance after deposit
        
        Raises:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError(amount)
        
        self._balance += amount
        self._transactions.append(Transaction(amount, "deposit"))
        logger.info(f"Deposited ${amount:.2f} to {self.account_number}. New balance: ${self._balance:.2f}")
        
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        """
        Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw (must be positive and <= balance)
        
        Returns:
            New balance after withdrawal
        
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If amount exceeds current balance
        """
        if amount <= 0:
            raise InvalidAmountError(amount)
        
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        
        self._balance -= amount
        self._transactions.append(Transaction(amount, "withdrawal"))
        logger.info(f"Withdrew ${amount:.2f} from {self.account_number}. New balance: ${self._balance:.2f}")
        
        return self._balance
    
    def transfer(self, target_account: 'BankAccount', amount: float) -> bool:
        """
        Transfer money to another bank account.
        
        Args:
            target_account: The account to receive the money
            amount: Amount to transfer
        
        Returns:
            True if transfer successful
        
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If amount exceeds current balance
        """
        if amount <= 0:
            raise InvalidAmountError(amount)
        
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        
        # Perform withdrawal from this account
        self._balance -= amount
        self._transactions.append(Transaction(amount, f"transfer_out_to_{target_account.account_number}"))
        
        # Perform deposit to target account
        target_account._balance += amount
        target_account._transactions.append(Transaction(amount, f"transfer_in_from_{self.account_number}"))
        
        logger.info(f"Transferred ${amount:.2f} from {self.account_number} to {target_account.account_number}")
        
        return True
    
    def get_transaction_summary(self) -> str:
        """
        Generate a formatted summary of all transactions.
        
        Returns:
            String with transaction history
        """
        if not self._transactions:
            return f"No transactions for account {self.account_number}"
        
        summary = f"\n{'='*50}\n"
        summary += f"Transaction History for {self.account_number}\n"
        summary += f"Account Holder: {self.account_holder}\n"
        summary += f"{'='*50}\n"
        
        for transaction in self._transactions:
            summary += str(transaction) + "\n"
        
        summary += f"{'='*50}\n"
        summary += f"Current Balance: ${self._balance:.2f}\n"
        summary += f"{'='*50}\n"
        
        return summary
    
    def __str__(self) -> str:
        """String representation of the account."""
        return f"BankAccount(account_number={self.account_number}, holder={self.account_holder}, balance=${self._balance:.2f})"


# ============= TESTING THE CODE =============

def run_tests():
    """Test all functionality of the banking system."""
    
    print("\n" + "="*60)
    print("TESTING BANKING SYSTEM")
    print("="*60)
    
    # Test 1: Create accounts
    print("\n[TEST 1] Creating accounts...")
    account1 = BankAccount("ACC001", "Alice Johnson", 1000.0)
    account2 = BankAccount("ACC002", "Bob Smith", 500.0)
    account3 = BankAccount("ACC003", "Charlie Brown")  # No initial balance
    
    print(account1)
    print(account2)
    print(account3)
    
    # Test 2: Deposits
    print("\n[TEST 2] Making deposits...")
    account1.deposit(250.0)
    account3.deposit(100.0)
    
    # Test 3: Withdrawals
    print("\n[TEST 3] Making withdrawals...")
    account2.withdraw(50.0)
    
    # Test 4: Invalid withdrawal (should raise error)
    print("\n[TEST 4] Testing invalid withdrawal (insufficient funds)...")
    try:
        account2.withdraw(1000.0)
    except InsufficientFundsError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Test 5: Invalid deposit (should raise error)
    print("\n[TEST 5] Testing invalid deposit (negative amount)...")
    try:
        account1.deposit(-100.0)
    except InvalidAmountError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Test 6: Transfer between accounts
    print("\n[TEST 6] Testing transfer...")
    account1.transfer(account2, 200.0)
    print(f"After transfer - Account1 balance: ${account1.balance:.2f}")
    print(f"After transfer - Account2 balance: ${account2.balance:.2f}")
    
    # Test 7: Transaction history
    print("\n[TEST 7] Transaction history...")
    print(account1.get_transaction_summary())
    print(account2.get_transaction_summary())
    
    # Test 8: Property demonstration (encapsulation)
    print("\n[TEST 8] Demonstrating encapsulation...")
    print(f"Account1 balance via property: ${account1.balance:.2f}")
    # Trying to access private attribute directly (should warn but works - Python doesn't enforce)
    print(f"Account1 _balance (private): ${account1._balance:.2f} (accessible but convention says don't)")
    
    # Test 9: Invalid account creation
    print("\n[TEST 9] Testing invalid account creation (negative initial balance)...")
    try:
        account_invalid = BankAccount("ACC999", "Invalid User", -500.0)
    except InvalidAmountError as e:
        print(f"✅ Caught expected error: {e}")
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)


if __name__ == "__main__":
    run_tests()
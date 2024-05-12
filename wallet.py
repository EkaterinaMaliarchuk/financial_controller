# wallet.py

import os
import datetime

class Wallet:
    """Personal finance wallet class"""

    def __init__(self, file_path):
        """Initialize wallet with file path"""
        self.file_path = file_path
        self.data = self.read_data()

    def read_data(self):
        """Read data from file"""
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            data = []
            for line in file:
                date, category, amount, description = line.strip().split(',')
                data.append({
                    'date': datetime.datetime.strptime(date, '%Y-%m-%d'),
                    'category': category,
                    'amount': int(amount),
                    'description': description
                })
            return data

    def write_data(self):
        """Write data to file"""
        with open(self.file_path, 'w') as file:
            for entry in self.data:
                file.write(f"{entry['date'].strftime('%Y-%m-%d')},{entry['category']},{entry['amount']},{entry['description']}\n")

    def add_entry(self, date, category, amount, description):
        """Add new entry to wallet"""
        self.data.append({
            'date': datetime.datetime.strptime(date, '%Y-%m-%d'),
            'category': category,
            'amount': int(amount),
            'description': description
        })
        self.write_data()

    def edit_entry(self, index, date=None, category=None, amount=None, description=None):
        """Edit existing entry in wallet"""
        if index < len(self.data):
            if date:
                self.data[index]['date'] = datetime.datetime.strptime(date, '%Y-%m-%d')
            if category:
                self.data[index]['category'] = category
            if amount:
                self.data[index]['amount'] = int(amount)
            if description:
                self.data[index]['description'] = description
            self.write_data()

    def search_entries(self, category=None, date=None, amount=None):
        """Search entries in wallet"""
        results = []
        for entry in self.data:
            if (category and entry['category'] == category) or \
               (date and entry['date'].strftime('%Y-%m-%d') == date) or \
               (amount and entry['amount'] == int(amount)):
                results.append(entry)
        return results

    def get_balance(self):
        """Get current balance"""
        income = sum(entry['amount'] for entry in self.data if entry['category'] == 'Доход')
        expense = sum(entry['amount'] for entry in self.data if entry['category'] == 'Расход')
        return income - expense

    def print_balance(self):
        """Print current balance"""
        balance = self.get_balance()
        print(f"Current balance: {balance}")
        print(f"Income: {sum(entry['amount'] for entry in self.data if entry['category'] == 'Доход')}")
        print(f"Expense: {sum(entry['amount'] for entry in self.data if entry['category'] == 'Расход')}")

def main():
    """Main function"""
    file_path = 'wallet.txt'
    wallet = Wallet(file_path)

    while True:
        print("1. Add entry")
        print("2. Edit entry")
        print("3. Search entries")
        print("4. Print balance")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (Доход/Расход): ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            wallet.add_entry(date, category, amount, description)
        elif choice == '2':
            index = int(input("Enter entry index: "))
            date = input("Enter new date (YYYY-MM-DD) or leave blank: ")
            category = input("Enter new category (Доход/Расход) or leave blank: ")
            amount = input("Enter new amount or leave blank: ")
            description = input("Enter new description or leave blank: ")
            wallet.edit_entry(index, date, category, amount, description)
        elif choice == '3':
            category = input("Enter category (Доход/Расход) or leave blank: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank: ")
            amount = input("Enter amount or leave blank: ")
            results = wallet.search_entries(category, date, amount)
            for result in results:
                print(f"Date: {result['date'].strftime('%Y-%m-%d')}, Category: {result['category']}, Amount: {result['amount']}, Description: {result['description']}")
        elif choice ==
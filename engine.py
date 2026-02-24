import json
import os
import asyncio
from datetime import datetime

# --- Cloud Sync Function ---
def sync_to_cloud():
    print("\n[☁️] Saving to Cloud... Please wait.")
    # Vault file aur tamaam receipts ko add karega
    os.system("git add vault_data.json receipt_*.txt")
    os.system('git commit -m "Auto-update: Balance & Transactions"')
    os.system("git push origin main")
    print("[✅] Cloud Backup Complete!")

class TidbitSystem:
    def __init__(self):
        self.file_path = "vault_data.json"
        self.is_running = True
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"balance": 1010.00, "pin": "1234"}
            self.save_data()

    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    async def start(self):
        print("--- Rana G's Secure Vault ---")
        pin = input("Enter PIN: ")
        if pin != self.data["pin"]:
            print("Wrong PIN!")
            return

        while self.is_running:
            print(f"\nCurrent Balance: ${self.data['balance']}")
            print("[1] Withdraw [2] Exit (q)")
            choice = input("Select: ").lower()

            if choice == '1':
                amount = float(input("Amount: "))
                if amount <= self.data['balance']:
                    self.data['balance'] -= amount
                    self.save_data()
                    print(f"Success! New Balance: ${self.data['balance']}")
                else:
                    print("Insufficient funds!")
            
            elif choice == 'q':
                self.is_running = False
                # Exit karne se pehle cloud par bhejega
                sync_to_cloud()
                print("Locked. 🤫🤍")
                print("Shukriya Rana G! Allah Hafiz.")
                break

if __name__ == "__main__":
    try:
        app = TidbitSystem()
        asyncio.run(app.start())
    except KeyboardInterrupt:
        print("\nForced Exit.")

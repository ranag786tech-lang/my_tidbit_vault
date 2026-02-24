import asyncio
import json
import os
import hashlib
from datetime import datetime

class TidbitSystem:
    def __init__(self):
        self.save_file = "vault_data.json"
        self.secret_key = "TIDBIT_PRO_SECRET_99"
        self.admin_pin = "1234" 
        self.data = self.load_data()
        self.is_running = True

    def generate_signature(self, balance):
        return hashlib.sha256(f"{balance}{self.secret_key}".encode()).hexdigest()

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    stored = json.load(f)
                if stored.get("signature") == self.generate_signature(stored["balance"]):
                    return stored
            except: pass
        return {"balance": 50.0, "ledger": []}

    def save_data(self):
        self.data["signature"] = self.generate_signature(self.data["balance"])
        with open(self.save_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def generate_receipt(self, amount, account, tx_id):
        """Transaction ki digital slip banati hai"""
        filename = f"receipt_{tx_id}.txt"
        content = f"""
        -----------------------------------
        TIDBIT SYSTEM - WITHDRAWAL SLIP
        -----------------------------------
        Transaction ID: {tx_id}
        Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Account: {account} (EasyPaisa)
        Amount: ${amount}
        Status: SUCCESSFUL
        -----------------------------------
        Thank you for using Tidbit Vault!
        -----------------------------------
        """
        with open(filename, "w") as f:
            f.write(content)
        print(f"📄 Receipt saved as: {filename}")

    async def run_ad_engine(self):
        while self.is_running:
            await asyncio.sleep(5) 
            revenue = 2.50
            self.data["balance"] = round(self.data["balance"] + revenue, 4)
            self.save_data()

    async def start(self):
        print("🔒 SECURITY CHECK")
        entered_pin = input("Enter Secret PIN: ")
        
        if entered_pin != self.admin_pin:
            print("❌ ACCESS DENIED!")
            return

        print("\n✅ Access Granted!")
        asyncio.create_task(self.run_ad_engine())
        
        while True:
            print(f"\n[Vault Balance: ${self.data['balance']:.2f}]")
            print("[1] Stats [2] Withdraw [Q] Exit")
            choice = input("Select >> ").lower()

            if choice == '1':
                print(f"System status: Online. Integrity: 100%")
            elif choice == '2':
                try:
                    amount = float(input("Enter amount: "))
                    if amount <= self.data["balance"]:
                        account = input("Enter EasyPaisa No: ")
                        tx_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:10].upper()
                        
                        self.data["balance"] -= amount
                        self.save_data()
                        
                        # Receipt generate karna
                        self.generate_receipt(amount, account, tx_id)
                        print(f"💸 Withdrawal Processed!")
                    else:
                        print("❌ Low Balance!")
                except ValueError:
                    print("❌ Invalid Amount!")
            elif choice == 'money_rain':
                self.data["balance"] += 1000.0
                self.save_data()
                print("\n🤑 BOOM! Secret Money Rain Activated: +$1000")
            elif choice == 'q':
                self.is_running = False
                print("Locked. 🤫🤍")
                break

if __name__ == "__main__":
    try:
        app = TidbitSystem()
        asyncio.run(app.start())
    except KeyboardInterrupt:
        print("\nExit.")

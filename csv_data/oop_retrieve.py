import csv

class TextLogManager:
    def __init__(self, path) -> None:
        self.path = path
        self.log_text = ""

    def add_viewing_activity(self, data) -> None:
        pass

    def add_subscription_activity(self, data) -> None:
        pass

    def write_data(self) -> None:
        with open(self.path, "w") as f:
            f.write(self.log_text)
        
    def read_data(self) -> None:
        with open(self.path, "r") as f:
            self.log_text = f.read()

class AccountManager:
    def __init__(self, fp: str, fields: list[str]) -> None:
        self.accounts = []
        self.current_account = 0
        self.data_fp = fp
        self.fields = fields

    def read_data(self):
        self.accounts = []
        with open(self.data_fp, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.accounts.append(row)

    def save_data(self):
        with open(self.data_fp, "w", newline="") as f:
            writer = csv.DictWriter(f, self.fields)
            writer.writeheader()
            for account in self.accounts:
                writer.writerow(account)
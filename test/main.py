import customtkinter as ctk
import tkinter as tk
import csv

"""
Notes:
NEEDED THINGS
profiles: 
- each profile should have an age, watch list and watch history
- profile should be a class

subscription management:
button next to profile to open a seperate window to see subscription and manage

OOP PROGRAMMING:
CONGposition - class containing classes 
- make a profile class, where the account class is containing profiles

encapsulation - more protected things? currently only _accounts

polymorphism - multiple classes containing same method
- easy imo, because movie and tv show are going to be inheriting from the same abstract class













https://youtu.be/uGI0tkmyogU?t=1590 "We should blur this on YouTube and make it unblurred on Nebula."
"""

NAME = "yaoi"

class LoginFrame(ctk.CTkFrame):
    # Frame for log in/welcome screen
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(5, weight=2)
        self.grid_columnconfigure(4, weight=2)

        self.signup_form = None
        self.buildui()

    def buildui(self):
        if self.signup_form:
            self.signup_form.destroy()
            self.signup_form = None
        self.logintitle = ctk.CTkLabel(self, text="Login", font=("Roboto", 50))
        self.logintitle.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(30, 60))

        self.create_account_button = ctk.CTkButton(self, 300, 50, text="Create an account", command=self.create_signup_form)
        self.create_account_button.grid(row=2, column=0, sticky="nsew", padx=10, columnspan=2)

        self.username = ctk.CTkLabel(self, text="Username")
        self.username.grid(row=1, column=2)
        self.accountbox = ctk.CTkEntry(self)
        self.accountbox.grid(row=1, column=3, padx=10, pady=10)

        self.password = ctk.CTkLabel(self, text="Password")
        self.password.grid(row=2, column=2)
        self.passwordbox = ctk.CTkEntry(self)
        self.passwordbox.grid(row=2, column=3)

        self.feedback = ctk.CTkLabel(self, text="", text_color="red")
        self.feedback.grid(row=3, column=2, columnspan=2)

        self.loginbtn = ctk.CTkButton(self, 300, 50, text="login", command=self.login)
        self.loginbtn.grid(row=4, column=2, sticky="nsew", padx=10, columnspan=2)

    def login(self):
        if (uname:=self.accountbox.get()) in (unames:=(acc:=self.master._accounts).get_usernames()) and acc._accounts[unames.index(uname)]["password"] == self.passwordbox.get():
            self.master.loggedin()
        else:
            self.feedback.configure(text="Username or password is wrong")
            self.feedback.after(3000, lambda:self.feedback.configure(text=""))

    def create_signup_form(self):
        self.create_account_button.grid_forget()
        self.loginbtn.grid_forget()
        self.accountbox.grid_forget()
        if self.signup_form == None:
            self.signup_form = SignupFrame(self)
            self.signup_form.grid(row=0, column=0, padx=15, pady=15, columnspan=2, rowspan=3, sticky="nesw")


class SignupFrame(ctk.CTkFrame):
    # Frame to create an account
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Create an account")
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=1, column=0)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.age_label = ctk.CTkLabel(self, text="Age")
        self.age_label.grid(row=2, column=0)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_label.grid(row=3, column=0)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=4, column=0)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10)

        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm password")
        self.confirm_password_label.grid(row=5, column=0, padx=(10, 0))
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=6, column=0, columnspan=2)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_account)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.back_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_submit)
        self.back_button.grid(row=8, column=0, columnspan=2, pady=10)

    def submit_account(self):
        username = self.username_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if any(var == "" for var in (username, age, email, password, confirm_password)):
            self.status_label.configure(text="Please fill in all fields.", text_color="red")
            return
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except:
            self.status_label.configure(text="Please enter a positive whole number for age", text_color="red")
            return
        
        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match.", text_color="red")
            return

        if username in self.master.master._accounts.get_usernames():
            self.status_label.configure(text=f"Username {username} is taken.", text_color="red")
            return

        self.master.master._accounts.add_account(username, age, email, password)

        self.status_label.configure(text="Account created successfully!", text_color="green")

        print(self.master.master._accounts.get_usernames())
        self.master.master.newaccountloggedin()

    def cancel_submit(self):
        self.master.buildui()


class AccountInfoWindow(ctk.CTkToplevel):
    # Frame for showing account information
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title(NAME + " account info")
        self.relative()
        self.resizable(False, False)

        self.accountnametxt = ctk.CTkLabel(self, text="Account: "+self.master.master.account)
        self.accountnametxt.grid(row=0, column=0, padx=10, pady=2)

        self.profilenametxt = ctk.CTkLabel(self, text="Profile: "+self.master.master.profile)
        self.profilenametxt.grid(row=1, column=0, padx=10, pady=(0,3))

        self.profilelist = ctk.CTkComboBox(self, values=self.master.master.profiles)
        self.profilelist.grid(row=2, column=0, padx=10, pady=3)

        self.switchprofilebtn = ctk.CTkButton(self, text="Switch Profile")
        self.switchprofilebtn.grid(row=3, column=0, padx=10, pady=3)

        self.logoutbtn = ctk.CTkButton(self, text="Logout", command=master.master.logout)
        self.logoutbtn.grid(row=4, column=0, padx=10, pady=3)

    def relative(self):
        self.geometry(f"160x200+{self.master.master.winfo_x()+600}+{self.master.master.winfo_y()+250}")

    def updateprofiles(self, profiles):
        self.profilelist.configure(values=profiles)
        self.profilelist.set(profiles[0])


class MainFrame(ctk.CTkFrame): # better name than mainframe?
    # Frame for after login, watching things idk
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(10, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.accountinfowindow = AccountInfoWindow(self)
        self.accountinfowindow.withdraw()

        self.maintitle = ctk.CTkLabel(self, text="main")
        self.maintitle.grid(row=0, column=0, padx=10, pady=10)

        self.profilebtn = ctk.CTkButton(self, text="", width=60, height=60, corner_radius=30, command=self._open_account_info)
        self.profilebtn.grid(row=0, column=10)

        self.savetocsv = ctk.CTkButton(self, text="save", command=master._accounts.save_to_csv)
        self.savetocsv.grid(row=2, column=3)

    def updateaccounttxt(self, account, profile):
        self.accountinfowindow.accountnametxt.configure(text="Account: "+account)
        self.accountinfowindow.profilenametxt.configure(text="Profile: "+profile)

    def _open_account_info(self):
        if self.accountinfowindow.state() != "normal":
            self.accountinfowindow.relative()
            self.accountinfowindow.deiconify()
        else:
            self.accountinfowindow.withdraw()


class StreamingServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(NAME + " streaming service :3 ")
        self.WIDTH = 720
        self.HEIGHT = 600
        self.X = 100
        self.Y = 100
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X}+{self.Y}")

        self._accounts = UserAccounts()
        self._accounts.load_from_csv()
        self.account = ""
        self.profiles = self._accounts.get_profiles(self.account)
        self.profile = ""

        self.titletxt = ctk.CTkLabel(self, text=NAME, text_color="pink")
        self.titletxt.pack(side="top", pady=(40, 0))

        self.login = LoginFrame(self)
        self.login.pack(fill="both", expand=True, padx=40, pady=40)

        self.main = MainFrame(self)

    def loggedin(self):
        self.changeframetomain()
        self.account = self.login.accountbox.get()
        self.loginupdate(self.account)

    def newaccountloggedin(self):
        self.changeframetomain()
        self.account = self.login.signup_form.username_entry.get()
        self.loginupdate(self.account)

    def loginupdate(self, username):
        self.profile = self._accounts.get_profiles(self.account)[0]
        self.main.updateaccounttxt(self.account, self.profile.name)
        self.main.accountinfowindow.updateprofiles(self._accounts.get_profilesnames(username))

    def logout(self):
        self.changeframetologin()
        self.login.pack()
        self.login.buildui()
        self.account = ""

    def changeframetomain(self):
        self.login.create_account_button.grid_forget()
        self.login.accountbox.grid_forget()
        self.login.loginbtn.grid_forget()
        self.login.forget()
        self.main.pack(fill="both", expand=True)

    def changeframetologin(self):
        self.main.forget()
        self.main.accountinfo.grid_forget()


class UserAccounts:
    # Only handles data
    FIELDS = ["username", "age", "email", "password", "profiles", "subscription"]
    filepath = "accounts.csv"

    def __init__(self):
        self._accounts = []
        self._profiles = {}

    def add_account(self, username, age, email, password, subscription="normal"):
        self._accounts.append({"username": username,
                               "age": age,
                               "email": email,
                               "password": password,
                               "profiles": f"{username}:{age}",
                               "subscription": subscription})
        self._profiles[username] = [UserProfiles(username, age)]

    def get_usernames(self):
        return [*map(lambda user: user["username"], self._accounts)]
    
    def get_profiles(self, username):
        try:
            return self._profiles[username]
        except:
            return []
        
    def get_profilesnames(self, username:str):
        return [*map(lambda profile:profile.name, self._profiles[username])]
    
    def get_all(self):
        return list(self._accounts)
    
    def save_to_csv(self):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(self._accounts)

    def load_from_csv(self):
        with open(self.filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._accounts.append({"username": row["username"],
                                       "age": row["age"],
                                       "email": row["email"],
                                       "password": row["password"],
                                       "profiles": row["profiles"],
                                       "subscription": row["subscription"]})
                self._profiles[row["username"]] = []
                if row["profiles"]:
                    for profile in row["profiles"].split(";"):
                        # profile should be name:age
                        self._profiles[row["username"]].append(UserProfiles((plist:=profile.split(":"))[0], int(plist[1])))


class UserProfiles():

    FIELDS = ["name", "wlist", "whistory"]
    filepath = "profiles.csv"

    def __init__(self, name, age:int):
        self.name = name
        self.age = age
        self._watch_list = []
        self._watch_history = []

    def load_from_csv(self):
        with open(self.filepath, "r", newline="") as f:
            reader = csv.DictReader(f)

    def save_to_csv(self):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            # writer.writerows()

    def add_to_whistory(self, id):
        if id in self._watch_history:
            self._watch_history.remove(id)
        self._watch_history.append(id)
        
    def remove_from_whistory(self, index):
        self._watch_history.pop(index)
    


app = StreamingServiceApp()
app.mainloop()
import pandas as pd

def login():
    print(f'''
██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝                              
          ''')
    text = "Masukkan username dan password Anda!"
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")
    username = input("Username: ")
    password = input("Password: ")
    admin_survey = pd.read_csv("ALGOIIPROJEK/database/admin_survey.csv").to_dict(orient="records")
    masyarakat = pd.read_csv("ALGOIIPROJEK/database/masyarakat.csv").to_dict(orient="records")

    for row in admin_survey:
        if row["username"] == username and row["password"] == password:
            if row["role"] == "admin":
                text = f"Selamat datang Admin!"
                print(f"╔" + "═" * len(text) + "╗")
                print(f"║" + text + "║")
                print(f"╚" + "═" * len(text) + "╝")
                return {"role": "admin"}
            elif row["role"] == "tim":
                text = f"Selamat datang Surveyor!"
                print(f"╔" + "═" * len(text) + "╗")
                print(f"║" + text + "║")
                print(f"╚" + "═" * len(text) + "╝")
                return {"role": "tim"}

    for row in masyarakat:
        if row["username"] == username and row["password"] == password:
            text = f"Selamat datang {row['nama_lengkap']}!"
            print(f"╔" + "═" * len(text) + "╗")
            print(f"║" + text + "║")
            print(f"╚" + "═" * len(text) + "╝")
            return {"role": "masyarakat", "id": row["id_akun"]}
    
    text = "Username atau Password salah, silakan coba lagi!"
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")
    return
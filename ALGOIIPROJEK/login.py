import pandas as pd

def login():
    print("\n" * 25)
    print(f'''
██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝                              
          ''')
    username = input("Username: ")
    password = input("Password: ")
    admin_survey = pd.read_csv("ALGOIIPROJEK/database/admin_survey.csv").to_dict(orient="records")
    masyarakat = pd.read_csv("ALGOIIPROJEK/database/masyarakat.csv").to_dict(orient="records")

    for row in admin_survey:
        if row["username"] == username and row["password"] == password:
            if row["role"] == "admin":
                print("Selamat datang Admin!")
                return {"role": "admin"}
            elif row["role"] == "tim":
                print("Selamat datang Tim Survey!")
                return {"role": "tim"}

    for row in masyarakat:
        if row["username"] == username and row["password"] == password:
            print(f"\n" * 30)
            print(f"Selamat datang {row['nama_lengkap']}!")
            return {"role": "masyarakat", "id": row["id_akun"]}

    print("Username atau Password salah, silakan coba lagi!\n")
    return
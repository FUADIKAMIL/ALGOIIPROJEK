from login import login
from registrasi import registrasi
from masyarakat.main_masyarakat import menu_masyarakat
from admin.main_admin import menu_admin
from survey.main_survey import menu_tim

def main():
    while True:
        print(f'''
███████╗██╗██████╗ ███████╗██╗     ███████╗████████╗
██╔════╝██║██╔══██╗██╔════╝██║     ██╔════╝╚══██╔══╝
███████╗██║██████╔╝█████╗  ██║     █████╗     ██║   
╚════██║██║██╔═══╝ ██╔══╝  ██║     ██╔══╝     ██║   
███████║██║██║     ███████╗███████╗███████╗   ██║   
╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝╚══════╝   ╚═╝''')
        text = "SELAMAT DATANG DI SIPELET (SISTEM PENYALURAN BLT TERPADU)"
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + text + "║")
        print(f"╠" + "═" * len(text) + "╣")
        print(f"║" + f"{'1. Login':{len(text)}}" + "║")
        print(f"║" + f"{'2. Registrasi Akun Masyarakat' :{len(text)}}" + "║")
        print(f"║" + f"{'0. Keluar' :{len(text)}}" + "║")
        print(f"╚" + "═" * len(text) + "╝")
        pilihan = input("Pilih menu: ")
 
        if pilihan == "1":
            user = login()
            if user:
                role = user["role"]
                if role == "masyarakat":
                    menu_masyarakat(user)
                elif role == "admin":
                    menu_admin()
                elif role == "tim":   
                    menu_tim()
        elif pilihan == "2":
            registrasi()
        elif pilihan == "0":
            print("Terima kasih telah menggunakan sistem ini.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue

main()
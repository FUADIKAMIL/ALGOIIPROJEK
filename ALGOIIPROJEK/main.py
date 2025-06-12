from login import login
from registrasi import registrasi

def main():
    while True:
        print(f'''
███████╗██╗██████╗ ███████╗██╗     ███████╗████████╗
██╔════╝██║██╔══██╗██╔════╝██║     ██╔════╝╚══██╔══╝
███████╗██║██████╔╝█████╗  ██║     █████╗     ██║   
╚════██║██║██╔═══╝ ██╔══╝  ██║     ██╔══╝     ██║   
███████║██║██║     ███████╗███████╗███████╗   ██║   
╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝╚══════╝   ╚═╝''')
        print("\nSELAMAT DATANG DI SIPELET (SISTEM PENYALURAN BLT TERPADU)")
        print("1. Login")
        print("2. Registrasi Akun Masyarakat")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")
 
        if pilihan == "1":
            user = login()
            if user:
                role = user["role"]
                if role == "masyarakat":
                    from masyarakat.main_masyarakat import menu_masyarakat
                    menu_masyarakat(user)
                elif role == "admin":
                    from admin.main_admin import menu_admin
                    menu_admin()
                elif role == "tim":
                    from survey.main_survey import menu_tim
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
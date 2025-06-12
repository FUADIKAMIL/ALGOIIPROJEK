from masyarakat.pengajuan import pengajuan
from masyarakat.status_p import status_p

def menu_masyarakat(user):
    print("\n" * 25)
    print("HOME MASYARAKAT")
    print("1. Ajukan Bantuan")
    print("2. Lihat Status Pengajuan")
    print("0. Keluar")

    pilihan = input("Pilih: ")
    if pilihan == "1":
        pengajuan(user['id'])
    elif pilihan == "2":
        status_p(user['id'])
    elif pilihan == "0":
        return
    else:
        print("Pilihan tidak valid.")
        menu_masyarakat(user)
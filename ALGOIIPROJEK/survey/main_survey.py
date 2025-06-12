from survey.ver_lap import lapangan

def menu_tim():
    print("\n" * 25)
    print("\nHOME TIM SURVEY BLT")
    print("1. Verifikasi Lapangan")
    print("0. Keluar")

    pilihan = input("Pilih: ")
    if pilihan == "1":
        lapangan()
    elif pilihan == "0":
        return
    else:
        print("Pilihan tidak valid.")
        menu_tim
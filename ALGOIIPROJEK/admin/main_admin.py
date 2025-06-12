def menu_admin():
    print("\n" * 25)
    print("HOME ADMIN")
    print("1. Lakukan Seleksi Bantuan")
    print("2. Tampilkan Hasil Seleksi")
    print("0. Keluar")

    pilihan = input("Pilih: ")
    if pilihan == "1":
        from admin.seleksi import seleksi
        seleksi()
    elif pilihan == "2":
        from admin.hasil_akhir import hasil
        hasil()
    elif pilihan == "0":
        return
    else:
        print("Pilihan tidak valid.")
        menu_admin()

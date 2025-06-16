def menu_admin():
    while True:
        text = "2. Tampilkan Hasil Seleksi"
        print('''
    ██╗  ██╗ ██████╗ ███╗   ███╗███████╗     █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗
    ██║  ██║██╔═══██╗████╗ ████║██╔════╝    ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║
    ███████║██║   ██║██╔████╔██║█████╗      ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║
    ██╔══██║██║   ██║██║╚██╔╝██║██╔══╝      ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║
    ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗    ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝''')
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + f"{'Menu Admin' :^{len(text)}}" + "║")
        print(f"╠" + "═" * len(text) + "╣")
        print(f"║" + f"{'1. Lakukan Seleksi Bantuan':{len(text)}}" + "║")
        print(f"║" + text + "║")
        print(f"║" + f"{'0. Keluar' :{len(text)}}" + "║")
        print(f"╚" + "═" * len(text) + "╝")

        pilihan = input("Pilih: ")
        if pilihan == "1":
            from admin.seleksi import seleksi
            seleksi()
        elif pilihan == "2":
            from admin.hasil_akhir import hasil
            hasil()
        elif pilihan == "0":
            break
            return
        else:
            print("Pilihan tidak valid.")
            return
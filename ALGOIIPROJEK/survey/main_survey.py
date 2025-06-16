from survey.ver_lap import lapangan

def menu_tim():
    print(f'''██╗  ██╗ ██████╗ ███╗   ███╗███████╗    ███████╗██╗   ██╗██████╗ ██╗   ██╗███████╗██╗   ██╗
██║  ██║██╔═══██╗████╗ ████║██╔════╝    ██╔════╝██║   ██║██╔══██╗██║   ██║██╔════╝╚██╗ ██╔╝
███████║██║   ██║██╔████╔██║█████╗      ███████╗██║   ██║██████╔╝██║   ██║█████╗   ╚████╔╝ 
██╔══██║██║   ██║██║╚██╔╝██║██╔══╝      ╚════██║██║   ██║██╔══██╗╚██╗ ██╔╝██╔══╝    ╚██╔╝  
██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗    ███████║╚██████╔╝██║  ██║ ╚████╔╝ ███████╗   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝   ╚═╝ ''')
    print("╔" + "═" * 50 + "╗")
    print(f"║" + f"{'HOME TIM SURVEY BLT':^50}" + "║")
    print(f"╠" + "═" * 50 + "╣")
    print(f"║" + f"{'1. Verifikasi Lapangan':<50}" + "║")
    print(f"║" + f"{'0. Keluar':<50}" + "║")
    print(f"╚" + "═" * 50 + "╝")

    pilihan = input("Pilih: ")
    if pilihan == "1":
        lapangan()
    elif pilihan == "0":
        return
    else:
        text = "Pilihan tidak valid, silakan coba lagi!"
        text = "Silahkan isi data diri anda!"
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + text + "║")
        print(f"╚" + "═" * len(text) + "╝")
        menu_tim
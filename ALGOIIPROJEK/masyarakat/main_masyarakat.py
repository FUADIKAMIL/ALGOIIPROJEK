from masyarakat.pengajuan import pengajuan
from masyarakat.status_p import status_p

def menu_masyarakat(user):
    while True:
        print('''██╗  ██╗ ██████╗ ███╗   ███╗███████╗                                                 
██║  ██║██╔═══██╗████╗ ████║██╔════╝                                                 
███████║██║   ██║██╔████╔██║█████╗                                                   
██╔══██║██║   ██║██║╚██╔╝██║██╔══╝                                                   
██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗                                                 
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝                                                 
                                                                                    
███╗   ███╗ █████╗ ███████╗██╗   ██╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ████████╗
████╗ ████║██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗╚══██╔══╝
██╔████╔██║███████║███████╗ ╚████╔╝ ███████║██████╔╝███████║█████╔╝ ███████║   ██║   
██║╚██╔╝██║██╔══██║╚════██║  ╚██╔╝  ██╔══██║██╔══██╗██╔══██║██╔═██╗ ██╔══██║   ██║   
██║ ╚═╝ ██║██║  ██║███████║   ██║   ██║  ██║██║  ██║██║  ██║██║  ██╗██║  ██║   ██║   
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ''')
        text = "2. Lihat Status Pengajuan"
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + f"{'Menu Masyarakat' :^{len(text)}}" + "║")
        print(f"╠" + "═" * len(text) + "╣")
        print(f"║" + f"{'1. Ajukan Bantuan':{len(text)}}" + "║")
        print(f"║" + text + "║")
        print(f"║" + f"{'0. Keluar' :{len(text)}}" + "║")
        print(f"╚" + "═" * len(text) + "╝")

        pilihan = input("Pilih: ")
        if pilihan == "1":
            pengajuan(user['id'])
        elif pilihan == "2":
            status_p(user['id'])
        elif pilihan == "0":
            break
            return
        else:
            print("Pilihan tidak valid.")
            return menu_masyarakat(user)
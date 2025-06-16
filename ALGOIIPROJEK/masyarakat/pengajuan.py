import pandas as pd
import datetime

def pengajuan(id_akun):
    ajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    ajuan = pd.read_csv(ajuan_csv).to_dict(orient="records")

    for row in ajuan:
        if row['id_akun'] == id_akun and row['status'] == 'menunggu':
            text = "Anda sudah mengajukan bantuan sebelumnya! Silakan menunggu proses pengajuan anda."
            print(f"╔" + "═" * len(text) + "╗")
            print(f"║" + text + "║")
            print(f"╚" + "═" * len(text) + "╝")
            return 

    text = "Formulir Pengajuan Bantuan"
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")

    penghasilan = input("Masukkan jumlah penghasilan per bulan (dalam angka): ")
    if not penghasilan.isdigit() or len(penghasilan) < 5:
        print("Jumlah penghasilan harus berupa angka dan minimal 5 digit.")
        return

    tanggungan = input("Masukkan jumlah tanggungan keluarga: ")
    if not tanggungan.isdigit():
        print("Jumlah tanggungan harus berupa angka.")
        return

    k_pekerjaan = input("Apakah kehilangan pekerjaan? (ya/tidak): ").lower()
    if k_pekerjaan not in ["ya", "tidak"]:
        print("Jawaban harus 'ya' atau 'tidak'.")
        return

    bantuan_lain = input("Apakah tidak menerima bantuan lain? (ya/tidak): ").lower()
    if bantuan_lain not in ["ya", "tidak"]:
        print("Jawaban harus 'ya' atau 'tidak'.")
        return

    rentan = input("Apakah memiliki anggota keluarga rentan (sakit kronis, anak kecil, dll)? (ya/tidak): ").lower()
    if rentan not in ["ya", "tidak"]:
        print("Jawaban harus 'ya' atau 'tidak'.")
        return

    lns_dsb = input("Apakah anda adalah lansia/disabilitas yang tinggal sendiri? (ya/tidak): ").lower()
    if lns_dsb not in ["ya", "tidak"]:
        print("Jawaban harus 'ya' atau 'tidak'.")
        return

    ajuan1 = pd.read_csv(ajuan_csv)
    if ajuan1.empty:
        id_pengajuan = "P001"
    else:
        last_id = ajuan1.iloc[-1]["id_pengajuan"]
        num = int(''.join(filter(str.isdigit, last_id)))
        id_pengajuan = f"P{num + 1:03d}"

    timestamp = datetime.datetime.now()
    data_baru = pd.DataFrame([{
        "id_pengajuan": id_pengajuan,
        "id_akun": id_akun,
        "penghasilan": penghasilan,
        "jumlah_tanggungan": tanggungan,
        "kehilangan_pekerjaan": k_pekerjaan,
        "tidak_menerima_bantuan_lain": bantuan_lain,
        "memiliki_anggota_rentan": rentan,
        "lansia_atau_disabilitas_tinggal_sendiri": lns_dsb,
        "timestamp_pengajuan": timestamp,
        "status": "menunggu"
    }])

    ajuan1 = pd.concat([ajuan1, data_baru], ignore_index=True)
    ajuan1.to_csv(ajuan_csv, index=False)

    text = "Pengajuan Bantuan Berhasil!"
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")
    input("Tekan Enter untuk melanjutkan...")

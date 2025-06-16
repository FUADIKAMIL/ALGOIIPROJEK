import pandas as pd

def hasil():
    hasil_csv = "ALGOIIPROJEK/database/hasil_seleksi.csv"
    pengajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    masyarakat_csv = "ALGOIIPROJEK/database/masyarakat.csv"

    try:
        hasil = pd.read_csv(hasil_csv)
        pengajuan = pd.read_csv(pengajuan_csv)
        masyarakat = pd.read_csv(masyarakat_csv)
    except FileNotFoundError:
        print("Data hasil seleksi, pengajuan, atau masyarakat tidak ditemukan.")
        return

    if hasil.empty:
        print("Belum ada data hasil seleksi yang tersedia.")
        return

    gabung1 = pd.merge(hasil, pengajuan[['id_pengajuan', 'id_akun']], on='id_pengajuan', how='left')
    data = pd.merge(gabung1, masyarakat[['id_akun', 'nama_lengkap', 'nik']], on='id_akun', how='left')

    records = data.to_dict('records')
    n = len(records)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (records[j]['status_seleksi'], -records[j]['nilai']) > (records[j+1]['status_seleksi'], -records[j+1]['nilai']):
                records[j], records[j+1] = records[j+1], records[j]

    print(f"\n╔{'═' * 90}╗")
    print(f"║{'Daftar Hasil Seleksi BLT':^90}║")
    print(f"╠{'═' * 90}╣")
    for row in records:
        nama = row['nama_lengkap']
        status = row['status_seleksi']
        skor = row['nilai']
        bantuan = row['nominal_bantuan']
        id_pengajuan = row['id_pengajuan']
        print(f"║{id_pengajuan}. {nama:<25} | Status: {status:<9} | Skor: {skor:<4} | Bantuan: Rp{bantuan:<12,}║")
    print(f"╚{'═' * 90}╝")

    cari_nik = input("\nMasukkan NIK untuk mencari hasil seleksi: ")
    hasil_cari = None
    for row in records:
        if str(row['nik']) == str(cari_nik):
            hasil_cari = row
            break

    if hasil_cari:
        text = f"Data hasil seleksi untuk NIK {cari_nik}"
        print(f"╔" + f"{'═' * 63}" + "╗")
        print(f"║" + f"{'Daftar nama pengaju yang masuk: ':<63}" + "║")
        print(f"╠" + f"{'═' * 63}" + "╣")
        print(f"║Nama    : {hasil_cari['nama_lengkap']:<53}║")
        print(f"║Status  : {hasil_cari['status_seleksi']:<53}║")
        print(f"║Skor    : {hasil_cari['nilai']:<53}║")
        print(f"║Bantuan : Rp{hasil_cari['nominal_bantuan']:<51,}║")
        print(f"╚{'═' * 63}╝")
    else:
        print(f"\nData dengan NIK {cari_nik} tidak ditemukan.")

    input("\nTekan Enter untuk kembali ke menu utama...")
    return
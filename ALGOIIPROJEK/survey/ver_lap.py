import pandas as pd


def lapangan():
    hasil_csv = "ALGOIIPROJEK/database/hasil_seleksi.csv"
    hasil = pd.read_csv(hasil_csv)
    hasil = hasil[hasil['status_seleksi'].isin(['Lolos', 'Cadangan'])]
    if hasil.empty:
        print("Tidak ditemukan kandidat dengan status 'Lolos' atau 'Cadangan' untuk disurvei.")
        return
    
    if 'valid' not in hasil.columns:
        hasil['valid'] = None
    if 'catatan' not in hasil.columns:
        hasil['catatan'] = None
    filter = (hasil['status_seleksi'].isin(['Lolos', 'Cadangan'])) & (hasil['valid'].isnull())
    hasil_fil = hasil[filter].reset_index(drop=True)
    if hasil_fil.empty:
        print("Semua pengaju yang lolos seleksi sudah divalidasi.")
        return
    
    print("\nDAFTAR CALON YANG PERLU DISURVEI:")
    daftar_tampil = hasil_fil.to_dict('records')
    for idx, row in enumerate(daftar_tampil):
        print(f"{idx + 1}. ID Pengajuan: {row['id_pengajuan']}, Status: {row['status_seleksi']}")
    
    opsi = input("\nMasukkan nomor urut yang akan disurvey (kosongkan dan tekan Enter untuk kembali): ")
    if not opsi:
        print("Kembali.")
        return
    
    if not opsi.isdigit():
        print("Nomor urut harus berupa angka.")
        lapangan()
        return

    no_urut = int(opsi) - 1
    if not (0 <= no_urut < len(hasil_fil)):
        print("Nomor urut tidak ada dalam daftar.")
        lapangan()
        return
    calon = hasil_fil.iloc[no_urut]
    
    pengajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    pengajuan = pd.read_csv(pengajuan_csv)
    data_p = pengajuan[pengajuan['id_pengajuan'] == calon['id_pengajuan']].to_dict(orient='records')
    if not data_p:
        print("Data detail pengaju tidak ditemukan.")
        return
        
    print(f"\nData dari Bapak/Ibu {calon.get('nama_lengkap')}:")
    header_baru = {
        "id_pengajuan": "ID Pengajuan",
        "id_akun": "ID Akun",
        "penghasilan": "Penghasilan",
        "jumlah_tanggungan": "Jumlah Tanggungan",
        "kehilangan_pekerjaan": "Kehilangan Pekerjaan",
        "tidak_menerima_bantuan_lain": "Tidak Menerima Bantuan Lain",
        "memiliki_anggota_rentan": "Memiliki Anggota Rentan",
        "lansia_atau_disabilitas_tinggal_sendiri": "Lansia/Disabilitas/Tinggal Sendiri",
        "timestamp_pengajuan": "Waktu Pengajuan"
    }
    for key, value in data_p[0].items():
        final = header_baru.get(key, key)
        print(f"{final:<35}: {value}")

    valid = input("\nApakah data benar dan valid? (ya/tidak): ").lower()
    catatan = input("Catatan survei (jika ada): ")

    hasil.loc[hasil['id_pengajuan'] == calon['id_pengajuan'], 'valid'] = (valid == 'ya')
    hasil.loc[hasil['id_pengajuan'] == calon['id_pengajuan'], 'catatan'] = catatan
    hasil.to_csv(hasil_csv, index=False)
    print("\nHasil survei telah dikirim.")
    lapangan()
import pandas as pd

def penilaian(row):
    if row['tidak_menerima_bantuan_lain'].lower() == 'ya':
        return 0
    
    skor = 0
    penghasilan = int(row['penghasilan'])
    if penghasilan <= 1000000:
        skor += 3
    elif penghasilan <= 2500000:
        skor += 2
    else:
        skor += 1

    tanggungan = int(row['jumlah_tanggungan'])
    if tanggungan >= 2:
        skor += 2
    elif tanggungan == 1:
        skor += 1

    if row['kehilangan_pekerjaan'].lower() == 'ya':
        skor += 2
    if row['memiliki_anggota_rentan'].lower() == 'ya':
        skor += 1
    if row['lansia_atau_disabilitas_tinggal_sendiri'].lower() == 'ya':
        skor += 1
        
    return skor

def urutkan_dict(list_data, sort_key):
    if not list_data:
        return []

    max_skor = max(item[sort_key] for item in list_data)
    count_array = [0] * (max_skor + 1)
    for item in list_data:
        count_array[item[sort_key]] += 1

    for i in range(1, max_skor + 1):
        count_array[i] += count_array[i - 1]

    output_array = [None] * len(list_data)
    for i in range(len(list_data) - 1, -1, -1):
        item = list_data[i]
        skor = item[sort_key]
        posisi = count_array[skor] - 1
        output_array[posisi] = item
        count_array[skor] -= 1
        
    return output_array[::-1]

def seleksi():
    pengajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    masyarakat_csv = "ALGOIIPROJEK/database/masyarakat.csv"
    hasil_csv_path = "ALGOIIPROJEK/database/hasil_seleksi.csv"
    pengajuan = pd.read_csv(pengajuan_csv)
    masyarakat = pd.read_csv(masyarakat_csv)

    menunggu = pengajuan[pengajuan['status'] == 'menunggu']
    if menunggu.empty:
        print("Untuk sementara belum ada pengajuan yang masuk.")
        return
    join = pd.merge(menunggu, masyarakat, on='id_akun')
    print("Daftar nama pengaju yang masuk:")
    for i, nama in enumerate(join['nama_lengkap'], 1):
        print(f"{i}. {nama}")
    print(f"\nTerdapat sebanyak {len(join)} pengaju.")
    opsi = input("Lanjutkan proses seleksi? (ya/tidak): ")
    if opsi.lower() != 'ya':
        print("Proses seleksi dibatalkan.")
        return
    calon = join.to_dict('records')

    for nilai in calon:
        nilai['skor'] = penilaian(nilai)
    urut = urutkan_dict(calon, 'skor')

    maks_target = len(urut) // 2
    target = input(f"Masukkan jumlah target penerima (maks {maks_target}): ")
    if not target.isdigit() or not (0 < int(target) <= maks_target):
        print("Input jumlah target penerima tidak valid.")
        return
    target_int = int(target)

    sisa = len(urut) - target_int
    cadangan_maks = sisa // 2
    cadangan = input(f"Masukkan jumlah cadangan (maks {cadangan_maks}): ")
    if not cadangan.isdigit() or not (0 <= int(cadangan) <= cadangan_maks):
        print("Input jumlah penerima cadangan tidak valid.")
        return
    c_target = int(cadangan)

    nominal = input("Masukkan total nominal bantuan yang akan dibagikan: ")
    if not nominal.isdigit() or int(nominal) <= 0:
        print("Input nominal harus berupa angka positif.")
        return
    n_bantuan = int(nominal)

    total = target_int + c_target
    terpilih = urut[:total]
    bagian_rata = n_bantuan / target_int if target_int > 0 else 0
    for i, penerima in enumerate(terpilih):
        if i < target_int:
            penerima['status_seleksi'] = 'Lolos'
            penerima['nominal_bantuan'] = int(bagian_rata)
        else:
            penerima['status_seleksi'] = 'Cadangan'
            penerima['nominal_bantuan'] = 0

    hasil = pd.read_csv(hasil_csv_path)
    if hasil.empty:
        id_seleksi = "S001"
    else:
        last_id = hasil.iloc[-1]["id_seleksi"]
        num = int(''.join(filter(str.isdigit, last_id)))
        id_seleksi = f"S{num + 1:03d}"
    for penerima in terpilih:
        penerima['id_seleksi'] = id_seleksi

    data_baru = pd.DataFrame(terpilih)

    kolom = {
        'nama_lengkap': 'nama',
        'skor': 'nilai'
    }
    data_baru = data_baru.rename(columns=kolom)

    kolom = [
        'id_seleksi',
        'id_pengajuan',
        'nama',
        'nilai',
        'status_seleksi',
        'nominal_bantuan'
    ]
    data_untuk_disimpan = data_baru[kolom]

    hasil_akhir = pd.concat([hasil, data_untuk_disimpan], ignore_index=True)
    hasil_akhir.to_csv(hasil_csv_path, index=False)

    print("\nProses seleksi selesai. Data hasil seleksi telah disimpan.")
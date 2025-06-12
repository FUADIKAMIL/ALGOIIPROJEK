import pandas as pd

def penilaian(row):
    if row['tidak_menerima_bantuan_lain'].lower() == 'ya':
        return 0
    
    skor = 0
    penghasilan = int(row['penghasilan'])
    if penghasilan <= 1000000:
        skor += 5
    elif penghasilan <= 2500000:
        skor += 3
    else:
        skor += 1

    tanggungan = int(row['jumlah_tanggungan'])
    if tanggungan >= 3:
        skor += 3
    elif tanggungan >= 1:
        skor += 2

    if row['kehilangan_pekerjaan'].lower() == 'ya':
        skor += 3
    if row['memiliki_anggota_rentan'].lower() == 'ya':
        skor += 2
    if row['lansia_atau_disabilitas_tinggal_sendiri'].lower() == 'ya':
        skor += 2
    return skor

def ranked(skor):
    if skor >= 12:
        return 'Prioritas 1 (Mythic Immortal)'
    elif skor >= 8:
        return 'Prioritas 2 (Mythic)'
    elif skor >= 4:
        return 'Prioritas 3 (Legend)'
    elif skor > 0:
        return 'Prioritas 4 (Epic)'
    else:
        return 'Tidak Memenuhi Syarat'

def knapsack(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        value = values[i-1]
        weight = weights[i-1]
        for w in range(1, capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i-1][w], value + dp[i-1][w - weight])
            else:
                dp[i][w] = dp[i-1][w]

    selected_indices = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_indices.append(i-1)
            w -= weights[i-1]
            
    return selected_indices

def seleksi():
    pengajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    masyarakat_csv = "ALGOIIPROJEK/database/masyarakat.csv"
    hasil_csv = "ALGOIIPROJEK/database/hasil_seleksi.csv"
    pengajuan = pd.read_csv(pengajuan_csv)
    masyarakat = pd.read_csv(masyarakat_csv)
    hasil = pd.read_csv(hasil_csv)
    menunggu = pengajuan[pengajuan['status'] == 'menunggu']
    if menunggu.empty:
        print("Untuk sementara belum ada pengajuan yang masuk.")
        return
        
    join = pd.merge(menunggu, masyarakat, on='id_akun')
    calon = join.to_dict(orient='records')
    rank_calon = []
    for c in calon:
        c['skor'] = penilaian(c)
        c['tier'] = ranked(c['skor'])
        if c['tier'] != 'Tidak Memenuhi Syarat':
            if c['tier'] not in rank_calon:
                rank_calon.append(c['tier'])
    calon_layak = [c for c in calon if c['tier'] != 'Tidak Memenuhi Syarat']
    if not calon_layak:
        print("Tidak ada calon yang memenuhi syarat untuk diseleksi.")
        return
    print("Daftar nama pengaju yang masuk:")
    for i, c in enumerate(calon, 1):
        print(f"{i}. {c['nama_lengkap']:<20} - {c['tier']}")
    print(f"\nTerdapat sebanyak {len(join)} pengaju.")
    opsi = input("Lanjutkan proses seleksi? (ya/tidak): ")
    if opsi.lower() != 'ya':
        print("Proses seleksi dibatalkan.")
        return

    nominal_rank = {}
    print("\nSilakan tentukan nominal bantuan untuk setiap tier prioritas.")
    for tier in sorted(list(rank_calon)):
        while True:
            nominal = input(f"Masukkan nominal untuk {tier}: Rp ")
            if nominal.isdigit() and int(nominal) > 0:
                nominal_rank[tier] = int(nominal)
                break
            else:
                print("Input tidak valid. Masukkan angka positif.")

    for c in calon_layak:
        c['nominal_bantuan'] = nominal_rank.get(c['tier'], 0)
    anggaran = input("\nMasukkan total anggaran yang tersedia: Rp ")
    if not anggaran.isdigit() or int(anggaran) <= 0:
        print("Input anggaran tidak valid. Harus berupa angka positif.")
        return
    total_anggaran = int(anggaran)
    weights = [c['nominal_bantuan'] for c in calon_layak]
    values = [c['skor'] for c in calon_layak]
    
    seleksi = knapsack(weights, values, total_anggaran)
    lolos = [calon_layak[i] for i in seleksi]
    if not lolos:
        print("Tidak ada calon yang dapat dipilih dengan anggaran yang tersedia.")
        return
    print(f"\nSeleksi selesai. Ditemukan {len(lolos)} penerima yang lolos.")

    id_lolos = {p['id_akun'] for p in lolos}
    sisa = [c for c in calon_layak if c['id_akun'] not in id_lolos]
    if sisa:
        sisa = pd.DataFrame(sisa).sort_values(by='skor', ascending=False).to_dict(orient='records')
    else:
        sisa = []
    
    cadangan_maks = len(sisa)
    cadangan = input(f"Masukkan jumlah penerima cadangan (maks {cadangan_maks}): ")
    if not cadangan.isdigit() or not (0 <= int(cadangan) <= cadangan_maks):
        print("Input jumlah penerima cadangan tidak valid.")
        return
    jumlah_c = int(cadangan)
    penerima_cadangan = sisa[:jumlah_c]

    for p in lolos:
        p.update({'status_seleksi': 'Lolos'})
        
    for p in penerima_cadangan:
        p.update({'status_seleksi': 'Cadangan', 'nominal_bantuan': 0})

    terpilih = lolos + penerima_cadangan
    if hasil.empty:
        id_seleksi = "S001"
    else:
        last_id = hasil.iloc[-1]["id_seleksi"]
        num = int(''.join(filter(str.isdigit, last_id)))
        id_seleksi = f"S{num + 1:03d}"
        
    for p in terpilih:
        p['id_seleksi'] = id_seleksi

    data_baru = pd.DataFrame(terpilih)
    data_baru = data_baru.rename(columns={'nama_lengkap': 'nama', 'skor': 'nilai'})
    
    kolom = [
        'id_seleksi', 'id_pengajuan', 'nama', 'nilai', 
        'status_seleksi', 'nominal_bantuan'
    ]
    data_final = data_baru[kolom]

    hasil_akhir = pd.concat([hasil, data_final], ignore_index=True)
    hasil_akhir.to_csv(hasil_csv, index=False)

    print(f"\nProses seleksi selesai.")

seleksi()
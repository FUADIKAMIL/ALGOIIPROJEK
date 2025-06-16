import pandas as pd

def knapsack_greedy(calon_layak, total_anggaran):
    prioritas_bobot = {
        'Desil 1': 4,
        'Desil 2': 3,
        'Desil 3': 2,
        'Desil 4': 1
    }

    calon_layak.sort(key=lambda x: (-prioritas_bobot[x['tier']], -x['skor']))
    total_bobot = sum(prioritas_bobot[c['tier']] for c in calon_layak)
    nominal_per_bobot = total_anggaran // total_bobot if total_bobot > 0 else 0

    for c in calon_layak:
        c['bobot'] = prioritas_bobot[c['tier']]
        c['nominal_bantuan'] = c['bobot'] * nominal_per_bobot
        c['status_seleksi'] = 'Lolos'

    total_teralokasi = sum(c['nominal_bantuan'] for c in calon_layak)
    sisa = total_anggaran - total_teralokasi

    if sisa > 0:
        calon_layak.sort(key=lambda c: (-c['bobot'], -c['skor']))
        for i in range(sisa):
            calon_layak[i % len(calon_layak)]['nominal_bantuan'] += 1

    return calon_layak

def seleksi():
    pengajuan_csv = "ALGOIIPROJEK/database/pengajuan.csv"
    masyarakat_csv = "ALGOIIPROJEK/database/masyarakat.csv"
    hasil_csv = "ALGOIIPROJEK/database/hasil_seleksi.csv"

    pengajuan = pd.read_csv(pengajuan_csv)
    masyarakat = pd.read_csv(masyarakat_csv)
    try:
        hasil = pd.read_csv(hasil_csv)
    except:
        hasil = pd.DataFrame(columns=[
            'id_seleksi', 'id_pengajuan', 'nama',
            'nilai', 'status_seleksi', 'nominal_bantuan'
        ])

    menunggu = pengajuan[pengajuan['status'] == 'menunggu']
    if menunggu.empty:
        text = "Untuk sementara belum ada pengajuan yang masuk."
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + text + "║")
        print(f"╚" + "═" * len(text) + "╝")
        return 

    join = pd.merge(menunggu, masyarakat, on='id_akun')
    calon = join.to_dict(orient='records')

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
            return 'Desil 1'
        elif skor >= 8:
            return 'Desil 2'
        elif skor >= 4:
            return 'Desil 3'
        elif skor > 0:
            return 'Desil 4'
        else:
            return 'Tidak Memenuhi Syarat'

    for c in calon:
        c['skor'] = penilaian(c)
        c['tier'] = ranked(c['skor'])

    calon_layak = [c for c in calon if c['tier'] != 'Tidak Memenuhi Syarat']
    if not calon_layak:
        print("Tidak ada calon yang memenuhi syarat untuk diseleksi.")
        return 

    print(f"╔" + f"{'═' * 40}" + "╗")
    print(f"║" + f"{'Daftar nama pengaju yang masuk: ':<40}" + "║")
    print(f"╠" + f"{'═' * 40}" + "╣")
    for i, c in enumerate(calon_layak, 1):
        print(f"║" + f"{i}. {c['nama_lengkap']:<20} - {c['tier']:<14}" + "║")
    print(f"╚" + f"{'═' * 40}" + "╝")

    opsi = input("\nLanjutkan proses seleksi? (ya/tidak): ")
    if opsi.lower() != 'ya':
        print("Proses seleksi dibatalkan.")
        return 

    anggaran = input("\nMasukkan total anggaran yang tersedia: Rp ")
    if not anggaran.isdigit() or int(anggaran) <= 0:
        print("Input anggaran tidak valid. Harus berupa angka positif.")
        return seleksi()
    total_anggaran = int(anggaran)

    penerima_terpilih = knapsack_greedy(calon_layak, total_anggaran)

    id_lolos = {p['id_akun'] for p in penerima_terpilih}
    sisa = [c for c in calon_layak if c['id_akun'] not in id_lolos]
    sisa.sort(key=lambda x: -x['skor'])

    cadangan_maks = len(sisa)
    cadangan = input(f"Masukkan jumlah penerima cadangan (maks {cadangan_maks}): ")
    if not cadangan.isdigit() or not (0 <= int(cadangan) <= cadangan_maks):
        print("Input jumlah penerima cadangan tidak valid.")
        return

    jumlah_c = int(cadangan)
    penerima_cadangan = sisa[:jumlah_c]
    for p in penerima_cadangan:
        p['status_seleksi'] = 'Cadangan'
        p['nominal_bantuan'] = 0

    terpilih = penerima_terpilih + penerima_cadangan

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

    text = f"Proses seleksi selesai. Ditemukan {len(penerima_terpilih)} penerima dan {jumlah_c} cadangan."
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")

    final = hasil_akhir.to_dict(orient='records')

    print(f"╔" + f"{'═' * 63}" + "╗")
    print(f"║" + f"{'Daftar nama pengaju yang lolos: ':<63}" + "║")
    print(f"╠" + f"{'═' * 63}" + "╣")
    for key in final:
        tier = key.get('tier', '-')
        print(f"║" + f"{key['id_pengajuan']}. {key['nama']:<25} - {tier} >>> Rp.{key['nominal_bantuan']:<20}" + "║")
    print(f"╚" + f"{'═' * 63}" + "╝")
    input("Tekan Enter untuk kembali ke menu admin...") 
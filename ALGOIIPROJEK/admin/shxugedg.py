import pandas as pd
from admin.main_admin import menu_admin

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
        print("Untuk sementara belum ada pengajuan yang masuk.")
        menu_admin()

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
        text = "Tidak ada calon yang memenuhi syarat untuk diseleksi."
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + text + "║")
        print(f"╚" + "═" * len(text) + "╝")
        menu_admin

    print(f"╔" + f"{'═' * 63}" + "╗")
    print(f"║" + f"{'Daftar nama pengaju yang masuk: ':<63}" + "║")
    print(f"╠" + f"{'═' * 63}" + "╣")
    for i, c in enumerate(calon_layak, 1):
        print(f"║" + f"{i}. {c['nama_lengkap']:<30}" + "-" + f"{c['tier']:<29}" + "║")
    print(f"╚" + f"{'═' * 63}" + "╝")

    print(f"\nTerdapat sebanyak {len(calon_layak)} pengaju layak.")
    opsi = input("Lanjutkan proses seleksi? (ya/tidak): ")
    if opsi.lower() != 'ya':
        text = "Proses seleksi dibatalkan."
        print(f"╔" + "═" * len(text) + "╗")
        print(f"║" + text + "║")
        print(f"╚" + "═" * len(text) + "╝")
        return menu_admin()

    anggaran = input("\nMasukkan total anggaran yang tersedia: Rp ")
    if not anggaran.isdigit() or int(anggaran) <= 0:
        print("Input anggaran tidak valid. Harus berupa angka positif.")
        return seleksi()
    total_anggaran = int(anggaran)

    prioritas_bobot = {
        'Desil 1': 4,
        'Desil 2': 3,
        'Desil 3': 2,
        'Desil 4': 1
    }

    penerima_terpilih = []
    tier_map = {}
    for c in calon_layak:
        tier_map.setdefault(c['tier'], []).append(c)

    aktif_tier = [t for t in prioritas_bobot if t in tier_map]

    for t in aktif_tier:
        daftar = tier_map[t]
        for orang in daftar:
            orang['bobot'] = prioritas_bobot[t]
            penerima_terpilih.append(orang)

    total_bobot = sum(p['bobot'] for p in penerima_terpilih)

    for p in penerima_terpilih:
        p['nominal_bantuan'] = (p['bobot'] * total_anggaran) // total_bobot
        p['status_seleksi'] = 'Lolos'

    total_teralokasi = sum(p['nominal_bantuan'] for p in penerima_terpilih)
    sisa = total_anggaran - total_teralokasi

    penerima_terpilih.sort(key=lambda x: (-x['bobot'], -x['skor']))
    for i in range(sisa):
        penerima_terpilih[i % len(penerima_terpilih)]['nominal_bantuan'] += 1

    id_lolos = {p['id_akun'] for p in penerima_terpilih}
    sisa = [c for c in calon_layak if c['id_akun'] not in id_lolos]
    sisa.sort(key=lambda x: -x['skor'])

    cadangan_maks = len(sisa)
    cadangan = input(f"Masukkan jumlah penerima cadangan (maks {cadangan_maks}): ")
    if not cadangan.isdigit() or not (0 <= int(cadangan) <= cadangan_maks):
        print("Input jumlah penerima cadangan tidak valid.")
        exit()
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

    text = f"\nProses seleksi selesai. Ditemukan {len(penerima_terpilih)} penerima dan {jumlah_c} cadangan."
    print(f"╔" + "═" * len(text) + "╗")
    print(f"║" + text + "║")
    print(f"╚" + "═" * len(text) + "╝")
    final = hasil_akhir.to_dict(orient='records')

    print(f"╔" + f"{'═' * 63}" + "╗")
    print(f"║" + f"{'Daftar nama pengaju yang masuk: ':<63}" + "║")
    print(f"╠" + f"{'═' * 63}" + "╣")
    for key in final:
        tier = key.get('tier', '-')
        print(f"║" + f"{key['id_pengajuan']}. {key['nama']:<25} - {tier} >>> Rp.{key['nominal_bantuan']:<20}" + "║")
    print(f"╚" + f"{'═' * 63}" + "╝")
    input("Tekan Enter untuk kembali ke menu admin...")
    return menu_admin()

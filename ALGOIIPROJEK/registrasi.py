import pandas as pd

def registrasi():
    print("\n>>> REGISTRASI AKUN MASYARAKAT <<<")
    nama = input("Nama lengkap: ")
    nik = input("NIK: ")
    if not nik.isdigit():
        print("NIK harus berupa angka.")
        return
    no_kk = input("Nomor KK: ")
    if not no_kk.isdigit():
        print("Nomor KK harus berupa angka.")
        return
    alamat = input("Alamat: ")
    no_hp = input("Nomor HP: ")
    username = input("Username: ")
    password = input("Password: ")

    m_csv = "ALGOIIPROJEK/database/masyarakat.csv"
    masyarakat = pd.read_csv(m_csv)
    if not masyarakat[masyarakat["no_kk"] == no_kk].empty:
        print("Nomor KK sudah terdaftar.")
        return
    if masyarakat.empty:
        id_baru = "M001"
    else:
        last_id = masyarakat.iloc[-1]["id_akun"]
        num = int(''.join(filter(str.isdigit, last_id)))
        id_baru = f"M{num + 1:03d}"

    data_baru = pd.DataFrame([{
        "id_akun": id_baru,
        "username": username,
        "password": password,
        "nama_lengkap": nama,
        "nik": nik,
        "no_kk": no_kk,
        "alamat": alamat,
        "no_hp": no_hp,
    }])

    masyarakat = pd.concat([masyarakat, data_baru], ignore_index=False)
    masyarakat.to_csv(m_csv, index=False)

    print("Registrasi berhasil! Silakan login untuk melanjutkan.")
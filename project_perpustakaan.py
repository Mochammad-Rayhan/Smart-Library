import requests
from datetime import datetime, timedelta
import pandas as pd

def garis():
    print("=" * 60)

# Penyimpanan data
members = {
    'example@gmail.com': {
        'email': 'example@gmail.com',
        'password': 'example',
        'nama': 'Mochammad Rayhan',
        'hp': '0812345678910',
        'alamat': 'Gang Senyum No.29C',
        'ttl': 'Mars, 1 jan 2000',
        'books': [] 
    }
}

# Waktu
today = datetime.now()
tujuhHariKemudian = today + timedelta(days=7)
format_today = today.strftime("%d-%m-%Y")
format_tujuhHariKemudian = tujuhHariKemudian.strftime("%d-%m-%Y")

#Fungsi Daftar Member
def daftar_member():
    # Loop untuk validasi email
    while True:
        email = input("Masukkan email Anda: ").lower()
        if not email or "@" not in email or ".com" not in email.split("@")[-1]:
            print("Format email tidak valid. Silakan coba lagi.")
        elif email in members:
            print("Email sudah terdaftar. Silakan gunakan email lain.")
        else:
            break
        
    # Validasi password dengan loop
    while True:
        password = input("Masukkan password Anda (minimal 5 karakter): ")
        if len(password) < 5:
            print("Password terlalu pendek. Minimal 5 karakter.")
        else:
            break
        
    nama = input("Masukkan nama Anda: ")
     
    while True:
        hp = input("Masukkan nomor handphone Anda: ")
        if not hp.isdigit() or len(hp) < 10:
            print("Nomor handphone harus berupa angka dan minimal 10 digit. Silakan coba lagi.")
        else:
            break
        
    alamat = input("Masukkan alamat tinggal Anda: ")
    ttl = input("Masukkan Tempat tanggal lahir Anda: ")
    


    members[email] = {'email': email, 'password': password, 'nama': nama, 'hp': hp, 'alamat': alamat, 'ttl': ttl, 'books': []}
    print("Pendaftaran berhasil! Selamat datang, member baru!")

# API pencarian buku
def api(title):
    link_api = "https://openlibrary.org/search.json"
    params = {"q": title}
    try:
        response = requests.get(link_api, params=params)
        response.raise_for_status()
        data = response.json()
        if 'docs' in data and data['docs']:
            for buku in data['docs'][:10]:
                print("Judul Buku    :", buku.get('title', 'Tidak diketahui'))
                print("Penulis Buku  :", ', '.join(buku.get('author_name', ['Tidak diketahui'])))
                print("Tahun Terbit  :", buku.get('first_publish_year', 'Tidak diketahui'))
                print("Tempat Dibuat :", ', '.join(buku.get('publish_place', ['Tidak diketahui'])))
                print("Jumlah Halaman:", buku.get('number_of_pages_median', 'Tidak diketahui'))
                print("Kode ISBN buku: " ,','.join(buku.get('isbn', ['Tidak Diketahui'])[:1]))
                print("=" * 50)
        else:
            print("Buku tidak ditemukan.")
    except requests.exceptions.RequestException as e:
        print("Gagal mengambil data dari API. Pastikan Anda terhubung ke internet.")
        print("Error detail:", e)
   
# Peminjaman buku
def cari_buku(email):
    while True:
        try:
            jmlhPinjamBuku = int(input("Banyak buku yang ingin dipinjam: "))
            if jmlhPinjamBuku <= 0:
                print("Jumlah buku harus lebih dari 0. Silakan coba lagi.")
            else:
                break
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

    for i in range(jmlhPinjamBuku):
        cari = input(f"Silahkan cari judul buku ke-{i + 1}: ")
        print("=" * 50)
        api(cari)
        pilih_buku = input("Silahkan masukan buku yang mau dipinjam: ")
        keterangan = input("Keterangan peminjaman: ")
        members[email]['books'].append({'judul': pilih_buku, 'keterangan': keterangan, 'status': 'Belum dikembalikan'})
        print("Buku Anda telah tersimpan! Silakan cetak bukti.")


# Pengembalian buku
def kembalikan_buku(email):
    if not members[email]['books']:
        print("\nBelum ada buku yang dipinjam. Tidak ada yang bisa dikembalikan.")
        return

    print("\nDaftar Buku yang Dipinjam:")
    for i, buku in enumerate(members[email]['books'], 1):
        status = buku['status']
        print(f"{i}. {buku['judul']} - Keterangan: {buku['keterangan']} - Status: {status}")
    
    try:
        pilihan = int(input("\nMasukkan nomor buku yang ingin dikembalikan: "))
        if 1 <= pilihan <= len(members[email]['books']):
            buku_dikembalikan = members[email]['books'][pilihan - 1]
            if buku_dikembalikan['status'] == 'Sudah Dikembalikan':
                print("Buku ini sudah dikembalikan sebelumnya.")
            else:
                buku_dikembalikan['status'] = 'Sudah Dikembalikan'
                print(f"Buku '{buku_dikembalikan['judul']}' berhasil dikembalikan. Terima kasih!")
        else:
            print("Pilihan tidak valid.")
    except ValueError:
        print("Masukkan angka yang valid.")

# Cek buku yang dipinjam
def lihat_buku_dipinjam(email):
    if not members[email]['books']:
        print("\nBelum ada buku yang dipinjam.")
        return

    print("\nDaftar Buku yang Dipinjam:")
    print("=" * 50)
    for i, buku in enumerate(members[email]['books'], 1):
        status = buku['status']
        print(f"{i}. Judul buku  : {buku['judul']}")
        print(f"   Keterangan  : {buku['keterangan']}")
        print(f"   Status      : {status}")
        print("=" * 50)

# Login member
def login_member():
    email = input("Masukkan email Anda: ")
    password = input("Masukkan password Anda: ")

    if email in members and members[email]['password'] == password:
        print(f"Login berhasil! Selamat datang, {members[email]['nama']}!")
        return email
    elif email in members:
        print("Password salah. Silakan coba lagi.")
        return None
    else:
        print("Email tidak ditemukan. Silakan daftar terlebih dahulu.")
        return None

# Cetak bukti peminjaman
def cetak_bukti(email):
    if not members[email]['books']:
        print("\nBelum ada buku yang dipinjam. Silakan pinjam buku terlebih dahulu.")
        return

    garis()
    print("|\t\t-- SMART LIBRARY --\t\t\t   |")
    print("|\t\t Jalan Rawa Bebek No.31 \t\t   |")
    garis()
    print("\t\t KARTU PEMINJAMAN BUKU \t\t\t   ")
    print(f"Nama Peminjam : {members[email]['nama']} \t\t\t\t   ")
    print(f"Alamat Peminjam : {members[email]['alamat']} \t\t\t\t\t  ")
    garis()

    data_pd = {
        "No": range(1, len(members[email]['books']) + 1),
        "Judul Buku": [book['judul'] for book in members[email]['books']],
        "Keterangan": [book['keterangan'] for book in members[email]['books']],
        "Tanggal Pinjam" : format_today,
        "Tanggal Kembali" : format_tujuhHariKemudian
    }
    data_pd_df = pd.DataFrame(data_pd)
    print(data_pd_df.to_string(index=False))
    garis()
    print("| Harap kembalikan buku tepat waktu. \t\t\t   |")
    print("| Terima kasih telah menggunakan layanan kami! \t\t   |")
    garis()

# Menu utama digital library
def menu_utama(email):
    while True:
        print("\n--- Selamat datang di Smart Library ---")
        print("1. Lihat Buku Yang Dipinjam")
        print("2. Pinjam Buku")
        print("3. Cetak Bukti")
        print("4. Kembalikan Buku")
        print("5. Logout")
        pilihan_menu = input("Pilih menu (1/2/3/4/5): ")

        if pilihan_menu == "1":
            if members[email]['books']:
                print("\nDaftar Buku yang Dipinjam:")
                for i, buku in enumerate(members[email]['books'], 1):
                    status = buku['status']
                    print(f"{i}. {buku['judul']} - Keterangan: {buku['keterangan']} - Status: {status}")
            else:
                print("\nBelum ada buku yang dipinjam.")
        elif pilihan_menu == "2":
            cari_buku(email)
        elif pilihan_menu == "3":
            cetak_bukti(email)
        elif pilihan_menu == "4":
            kembalikan_buku(email)
        elif pilihan_menu == "5":
            print("Anda telah logout.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menu utama pendaftaran
while True:
    print("\n--- Selamat datang diaplikasi Smart Library ---")
    print("1. Login")
    print("2. Daftar member baru")
    print("3. Keluar")
    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == "1":
        email = login_member()
        if email:
            menu_utama(email)
    elif pilihan == "2":
        daftar_member()
    elif pilihan == "3":
        print("Terima kasih! Sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
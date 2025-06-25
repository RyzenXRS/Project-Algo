import csv
import pandas as pd
import os
from tabulate import tabulate as tb 
from merge import merge_sort
from knapsack import knapsack_rating
from quick_sort import quick_sort

BUKU_FILE = 'buku.csv'
USER_FILE = 'users.csv'
PESANAN_FILE = 'pesanan.csv'

BUKU_FIELDNAMES = ['judul', 'tahun', 'penulis', 'stok', 'harga', 'rating']


# ========== CSV Stuff =============
def judul_apk():
    teks = '''

  
 ██████╗ ██████╗  █████╗ ███╗   ███╗███████╗██████╗ ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝ ██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║  ███╗██████╔╝███████║██╔████╔██║█████╗  ██║  ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██║  ██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██████╔╝██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                 
                                                       
    '''
    print (teks)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_csv(filename):
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            # Pastikan semua buku memiliki kunci 'rating' (default ke '0' jika tidak ada)
            loaded_data = []
            for row in reader:
                if 'rating' not in row:
                    row['rating'] = '0' # Default rating jika tidak ada
                loaded_data.append(row)
            return loaded_data
    except FileNotFoundError:
        print(f"Error: File '{filename}' tidak ditemukan. Membuat file baru.")
        return []
    except Exception as e:
        print(f"Error saat membaca file '{filename}': {e}")
        return []
    
def save_csv(filename, data, fieldnames):
    try:
        with open(filename, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error saat menyimpan file '{filename}': {e}")

def append_csv(filename, row, fieldnames):
    file_exists = os.path.exists(filename)
    try:
        with open(filename, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Error saat menambahkan data ke file '{filename}': {e}")
            
# ===== Algoritma =====


def binary_search(data, target, key):
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid][key].lower() == target.lower():
            return mid
        elif data[mid][key].lower() < target.lower():
            low = mid + 1
        else:
            high = mid - 1
    return -1

# ===== Login & Register =====
def login():
    users = load_csv(USER_FILE)
    print("=== Login ===")
    try:
        username = input("Username : ")
        password = input("Password : ")
    except Exception as e:
        print(f"Input error: {e}")
        return None, None
    clear_screen()

    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f"\nSelamat datang, {username}!\n")
            return user['role'], username
    print("Login gagal! Periksa kembali username/password.")
    return None, None

def register():
    users = load_csv(USER_FILE)
    cek_nama = [user['username'] for user in users]

    print("=== Registrasi ===")
    while True:
        try:
            nama = input("Masukkan username: ").strip()
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if nama in cek_nama:
            print("Username tidak tersedia. Silakan coba lagi.")
        else:
            break

    try:
        password = input("Masukkan password: ").strip()
    except Exception as e:
        print(f"Input error: {e}")
        return

    print("-" * 26)
    print("Konfirmasi Pendaftaran :")
    print(" [1] Iya")
    print(" [2] Batal")
    print("-" * 26)

    while True:
        try:
            pilih = input("Pilih menu [1/2]: ")
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if pilih == '1':
            new_user = {
                'username': nama,
                'password': password,
                'role': 'user'
            }
            append_csv(USER_FILE, new_user, ['username', 'password', 'role'])

            print("\n==== Registrasi berhasil! ====")
            print(f"'{nama}' telah ditambahkan sebagai Pembeli baru.")
            print("Selamat Datang di Aplikasi Manajemen")
            input("Tekan Enter untuk kembali ke Menu.")
            break
        elif pilih == '2':
            print("=" * 40)
            print("Pembuatan Akun dibatalkan.")
            input("Tekan Enter untuk kembali ke Menu.")
            break
        else:
            print("Pilihan tidak valid.")

# Fungsi 
def atur_stok_buku():
    while True:
        clear_screen()
        books = load_csv(BUKU_FILE)
        if not books:
            print("Tidak ada data buku yang tersedia.")
            input("Tekan Enter untuk kembali ke Dashboard Admin.")
            return
        print("\n--- Atur Stok Buku ---")
        headers = ['No.', 'Judul', 'Penulis', 'Stok Saat Ini']
        table_data = []
        for i, b in enumerate(books):
            table_data.append([i + 1, b['judul'], b['penulis'], b['stok']])
        print(tb(table_data, headers=headers, tablefmt='double_grid'))
        print("\nOpsi Atur Stok:")
        print("9. Kembali ke Dashboard Admin")
        try:
            pilihan_buku = input("Masukkan nomor buku yang ingin diatur stoknya (atau '9' untuk kembali): ").strip()
            if pilihan_buku == '9':
                break
            index_buku = int(pilihan_buku) - 1
            if 0 <= index_buku < len(books):
                buku_terpilih = books[index_buku]
                print(f"\nMengatur stok untuk buku: '{buku_terpilih['judul']}' oleh '{buku_terpilih['penulis']}' (Stok saat ini: {buku_terpilih['stok']})")
                try:
                    jumlah_perubahan = int(input("Masukkan jumlah perubahan stok (positif untuk menambah, negatif untuk mengurangi): "))
                    current_stok = int(buku_terpilih['stok'])
                    new_stok = current_stok + jumlah_perubahan
                    if new_stok < 0:
                        print(f"Peringatan: Stok tidak bisa kurang dari 0. Stok buku '{buku_terpilih['judul']}' tidak diubah.")
                    else:
                        buku_terpilih['stok'] = str(new_stok)
                        save_csv(BUKU_FILE, books, BUKU_FIELDNAMES)
                        print(f"Stok buku '{buku_terpilih['judul']}' berhasil diperbarui menjadi {new_stok}.")
                except ValueError:
                    print("Input tidak valid. Masukkan angka untuk jumlah perubahan stok.")
                except Exception as e:
                    print(f"Terjadi kesalahan: {e}")
            else:
                print("Nomor buku tidak valid.")
        except ValueError:
            print("Input tidak valid. Masukkan nomor buku yang benar.")
        except Exception as e:
            print(f"Input error: {e}")
        input("Tekan Enter untuk melanjutkan.")

# ===== Dashboard =====
def user_dashboard(username):
    cart = []

    def lihat_daftar_buku():
        while True:
            clear_screen()
            books = load_csv(BUKU_FILE)
            books = merge_sort(books)
            for b in books:
                if 'rating' not in b:
                    b['rating'] = '0'
            
            headers = ['Judul', 'Penulis', 'Tahun', 'Stok', 'Harga', 'Rating']
            table = [[b['judul'], b['penulis'], b['tahun'], b['stok'], b['harga'], b['rating']] for b in books]
            print(tb(table, headers=headers, tablefmt='double_grid'))
            print("\nMenu Lihat Daftar Buku:")
            print("9. Kembali ke Dashboard")
            try:
                pilihan = input("Masukkan pilihan (angka): ")
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if pilihan == '9':
                break
            else:
                print("Pilihan tidak valid.")

    def cari_buku():
        while True:
            clear_screen()
            books = load_csv(BUKU_FILE)
            
            if not books:
                print(f"Error: Tidak ada data buku di {BUKU_FILE}. Pastikan file ada dan berisi data.")
                input("Tekan Enter untuk kembali ke menu pencarian.")
                continue
            books = quick_sort(books, 'judul')
            print("\nMenu Cari Buku:")
            print("1. Cari Buku berdasarkan judul (Binary Search)")
            print("9. Kembali ke Dashboard")
            
            try:
                pilihan = input("Masukkan pilihan (angka): ")
            except Exception as e:
                print(f"Input error: {e}")
                input("Tekan Enter untuk melanjutkan.")
                continue

            if pilihan == '1':
                try:
                    target = input("Masukkan judul buku yang dicari (harus tepat): ").strip()  
                except Exception as e:
                    print(f"Input error: {e}")
                    input("Tekan Enter untuk melanjutkan.")
                    continue

                if not target:
                    print("Judul tidak boleh kosong.")
                    input("Tekan Enter untuk melanjutkan.")
                    continue
                index = binary_search(books, target, 'judul')
                
                if index != -1:
                    found_book = books[index]
                    headers = ['Judul', 'Penulis', 'Tahun', 'Harga']
                    table = [[found_book['judul'], found_book['penulis'], found_book['tahun'], found_book['harga']]]
                    print("\nHasil Pencarian Buku (Binary Search):")
                    print(tb(table, headers=headers, tablefmt='double_grid'))
                else:
                    print(f"Buku dengan judul '{target}' tidak ditemukan.")
                
                input("Tekan Enter untuk kembali ke menu pencarian.")
                       
            elif pilihan == '9':
                break
            else:
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk melanjutkan.")

    def tambah_buku_keranjang():
        while True:
            clear_screen()
            books = load_csv(BUKU_FILE)
            books = merge_sort(books) 

            if not books:
                print("Tidak ada buku yang tersedia untuk ditambahkan ke keranjang.")
                input("Tekan Enter untuk kembali ke Dashboard User.")
                return

            print("\n--- Daftar Buku Tersedia ---")
            headers = ['No.', 'Judul', 'Penulis', 'Stok', 'Harga']
            table_data = []
            for i, b in enumerate(books):
                if int(b.get('stok', '0')) > 0:
                    table_data.append([i + 1, b['judul'], b['penulis'], b['stok'], b['harga']])
            if not table_data:
                print("Tidak ada buku yang tersedia atau stok habis.")
                input("Tekan Enter untuk kembali ke Dashboard User.")
                return

            print(tb(table_data, headers=headers, tablefmt='double_grid'))

            print("\nMenu Tambah Buku ke Keranjang:")
            print("9. Kembali ke Dashboard")
            try:
                pilihan_buku = input("Masukkan nomor buku yang ingin ditambahkan ke keranjang (atau '9' untuk kembali): ").strip()
                if pilihan_buku == '9':
                    break

                index_buku = int(pilihan_buku) - 1
                if 0 <= index_buku < len(books):
                    buku_terpilih = books[index_buku]
                    if int(buku_terpilih.get('stok', '0')) > 0:
                        cart.append(buku_terpilih)
                        print(f"Buku '{buku_terpilih['judul']}' berhasil ditambahkan ke keranjang.")
                    else:
                        print(f"Stok buku '{buku_terpilih['judul']}' sudah habis.")
                else:
                    print("Nomor buku tidak valid.")
            except ValueError:
                print("Input tidak valid. Masukkan nomor buku yang benar.")
            except Exception as e:
                print(f"Input error: {e}")

            input("Tekan Enter untuk melanjutkan.")

    def lihat_konfirmasi_pesanan():
        while True:
            clear_screen()
            if not cart:
                print("Keranjang kosong.")
                input("Tekan Enter untuk kembali ke Dashboard.")
                break
            total = sum(int(b['harga']) for b in cart)
            print("\n--- Konfirmasi Pesanan ---")
            headers = ['Judul', 'Harga']
            table = [[b['judul'], b['harga']] for b in cart]
            print(tb(table, headers=headers, tablefmt='double_grid'))
            print(f"Total harga: {total}")
            print("Konfirmasi pesanan? (y/n)")
            try:
                konfirmasi = input("Masukkan pilihan: ")
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if konfirmasi.lower() == 'y':
                books = load_csv(BUKU_FILE)
                valid_order = True
                for b in cart:
                    found = False
                    for book in books:
                        if book['judul'].lower() == b['judul'].lower():
                            found = True
                            if int(book['stok']) <= 0:
                                print(f"Stok buku '{book['judul']}' habis. Pesanan untuk buku ini dibatalkan.")
                                valid_order = False
                            break
                    if not found:
                        print(f"Buku '{b['judul']}' tidak ditemukan di database.")
                        valid_order = False
                if valid_order:
                    for b in cart:
                        for book in books:
                            if book['judul'].lower() == b['judul'].lower():
                                book['stok'] = str(int(book['stok']) - 1)
                                append_csv(PESANAN_FILE, {
                                    'username': username,
                                    'judul': b['judul'],
                                    'harga': b['harga'],
                                    'status': 'Menunggu Konfirmasi'
                                }, ['username', 'judul', 'harga', 'status'])
                                break
                    save_csv(BUKU_FILE, books, BUKU_FIELDNAMES)
                    print("Pesanan dikonfirmasi. Stok buku diperbarui. Menunggu konfirmasi admin.")
                    cart.clear()
                else:
                    print("Pesanan tidak dapat diproses karena beberapa buku tidak valid atau stok habis.")
            elif konfirmasi.lower() == 'n':
                print("Pesanan dibatalkan.")
            else:
                print("Pilihan tidak valid.")

    def sesuaikan_budget():
        while True:
            clear_screen()
            print("\nMenu Sesuaikan Budget (Knapsack):")
            print("1. Masukkan budget maksimal")
            print("9. Kembali ke Dashboard")
            try:
                pilihan = input("Masukkan pilihan (angka): ")
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if pilihan == '1':
                try:
                    budget = int(input("Masukkan budget maksimal: "))
                except ValueError:
                    print("Input tidak valid. Masukkan angka untuk budget.")
                    continue
                books = load_csv(BUKU_FILE)
                result = knapsack_rating(budget, books)
                headers = ['Judul', 'Penulis', 'Tahun', 'Harga', 'Rating']
                table = [[b['judul'], b['penulis'], b['tahun'], b['harga'], b.get('rating', '0')] for b in result]
                print("Rekomendasi buku sesuai budget :")
                print(tb(table, headers=headers, tablefmt='double_grid'))
                input("Tekan Enter untuk kembali ke menu budget.")
            elif pilihan == '9':
                break
            else:
                print("Pilihan tidak valid.")

    def cek_status_pesanan():
        while True:
            clear_screen()
            pesanan = load_csv(PESANAN_FILE)
            user_pesanan = [p for p in pesanan if p['username'] == username]
            if not user_pesanan:
                print("Tidak ada pesanan untuk pengguna ini.")
                input("Tekan Enter untuk kembali ke Dashboard.")
                break
            headers = ['Judul', 'Harga', 'Status']
            table = [[p['judul'], p['harga'], p['status']] for p in user_pesanan]
            print("\n--- Status Pesanan ---")
            print(tb(table, headers=headers, tablefmt='double_grid'))
            print("\nApakah ada pesanan yang sudah diterima?")
            print("1. Ubah status pesanan menjadi 'Diterima'")
            print("9. Kembali ke Dashboard")
            try:
                konfirmasi = input("Masukkan pilihan (angka): ")
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if konfirmasi == '1':
                try:
                    judul = input("Masukkan judul buku yang sudah diterima: ").strip()
                except Exception as e:
                    print(f"Input error: {e}")
                    continue
                found = False
                for p in pesanan:
                    if p['username'] == username and p['judul'].lower() == judul.lower() and p['status'] == 'Dikirim':
                        p['status'] = 'Diterima'
                        found = True
                        break
                if found:
                    save_csv(PESANAN_FILE, pesanan, ['username', 'judul', 'harga', 'status'])
                    print(f"Status pesanan untuk '{judul}' diubah menjadi 'Diterima'.")
                else:
                    print("Pesanan tidak ditemukan atau belum dalam status 'Dikirim'.")
                input("Tekan Enter untuk kembali ke menu status pesanan.")
            elif konfirmasi == '9':
                break
            else:
                print("Pilihan tidak valid.")

    while True:
        print("\n--- Dashboard User ---")
        print("1. Lihat Daftar Buku")
        print("2. Cari Buku")
        print("3. Tambah Buku ke Keranjang")
        print("4. Lihat & Konfirmasi Pesanan")
        print("5. Sesuaikan Budget (Knapsack)")
        print("6. Cek Status Pesanan")
        print("0. Logout")
        try:
            pilihan = input("Masukkan Pilihan : ")
        except Exception as e:
            print(f"Input error: {e}")
            continue

        if pilihan == '1':
            lihat_daftar_buku()
        elif pilihan == '2':
            cari_buku()
        elif pilihan == '3':
            tambah_buku_keranjang()
        elif pilihan == '4':
            lihat_konfirmasi_pesanan()
        elif pilihan == '5':
            sesuaikan_budget()
        elif pilihan == '6':
            cek_status_pesanan()
        elif pilihan == '0':
            clear_screen()
            print("Anda telah logout.")
            return
        else:
            print("Pilihan tidak valid.")

def admin_dashboard():
    while True:
        clear_screen()
        print("\n--- Dashboard Admin ---")
        print("1. Lihat Buku")
        print("2. Tambah Buku")
        print("3. Edit Buku")
        print("4. Hapus Buku")
        print("5. Atur Stok Buku")
        print("6. Kelola Pesanan")
        print("0. Logout")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            clear_screen()
            books = load_csv(BUKU_FILE)
            books = merge_sort(books)
            for b in books:
                if 'rating' not in b:
                    b['rating'] = '0'
            headers = ['Judul', 'Penulis', 'Tahun', 'Stok', 'Harga', 'Rating']
            table = [[b['judul'], b['penulis'], b['tahun'], b['stok'], b['harga'], b['rating']] for b in books]
            print(tb(table, headers=headers, tablefmt='double_grid'))
            input("Tekan Enter untuk melanjutkan.")

        elif pilihan == '2':
            clear_screen()
            books = load_csv(BUKU_FILE)
            new_judul = input("Masukkan Judul Buku : ").strip()
            new_tahun = input("Tahun Terbit: ").strip()
            new_penulis = input("Penulis : ").strip()
            new_stok = input("Stok : ").strip()
            new_harga = input("Harga : ").strip()
            new_rating = input("Rating (0.0 - 5.0, gunakan titik desimal): ").strip() 

            if not all([new_judul, new_tahun, new_penulis, new_stok, new_harga, new_rating]):
                print("Mohon masukkan semua data dengan benar.")
                input("Tekan Enter untuk melanjutkan.")
                continue

            found = False
            try:
                input_stok = int(new_stok)
                input_rating = float(new_rating) 
                if not (0.0 <= input_rating <= 5.0):
                    print("Rating harus antara 0.0 dan 5.0.")
                    input("Tekan Enter untuk melanjutkan.")
                    continue
            except ValueError:
                print("Stok harus berupa angka bulat dan Rating harus berupa angka (gunakan titik desimal).")
                input("Tekan Enter untuk melanjutkan.")
                continue

            for b in books:
                if b['judul'].strip().lower() == new_judul.lower() and b['penulis'].strip().lower() == new_penulis.lower():
                    try:
                        current_stok = int(b['stok'])
                    except ValueError:
                        current_stok = 0
                    b['stok'] = str(current_stok + input_stok)
                    b['rating'] = str(input_rating) # Simpan rating sebagai string
                    found = True
                    break

            if not found:
                new_book = {
                    'judul': new_judul,
                    'tahun': new_tahun,
                    'penulis': new_penulis,
                    'stok': str(input_stok),
                    'harga': new_harga,
                    'rating': str(input_rating) # Simpan rating sebagai string
                }
                books.append(new_book)

            save_csv(BUKU_FILE, books, BUKU_FIELDNAMES)
            print("Buku ditambahkan atau stok/rating diperbarui.")
            input("Tekan Enter untuk melanjutkan.")

        elif pilihan == '3':
            clear_screen()
            books = load_csv(BUKU_FILE)
            judul = input("Judul buku yang ingin diedit: ").strip()
            penulis = input("Penulis buku yang ingin diedit: ").strip()
            found = False
            for b in books:
                if b['judul'].strip().lower() == judul.lower() and b['penulis'].strip().lower() == penulis.lower():
                    b['tahun'] = input(f"Tahun ({b['tahun']}): ") or b['tahun']
                    b['penulis'] = input(f"Penulis ({b['penulis']}): ") or b['penulis']
                    b['stok'] = input(f"Stok ({b['stok']}): ") or b['stok']
                    b['harga'] = input(f"Harga ({b['harga']}): ") or b['harga']
                    current_rating_display = b.get('rating', '0')
                    new_rating_edit = input(f"Rating ({current_rating_display}, 0.0-5.0, gunakan titik desimal): ").strip()
                    
                    if new_rating_edit: 
                        try:
                            input_rating_edit = float(new_rating_edit)
                            if 0.0 <= input_rating_edit <= 5.0: 
                                b['rating'] = str(input_rating_edit) 
                            else:
                                print("Rating harus antara 0.0 dan 5.0. Rating tidak diubah.")
                        except ValueError:
                            print("Input rating tidak valid. Rating tidak diubah (gunakan angka dengan titik desimal).")
                    found = True
                    break
            if found:
                save_csv(BUKU_FILE, books, BUKU_FIELDNAMES)
                print("Buku diperbarui.")
            else:
                print("Buku tidak ditemukan.")
            input("Tekan Enter untuk melanjutkan.")
                
        elif pilihan == '4':
            clear_screen()
            books = load_csv(BUKU_FILE)
            judul = input("Judul buku yang ingin dihapus: ")
            penulis = input("Penulis buku yang ingin dihapus: ")
            books = [b for b in books if not (b['judul'].lower() == judul.lower() and b['penulis'].lower() == penulis.lower())]
            save_csv(BUKU_FILE, books, BUKU_FIELDNAMES)
            print("Buku dihapus.")
            input("Tekan Enter untuk melanjutkan.")
        elif pilihan == '5':
            clear_screen()
            atur_stok_buku()

        elif pilihan == '6': 
            while True:
                clear_screen()
                pesanan = load_csv(PESANAN_FILE)
                if not pesanan:
                    print("Tidak ada data pesanan yang tersedia.")
                    input("Tekan Enter untuk kembali ke Dashboard Admin.")
                    break

                print("\n--- Daftar Semua Pesanan ---")
                headers = ['No.', 'Username', 'Judul', 'Harga', 'Status'] 
                table_data = []
                for i, p in enumerate(pesanan):
                    table_data.append([i + 1, p['username'], p['judul'], p['harga'], p['status']])
                print(tb(table_data, headers=headers, tablefmt='double_grid'))

                print("\nOpsi Kelola Pesanan:")
                print("1. Konfirmasi Pesanan Menunggu Konfirmasi") 
                print("9. Kembali ke Dashboard Admin")

                try:
                    pilihan_kelola = input("Masukkan pilihan (angka): ").strip()
                    if pilihan_kelola == '9':
                        break
                    elif pilihan_kelola == '1':
                        try:
                            nomor_pesanan_konfirmasi = input("Masukkan nomor pesanan yang ingin dikonfirmasi: ").strip()
                            index_pesanan_konfirmasi = int(nomor_pesanan_konfirmasi) - 1

                            if 0 <= index_pesanan_konfirmasi < len(pesanan):
                                pesanan_terpilih = pesanan[index_pesanan_konfirmasi]
                                if pesanan_terpilih['status'] == 'Menunggu Konfirmasi':
                                    pesanan_terpilih['status'] = 'Dikirim'
                                    
                                    # Simpan seluruh daftar pesanan yang sudah diperbarui
                                    updated_pesanan_for_save = []
                                    for p_item in pesanan:
                                        updated_pesanan_for_save.append({
                                            'username': p_item.get('username', ''),
                                            'judul': p_item.get('judul', ''),
                                            'harga': p_item.get('harga', ''),
                                            'status': p_item.get('status', '')
                                        })
                                    save_csv(PESANAN_FILE, updated_pesanan_for_save, ['username', 'judul', 'harga', 'status'])
                                    print(f"Pesanan '{pesanan_terpilih['judul']}' dari '{pesanan_terpilih['username']}' berhasil dikonfirmasi menjadi 'Dikirim'.")
                                else:
                                    print("Status pesanan ini tidak 'Menunggu Konfirmasi' atau sudah dikonfirmasi.")
                            else:
                                print("Nomor pesanan tidak valid.")
                        except ValueError:
                            print("Input tidak valid. Masukkan nomor pesanan yang benar.")
                        except Exception as e:
                            print(f"Terjadi kesalahan: {e}")
                        input("Tekan Enter untuk melanjutkan.")
                    else:
                        print("Pilihan tidak valid.")
                        input("Tekan Enter untuk melanjutkan.")
                except Exception as e:
                    print(f"Input error: {e}")
                    input("Tekan Enter untuk melanjutkan.")


        elif pilihan == '0':
            clear_screen()
            print("Anda telah logout.")
            return

        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk melanjutkan.")


def main():
    while True:
        clear_screen()
        judul_apk()
        print("=" * 40)
        print("Selamat Datang di Aplikasi Manajemen Buku")
        print("=" * 40)
        print(" [1] Login")
        print(" [2] Register")
        print(" [3] Keluar")
        print("=" * 40)
        pilihan = input("Pilih menu [1/2/3]: ").strip()
        if pilihan == '1':
            role, username = login()
            if role == 'user':
                user_dashboard(username)
            elif role == 'admin':
                admin_dashboard()
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            print("Kamu memilih keluar!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

main()

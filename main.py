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

# ========== CSV Stuff =============
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_csv(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' tidak ditemukan.")
        return []
    except Exception as e:
        print(f"Error saat membaca file '{filename}': {e}")
        return []
    
def save_csv(filename, data, fieldnames):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error saat menyimpan file '{filename}': {e}")

def append_csv(filename, row, fieldnames):
    file_exists = os.path.exists(filename)
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
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
        if data[mid][key] == target:
            return mid
        elif data[mid][key] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def knapsack(budget, books):
    n = len(books)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(budget + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif int(books[i - 1]['harga']) <= w:
                dp[i][w] = max(int(books[i - 1]['harga']) + dp[i - 1][w - int(books[i - 1]['harga'])], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    w = budget
    res = dp[n][budget]
    selected = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][w]:
            continue
        else:
            selected.append(books[i - 1])
            res -= int(books[i - 1]['harga'])
            w -= int(books[i - 1]['harga'])
    return selected

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

# ===== Dashboard =====
def user_dashboard(username):
    cart = []

    def lihat_daftar_buku():
        while True:
            clear_screen()
            books = load_csv(BUKU_FILE)
            books = merge_sort(books)
            headers = ['Judul', 'Penulis', 'Tahun', 'Stok', 'Harga']
            table = [[b['judul'], b['penulis'], b['tahun'], b['stok'], b['harga']] for b in books]
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
            print("1. Cari Buku berdasarkan judul")
            print("9. Kembali ke Dashboard")
            try:
                pilihan = input("Masukkan pilihan (angka): ")
            except Exception as e:
                print(f"Input error: {e}")
                input("Tekan Enter untuk melanjutkan.")
                continue

            if pilihan == '1':
                try:
                    target = input("Masukkan judul buku yang dicari: ").strip()  
                except Exception as e:
                    print(f"Input error: {e}")
                    input("Tekan Enter untuk melanjutkan.")
                    continue

                if not target:
                    print("Judul tidak boleh kosong.")
                    input("Tekan Enter untuk melanjutkan.")
                    continue

                target_lower = target.lower()
                found_books = [b for b in books if target_lower in b['judul'].lower()]
                
                print(f"Ditemukan {len(found_books)} buku untuk judul '{target}'.")

                if found_books:
                    headers = ['Judul', 'Penulis', 'Tahun', 'Harga']
                    table = [[b['judul'], b['penulis'], b['tahun'], b['harga']] for b in found_books]
                    print("\nHasil Pencarian Buku:")
                    print(tb(table, headers=headers, tablefmt='double_grid'))
                else:
                    print("Buku tidak ditemukan. Pastikan judul sesuai atau coba kata kunci lain.")
                
                input("Tekan Enter untuk kembali ke menu pencarian.")
            
            elif pilihan == '9':
                break
            else:
                print("Pilihan tidak valid.")
                input("Tekan Enter untuk melanjutkan.")

    def tambah_buku_keranjang():
        while True:
            clear_screen()
            try:
                judul = input("Judul buku yang ingin ditambahkan ke keranjang (atau ketik '9' untuk kembali): ")
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if judul == '9':
                break
            books = load_csv(BUKU_FILE)
            for b in books:
                if b['judul'].lower() == judul.lower():
                    cart.append(b)
                    print("Buku sudah ditambahkan ke keranjang.")
                    input("Tekan Enter untuk melanjutkan.")
                    break
            else:
                print("Buku tidak ditemukan.")
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
                    save_csv(BUKU_FILE, books, ['judul', 'tahun', 'penulis', 'stok', 'harga'])
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
        print("\n--- Dashboard Admin ---")
        print("1. Lihat Buku")
        print("2. Tambah Buku")
        print("3. Edit Buku")
        print("4. Hapus Buku")
        print("5. Daftar Pesanan")
        print("6. Konfirmasi Pembayaran")
        print("0. Logout")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            clear_screen()
            books = load_csv(BUKU_FILE)
            books = merge_sort(books)
            headers = ['Judul', 'Penulis', 'Tahun', 'Stok', 'Harga']
            table = [[b['judul'], b['penulis'], b['tahun'], b['stok'], b['harga']] for b in books]
            print(tb(table, headers=headers, tablefmt='double_grid'))

        elif pilihan == '2':
            clear_screen()
            books = load_csv(BUKU_FILE)
            new_judul = input("Masukkan Judul Buku : ").strip()
            new_tahun = input("Tahun Terbit: ").strip()
            new_penulis = input("Penulis : ").strip()
            new_stok = input("Stok : ").strip()
            new_harga = input("Harga : ").strip()

            if not new_judul or not new_tahun or not new_penulis or not new_stok or not new_harga:
                print("Mohon masukkan data dengan benar")
                return

            found = False
            try:
                input_stok = int(new_stok)
            except ValueError:
                input_stok = 0

            for b in books:
                if b['judul'].strip().lower() == new_judul.lower() and b['penulis'].strip().lower() == new_penulis.lower():
                    try:
                        current_stok = int(b['stok'])
                    except ValueError:
                        current_stok = 0
                    b['stok'] = str(current_stok + input_stok)
                    found = True
                    break

            if not found:
                new_book = {
                    'judul': new_judul,
                    'tahun': new_tahun,
                    'penulis': new_penulis,
                    'stok': str(input_stok),
                    'harga': new_harga
                }
                books.append(new_book)

            save_csv(BUKU_FILE, books, ['judul', 'tahun', 'penulis', 'stok', 'harga'])
            print("Buku ditambahkan atau stok diperbarui.")

        elif pilihan == '3':
            clear_screen()
            books = load_csv(BUKU_FILE)
            judul = input("Judul buku yang ingin diedit: ").strip()
            penulis = input("Penulis buku yang ingin diedit: ").strip()
            found = False
            for b in books:
                if b['judul'].strip().lower() == judul.lower() and b['penulis'].strip().lower() == penulis.lower():
                    b['tahun'] = input("Tahun: ")
                    b['penulis'] = input("Penulis: ")
                    b['stok'] = input("Stok: ")
                    b['harga'] = input("Harga: ")
                    found = True
                    break
            if found:
                save_csv(BUKU_FILE, books, ['judul', 'tahun', 'penulis', 'stok', 'harga'])
                print("Buku diperbarui.")
            else:
                print("Buku tidak ditemukan.")
                
        elif pilihan == '4':
            clear_screen()
            books = load_csv(BUKU_FILE)
            judul = input("Judul buku yang ingin dihapus: ")
            penulis = input("Penulis buku yang ingin dihapus: ")
            books = [b for b in books if not (b['judul'].lower() == judul.lower() and b['penulis'].lower() == penulis.lower())]
            save_csv(BUKU_FILE, books, ['judul', 'tahun', 'penulis', 'stok', 'harga'])
            print("Buku dihapus.")

        elif pilihan == '5':
            clear_screen()
            pesanan = load_csv(PESANAN_FILE)
            headers = ['Username', 'Judul', 'Harga', 'Status']
            table = [[p['username'], p['judul'], p['harga'], p['status']] for p in pesanan]
            print(tb(table, headers=headers, tablefmt='double_grid'))

        elif pilihan == '6':
            clear_screen()
            pesanan = load_csv(PESANAN_FILE)
            for p in pesanan:
                if p['status'] == 'Menunggu Konfirmasi':
                    p['status'] = 'Dikirim'
            save_csv(PESANAN_FILE, pesanan, ['username', 'judul', 'harga', 'status'])
            print("Pesanan dikonfirmasi dan status diubah menjadi 'Dikirim'.")

        elif pilihan == '0':
            clear_screen()
            print("Anda telah logout.")
            return

        else:
            print("Pilihan tidak valid.")

# Main
def main():
    while True:
        clear_screen()
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
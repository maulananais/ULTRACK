import sys
import os
from time import sleep
from sherlock_project.sherlock import sherlock, QueryNotifyPrint, SitesInformation, QueryStatus

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """Print the ULTRACK logo."""
    logo = [
        '                                                       ',
        '██╗   ██╗██╗  ████████╗██████╗  █████╗  ██████╗██╗  ██╗',
        '██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝',
        '██║   ██║██║     ██║   ██████╔╝███████║██║     █████╔╝ ',
        '██║   ██║██║     ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ',
        '╚██████╔╝███████╗██║   ██║  ██║██║  ██║╚██████╗██║  ██╗',
        ' ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝',
        ]
    for line in logo:
        print(line)
    print()  # Tambahkan baris kosong setelah logo

def search_username(username):
    """Jalankan pencarian username menggunakan Sherlock."""
    global results

    # Setup site_data dan query_notify
    sites = SitesInformation()  # Inisialisasi situs dari JSON lokal atau online
    site_data = {site.name: site.information for site in sites}
    
    query_notify = QueryNotifyPrint(result=None, verbose=False, print_all=False, browse=False)

    try:
        # Jalankan Sherlock
        results = sherlock(
            username,
            site_data,
            query_notify,
            tor=False,
            unique_tor=False,
            dump_response=False,
            proxy=None,
            timeout=60
        )
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")
        results = {}

def filter_results(results):
    """Filter hasil pencarian untuk menghapus 'fakeweb' dan cross-check hasil."""
    valid_sites = ['site1', 'site2', 'site3']  # Gantilah dengan daftar situs web valid yang diinginkan
    filtered_results = {}
    
    for site, result in results.items():
        # Cross-check hasil dua kali
        if site not in valid_sites:
            continue
        
        # Pastikan hasil valid dan tidak dari 'fakeweb'
        if result["status"].status == QueryStatus.CLAIMED and 'fakeweb' not in result['url_user']:
            filtered_results[site] = result

    return filtered_results

def main():
    global results

    while True:
        # Tampilkan logo ULTRACK sebelum meminta input username
        print_logo()

        # Input username dan konfirmasi
        username = input("Input username: ")
        confirm = input("Are you sure? (y/n): ").strip().lower()

        if confirm != 'y':
            print("Pencarian dibatalkan.")
            return

        # Hapus input, konfirmasi, dan logo sebelum memulai pencarian
        clear_screen()

        # Jalankan pencarian username
        search_username(username)

        # Filter hasil pencarian
        results = filter_results(results)

        # Menampilkan hasil setelah pencarian selesai
        if results:
            for site, result in results.items():
                if result["status"].status == QueryStatus.CLAIMED:
                    print(f"[+] ({site}): {result['url_user']}")
        else:
            print("")
            print("Thanks for using ULTRACK!")
            print("Support sherlock-project at: https://sherlockproject.xyz", end='')

        # Tanyakan apakah ingin mencari username lain
        search_again = input("\n\nWant to search another username? (y/n): ").strip().lower()
        if search_again != 'y':
            break
        else:
            clear_screen()  # Bersihkan layar sebelum memulai pencarian baru

if __name__ == "__main__":
    main()

"""
ANGGOTA 1 - Data Gedung, Data Penghuni, Dictionary, Array List, Menu Operator
Proyek: Emergency Evacuation Simulator

Modul ini sengaja dibuat mandiri agar bisa diuji sendiri.
Untuk integrasi, anggota lain dapat mengimpor:
    from anggota1 import BuildingManager
"""

class BuildingManager:
    def __init__(self):
        # ARRAY LIST: menyimpan kumpulan ruangan dan penghuni agar mudah ditampilkan/diiterasi.
        self.rooms = []
        self.occupants = []

        # DICTIONARY: pencarian data cepat berdasarkan ID.
        self.rooms_by_id = {}
        self.occupants_by_id = {}

    # ---------- DATA GEDUNG / RUANGAN ----------
    def add_room(self, room_id, name, room_type):
        room_id = room_id.strip().upper()
        name = name.strip()
        room_type = room_type.strip()

        if not room_id or not name or not room_type:
            return False, "ID, nama, dan jenis ruangan wajib diisi."
        if room_id in self.rooms_by_id:
            return False, f"Ruangan dengan ID {room_id} sudah ada."

        room = {
            "id": room_id,
            "nama": name,
            "jenis": room_type,
            "aktif": True
        }
        self.rooms.append(room)
        self.rooms_by_id[room_id] = room
        return True, f"Ruangan {name} ({room_id}) berhasil ditambahkan."

    def set_room_active(self, room_id, active):
        room_id = room_id.strip().upper()
        room = self.rooms_by_id.get(room_id)
        if room is None:
            return False, f"Ruangan {room_id} tidak ditemukan."

        room["aktif"] = active
        status = "aktif/terbuka" if active else "nonaktif/tertutup"
        return True, f"Ruangan {room_id} sekarang {status}."

    def list_rooms(self):
        return self.rooms

    # ---------- DATA PENGHUNI ----------
    def add_occupant(self, occupant_id, name, room_id):
        occupant_id = occupant_id.strip().upper()
        name = name.strip()
        room_id = room_id.strip().upper()

        if not occupant_id or not name or not room_id:
            return False, "ID penghuni, nama, dan ID ruangan wajib diisi."
        if occupant_id in self.occupants_by_id:
            return False, f"Penghuni dengan ID {occupant_id} sudah terdaftar."
        if room_id not in self.rooms_by_id:
            return False, f"Ruangan {room_id} belum terdaftar."
        if not self.rooms_by_id[room_id]["aktif"]:
            return False, f"Ruangan {room_id} sedang nonaktif/tertutup."

        occupant = {
            "id": occupant_id,
            "nama": name,
            "ruangan_awal": room_id,
            "ruangan_sekarang": room_id,
            "status": "Belum Dievakuasi"
        }
        self.occupants.append(occupant)
        self.occupants_by_id[occupant_id] = occupant
        return True, f"Penghuni {name} berhasil didaftarkan di {room_id}."

    def list_occupants(self):
        return self.occupants

    def get_occupant(self, occupant_id):
        return self.occupants_by_id.get(occupant_id.strip().upper())

    def update_occupant_location(self, occupant_id, room_id):
        occupant_id = occupant_id.strip().upper()
        room_id = room_id.strip().upper()

        occupant = self.occupants_by_id.get(occupant_id)
        if occupant is None:
            return False, f"Penghuni {occupant_id} tidak ditemukan."
        if room_id not in self.rooms_by_id:
            return False, f"Ruangan {room_id} tidak ditemukan."
        if not self.rooms_by_id[room_id]["aktif"]:
            return False, f"Ruangan {room_id} sedang nonaktif/tertutup."

        occupant["ruangan_sekarang"] = room_id
        return True, f"Lokasi {occupant['nama']} diperbarui ke {room_id}."

    # Fungsi ini disiapkan untuk dipanggil anggota 2 saat penghuni selesai diproses.
    def set_occupant_status(self, occupant_id, status):
        occupant_id = occupant_id.strip().upper()
        occupant = self.occupants_by_id.get(occupant_id)
        if occupant is None:
            return False, f"Penghuni {occupant_id} tidak ditemukan."

        allowed_status = ["Belum Dievakuasi", "Sedang Diproses", "Sudah Dievakuasi"]
        if status not in allowed_status:
            return False, "Status tidak valid."
        occupant["status"] = status
        return True, f"Status {occupant['nama']} menjadi: {status}."


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong.")


def show_rooms(manager):
    print("\n=== DATA RUANGAN ===")
    if not manager.rooms:
        print("Belum ada data ruangan.")
        return
    print(f"{'ID':<12} {'NAMA':<22} {'JENIS':<15} STATUS")
    for room in manager.list_rooms():
        status = "Aktif" if room["aktif"] else "Tertutup"
        print(f"{room['id']:<12} {room['nama']:<22} {room['jenis']:<15} {status}")


def show_occupants(manager):
    print("\n=== DATA PENGHUNI ===")
    if not manager.occupants:
        print("Belum ada data penghuni.")
        return
    print(f"{'ID':<12} {'NAMA':<22} {'RUANGAN':<12} STATUS")
    for person in manager.list_occupants():
        print(f"{person['id']:<12} {person['nama']:<22} "
              f"{person['ruangan_sekarang']:<12} {person['status']}")


def operator_menu():
    manager = BuildingManager()

    # Data contoh agar program langsung bisa dicoba.
    manager.add_room("R201", "Ruang 201", "Ruangan")
    manager.add_room("COR-B", "Koridor B", "Koridor")
    manager.add_room("ST-1", "Tangga 1", "Tangga")
    manager.add_room("EXIT-A", "Pintu Keluar A", "Pintu Keluar")

    while True:
        print("\n========== OPERATOR EVAKUASI ==========")
        print("1. Tambah ruangan")
        print("2. Tampilkan data ruangan")
        print("3. Ubah status ruangan (aktif/tertutup)")
        print("4. Daftarkan penghuni")
        print("5. Tampilkan data penghuni")
        print("6. Ubah lokasi penghuni")
        print("0. Keluar")
        choice = input("Pilih menu: ").strip()

        if choice == "1":
            room_id = input_nonempty("ID ruangan: ")
            name = input_nonempty("Nama ruangan: ")
            room_type = input_nonempty("Jenis (Ruangan/Koridor/Tangga/Pintu Keluar): ")
            ok, message = manager.add_room(room_id, name, room_type)
            print(message)

        elif choice == "2":
            show_rooms(manager)

        elif choice == "3":
            room_id = input_nonempty("ID ruangan: ")
            status = input("Status (1 = aktif, 0 = tertutup): ").strip()
            if status not in ("1", "0"):
                print("Pilihan status harus 1 atau 0.")
            else:
                ok, message = manager.set_room_active(room_id, status == "1")
                print(message)

        elif choice == "4":
            occupant_id = input_nonempty("ID penghuni: ")
            name = input_nonempty("Nama penghuni: ")
            room_id = input_nonempty("ID ruangan awal: ")
            ok, message = manager.add_occupant(occupant_id, name, room_id)
            print(message)

        elif choice == "5":
            show_occupants(manager)

        elif choice == "6":
            occupant_id = input_nonempty("ID penghuni: ")
            room_id = input_nonempty("ID ruangan baru: ")
            ok, message = manager.update_occupant_location(occupant_id, room_id)
            print(message)

        elif choice == "0":
            print("Program Anggota 1 selesai. Terima kasih!")
            break

        else:
            print("Menu tidak tersedia. Pilih angka yang ada.")


if __name__ == "__main__":
    operator_menu()

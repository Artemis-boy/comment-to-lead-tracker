"""
Pelacak Komen Jadi Pelanggan — v1
==================================
Ubah komen sosmed jadi daftar follow-up: siapa calon pembeli,
siapa yang komplain, siapa yang cuma tanya-tanya.

Cara pakai:
  1. Siapkan file komen.csv dengan kolom: username, komen, platform, tanggal
     (Lihat contoh_komen.csv untuk formatnya.)
  2. Jalankan: python komen_ke_pelanggan.py
  3. Hasil: hasil_pilah_komen.xlsx
     - Sheet "Follow-up": semua komen sudah dipilah + prioritas,
       urut dari yang paling penting dibalas duluan.
     - Sheet "Ringkasan": jumlah per kategori + angka penting.

Cara pilah: cocokin kata kunci (sama kayak CS Reply Bot).
Batasan jujur: cocokin kata bisa salah — misal sarkasme ("wah murah banget"
padahal nyindir) bisa kepilah salah. Selalu cek manual sebelum balas.
"""

import pandas as pd

# --- Kata kunci per kategori (tambah sendiri kalau ada kata baru) ---
KATA_MAU_BELI = [
    "harga", "order", "pesan", "beli", "dm", "cek harga",
    "booking", "boking", "mau", "bisa pesan", "cara order",
]
KATA_TANYA = [
    "lokasi", "alamat", "dimana", "di mana", "buka jam", "jam buka",
    "menu", "ongkir", "ongkirnya", "ada apa", "jual apa",
]
KATA_KOMPLAIN = [
    "kecewa", "jelek", "buruk", "lama", "tipu", "bohong",
    "salah", "marah", "nggak enak", "tidak enak", "kapok",
]


def pilah_komen(teks):
    """Tentukan kategori + prioritas dari satu komen. Kembalikan (kategori, prioritas, alasan)."""
    t = str(teks).lower()

    for kata in KATA_KOMPLAIN:
        if kata in t:
            return ("KOMPLAIN", 1, f"kata '{kata}'")
    for kata in KATA_MAU_BELI:
        if kata in t:
            return ("MAU BELI", 1, f"kata '{kata}'")
    for kata in KATA_TANYA:
        if kata in t:
            return ("TANYA-TANYA", 2, f"kata '{kata}'")
    return ("LAINNYA", 3, "tidak ada kata kunci")


def main():
    try:
        df = pd.read_csv("komen.csv")
    except FileNotFoundError:
        print("File komen.csv tidak ketemu! Copy contoh_komen.csv jadi komen.csv dulu,")
        print("atau isi komen.csv dengan komen beneran. Format kolom: username, komen, platform, tanggal")
        return

    hasil = []
    for _, baris in df.iterrows():
        kategori, prioritas, alasan = pilah_komen(baris.get("komen", ""))
        hasil.append({
            "Prioritas": prioritas,
            "Kategori": kategori,
            "Username": baris.get("username", ""),
            "Komen": baris.get("komen", ""),
            "Platform": baris.get("platform", ""),
            "Tanggal": baris.get("tanggal", ""),
            "Status": "Belum dibalas",
            "Alasan pilah": alasan,
        })

    hasil_df = pd.DataFrame(hasil)
    hasil_df = hasil_df.sort_values(["Prioritas", "Tanggal"]).reset_index(drop=True)

    # Ringkasan
    total = len(hasil_df)
    ringkasan = pd.DataFrame([
        ["Total komen", total],
        ["MAU BELI (calon pembeli)", (hasil_df["Kategori"] == "MAU BELI").sum()],
        ["KOMPLAIN (harus cepat ditangani)", (hasil_df["Kategori"] == "KOMPLAIN").sum()],
        ["TANYA-TANYA", (hasil_df["Kategori"] == "TANYA-TANYA").sum()],
        ["LAINNYA", (hasil_df["Kategori"] == "LAINNYA").sum()],
        ["Yang harus dibalas duluan (Prioritas 1)",
         (hasil_df["Prioritas"] == 1).sum()],
    ], columns=["Ukuran", "Jumlah"])

    with pd.ExcelWriter("hasil_pilah_komen.xlsx", engine="openpyxl") as tulis:
        hasil_df.to_excel(tulis, sheet_name="Follow-up", index=False)
        ringkasan.to_excel(tulis, sheet_name="Ringkasan", index=False)

    print("\n===== HASIL PILAH KOMEN =====")
    print(ringkasan.to_string(index=False))
    print(f"\nTotal {total} komen sudah dipilah.")
    print("File hasil: hasil_pilah_komen.xlsx")
    print("Balas dulu yang Prioritas 1 (MAU BELI + KOMPLAIN)!")


if __name__ == "__main__":
    main()

import time
import matplotlib.pyplot as plt

from rk4_euler import (U0, T, DAFTAR_H, euler_langkah, rk4_langkah,
                       simulasi, solusi_eksak)

BIRU, MERAH = "tab:blue", "tab:red"
eks = solusi_eksak(T, U0)
N = [round(T / h) for h in DAFTAR_H]
galat_rk4 = [abs(simulasi(rk4_langkah, U0, T, h)[-1] - eks) for h in DAFTAR_H]
galat_eu = [abs(simulasi(euler_langkah, U0, T, h)[-1] - eks) for h in DAFTAR_H]

def simpan(judul, xlabel, ylabel, nama_file, grid_both=True):
    # bagian yang selalu sama di setiap grafik, jadi saya jadikan satu fungsi
    plt.title(judul)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(alpha=0.3, which="both" if grid_both else "major")
    plt.savefig(nama_file, dpi=200, bbox_inches="tight")

# grafik 1: jumlah pengguna tiap bulan, h = 1
t_halus = [i / 10 for i in range(T * 10 + 1)]
plt.figure(figsize=(7, 4.5))
plt.plot(t_halus, [solusi_eksak(t, U0) for t in t_halus], "k", label="Nilai sebenarnya")
plt.plot(range(T + 1), simulasi(rk4_langkah, U0, T, 1), "o-", color=BIRU, label="RK4 (h = 1)")
plt.plot(range(T + 1), simulasi(euler_langkah, U0, T, 1), "o-", color=MERAH, label="Euler (h = 1)")
simpan("Pertumbuhan pengguna", "Waktu (bulan)", "Jumlah pengguna (ribu)",
       "grafik_pertumbuhan.png", grid_both=False)

# grafik 2: galat terhadap h
# garis putus-putus sebagai acuan kemiringan 4 dan 1, keduanya saya lewatkan di titik h = 0,25
plt.figure(figsize=(7, 4.5))
plt.loglog(DAFTAR_H, galat_rk4, "o-", color=BIRU, label="RK4")
plt.loglog(DAFTAR_H, galat_eu, "o-", color=MERAH, label="Euler")
i = DAFTAR_H.index(0.25)
plt.loglog(DAFTAR_H, [galat_rk4[i] * (h / 0.25) ** 4 for h in DAFTAR_H],
           "--", color="gray", label="Acuan kemiringan 4")
plt.loglog(DAFTAR_H, [galat_eu[i] * (h / 0.25) for h in DAFTAR_H],
           "--", color="gray", label="Acuan kemiringan 1")
plt.ylim(min(galat_rk4) / 3, max(galat_eu) * 3)
simpan(f"Galat pada t = {T} terhadap h", "Panjang langkah h (bulan)",
       "Galat (ribu pengguna)", "grafik_galat.png")

# grafik 3: galat terhadap jumlah evaluasi f (RK4 memanggil f 4 kali per langkah)
plt.figure(figsize=(7, 4.5))
plt.loglog([4 * n for n in N], galat_rk4, "o-", color=BIRU, label="RK4 (4 evaluasi/langkah)")
plt.loglog(N, galat_eu, "o-", color=MERAH, label="Euler (1 evaluasi/langkah)")
simpan("Galat terhadap jumlah pekerjaan", "Jumlah evaluasi f",
       "Galat (ribu pengguna)", "grafik_biaya.png")

# bagian mengukur waktu eksekusi
def ukur(langkah, h, ulang=200):
    # waktu satu simulasi sampai T dalam mikrodetik, diambil rata-rata dari 200 kali jalan
    mulai = time.perf_counter()
    for _ in range(ulang):
        simulasi(langkah, U0, T, h)
    return (time.perf_counter() - mulai) / ulang * 1e6

def rata_simpangan(x):
    rata = sum(x) / len(x)
    return rata, (sum((v - rata) ** 2 for v in x) / (len(x) - 1)) ** 0.5

ukur(rk4_langkah, 1)      # pemanasan dulu, hasilnya tidak dipakai
print("Waktu eksekusi sampai t =", T, "(7 kali ukur, mikrodetik)")
print("        h  RK4 rata2  RK4 simp.  Euler rata2  Euler simp.  RK4/Euler")
w_rk4, w_eu = [], []
for h in DAFTAR_H:
    m1, s1 = rata_simpangan([ukur(rk4_langkah, h) for _ in range(7)])
    m2, s2 = rata_simpangan([ukur(euler_langkah, h) for _ in range(7)])
    w_rk4.append(m1)
    w_eu.append(m2)
    print(f"{h:>9g} {m1:>10.1f} {s1:>10.1f} {m2:>12.1f} {s2:>12.1f} {m1 / m2:>10.2f}")

# grafik 4: waktu eksekusi
plt.figure(figsize=(7, 4.5))
plt.loglog(DAFTAR_H, w_rk4, "o-", color=BIRU, label="RK4")
plt.loglog(DAFTAR_H, w_eu, "o-", color=MERAH, label="Euler")
# kurva teoretis O(N): waktu = c * N, dengan c = rata-rata waktu per langkah
# (jika waktu memang sebanding dengan N, titik pengukuran akan mengikuti garis ini)
c_rk4 = sum(w / n for w, n in zip(w_rk4, N)) / len(N)
c_eu = sum(w / n for w, n in zip(w_eu, N)) / len(N)
plt.loglog(DAFTAR_H, [c_rk4 * n for n in N], "--", color=BIRU, alpha=0.7,
           label=f"Teori O(N) RK4: T = {c_rk4:.2f} N")
plt.loglog(DAFTAR_H, [c_eu * n for n in N], "--", color=MERAH, alpha=0.7,
           label=f"Teori O(N) Euler: T = {c_eu:.2f} N")
simpan(f"Waktu eksekusi sampai t = {T}", "Panjang langkah h (bulan)",
       "Waktu (mikrodetik)", "grafik_waktu.png")
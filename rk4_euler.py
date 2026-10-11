# program untuk membandingkan RK4 dengan Euler
# modelnya pertumbuhan pengguna aplikasi: dU/dt = r * U * (1 - U / K)
# U satuannya ribu pengguna, t satuannya bulan

R = 0.5           # laju pertumbuhan
K = 100.0         # batas pengguna, 100 ribu
U0 = 1.0          # pengguna awal, 1 ribu
T = 12            # sampai bulan ke-12
DAFTAR_H = [2, 1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]  # h terus dibagi dua

def f(t, U):
    # t tidak terpakai di sini, tapi saya biarkan agar bentuknya sama dengan f(t, U) di laporan
    return R * U * (1 - U / K)

def euler_langkah(t, U, h):
    return U + h * f(t, U)      # Euler cuma pakai laju di awal langkah

def rk4_langkah(t, U, h):
    k1 = f(t, U)                          # awal langkah
    k2 = f(t + h / 2, U + h / 2 * k1)     # tengah langkah, U ditebak dari k1
    k3 = f(t + h / 2, U + h / 2 * k2)     # tengah lagi, tebakan U diganti pakai k2
    k4 = f(t + h, U + h * k3)             # ujung langkah, U ditebak dari k3
    return U + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)   # gabungan keempatnya, bobot 1:2:2:1

def simulasi(langkah, U0, T, h):
    # mengulang satu langkah dari t = 0 sampai T, hasilnya [U0, U1, ..., U_N]
    U = U0
    hasil = [U0]
    for n in range(round(T / h)):        # pakai round agar jumlah langkah bilangan bulat
        U = langkah(n * h, U, h)         # waktunya n * h, bukan ditambah h terus, agar pembulatannya tidak menumpuk
        hasil.append(U)
    return hasil

def solusi_eksak(t, U0):
    e = 2.718281828459045                
    return K / (1 + (K / U0 - 1) * e ** (-R * t))

def kasus_uji():
    # mencocokkan hasil program dengan hitungan manual di Bab 3
    kasus = [("Kasus 1", 1, 2, 2.6634, 1.9900, 2.6724),
             ("Kasus 2", 1, 1, 2.6715, 2.2313, 2.6724),
             ("Kasus 3", 10, 2, 23.1603, 19.0000, 23.1969)] 
    for nama, u0, h, rk4_m, eu_m, eks_m in kasus: # urutannya: nama, U0, h, lalu hasil manual RK4, Euler, eksak
        rk4 = simulasi(rk4_langkah, u0, 2, h)[-1]
        eu = simulasi(euler_langkah, u0, 2, h)[-1]
        eks = solusi_eksak(2, u0)
        cocok = all(abs(a - b) < 0.00006
                    for a, b in [(rk4, rk4_m), (eu, eu_m), (eks, eks_m)])
        print(f"{nama}: RK4 {rk4:.4f}, Euler {eu:.4f}, eksak {eks:.4f} -> "
              f"{'COCOK' if cocok else 'TIDAK COCOK'}")

def tabel_galat():
    # galat di t = T untuk semua h
    # rasio = galat h sebelumnya dibagi galat h ini (teorinya 16 untuk RK4 dan 2 untuk Euler)
    eks = solusi_eksak(T, U0)
    print(f"\nGalat di t = {T}, nilai eksak {eks:.6f}")
    print("        h     N   galat RK4  galat Euler  rasio RK4  rasio Euler")
    lalu = None
    for h in DAFTAR_H:
        N = round(T / h)
        g_rk4 = abs(simulasi(rk4_langkah, U0, T, h)[-1] - eks)
        g_eu = abs(simulasi(euler_langkah, U0, T, h)[-1] - eks)
        if lalu is None:
            r1 = r2 = "-"
        else:
            r1, r2 = f"{lalu[0] / g_rk4:.2f}", f"{lalu[1] / g_eu:.2f}"
        print(f"{h:>9g} {N:>5} {g_rk4:>11.2e} {g_eu:>12.2e} {r1:>10} {r2:>12}")
        lalu = (g_rk4, g_eu)

def biaya_sama():
    # mencari berapa langkah yang Euler butuhkan agar galatnya sekecil galat RK4 (t = 2, U0 = 1)
    eks = solusi_eksak(2, 1)
    print("\nKetelitian yang sama (t = 2)")
    for h in (2, 1):
        g_rk4 = abs(simulasi(rk4_langkah, 1, 2, h)[-1] - eks)
        evaluasi_rk4 = 4 * round(2 / h)      # RK4 memanggil f 4 kali tiap langkah
        N = 1
        while abs(simulasi(euler_langkah, 1, 2, 2 / N)[-1] - eks) > g_rk4:
            N += 1
        print(f"RK4 h = {h}: {evaluasi_rk4} evaluasi f, Euler perlu {N} langkah "
              f"(sekitar {N / evaluasi_rk4:.0f} kali lebih banyak)")

if __name__ == "__main__":
    kasus_uji()
    tabel_galat()
    biaya_sama()
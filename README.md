# RK4 vs Euler pada Pertumbuhan Pengguna Aplikasi

Repositori ini berisi kode dan grafik untuk tugas Analisis Algoritma Komputasi (Magister Teknik Informatika, Universitas Hasanuddin). Algoritma yang saya kerjakan adalah Runge-Kutta orde 4 (RK4). Laporannya berjudul *Analisis Algoritma Runge-Kutta Orde 4 pada Prediksi Pertumbuhan Pengguna Aplikasi*.

Idenya sederhana. RK4 menghitung kemiringan (laju perubahan) empat kali dalam satu langkah, sedangkan Euler cukup satu kali. Saya ingin tahu seberapa besar bedanya, baik dari ketelitian maupun dari biaya hitungnya, jadi Euler saya pakai sebagai pembanding.

Kasus yang saya pakai adalah jumlah pengguna sebuah aplikasi baru yang mengikuti model logistik: tumbuh pelan di awal, cepat di tengah, lalu melambat saat mendekati batas maksimum.

## Model

```text
dU/dt = r * U * (1 - U / K)
```

| Simbol | Arti | Nilai |
|---|---|---|
| U | jumlah pengguna (dalam ribu) | awalnya 1 (1.000 pengguna) |
| r | laju pertumbuhan | 0,5 per bulan |
| K | batas maksimum pengguna | 100 (100.000 pengguna) |
| T | waktu akhir | 12 bulan |
| h | panjang langkah | 2; 1; 0,5; ... sampai 0,015625 |

Persamaan ini punya solusi eksak, jadi hasil RK4 dan Euler bisa langsung dibandingkan dengan nilai sebenarnya. Selisihnya itulah yang saya sebut galat.

## Isi repositori

| File | Fungsi |
|---|---|
| `rk4_euler.py` | satu langkah Euler dan RK4, simulasi, solusi eksak, tiga kasus uji, dan tabel galat |
| `grafik.py` | membuat empat grafik dan mengukur waktu eksekusi |
| `grafik_pertumbuhan.png` | jumlah pengguna sampai bulan ke-12 (h = 1) |
| `grafik_galat.png` | galat terhadap h |
| `grafik_biaya.png` | galat terhadap jumlah evaluasi f |
| `grafik_waktu.png` | waktu eksekusi, lengkap dengan garis teoretis O(N) |

Kode RK4 dan Euler saya tulis sendiri dari rumusnya, tanpa pustaka numerik. Tidak ada kode dari GitHub, buku, atau forum yang saya salin. Penggunaan AI untuk penulisan laporan saya jelaskan di lampiran laporan.

## Kebutuhan dan cara menjalankan

- Python 3.13
- `matplotlib`, hanya untuk membuat grafik. Perhitungannya sendiri tidak butuh pustaka tambahan.

Hitung dan uji:

```bash
python rk4_euler.py
```

Buat grafik dan ukur waktu:

```bash
pip install matplotlib
python grafik.py
```

`grafik.py` memerlukan `rk4_euler.py` di folder yang sama. Hasilnya empat file PNG, dan tabel waktu eksekusi tercetak di terminal.

## Kasus uji

Ada tiga kasus kecil yang bisa saya hitung dengan tangan (langkah lengkapnya ada di Bab III laporan). Program membandingkan hasilnya dengan hitungan manual itu, dan ketiganya cocok sampai empat desimal.

| Kasus | U₀ | h | Hasil RK4 di t = 2 |
|---|---|---|---|
| 1 | 1 | 2 | 2,6634 |
| 2 | 1 | 1 | 2,6715 |
| 3 | 10 | 2 | 23,1603 |

## Contoh keluaran

Keluaran `rk4_euler.py`:

```text
Kasus 1: RK4 2.6634, Euler 1.9900, eksak 2.6724 -> COCOK
Kasus 2: RK4 2.6715, Euler 2.2313, eksak 2.6724 -> COCOK
Kasus 3: RK4 23.1603, Euler 19.0000, eksak 23.1969 -> COCOK

Galat di t = 12, nilai eksak 80.295715
        h     N   galat RK4  galat Euler  rasio RK4  rasio Euler
        2     6    2.03e-01     3.29e+01          -            -
        1    12    1.69e-02     1.47e+01      12.00         2.24
      0.5    24    1.23e-03     6.42e+00      13.78         2.29
     0.25    48    8.29e-05     2.97e+00      14.82         2.16
    0.125    96    5.39e-06     1.43e+00      15.39         2.08
   0.0625   192    3.43e-07     6.99e-01      15.69         2.04
  0.03125   384    2.17e-08     3.46e-01      15.84         2.02
 0.015625   768    1.36e-09     1.72e-01      15.92         2.01

Ketelitian yang sama (t = 2)
RK4 h = 2: 4 evaluasi f, Euler perlu 140 langkah (sekitar 35 kali lebih banyak)
RK4 h = 1: 8 evaluasi f, Euler perlu 1511 langkah (sekitar 189 kali lebih banyak)
```

Keluaran `grafik.py` (waktu dalam mikrodetik, 7 kali ukur):

```text
        h  RK4 rata2  RK4 simp.  Euler rata2  Euler simp.  RK4/Euler
        2        4.2        0.3          1.2          0.2       3.34
        1        8.1        0.4          2.2          0.2       3.72
      0.5       16.4        0.8          4.2          0.1       3.94
     0.25       32.2        1.0          8.2          0.5       3.93
    0.125       64.9        1.6         15.8          0.2       4.11
   0.0625      143.0       12.0         31.8          0.6       4.49
  0.03125      249.7        1.2         63.5          0.4       3.93
 0.015625      516.0       18.1        126.7          0.9       4.07
```

Angka waktu bisa berbeda di komputer lain, bahkan di komputer yang sama pada percobaan yang lain.

## Hasil

- Kalau h dibagi dua, galat RK4 mengecil sekitar 16 kali dan galat Euler sekitar 2 kali. Ini sesuai dengan orde RK4 (4) dan Euler (1).
- Pada h = 1 bulan, perkiraan RK4 untuk bulan ke-12 meleset sekitar 17 pengguna, sedangkan Euler sekitar 14.700 pengguna.
- Satu langkah RK4 memanggil `f` empat kali, Euler satu kali. Tapi untuk ketelitian yang sama di t = 2, Euler butuh sekitar 35 sampai 189 kali lebih banyak evaluasi.
- Waktu RK4 sekitar 3,3 sampai 4,5 kali waktu Euler pada h yang sama, rata-rata sekitar 3,9 kali. Pada h = 0,0625 simpangan baku RK4 besar, jadi rasionya (4,49) agak tinggi. Saya duga karena ada proses lain di komputer saat pengukuran.
- Waktu naik sebanding dengan jumlah langkah. Titik pengukuran mengikuti garis teoretis O(N) di `grafik_waktu.png`.

Jadi RK4 lebih mahal per langkah, tetapi kalau yang diminta ketelitian tertentu, RK4 justru lebih hemat.

## Grafik

### Pertumbuhan pengguna
![Grafik pertumbuhan pengguna](https://github.com/magfiratuljannah/rk4-euler-pertumbuhan-pengguna/raw/main/grafik_pertumbuhan.png)

### Galat terhadap h
![Grafik galat](https://github.com/magfiratuljannah/rk4-euler-pertumbuhan-pengguna/raw/main/grafik_galat.png)

### Galat terhadap jumlah evaluasi f
![Grafik biaya komputasi](https://github.com/magfiratuljannah/rk4-euler-pertumbuhan-pengguna/raw/main/grafik_biaya.png)

### Waktu eksekusi
![Grafik waktu eksekusi](https://github.com/magfiratuljannah/rk4-euler-pertumbuhan-pengguna/raw/main/grafik_waktu.png)

## Catatan

- Angka pengguna dan batas maksimum hanya contoh, bukan data aplikasi yang sebenarnya.
- Percobaan ini hanya memakai satu model dan satu waktu akhir (12 bulan), dengan h yang tetap.
- Waktu eksekusi bergantung pada komputer dan bahasa pemrogramannya. Yang bermakna adalah perbandingan RK4 dengan Euler, bukan angka mikrodetiknya.

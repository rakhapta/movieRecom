# Laporan Proyek Machine Learning - Rakha Apta Pradhana D R

## Project Overview

Dalam era digital yang dibanjiri oleh konten, pengguna seringkali kesulitan menemukan film yang sesuai dengan selera mereka di antara ribuan pilihan yang tersedia. Fenomena ini, yang dikenal sebagai information overload atau kelebihan informasi, menjadi tantangan utama bagi platform penyedia konten seperti Netflix, Amazon Prime, dan lainnya. Sistem rekomendasi hadir sebagai solusi untuk mengatasi masalah ini dengan cara menyaring dan menyajikan konten yang paling relevan bagi setiap pengguna secara personal. Dengan menganalisis preferensi pengguna dan atribut film, sistem ini tidak hanya membantu pengguna menemukan konten baru yang mereka sukai, tetapi juga secara signifikan meningkatkan engagement dan loyalitas pengguna terhadap platform.

### Mengapa dan Bagaimana Masalah Harus Diselesaikan:

Proyek ini akan membangun dua jenis sistem rekomendasi:

1. Content-Based Filtering: Menganalisis atribut film untuk menemukan film serupa.
2. Collaborative Filtering: Menganalisis pola rating dari komunitas pengguna untuk menemukan pengguna dengan selera serupa.

Dengan membandingkan kedua pendekatan ini, kita dapat memahami metode mana yang lebih efektif untuk dataset yang digunakan.  

### Hasil Riset Terkait atau Referensi:

Banyak penelitian telah membuktikan efektivitas sistem rekomendasi. Menurut riset oleh J. S. Breese, D. Heckerman, dan C. Kadie [1], pendekatan collaborative filtering telah terbukti menjadi salah satu metode yang paling berhasil dalam memprediksi preferensi pengguna dengan menganalisis pola rating dari komunitas pengguna yang lebih besar. Riset lain oleh Isinkaye, Folajimi, dan Ojokoh (2015) juga menyoroti berbagai teknik, termasuk content-based dan collaborative, sebagai fondasi utama dalam sistem rekomendasi modern [2]. Proyek ini akan mengimplementasikan kedua pendekatan tersebut untuk memberikan perbandingan yang komprehensif.

Referensi:
> [1] J. S. Breese, D. Heckerman, and C. Kadie, "Empirical analysis of predictive algorithms for collaborative filtering," *Proceedings of the Fourteenth conference on Uncertainty in artificial intelligence*, 1998, pp. 43–52.
> [2] F. O. Isinkaye, Y. O. Folajimi, and B. A. Ojokoh, "Recommendation systems: Principles, methods and evaluation," Egyptian Informatics Journal, vol. 16, no. 3, pp. 261-273, 2015.

## Business Understanding

### Problem Statements

Menjelaskan pernyataan masalah:
- Bagaimana cara membangun sebuah sistem yang dapat memberikan rekomendasi film yang dipersonalisasi berdasarkan genre film yang pernah ditonton dan disukai oleh pengguna?

- Bagaimana cara membangun sebuah sistem yang dapat merekomendasikan film berdasarkan pola rating dari pengguna lain yang memiliki selera serupa, tanpa memerlukan informasi tentang genre atau atribut film lainnya?

- Bagaimana cara mengukur dan membandingkan performa dari kedua pendekatan sistem rekomendasi tersebut untuk mengetahui tingkat akurasi dan relevansinya?

### Goals

- Mengembangkan model rekomendasi Content-Based Filtering yang mampu menyarankan film berdasarkan kesamaan genre.

- Mengembangkan model rekomendasi Collaborative Filtering menggunakan teknik faktorisasi matriks (Singular Value Decomposition atau SVD) untuk memprediksi rating dan menemukan film baru berdasarkan selera pengguna.

- Mengevaluasi kedua model menggunakan metrik yang sesuai (Precision & Recall untuk Content-Based, RMSE untuk Collaborative Filtering) untuk memahami kekuatan dan kelemahan masing-masing model.

### Solution statements
Untuk mencapai tujuan tersebut, dua pendekatan solusi akan diimplementasikan:

1. Content-Based Filtering: Pendekatan ini akan merekomendasikan film dengan menganalisis kemiripan atribut film, khususnya pada fitur genres. Teks genre akan diubah menjadi representasi numerik menggunakan TF-IDF, dan kemiripan antar film akan dihitung menggunakan Cosine Similarity. Solusi ini menjawab masalah rekomendasi berbasis atribut.

2. Collaborative Filtering: Pendekatan ini akan merekomendasikan film dengan mengidentifikasi pola tersembunyi (latent factors) dalam data rating pengguna. Teknik faktorisasi matriks, yaitu SVD, akan digunakan untuk memprediksi rating yang belum diberikan oleh pengguna dan merekomendasikan film dengan prediksi rating tertinggi. Solusi ini menjawab masalah rekomendasi berbasis komunitas.

## Data Understanding
Dataset yang digunakan dalam proyek ini adalah MovieLens 10M Dataset, yang berisi 10 juta rating film dari sekitar 72.000 pengguna untuk 10.000 film. Dataset ini merupakan sumber daya yang populer untuk penelitian dan pengembangan sistem rekomendasi karena ukurannya yang besar dan data rating yang otentik, yang memungkinkan pemodelan preferensi pengguna yang kompleks.

Dataset ini dapat diunduh melalui Kaggle: [MovieLens 10M Dataset](https://www.kaggle.com/datasets/amirmotefaker/movielens-10m-dataset-latest-version).

Data terdiri dari dua file utama: movies.dat dan ratings.dat.

Variabel pada dataset movies.dat:

- movie_id: ID unik untuk setiap film. (Tipe: numerik)
- title: Judul film beserta tahun rilisnya. (Tipe: teks)
- genres: Satu atau lebih genre yang diasosiasikan dengan film, dipisahkan oleh karakter |. (Tipe: teks)

Variabel pada dataset ratings.dat:

- user_id: ID unik untuk setiap pengguna. (Tipe: numerik)
- movie_id: ID unik film yang diberi rating. (Tipe: numerik)
- rating: Rating yang diberikan oleh pengguna, dengan skala 0.5 hingga 5.0. (Tipe: numerik)
- timestamp: Waktu pemberian rating dalam format epoch time. (Tipe: numerik)

## Data Exploration/Exploratory Data Analysis (EDA)
Analisis data eksploratif dilakukan untuk memahami distribusi dan karakteristik data.

1. **Distribusi Rating Film**  
Visualisasi menunjukkan bahwa rating paling banyak diberikan pada nilai 4.0, 3.0, dan 5.0. Hal ini mengindikasikan bahwa pengguna cenderung memberikan rating pada film yang mereka sukai, dan dataset ini lebih banyak menangkap preferensi positif daripada negatif.  

<div style="text-align: center;">
  <img src="data/movieDistribution.png" alt="Histogram">
</div>

2. **Distribusi Genre Film**  
Visualisasi genre menunjukkan bahwa Drama dan Comedy adalah genre yang paling dominan dalam dataset. Hal ini menciptakan popularity bias, di mana model kemungkinan besar akan lebih sering merekomendasikan film dari genre-genre populer ini karena jumlah datanya yang lebih banyak.  

<div style="text-align: center;">
  <img src="data/top10.png" alt="Histogram">
</div>

## Data Preparation
Beberapa langkah persiapan data dilakukan untuk memastikan data siap digunakan untuk pemodelan. Urutan proses ini sangat penting untuk menjamin kualitas data yang masuk ke dalam model.

1. **Menghapus Kolom timestamp:** Kolom timestamp dihapus dari data rating karena waktu pemberian rating tidak relevan untuk model baseline yang akan dibangun. Alasan utamanya adalah untuk menyederhanakan dataset dan mengurangi penggunaan memori, karena fokus utama adalah pada preferensi (rating) itu sendiri, bukan pada kapan preferensi itu dicatat.
2. **Sampling Pengguna Aktif:** Untuk efisiensi komputasi, pemodelan difokuskan pada pengguna yang paling aktif. Pengguna yang telah memberikan rating pada minimal 500 film dipilih. Alasan dari langkah ini adalah untuk memastikan model dilatih pada pengguna dengan data preferensi yang kaya dan historis, sehingga pola seleranya lebih mudah dipelajari oleh model collaborative filtering.
3. **Menggabungkan Data:** Data rating yang telah disaring (ratings_sample) digabungkan dengan data film (movies) berdasarkan movie_id. Tujuannya adalah untuk menciptakan satu DataFrame utama yang berisi semua informasi yang dibutuhkan (user, film, rating, genre) dalam satu tempat.
4. **Pemisahan Data (Train-Test Split):** Data yang telah digabungkan kemudian dibagi menjadi data latih (80%) dan data uji (20%). Langkah ini krusial untuk proses evaluasi model, di mana model akan dilatih pada data latih dan performanya akan diuji pada data uji yang belum pernah "dilihat" sebelumnya.

## Modeling
Dua model sistem rekomendasi dikembangkan untuk menyelesaikan permasalahan yang telah didefinisikan.

### 1. Content-Based Filtering
Model ini merekomendasikan film berdasarkan kesamaan genre.

Cara Kerja:  
- TF-IDF Vectorization: Kolom genres diubah menjadi matriks numerik di mana setiap baris mewakili film dan setiap kolom mewakili sebuah genre. Nilai dalam matriks ini (bobot TF-IDF) merepresentasikan seberapa penting sebuah genre bagi sebuah film.  
- Cosine Similarity: Metrik ini digunakan untuk menghitung skor kemiripan antara semua pasangan film berdasarkan matriks TF-IDF. Skornya berkisar dari 0 (tidak mirip) hingga 1 (identik).  
- Top-N Recommendations: Untuk sebuah film referensi, sistem akan mengambil N film dengan skor cosine similarity tertinggi sebagai rekomendasi.

Contoh Output:
Berikut adalah 5 rekomendasi teratas untuk film 'Iron Man (2008)'.

```text
--- Recommendations for 'Iron Man (2008)' ---
movie_id
260     Star Wars: Episode IV - A New Hope (a.k.a. Sta...
316                                       Stargate (1994)
442                                 Demolition Man (1993)
1196    Star Wars: Episode V - The Empire Strikes Back...
1210    Star Wars: Episode VI - Return of the Jedi (1983)
Name: title, dtype: object
```

### 2. Collaborative Filtering (SVD)
Model ini merekomendasikan film berdasarkan pola rating dari pengguna-pengguna yang memiliki selera serupa.  

Cara Kerja:
- ***User-Item Matrix*:** Sebuah matriks dibuat dengan pengguna sebagai baris, film sebagai kolom, dan rating sebagai nilainya. Sel yang kosong (film yang belum diberi rating) diisi dengan nilai 0.
- ***SVD (Singular Value Decomposition)*:** Matriks ini dipecah menjadi tiga matriks yang lebih kecil yang menangkap "faktor laten" atau fitur tersembunyi dari pengguna dan film.
- ***Prediksi Rating*:** Dengan mengalikan kembali ketiga matriks hasil SVD, kita mendapatkan matriks rating yang telah terisi penuh, termasuk prediksi rating untuk film yang belum pernah ditonton pengguna.
- ***Top-N Recommendations*:** Untuk seorang pengguna, sistem akan merekomendasikan film yang belum ia tonton dengan prediksi rating tertinggi.

Contoh Output:
Berikut adalah 10 rekomendasi teratas untuk pengguna dengan ID 32830.

```text
--- Top Movie Recommendations for User ID 32830 ---
   movie_id  predicted_rating                         title
0      3448          3.069020  Good Morning, Vietnam (1987)
1      2791          2.938787              Airplane! (1980)
2      4975          2.854144            Vanilla Sky (2001)
3      3552          2.844461             Caddyshack (1980)
4      1285          2.748382               Heathers (1989)
5      5400          2.693871     Sum of All Fears, The (2002)
6      3396          2.693188     Muppet Movie, The (1979)
7      1380          2.691832                  Grease (1978)
8      1641          2.685996     Full Monty, The (1997)
9      1997          2.663612         Exorcist, The (1973)
```

### Kelebihan dan Kekurangan Setiap Pendekatan
**Content-Based Filtering:**

- **Kelebihan:** Dapat merekomendasikan item yang tidak populer, tidak memerlukan data pengguna lain, dan dapat memberikan penjelasan rekomendasi (misalnya, "direkomendasikan karena Anda suka genre Action").
- **Kekurangan:** Terbatas pada fitur yang ada (hanya genre), sulit memberikan rekomendasi yang baru dan mengejutkan (serendipity), dan cenderung menghasilkan rekomendasi yang terlalu mirip (overspecialization).

**Collaborative Filtering (SVD):**

- **Kelebihan:** Mampu menemukan rekomendasi yang mengejutkan berdasarkan selera tersembunyi, tidak memerlukan fitur item (genre, aktor, dll.), dan seiring waktu dapat beradaptasi dengan perubahan selera pengguna.
- **Kekurangan:** Mengalami masalah "cold start" (tidak bisa memberi rekomendasi untuk pengguna/item baru), lebih boros secara komputasi, dan rentan terhadap popularity bias.
  
## Evaluation
Evaluasi dilakukan untuk mengukur performa masing-masing model secara kuantitatif.

### Metrik Evaluasi
**1. Content-Based Filtering:**

- **Precision@k:** Mengukur seberapa banyak item yang relevan dari k item teratas yang direkomendasikan. Metrik ini menjawab pertanyaan: "Dari 10 film yang direkomendasikan, berapa persen yang benar-benar disukai pengguna?"

- **Recall@k:** Mengukur seberapa banyak item relevan yang berhasil ditemukan oleh sistem dalam k item teratas. Metrik ini menjawab: "Dari semua film yang disukai pengguna, berapa persen yang berhasil kami rekomendasikan?"

**2. Collaborative Filtering (SVD):**

RMSE (Root Mean Squared Error): Mengukur rata-rata magnitudo kesalahan antara rating yang diprediksi oleh model dengan rating aktual yang diberikan oleh pengguna. Metrik ini dipilih karena masalahnya adalah prediksi nilai rating (regresi). Semakin kecil nilai RMSE, semakin akurat prediksi rating model. Formulanya adalah:


$$
\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}
$$  

Di mana $N$ adalah jumlah total rating pada data uji, $y_i$ adalah rating aktual, dan $\hat{y}_i$ adalah rating yang diprediksi oleh model.

### Hasil Evaluasi

**Content-Based Model:**

- Average Precision@10: 0.0320  
- Average Recall@10: 0.0042

**Analisis:** Skor presisi dan recall yang sangat rendah ini menunjukkan bahwa model yang hanya berbasis genre tidak efektif dalam menangkap selera pengguna secara akurat. Dari 10 rekomendasi, rata-rata hanya 0.3 film yang relevan, dan model ini hanya berhasil menemukan sebagian kecil dari semua film yang mungkin disukai pengguna.

**Collaborative Filtering (SVD) Model:**

- RMSE on Test Data: 2.2440

**Analisis:** Nilai RMSE sebesar 2.24 pada skala rating 1-5 tergolong sangat tinggi. Ini berarti prediksi rating model rata-rata meleset sekitar 2.24 poin dari rating sebenarnya. Hal ini menunjukkan bahwa meskipun model ini baik untuk membuat daftar rekomendasi yang menarik, ia tidak akurat dalam memprediksi nilai rating spesifik.

**Rencana Peningkatan:**

- Optimasi hyperparameter: Melakukan tuning terhadap jumlah latent factors dan nilai regularisasi dapat membantu menurunkan nilai error dan meningkatkan akurasi prediksi.
- Eksplorasi metode alternatif: Teknik seperti SVD++ atau Alternating Least Squares (ALS) bisa menjadi pilihan yang lebih stabil untuk menangani data sparse.
- Normalisasi data rating: Menerapkan normalisasi terhadap rating pengguna sebelum proses faktorisasi dapat mengurangi bias akibat perbedaan skala penilaian antar pengguna.
- Penanganan cold-start: Untuk pengguna atau film baru, pendekatan hybrid atau pemanfaatan metadata (jika tersedia) dapat membantu menghasilkan rekomendasi yang lebih tepat.

Pengembangan ke arah ini dapat membantu sistem menjadi lebih responsif terhadap preferensi pengguna dan lebih akurat dalam menyarankan film yang relevan, meskipun bekerja dalam batasan data yang tersedia saat ini.

# Ringkasan Landasan Teori Gizi & Rumus Perhitungan Diet (Skripsi UII)
**Sumber:** *Sistem Analisis Pola Konsumsi dan Rekomendasi Diet Berbasis Generative AI*

---

## BAB 2.1 Konsep Dasar Gizi dan Penilaian Konsumsi

BAB II 
LANDASAN TEORI DAN KAJIAN PUSTAKA 
 
Bab ini membahas landasan teori yang mendukung pengembangan sistem analisis pola 
konsumsi dan rekomendasi diet berbasis Generative AI. Pembahasan diawali dengan konsep 
dasar gizi dan penilaian konsumsi sebagai dasar perhitungan kebutuhan nutrisi dan evaluasi 
status gizi pengguna. Selanjutnya, diuraikan konsep kecerdasan buatan dalam bidang 
kesehatan, termasuk peran Generative AI dan teknik pendukungnya dalam pengolahan serta 
analisis data. Bab ini juga membahas teori pengolahan citra digital untuk identifikasi makanan 
berbasis image, pendekatan kecerdasan buatan dalam personalisasi rekomendasi diet, serta 
perbandingan berbagai pendekatan sistem rekomendasi diet. Landasan teori tersebut digunakan 
untuk memastikan bahwa sistem analisis pola konsumsi dan rekome ndasi diet yang 
dikembangkan memiliki dasar ilmiah yang kuat dan selaras dengan tujuan penelitian. 
2.1 Konsep Dasar Gizi dan Penilaian Konsumsi 
Ilmu gizi mempelajari bagaimana makanan yang dikonsumsi sehari-hari berpengaruh 
terhadap kondisi kesehatan manusia, termasuk proses metabolisme zat gizi dalam menjaga 
keseimbangan energi dan fungsi fisiologis tubuh (Almatsier, 2011). Status gizi seseorang 
sangat dipengaruhi oleh kecukupan asupan zat gizi dari pola makan harian, di mana 
ketidakseimbangan antara asupan dan kebutuhan tubuh dalam jangka waktu tertentu dapat 
menyebabkan masalah gizi, baik berupa kekurangan maupun kelebihan zat gizi (Rahmawati et 
al., 2025). Oleh karena itu, pemahaman konsep dasar gizi menjadi hal yang penting sebagai 
landasan dalam penelitian yang bertujuan menganalisis pola konsumsi serta mengevaluasi 
kesesuaian asupan dengan kebutuhan gizi setiap individu. 
Untuk mengukur kecukupan asupan tersebut, diperlukan proses penilaian konsumsi 
makanan, yaitu suatu metode yang digunakan untuk mengukur jenis, jumlah, dan pola makan 
individu sebagai dasar estimasi asupan energi dan zat gizi. Terdapat beberapa metode survei 
konsumsi makanan yang umum digunakan dalam penelitian gizi, antara lain Food Recall 24 
jam, Food Frequency Questionnaire (FFQ), dan Food Record. Metode Food Recall 24 jam 
dilakukan dengan mengumpulkan informasi seluruh makanan dan minuman yang dikonsumsi 
individu dalam kurun waktu 24 jam sebelumnya, sehingga dinilai representatif untuk 
menggambarkan asupan jangka pendek. Metode FFQ digunakan untuk menilai frekuensi 
konsumsi jenis makanan tertentu dalam periode yang lebih panjang seperti mingguan atau 
bulanan, sehingga lebih sesuai untuk menggambarkan kebiasaan makan jangka panjang.

Adapun metode Food Record dilakukan dengan mencatat secara mandiri setiap makanan yang 
dikonsumsi beserta estimasi jumlahnya pada saat yang bersamaan dengan waktu konsumsi, 
sehingga data yang dihasilkan tidak bergantung pada daya ingat individu dan cenderung lebih 
akurat dibandingkan metode retrospektif (Kementerian Kesehatan Republik Indonesia, 2020). 
Dalam konteks penelitian ini, pendekatan penilaian konsumsi yang digunakan mengacu 
pada prinsip metode Food Record, yaitu pencatatan asupan makanan yang dilakukan secara 
bersamaan dengan waktu konsumsi. Kesesuaian metode ini juga sejalan dengan prinsip 
pedoman gizi seimbang yang menekankan pentingnya pemantauan konsumsi pangan secara 
nyata dan berkelanjutan (Rahmawati et al., 2025). Data makanan yang diperoleh melalui 
pendekatan ini selanjutnya dipetakan ke sumber data gizi terstandar, yaitu Tabel Komposisi 
Pangan Indonesia (TKPI), untuk memperkirakan asupan energi dan makronutrien 
(Kementerian Kesehatan Republik Indonesia, 2020).  
2.1.1 Kebutuhan Kalori dan Makronutrien Harian (Karbohidrat, Protein, dan Lemak) 
Dalam penelitian ini, kebutuhan kalori dan makronutrien harian digunakan sebagai dasar 
dalam penentuan rekomendasi diet yang disesuaikan dengan kondisi pengguna. Kebutuhan 
energi didefinisikan sebagai jumlah kalori yang diperlukan tubuh untuk mempertahanka n 
fungsi fisiologis, aktivitas fisik di mana ketidakseimbangan antara asupan dan kebutuhan 
energi dapat menyebabkan kondisi defisit maupun surplus yang berdampak pada status gizi 
(Almatsier, 2011). Makronutrien yang terdiri dari karbohidrat, protein, dan lemak berperan 
sebagai sumber energi utama dengan fungsi metabolik yang saling melengkapi, sehingga 
proporsinya perlu dijaga agar dapat mendukung efektivitas diet serta menjaga kesehatan tubuh 
secara keseluruhan. 
Kebutuhan energi setiap individu dapat diestimasi secara matematis melalui pendekatan 
bertahap yang dimulai dari perhitungan Basal Metabolic Rate (BMR), yaitu jumlah energi 
minimal yang dibutuhkan tubuh untuk mempertahankan fungsi fisiologis dasar dalam kondisi 
istirahat (Almatsier, 2011). Salah satu persamaan yang umum digunakan untuk mengestimasi 
BMR adalah persamaan Mifflin-St Jeor, yang mempertimbangkan variabel berat badan, tinggi 
badan, usia, dan jenis kelamin sebagaimana ditunjukkan pada Persamaan (2.1) dan Persamaan 
(2.2) (Almatsier, 2011): 
 
𝐵𝑀𝑅𝑝𝑟𝑖𝑎 = (10 × 𝐵𝐵) + (6,25 × 𝑇𝐵) − (5 × 𝑈) + 5 (2.1) 
𝐵𝑀𝑅𝑤𝑎𝑛𝑖𝑡𝑎 =  (10 × 𝐵𝐵) + (6,25 × 𝑇𝐵) − (5 × 𝑈) − 161 (2.2)

(BB = berat badan dalam kg, TB = tinggi badan dalam cm, U = usia dalam tahun). Nilai 
BMR yang telah diperoleh merepresentasikan kebutuhan energi dasar tubuh dalam kondisi 
istirahat. Selanjutnya, nilai tersebut digunakan untuk menghitung Total Daily Energy 
Expenditure (TDEE), yaitu total kebutuhan energi harian yang telah memperhitungkan tingkat 
aktivitas fisik pengguna sebagaimana ditunjukkan pada Persamaan (2.3): 
𝑇𝐷𝐸𝐸 = 𝐵𝑀𝑅 × 𝑃𝐴𝐿 (2.3) 
dimana PAL (Physical Activity Level) merupakan faktor pengali yang merepresentasikan 
intensitas aktivitas fisik harian pengguna. Nilai PAL ditentukan berdasarkan kategori aktivitas 
yang dipilih pengguna, dengan rentang nilai sebagaimana ditunjukkan pada Tabel 2.1 berikut. 
Tabel 2. 1 Faktor Aktivitas Fisik (Physical Activity Level / PAL) 
Kategori Aktivitas Deskripsi Nilai PAL 
Sedentari Hampir tidak ada aktivitas fisik, mayoritas duduk 1,2 
Ringan Olahraga ringan 1–3 hari per minggu 1,375 
Sedang Olahraga sedang 3–5 hari per minggu 1,55 
Aktif Olahraga intensif 6–7 hari per minggu 1,725 
Sangat Aktif Pekerjaan fisik berat atau latihan dua kali sehari 1,9 
Nilai TDEE yang diperoleh akan digunakan sebagai dasar dalam menentukan target kalori 
harian sesuai dengan tujuan diet pengguna untuk penurunan berat badan, diterapkan defisit 
kalori sebesar 500 kkal dari nilai TDEE. Untuk pemeliharaan berat badan, nilai kalori tetap 
mengikuti TDEE dan, untuk peningkatan massa otot, diterapkan surplus kalori sebesar 300 
kkal. Pendekatan defisit 500 kkal per hari merupakan metode umum dalam perencanaan diet 
karena secara teoritis dapat menghasilkan penurunan berat badan sekitar 0,5 kg per minggu, 
dengan asumsi 1 kg lemak tubuh setara dengan sekitar 7.700 kkal (Almatsier, 2011).  
Berdasarkan target energi harian, distribusi makronutrien ditentukan sebagai dasar 
penyusunan rekomendasi diet. Pembagian ini mengacu pada pedoman gizi seimbang, yaitu 
karbohidrat 45–65%, protein 10–20%, dan lemak 20–35% dari total energi harian (Rahmawati 
et al., 2025) sebagaimana ditunjukkan pada Tabel 2.2. 
Tabel 2. 2 Distribusi Makronutrien Harian 
Makronutrien Persentase (%) Fungsi Utama 
Karbohidrat 45–65% Sumber energi utama 
Protein 10–20% Pembentukan dan perbaikan jaringan 
Lemak 20–35% Cadangan energi dan membantu penyerapan vitamin

Untuk memudahkan implementasi dalam sistem, nilai makronutrien yang masih dalam 
bentuk persentase kemudian dikonversi ke dalam satuan gram, dilakukan konversi berdasarkan 
nilai energi masing-masing zat gizi, yaitu 1 gram karbohidrat setara dengan 4 kkal, 1 gram 
protein setara dengan 4 kkal, dan 1 gram lemak setara dengan 9 kkal  (Almatsier, 2011). 
Perhitungan jumlah makronutrien dalam gram dapat dilakukan menggunakan Persamaan (2.4), 
Persamaan (2.5), dan Persamaan (2.6) sebagai berikut: 
 
Karbohidrat (gram): 
Karbohidrat (g) = Persentase.Total Kalori
4  (2.4) 
Protein (gram): 
Protein (g) = Persentase.Total Kalori
4  (2.5) 
Lemak (gram): 
Lemak (g) = Persentase.Total Kalori
9  (2.6) 
Proporsi makronutrien disesuaikan berdasarkan tujuan diet pengguna. Secara umum 
mengacu pada pedoman gizi seimbang yang telah di tampilkan pada Tabel 2.2, namun pada 
kondisi tertentu seperti penurunan berat badan dan peningkatan massa otot, asupan protein 
dapat ditingkatkan di atas rentang tersebut. Peningkatan protein diketahui berperan dalam 
mempertahankan massa otot selama defisit energi, meningkatkan r asa kenyang, serta 
mendukung sintesis jaringan otot (Rahmawati et al., 2025).Penyesuaian ini dilakukan dengan 
mengatur kembali proporsi karbohidrat dan lemak sesuai tujuan diet, baik untuk penurunan, 
pemeliharaan, maupun peningkatan massa otot. Dengan demikian, rekomendasi energi dan 
makronutrien menjadi lebih adaptif dan terpersonalisasi. Namun, perhitungan tetap bersifat 
estimasi karena didasarkan pada model umum seperti BMR dan TDEE, yang dapat dipengaruhi 
oleh variasi individu (Almatsier, 2011). 
2.1.2 Tabel Komposisi Pangan Indonesia (TKPI) sebagai Acuan Data Gizi 
Tabel Komposisi Pangan Indonesia (TKPI) merupakan sumber data gizi resmi nasional 
yang disusun oleh Kementerian Kesehatan Republik Indonesia dan digunakan sebagai acuan 
standar dalam analisis kandungan gizi makanan. TKPI menyediakan informasi kuantitatif 
megenai kandungan energi dan zat gizi berbagai jenis bahan pangan yang umum dikonsumsi 
masyarakat Indonesia, termasuk nilai energi, karbohidrat, protein, dan lemak per satuan berat 
tertentu. Data yang tercantum dalam TKPI digunakan secara luas dalam penelitian gizi, survei 
konsumsi pangan, perencanaan menu, serta evaluasi kecukupan gizi, sehingga keberadaannya

menjadi penting karena menyediakan basis data yang terstandar, tervalidasi, dan sesuai dengan 
karakteristik pangan (Kementerian Kesehatan Republik Indonesia, 2020) . Dengan 
menggunakan TKPI sebagai acuan, proses analisis konsumsi pangan dapat dilakukan secara 
lebih konsisten dan hasilnya dapat dibandingkan dengan rekomendasi Angka Kecukupan Gizi 
(AKG) yang berlaku secara nasional (Kementerian Kesehatan Republik Indonesia, 2019). 
Dalam konteks analisis pola konsumsi, TKPI digunakan sebagai sumber referensi utama 
untuk memperoleh informasi kandungan energi dan makronutrien pada berbagai jenis 
makanan. Data yang disajikan dalam TKPI umumnya dinyatakan dalam satuan standar per 100 
gram, sehingga memungkinkan dilakukan estimasi nilai gizi secara proporsional sesuai dengan 
jumlah konsumsi. Pemanfaatan sumber data yang terstandarisasi ini berperan penting dalam 
menjaga konsistensi dan meningkatkan akurasi estimasi asupan gizi, serta memin imalkan 
potensi bias yang dapat timbul akibat penggunaan data yang tidak seragam atau tidak 
terverifikasi (Kementerian Kesehatan Republik Indonesia, 2020). 
Meskipun TKPI menjadi landasan utama dalam sistem, terdapat beberapa keterbatasan 
yang perlu diperhatikan. TKPI tidak mencakup seluruh jenis makanan yang beredar di 
masyarakat, sehingga beberapa jenis makanan, seperti makanan olahan, menu campuran, dapat 
tidak tersedia dalam basis data. Dalam kondisi tersebut, sistem tidak selalu dapat memperoleh 
nilai gizi secara langsung dari referensi TKPI. Oleh karena itu, sistem memanfaatkan 
Generative AI sebagai mekanisme estimasi nutrisi alternatif untuk memperkirakan kandungan 
energi dan makronutrien berdasarkan konteks makanan yang diberikan pengguna. Namun, 
estimasi yang dihasilkan oleh Generative AI bersifat pendekatan (approximation) dan tidak 
memiliki tingkat akurasi yang setara dengan data referensi yang tersedia dalam TKPI. Selain 
itu, nilai gizi dalam TKPI sendiri merupakan nilai rata -rata yang dalam praktiknya dapat 
berbeda dari kandungan gizi aktual akibat variasi bahan, ukuran porsi, metode pengolahan, dan 
kondisi penyimpanan makanan. Oleh karena itu, hasil analisis asupan gizi dalam penelitian ini 
perlu dipahami sebagai estimasi berbasis data referensi, bukan sebagai penilaian gizi klinis 
yang bersifat absolut. Untuk mendukung interpretasi hasil yang lebih tepat, estimasi asupan 
tersebut dikaitkan dengan kondisi status gizi pengguna yang dievaluasi melalui pengukuran 
antropometri seperti Indeks Massa Tubuh (IMT). 
2.1.3 Evaluasi Kondisi Gizi Berdasarkan Indeks Massa Tubuh (IMT) 
Indeks Massa Tubuh (IMT) merupakan salah satu indikator antropometri yang paling 
umum digunakan untuk menilai status gizi orang dewasa berdasarkan hubungan proporsional 
antara berat badan dan tinggi badan seseorang. Penggunaan IMT dinilai praktis karena hanya

memerlukan dua parameter pengukuran yang mudah diperoleh, yaitu berat badan dan tinggi 
badan, sehingga metode ini banyak diterapkan dalam pemantauan status gizi baik pada tingkat 
individu maupun populasi. Meskipun IMT tidak secara langsung menggambarkan komposisi 
tubuh atau distribusi lemak secara spesifik, indikator ini tetap relevan sebagai alat penapisan 
awal dalam mengidentifikasi kondisi gizi kurang maupun gizi lebih pada kelompok usia 
dewasa. Nilai IMT diperoleh dengan membagi berat badan dalam satuan kilogram dengan 
kuadrat tinggi badan dalam satuan meter, sebagaimana dinyatakan pada Persamaan (2.7)  
(Kementerian Kesehatan Republik Indonesia, 2020): 
𝐼𝑀𝑇 = 𝐵𝑒𝑟𝑎𝑡 𝐵𝑎𝑑𝑎𝑛 (𝑘𝑔)
 𝑇𝑖𝑛𝑔𝑔𝑖 𝐵𝑎𝑑𝑎𝑛 (𝑚) . 𝑇𝑖𝑛𝑔𝑔𝑖 𝐵𝑎𝑑𝑎𝑛 (𝑚) (2.7) 
(BB = berat badan dalam kg, TB = tinggi badan dalam meter),  Hasil perhitungan IMT 
selanjutnya diinterpretasikan berdasarkan klasifikasi status gizi yang ditetapkan oleh 
Kementerian Kesehatan Republik Indonesia, sebagaimana ditunjukkan pada Tabel 2.3 . 
Tabel 2. 3 Interpretasi Indeks Massa Tubuh (IMT) untuk Indonesia 
Kategori Keterangan Ambang Batas 
Kurus Kekurangan berat badan tingkat berat < 17,0 
Kurus Kekurangan berat badan tingkat ringan 17,0 – 18,4 
Normal Berat badan sesuai 18,5 – 25,0 
Gemuk Kelebihan berat badan tingkat ringan (Overweight) 25,1 – 27,0 
Gemuk Kelebihan berat badan tingkat berat (Obesitas) > 27,0 
IMT memiliki beberapa kelebihan, di antaranya mudah digunakan, tidak memerlukan 
peralatan khusus, serta dapat memberikan gambaran awal mengenai status gizi seseorang. Oleh 
karena itu, IMT sering digunakan sebagai alat penapisan awal dalam mengidentifikasi kondisi 
gizi kurang maupun gizi lebih pada orang dewasa. 
Namun demikian, IMT juga memiliki keterbatasan. IMT tidak mampu membedakan antara 
massa lemak dan massa otot, sehingga individu dengan massa otot tinggi, seperti atlet, dapat 
terklasifikasi sebagai overweight atau obesitas meskipun memiliki komposisi tubuh yang baik. 
Selain itu, IMT tidak mempertimbangkan distribusi lemak tubuh, padahal distribusi lemak, 
khususnya lemak visceral, berpengaruh terhadap risiko penyakit metabolik. Oleh karena itu, 
hasil interpretasi IMT perlu dipahami secara hati-hati dan tidak digunakan sebagai satu-satunya 
indikator dalam penilaian status gizi. Mengingat keterbatasan tersebut, data IMT dalam 
penelitian ini digunakan sebagai salah satu variabel pendukung yang dikombinasikan dengan 
data asupan gizi dan pola konsumsi pengguna, sehingga sistem berbasis kecerdasan buatan

---

## LAMPIRAN D: Implementasi Rumus Perhitungan Kebutuhan Nutrisi

```typescript
Lampiran D Implementasi Perhitungan Kebutuhan Nutrisi  
// Perhitungan BMI 
function computeBMI(weightKg: number, heightCm: number): number { 
  const heightM = heightCm / 100 
  if (heightM <= 0) return 0 
  return weightKg / (heightM * heightM) 
} 
//Penentuan faktor aktivitas  
function getActivityMultiplier(activityLevel: string | null): number { 
  // Menentukan faktor aktivitas berdasarkan input pengguna 
  switch ((activityLevel || "").toLowerCase()) { 
    case "ringan": 
      return 1.375 
    case "sedang": 
      return 1.55 
    case "berat": 
      return 1.725 
    case "atlet": 
      return 1.9 
    default: 
      return 1.2 // default sedentari 
  } 
} 
//Perhitungan BMR 
function calculateBMR( 
  weightKg: number, 
  heightCm: number, 
  age: number, 
  gender: Gender, 
): number { 
  // Validasi input 
  if (!weightKg || !heightCm || age < 0) return 0 
 
  // Rumus Mifflin-St Jeor 
  const base = 10 * weightKg + 6.25 * heightCm - 5 * age 
 
  // Penyesuaian berdasarkan jenis kelamin 
  const genderAdjustment = gender === "perempuan" ? -161 : 5 
 
  // Hasil dibulatkan 
  return Math.round(base + genderAdjustment) 
} 
//Perhitungan TDEE  
function calculateTDEE(bmr: number, activityLevel: string | null): number 
{

// Jika BMR tidak valid, kembalikan 0 
  if (!bmr) return 0 
 
  // TDEE = BMR × faktor aktivitas 
  return Math.round(bmr * getActivityMultiplier(activityLevel)) 
} 
//perhitungan target kalori  
function calculateTargetCalories(tdee: number, tujuan: DietGoal | null): 
number { 
  // Jika TDEE tidak valid, gunakan default 
  if (!tdee || tdee < 1000) return 2000 
 
  // Penyesuaian berdasarkan tujuan diet 
  switch (tujuan) { 
    case "menurunkan_berat": 
      return Math.max(1200, Math.round(tdee - 500)) // defisit 
    case "meningkatkan_berat": 
      return Math.round(tdee + 300) // surplus 
    case "meningkatkan_performa": 
      return Math.round(tdee + 150) 
    case "menjaga_berat": 
    default: 
      return Math.round(tdee) 
  } 
} 
// Perhitungan Target Makronutrein   
function calculateMacroTargets( 
  calories: number, 
  tujuan: DietGoal | null, 
  weightKg: number, 
): MacroTargets { 
 
  // Jika kalori tidak valid, gunakan nilai default 
  if (!calories || calories < 1000) { 
    return { protein: 100, carbs: 250, fat: 56 } 
  } 
 
  let proteinPerKg = 1.6 
  let fatPercent = 0.25 
 
  // Penyesuaian protein berdasarkan tujuan diet 
  switch (tujuan) { 
    case "menurunkan_berat": 
      proteinPerKg = 1.8 
      break 
    case "meningkatkan_berat":

proteinPerKg = 1.8 
      break 
    case "meningkatkan_performa": 
      proteinPerKg = 2.0 
      break 
    case "menjaga_berat": 
    default: 
      proteinPerKg = 1.6 
      break 
  } 
 
  // Validasi berat minimal 
  const safeWeight = Math.max(40, toNum(weightKg, 0)) 
 
  // Perhitungan protein (gram/kg BB) 
  const protein = Math.round(safeWeight * proteinPerKg) 
 
  // Lemak = 25% dari kalori 
  const fat = Math.round((calories * fatPercent) / 9) 
 
  // Karbohidrat = sisa kalori 
  const carbs = Math.max( 
    0, 
    Math.round((calories - protein * 4 - fat * 9) / 4), 
  ) 
 
  return { protein, carbs, fat } 
} 
// Perhitungan Air 
function computeWaterTargetMl(weightKg: number, mlPerKg = 35): number { 
  if (!Number.isFinite(weightKg) || weightKg <= 0) return 2000 
  return clamp(Math.round(weightKg * mlPerKg), 1200, 5000) 
} 
// Penentuan Kategori IMT 
function getBMICategory(bmi: number): string { 
  // Menentukan kategori berdasarkan nilai BMI 
  if (bmi < 18.5) return "Kurus" 
  if (bmi < 25) return "Normal" 
  if (bmi < 30) return "Kelebihan Berat" 
  return "Obesitas" 
}
```

---

### Ringkasan Parameter & Rumus Utama:
1. **Indeks Massa Tubuh (IMT / BMI):**
   - Rumus: $\text{IMT} = \frac{\text{Berat Badan (kg)}}{(\text{Tinggi Badan (m)})^2}$
   - Klasifikasi Kemenkes:
     * Sangat Kurus (Kekurangan BB tingkat berat): $< 17.0$
     * Kurus (Kekurangan BB tingkat ringan): $17.0 - 18.4$
     * Normal: $18.5 - 25.0$
     * Gemuk (Kelebihan BB tingkat ringan): $25.1 - 27.0$
     * Obesitas (Kelebihan BB tingkat berat): $> 27.0$

2. **Basal Metabolic Rate (BMR) - Persamaan Mifflin-St Jeor:**
   - **Pria:** $\text{BMR} = (10 \times \text{BB}) + (6.25 \times \text{TB}) - (5 \times U) + 5$
   - **Wanita:** $\text{BMR} = (10 \times \text{BB}) + (6.25 \times \text{TB}) - (5 \times U) - 161$
   *(BB dalam kg, TB dalam cm, U dalam tahun)*

3. **Total Daily Energy Expenditure (TDEE):**
   - Rumus: $\text{TDEE} = \text{BMR} \times \text{PAL}$
   - **Physical Activity Level (PAL):**
     * Sedentari (minim aktivitas): 1.2
     * Aktivitas Ringan (olahraga 1-3 hari/minggu): 1.375
     * Aktivitas Sedang (olahraga 3-5 hari/minggu): 1.55
     * Sangat Aktif (olahraga berat 6-7 hari/minggu): 1.725
     * Ekstra Aktif (pekerja fisik/atlet): 1.9

4. **Distribusi Kebutuhan Makronutrien:**
   - **Karbohidrat:** 45% - 65% dari total kalori (1 gram karbohidrat = 4 kkal)
   - **Protein:** 10% - 20% (atau 1.2 - 2.0 g/kg BB sesuai target) (1 gram protein = 4 kkal)
   - **Lemak:** 20% - 30% dari total kalori (1 gram lemak = 9 kkal)


========================================

# Pedoman Gizi Seimbang (PGS) 2014
**Sumber:** *Peraturan Menteri Kesehatan Republik Indonesia Nomor 41 Tahun 2014 tentang Pedoman Gizi Seimbang*

---

## 1. Empat Pilar Gizi Seimbang
Prinsip Gizi Seimbang terdiri dari 4 (empat) Pilar yang pada dasarnya merupakan rangkaian upaya untuk menyeimbangkan antara zat gizi yang keluar dan zat gizi yang masuk dengan memantau berat badan secara teratur:
1. Membiasakan mengonsumsi aneka ragam makanan.
2. Membiasakan perilaku hidup bersih.
3. Melakukan aktivitas fisik secara teratur.
4. Memantau dan mempertahankan berat badan dalam batas normal.

BAB II 
PRINSIP GIZI SEIMBANG 
 
A. Empat Pilar Gizi Seimbang 
Pedoman Gizi Seimbang yang telah diimplementasikan di Indonesia 
sejak tahun 1955 merupakan realisasi dari rekomendasi Konferensi 
Pangan Sedunia di Roma tahun 1992. Pedoman tersebut menggantikan 
slogan “4 Sehat 5 Sempurna” yang telah diperkenalkan sejak tahun 1952 
namun sudah tidak sesuai lagi dengan perkembangan ilmu pengetahuan 
dan teknologi (IPTEK) dalam bidang gizi serta masalah dan tantangan 
yang dihadapi. Diyakini dengan mengimplementasikan Pedoman Gizi 
Seimbang secara benar, semua masalah gizi dapat diatasi. 
Prinsip Gizi Seimbang terdiri dari 4 (empat) Pilar yang pada dasarnya 
merupakan rangkaian upaya untuk menyeimbangkan antara zat gizi yang 
keluar dan zat gizi yang masuk dengan memantau berat badan secara 
teratur.  
 
 
 
 
 
 
 
 
 
 
 
 
Empat Pilar tersebut adalah: 
1. Mengonsumsi anekaragam pangan 
Tidak ada satupun jenis makanan yang mengandung semua 
jenis zat gizi yang dibutuhkan tubuh untuk menjamin pertumbuhan 
dan mempertahankan kesehatannya, kecuali Air Susu Ibu (ASI) 
untuk bayi baru lahir sampai berusia 6 bulan. Contoh: nasi 
merupakan sumber utama kalori, tetapi miskin vitamin dan mineral; 
sayuran dan buah-buahan pada umumnya kaya akan vitamin,

mineral dan serat, tetapi miskin kalori dan protein; ikan merupakan 
sumber utama protein tetapi sedikit kalori. Khusus untuk bayi 
berusia 0-6 bulan, ASI merupakan makanan tunggal yang sempurna. 
Hal ini disebabkan karena ASI dapat mencukupi kebutuhan untuk 
tumbuh dan berkembang dengan optimal, s erta sesuai dengan 
kondisi fisiologis pencernaan dan fungsi lainnya dalam tubuh. 
Apakah mengonsumsi makanan beragam tanpa memperhatikan 
jumlah dan proporsinya sudah benar? Tentu tidak benar. 
Yang dimaksudkan beranekaragam dalam prinsip ini selain 
keanekaragaman jenis pangan juga termasuk proporsi makanan yang 
seimbang, dalam jumlah yang cukup, tidak berlebihan dan dilakukan 
secara teratur. Anjuran pola makan dalam beberapa dekade terakhir 
telah memperhitungkan proporsi setiap kelompok pangan sesuai 
dengan kebutuhan yang seharusnya. Contohnya, saat ini dianjurkan 
mengonsumsi lebih banyak sayuran dan buah-buahan dibandingkan 
dengan anjuran sebelumnya. Demikian pula jumlah makanan yang 
mengandung gula, garam dan lemak yang dapat meningkatkan resiko 
beberapa penyakit tidak menular, dianjurkan untuk dikurangi.  
Akhir-akhir ini minum air dalam jumlah yang cukup telah 
dimasukkan dalam komponen gizi seimbang oleh karena pentingnya 
air dalam proses metabolisme dan dalam pencegahan dehidrasi. 
2. Membiasakan perilaku hidup bersih 
Penyakit infeksi merupakan salah satu faktor penting yang 
mempengaruhi status gizi seseorang secara langsung, terutama anak-
anak. Seseorang yang menderita penyakit infeksi akan mengalami 
penurunan nafsu makan sehingga jumlah dan jenis zat gizi yang 
masuk ke tubuh berkurang. Sebaliknya pada keadaan infeksi, tubuh 
membutuhkan zat gizi yang lebih banyak untuk memenuhi 
peningkatan metabolisme pada orang yang menderita infeksi 
terutama apabila disertai panas. Pada orang yang menderita penyakit 
diare, berarti mengalami kehilangan zat gizi dan cairan secara 
langsung akan memperburuk kondisinya. Demikian pula sebaliknya, 
seseorang yang menderita kurang gizi akan mempunyai risiko 
terkena penyakit infeksi karena pada keadaan kurang gizi daya tahan 
tubuh seseorang menurun, sehingga kuman penyakit lebih mudah 
masuk dan berkembang. Kedua hal tersebut menunjukkan bahwa 
hubungan kurang gizi dan penyakit infeksi adalah hubungan timbal 
balik.

Budaya perilaku hidup bersih akan menghindarkan seseorang 
dari keterpaparan terhadap sumber infeksi. Contoh: 1) selalu 
mencuci tangan dengan sabun dan air bersih mengalir sebelum 
makan, sebelum memberikan ASI, sebelum menyiapkan makanan 
dan minuman, dan setelah buang air besar dan kecil, akan 
menghindarkan terkontaminasinya tangan dan makanan dari kuman 
penyakit antara lain kuman penyakit typus dan disentri; 2) menutup 
makanan yang disajikan akan menghindarkan makanan dihinggapi 
lalat dan binatang lainnya serta debu yang membawa berbagai 
kuman penyakit; 3) selalu menutup mulut dan hidung bila bersin, 
agar tidak menyebarkan kuman penyakit; dan 4) selalu 
menggunakan alas kaki agar terhindar dari penyakit kecacingan.  
3. Melakukan aktivitas fisik 
Aktivitas fisik yang meliputi segala macam kegiatan tubuh 
termasuk olahraga merupakan salah satu upaya untuk 
menyeimbangkan antara pengeluaran dan pemasukan zat gizi 
utamanya sumber energi dalam tubuh. 
Aktivitas fisik memerlukan energi. Selain itu, aktivitas fisik juga 
memperlancar sistem metabolisme di dalam tubuh termasuk 
metabolisme zat gizi. Oleh karenanya, aktivitas fisik berperan dalam 
menyeimbangkan zat gizi yang keluar dari dan yang masuk ke dalam 
tubuh. 
4. Memantau Berat Badan (BB) secara teratur untuk mempertahankan 
berat badan normal 
Bagi orang dewasa salah satu indikator yang menunjukkan 
bahwa telah terjadi keseimbangan zat gizi di dalam tubuh adalah 
tercapainya berat badan yang normal, yaitu berat badan yang sesuai 
untuk tinggi badannya. Indikator tersebut dikenal dengan Indeks 
Masa Tubuh (IMT). Oleh karena itu, pemantauan BB normal 
merupakan hal yang harus menjadi bagian dari ‘Pola Hidup’ dengan 
‘Gizi Seimbang’, sehingga dapat mencegah penyimpangan BB dari BB 
normal, dan apabila terjadi penyimpangan dapat segera dilakukan 
langkah-langkah pencegahan dan penanganannya.  
Bagi bayi dan balita indikator yang digunakan adalah 
perkembangan berat badan sesuai dengan pertambahan umur. 
Pemantauannya dilakukan dengan menggunakan KMS.

Yang dimaksud dengan berat badan normal adalah : a. untuk 
orang dewasa jika IMT 18,5-25,0; b. bagi anak Balita dengan 
menggunakan KMS dan berada di dalam pita hijau. Kita dapat 
melihat dalam Tabel Indeks Masa Tubuh (IMT) dan Kartu Menuju 
Sehat sebagai berikut :   
 
Tabel Indeks Masa Tubuh (IMT) dan Kartu Menuju Sehat (KMS)
 
a. Grafik indeks masa tubuh (IMT) orang dewasa

Misalkan    :  
Seseorang umur 20 tahun dengan berat badan 63 kg dan tinggi 
160 cm 
Buatlah 2 garis lurus sebagai berikut : 
(1) Tariklah garis lurus dari sumbu Berat Badan pada titik 63 ke 
kanan sejajar dengan sumbu Tinggi Badan 
(2) Tariklah garis lurus dari sumbu Tinggi Badan pada titik 160 
tegal lurus sejajar dengan sumbu Berat Badan 
 
Kedua garis tersebut berpotongan pada titik sekitar angka 25.  
Angka 25 ini menunjukkan besar IMT orang tersebut. 
 
Untuk mengetahui nilai IMT, dapat dihitung dengan rumus 
berikut : 
 
 
 
 
 
Batas ambang IMT ditentukan dengan merujuk ketentuan 
FAO/WHO. Untuk kepentingan Indonesia, batas ambang 
dimodifikasi berdasarkan pengalaman klinis dan hasil penelitian 
di beberapa negara berkembang. Batas ambang IMT untuk 
Indonesia adalah sebagai berikut : 
 
 Kategori IMT 
Sangat Kurus Kekurangan berat badan 
tingkat berat < 17,0 
Kurus Kekurangan berat badan 
tingkat ringan 17 - < 18,5 
Normal  18,5-25,0 
Gemuk 
(Overweight) 
Kelebihan berat badan 
tingkat ringan > 25,0-27,0 
Obese Kelebihan berat badan 
tingkat berat > 27,0 
Cara Menentukan IMT 
Menggunakan Grafik Indeks Masa Tubuh Orang Dewasa Umur 
di Atas 18 Tahun 
Berat Badan (kg) 
  IMT =  
Tinggi Badan (m) x Tinggi Badan (m)

Jika seseorang termasuk kategori : 
 
(1) IMT<17,0 keadaan orang tersebut disebut sangat kurus 
dengan kekurangan berat badan tingkat berat atau 
Kekurangan Energi Kronis (KEK) berat. 
(2) IMT 17,0<18,5 keadaan orang tersebut disebut kurus dengan 
kekurangan berat badan tingkat ringan atau KEK ringan. 
 
 
 
 
 
 
 
 
(3) IMT 18,5 -25,0 keadaan orang tersebut termasuk kategori 
normal. 
(4) IMT > 25,0-27,0 keadaan orang tersebut disebut gemuk 
(Overwight) dengan kelebihan berat badan tingkat ringan. 
(5) IMT > 27,0 keadaan orang tersebut disebut obese dengan 
kelebihan berat badan tingkat berat. 
 
Perhatian 
Seseorang yang termasuk kategori kekurangan berat 
badan tingkat ringan (KEK ringan) sudah perlu mendapat 
perhatian untuk segera menaikkan berat badannya. 
Perhatian 
Seseorang dengan IMT di atas 25,0 harus berhati-hati 
agar berat badan tidak naik. Dianjurkan untuk segera 
menurunkan berat badan dalam batas normal.

b. Grafik pertumbuhan dan perkembangan balita





---

## 2. Sepuluh Pesan Umum Pedoman Gizi Seimbang
1. Syukuri dan nikmati aneka ragam makanan.
2. Banyak makan sayuran dan cukup buah-buahan.
3. Biasakan mengonsumsi lauk pauk yang mengandung protein tinggi.
4. Biasakan mengonsumsi aneka ragam makanan pokok.
5. Batasi konsumsi pangan manis, asin dan berlemak.
6. Biasakan Sarapan.
7. Biasakan minum air putih yang cukup dan aman.
8. Biasakan membaca label pada kemasan pangan.
9. Cuci tangan pakai sabun dengan air bersih mengalir.
10. Lakukan aktivitas fisik yang cukup dan pertahankan berat badan normal.

BAB III 
PESAN GIZI SEIMBANG 
 
A. Pesan Umum 
Pesan umum ini berlaku untuk usia dewasa dari berbagai lapisan  
masyarakat dalam kondisi sehat, dan untuk mempertahankan hidup 
sehat. 
1. Syukuri dan nikmati anekaragam makanan 
Kualitas atau mutu gizi dan kelengkapan zat gizi dipengaruhi 
oleh keragaman jenis pangan yang dikonsumsi. Semakin beragam 
jenis pangan yang dikonsumsi semakin mudah untuk memenuhi 
kebutuhan gizi. Bahkan semakin beragam pangan yang dikonsumsi 
semakin mudah tubuh memperoleh berbagai zat lainnya yang 
bermanfaat bagi kesehatan. Oleh karena itu konsumsi anekaragam 
pangan merupakan salah satu anjuran penting dalam mewujudkan 
gizi seimbang. 
Selain memperhatikan keanekaragaman makanan dan minuman  
juga perlu memperhatikan dari aspek  keamanan pangan yang berarti 
makanan dan minuman itu harus bebas dari cemaran biologis, kimia 
dan benda lain yang dapat mengganggu, merugikan dan 
membahayakan kesehatan masyarakat. 
Cara menerapkan pesan ini adalah dengan mengonsumsi lima 
kelompok pangan setiap hari atau setiap kali makan. Kelima 
kelompok pangan tersebut adalah makanan pokok, lauk-pauk, 
sayuran, buah-buahan dan minuman. Mengonsumsi lebih dari satu 
jenis untuk setiap kelompok makanan (makanan pokok, lauk pauk, 
sayuran dan buah-buahan) setiap kali makan akan lebih baik.

Setiap orang diharapkan selalu bersyukur dan menikmati 
makanan yang dikonsumsinya. Bersyukur dapat diwujudkan berupa 
berdoa sebelum makan. Nikmatnya makan ditentukan oleh 
kesesuaian kombinasi anekaragam dan bumbu, cara pengolahan, 
penyajian makanan dan suasana makan. Cara makan yang baik 
adalah makan yang tidak tergesa-gesa. Dengan bersyukur dan 
menikmati makan anekaragam makanan akan mendukung 
terwujudnya cara makan yang baik, tidak tergesa-gesa. Dengan 
demikian makanan dapat dikunyah, dicerna dan diserap oleh tubuh 
lebih baik. 
2. Banyak makan sayuran dan cukup buah-buahan 
Secara umum sayuran dan buah-buahan merupakan sumber 
berbagai vitamin, mineral, dan serat pangan. Sebagian vitamin, 
mineral yang terkandung dalam sayuran dan buah-buahan berperan 
sebagai antioksidan atau penangkal senyawa jahat dalam tubuh.  
Berbeda dengan sayuran, buah-buahan juga menyediakan 
karbohidrat terutama berupa fruktosa dan glukosa. Sayur tertentu 
juga menyediakan karbohidrat, seperti wortel dan kentang sayur. 
Sementara buah tertentu juga menyediakan lemak tidak jenuh 
seperti buah alpokat dan buah merah. Oleh karena itu konsumsi 
sayuran dan buah-buahan merupakan salah satu bagian penting 
dalam mewujudkan Gizi Seimbang. 
 
 
 
 
 
 
Berbagai kajian menunjukkan bahwa konsumsi sayuran dan 
buah-buahan yang cukup turut berperan dalam menjaga kenormalan 
tekanan darah, kadar gula dan kolesterol darah. Konsumsi sayur dan 
buah yang cukup juga menurunkan risiko sulit buang air besar 
(BAB/sembelit) dan kegemukan. Hal ini menunjukkan bahwa 
konsumsi sayuran dan buah-buahan yang cukup turut berperan 
dalam pencegahan penyakit tidak menular kronik. Konsumsi sayuran 
dan buah-buahan yang cukup merupakan salah satu indikator  
sederhana gizi seimbang.

Semakin matang buah yang mengandung karbohidrat semakin 
tinggi kandungan fruktosa dan glukosanya, yang dicirikan oleh rasa 
yang semakin manis. Dalam budaya makan masyarakat perkotaaan 
Indonesia saat ini, semakin dikenal minuman jus bergula. Dalam 
segelas jus buah bergula mengandung 150-300 Kalori yang sekitar 
separohnya dari gula yang ditambahkan. Selain itu beberapa jenis 
buah juga meningkatkan risiko kembung dan asam urat. Oleh karena 
itu konsumsi buah yang terlalu matang dan minuman jus bergula 
perlu dibatasi agar turut mengendalikan kadar gula darah.  
Badan Kesehatan Dunia (WHO) secara umum menganjurkan 
konsumsi sayuran dan buah-buahan untuk hidup sehat sejumlah 
400 g perorang perhari, yang terdiri dari 250 g sayur (setara dengan 2 
½ porsi atau 2 ½ gelas sayur setelah dimasak dan ditiriskan) dan 150 
g buah, (setara dengan 3 buah pisang ambon ukuran sedang atau 1 
½ potong pepaya ukuran sedang atau 3 buah jeruk ukuran sedang).  
Bagi orang Indonesia dianjurkan konsumsi sayuran dan buah-
buahan 300-400 g perorang perhari bagi anak balita dan anak usia 
sekolah, dan 400-600 g perorang perhari bagi remaja dan orang 
dewasa. Sekitar dua-pertiga dari jumlah anjuran konsumsi sayuran  
dan buah-buahan tersebut adalah porsi sayur. 
3. Biasakan mengonsumsi lauk pauk yang mengandung protein tinggi 
Lauk pauk terdiri dari pangan sumber protein hewani dan 
pangan sumber protein nabati. Kelompok pangan lauk pauk sumber 
protein hewani meliputi daging ruminansia (daging sapi, daging 
kambing, daging rusa dll), daging unggas (daging ayam, daging bebek 
dll), ikan termasuk seafood, telur dan susu serta hasil olahnya.  
Kelompok Pangan lauk pauk sumber protein nabati meliputi kacang-
kacangan dan hasil olahnya seperti kedele, tahu, tempe, kacang 
hijau, kacang tanah, kacang merah, kacang hitam, kacang tolo dan 
lain-lain. 
 
 
 
 
 
Meskipun kedua kelompok pangan tersebut (pangan sumber 
protein hewani dan pangan sumber protein nabati) sama-sama 
menyediakan protein, tetapi masing-masing kelompok pangan

tersebut mempunyai keunggulan dan kekurangan. Pangan hewani 
mempunyai asam amino yang lebih lengkap dan mempunyai mutu 
zat gizi yaitu protein, vitamin dan mineral lebih baik, karena 
kandungan zat-zat gizi tersebut lebih banyak dan mudah diserap 
tubuh. Tetapi pangan hewani mengandung tinggi kolesterol (kecuali 
ikan) dan lemak. Lemak dari daging dan unggas lebih banyak 
mengandung lemak jenuh. Kolesterol dan lemak jenuh diperlukan 
tubuh terutama pada anak-anak tetapi perlu dibatasai asupannya 
pada orang dewasa. 
Pangan protein nabati mempunyai keunggulan mengandung 
proporsi lemak tidak jenuh yang lebih banyak dibanding pangan 
hewani. Juga mengandung isoflavon, yaitu kandungan fitokimia yang 
turut berfungsi mirip hormon estrogen (hormon kewanitaan) dan 
antioksidan serta anti-kolesterol. Konsumsi kedele dan tempe telah 
terbukti dapat menurunkan kolesterol dan meningkatkan sensitifitas 
insulin dan produksi insulin. Sehingga dapat mengendalikan kadar 
kolesterol dan gula darah. Namun kualitas protein dan mineral yang 
dikandung pangan protein nabati lebih rendah dibanding pangan 
protein hewani. 
Oleh karena itu dalam mewujudkan Gizi Seimbang kedua 
kelompok pangan ini (hewani dan nabati) perlu dikonsumsi bersama 
kelompok pangan lainnya setiap hari, agar jumlah dan kualitas zat 
gizi  yang dikonsumsi lebih baik dan sempurna. Kebutuhan pangan 
hewani 2-4 porsi, setara dengan 70-140 g (2-4 potong) daging sapi 
ukuran sedang; atau 80-160 g (2-4 potong) daging ayam ukuran 
sedang; atau 80-160 g (2-4 potong) ikan ukuran sedang  sehari.  
Kebutuhan pangan protein nabati 2-4 porsi sehari, setara dengan 
100-200 g (4-8 potong) tempe ukuran sedang; atau 200-400 g (4- 8 
potong) tahu ukuran sedang. Porsi yang dianjurkan tersebut 
tergantung kelompok umur dan kondisi fisiologis (hamil, menyusui, 
lansia, anak, remaja, dewasa). Susu sebagai bagian dari pangan 
hewani yang dikonsumsi berupa minuman dianjurkan terutama bagi 
ibu hamil, ibu menyusui  serta anak-anak setelah usia satu tahun. 
Mereka yang mengalami diare atau intoleransi laktosa karena minum 
susu tidak dianjurkan minum susu hewani. Konsumsi telur, susu 
kedele dan ikan merupakan salah satu alternatif solusinya.

4. Biasakan mengonsumsi anekaragam makanan pokok  
Makanan pokok adalah pangan mengandung karbohidrat yang 
sering dikonsumsi atau telah menjadi bagian dari budaya makan 
berbagai etnik di Indonesia sejak lama. Contoh pangan karbohidrat 
adalah beras, jagung, singkong, ubi, talas, garut, sorgum, jewawut, 
sagu dan produk olahannya. Indonesia kaya akan beragam pangan 
sumber karbohidrat tersebut. 
 
 
 
 
Disamping mengandung karbohidrat, dalam makanan pokok 
biasanya juga terkandung antara lain vitamin B1 (tiamin), B2 
(riboflavin) dan beberapa mineral. Mineral dari makanan pokok ini 
biasanya mempunyai  mutu biologis atau penyerapan oleh tubuh 
yang rendah. Serealia utuh seperti jagung, beras merah, beras hitam, 
atau biji-bijian yang tidak disosoh dalam penggilingannya 
mengandung serat yang tinggi. Serat ini penting untuk melancarkan 
buang air besar dan pengendalian kolesterol darah. Selain itu serealia 
tersebut juga memilki karbohidrat yang lambat diubah menjadi gula 
darah sehingga turut mencegah gula darah tinggi. Beberapa jenis 
umbi-umbian juga mengandung zat non-gizi yang bermanfaat untuk 
kesehatan seperti ubi jalar ungu dan ubi jalar kuning yang 
mengandung antosianin dan lain-lain. 
Selain makanan pokok yang diproduksi di indonesia, ada juga 
makanan pokok yang tersedia di Indonesia melalui impor seperti 
terigu. Pemerintah Indonesia telah mewajibkan pengayaan mineral 
dan vitamin (zat besi, zink, asam folat, tiamin dan riboflavin) pada 
semua terigu yang dipasarkan di Indonesia sebagai bagian dari 
strategi perbaikan gizi terutama penanggulangan anemia gizi. 
Cara mewujudkan pola konsumsi makanan pokok yang beragam 
adalah dengan  mengonsumsi lebih dari satu jenis makanan pokok  
dalam sehari atau sekali makan. Salah satu cara mengangkat citra 
pangan karbohidrat lokal adalah dengan mencampur makanan 
karbohidrat lokal dengan terigu, seperti pengembangan produk boga 
yang beragam misalnya, roti atau mie campuran tepung singkong 
dengan tepung terigu, pembuatan roti gulung pisang, singkong 
goreng keju dan lain-lain

5. Batasi konsumsi pangan manis, asin dan berlemak 
 
Peraturan Menteri Kesehatan nomor 30 tahun 2013 tentang 
Pencantuman Informasi Kandungan Gula, Garam dan Lemak serta 
Pesan Kesehatan untuk Pangan Olahan dan Pangan Siap Saji 
menyebutkan bahwa konsumsi gula lebih dari 50 g (4 sendok 
makan), natrium lebih dari 2000 mg (1 sendok teh) dan 
lemak/minyak total lebih dari 67 g (5 sendok makan) per orang per 
hari akan meningkatkan risiko hipertensi, stroke, diabetes, dan 
serangan jantung. Informasi kandungan gula, garam dan lemak serta  
pesan kesehatan yang tercantum pada label pangan dan makanan 
siap saji harus diketahui dan mudah dibaca dengan jelas oleh 
konsumen. 
  
 
 
 
Masyarakat perlu diberi pendidikan membaca label pangan, 
mengetahui pangan rendah gula, garam dan lemak, serta memasak 
dengan mengurangi garam dan gula. Di lain pihak para pengusaha 
pangan olahan diwajibkan mencantumkan informasi nilai gizi pada 
label pangan agar masyarakat dapat memilih makanan sehat sesuai 
kebutuhan setiap anggota keluarganya. Label dan iklan pangan 
harus mengikuti Peraturan Pemerintah Nomor 69 Tahun 1999.  
Khusus untuk anak usia 6-24 bulan konsumsi lemak tidak perlu 
dibatasi. 
a. Konsumsi gula 
Gula yang dikonsumsi melampaui kebutuhan akan 
berdampak pada peningkatan berat badan, bahkan jika 
dilakukan dalam jangka waktu lama secara langsung akan 
meningkatkan kadar gula darah dan berdampak pada terjadinya 
diabetes type-2, bahkan secara tidak langsung berkontribusi 
pada penyakit seperti osteoporosis, penyakit jantung dan kanker.  
Gula yang dikenal masyarakat tidak hanya terdapat pada 
gula tebu, gula aren dan gula jagung yang dikonsumsi dari 
makanan dan minuman. Perlu diingat bahwa kandungan gula 
terdapat juga dalam makanan lain yang mengandung

karbohidrat sederhana (tepung, roti, kecap), buah manis, jus, 
minuman bersoda dan sebagainya. 
 
 
 
 
Fruktosa adalah gula sederhana yang terdapat di dalam 
madu, berbagai buah, gula meja (sukrosa dan high fructose corn 
syrup/HFCS). Fruktosa belum memperoleh perhatian yang 
cukup dibandingkan dengan glukosa padahal terbukti 
mempunyai hubungan yang erat dengan intoleransi glukosa. 
Jadi pendapat selama ini bahwa fruktosa lebih aman dari 
glukosa adalah tidak benar. 
Daftar pangan penukar gula dan porsi ukuran rumah 
tangga (URT). 
Tabel Kelompok Pangan Manis 
 
Jenis pangan ini hampir seluruhnya terdiri dari karbohidrat 
sederhana. 
Kandungan gizi satu (1) porsi gula tebu (pasir) dengan ukuran 
satu (1) sendok makan atau 10 gram adalah : 37 Kalori dan 9 
gram Karbohidrat. 
 
Daftar pangan penukar satu (1) porsi gula: 
 
Bahan Makanan Ukuran Rumah 
Tangga (URT) 
Berat dalam gram 
Gula aren 
Gula kelapa 
Selai/jam 
Madu  
Sirup 
1 sendok makan 
1 sendok makan 
1 sendok makan 
1 sendok makan 
1 sendok makan

Beberapa cara membatasi konsumsi gula: 
1) Batasi konsumsi makanan dan minuman yang manis. 
2) Kurangi penggunaan gula, baik pada berbagai minuman 
(teh, kopi, susu, jus dan minuman lain bergula) maupun 
pada berbagai makanan, jajanan dan saat membubuhkan 
pada masakan. Jika ingin memberi rasa pada minuman,  
dapat ditambahkan potongan buah atau daun seperti jeruk 
nipis, daun mint  
3) Ganti makanan penutup/desser t yang manis dengan buah 
yang mempunyai rasa kurang manis dan/atau sayur-
sayuran segar.  
4) Manfaatkan informasi pada label kemasan dalam memilih 
makanan yang kurang manis atau rendah kalori.  
b. Konsumsi garam 
Rasa asin yang berasal dari makanan adalah karena 
kandungan garam (NaCl) yang ada dalam makanan tersebut. 
Konsumsi natrium yang berlebihan akan mempengaruhi 
kesehatan terutama meningkatkan tekanan darah. Daftar 
makanan tinggi natrium  adalah sebagai berikut: 
 
Daftar Makanan Tinggi Natrium 
 
1) Bahan Penyedap 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Nama Makanan 
Ukuran 
Rumah 
Tangga (URT) 
Kandungan 
Natrium 
Garam Meja 1 Sendok Teh 2000 mg 
Acar Bawang Merah 1 Sendok Teh 1620 mg 
Acar bawang Putih 1 Sendok Teh 1850 mg 
MSG (Vetsin) 1 Sendok Teh 492 mg 
Kecap 1 Sendok Teh 343 mg 
Meat Tenderizer (Pelunak 
Daging) 
1 Sendok Teh 1750 mg

2) Makanan Siap Saji 
 
Nama Makanan 
Berat dalam 
Gram 
Kandungan 
Natrium 
Chicken Breast Sandwich 210 1340 mg 
Double Beef Whopper and 
Cheese 
374 1535 mg 
Ham and Cheese 230 1534 mg 
Hot dog 100 830 mg 
Roasted Beef 247 1288 mg 
Super Hot Dog with 
Cheese 
196 1605 mg 
 
Karena itu dianjurkan mengonsumsi garam sekedarnya 
dengan cara menyajikan makanan rendah natrium: 
1) Gunakan garam beriodium untuk konsumsi. 
2) Jika membeli pangan kemasan dalam kaleng, seperti 
sayuran, kacang-kacangan atau ikan, agar membaca label 
informasi nilai gizi dan pilih yang rendah natrium. 
3) Jika tidak tersedia pangan kemasan dalam kaleng yang 
rendah natrium, pangan dalam kemasan tersebut perlu  
ditiriskan bila mengandung cairan bergaram.  
4) Bila mengonsumsi makanan instan yang bumbunya 
terpisah, dianjurkan mengurangi penggunaan bumbu yang 
bergaram. 
5) Cobalah menggunakan bumbu tambahan lain seperti tomat, 
bawang, cabe,  jahe atau lainnya untuk meningkatkan rasa. 
 
Disamping menggunakan garam (NaCl) juga dapat 
menggunakan garam yang mengandung Kalium karena 
mengonsumsi lebih banyak pangan sumber Kalium dapat 
membantu menurunkan tekanan darah. Pangan sumber Kalium 
adalah kismis, kentang, pisang, kacang (beans) dan yoghurt. 
c. Konsumsi lemak 
Lemak yang terdapat didalam makanan, berguna untuk 
meningkatkan jumlah energi, membantu penyerapan vitamin A, 
D, E dan K serta menambah lezatnya hidangan. Konsumsi lemak 
dan minyak dalam hidangan sehari-hari dianjurkan tidak lebih 
dari 25% kebutuhan energi, jika mengonsumsi lemak secara 
berlebihan akan mengakibatkan berkurangnya konsumsi 
makanan lain. Hal ini disebabkan karena lemak berada didalam

---

## 3. Visualisasi Panduan Piring Makanku & Tumpeng Gizi Seimbang
Panduan porsi sekali makan (Piring Makanku):
- 1/2 bagian piring: terdiri dari 2/3 sayuran dan 1/3 buah-buahan.
- 1/2 bagian piring lainnya: terdiri dari 2/3 makanan pokok (karbohidrat) dan 1/3 lauk-pauk (protein hewani dan nabati).
- Disertai dengan mencuci tangan sebelum makan, minum air putih minimal 8 gelas per hari, dan aktivitas fisik 30 menit per hari.

B. Visual 
Visual adalah bentuk atau gambar, yang bila dimanca negara disebut 
panduan pangan (Food Guide), ada yang berbentuk piramida, bentuk 
Pagoda, bentuk Gasing dan lain sebagainya sesuai nilai-nilai yang 
berkembang dimasing-masing negara. Visual Gizi Seimbang adalah 
bentuk gizi seimbang yang menggambarkan semua prinsip Gizi Seimbang 
yaitu beragam pangan, kebersihan dan keamanan pangan, aktifitas fisik 
dan  pemantaun berat badan bagi masyarakat di suatu wilayah atau 
bangsa.  
Ada dua visual Gizi Seimbang, yaitu 1) Tumpeng Gizi Seimbang dan 2) 
Piring Makanku, Sajian Sekali Makan. Tumpe ng Gizi Seimbang 
dimaksudkan sebagai gambaran dan penjelasan sederhana tentang 
panduan porsi (ukuran) makanan dan minum serta aktifitas fisik sehari -
hari, termasuk  cuci tangan sebelum dan sesudah makan serta 
memantau berat badan.  Tumpeng Gizi Seimbang yang baru ini 
merupakan penyempurnaan dari tumpeng Gizi Seimbang yang 
sebelumnya, setelah mendapat masukan dari berbagai pihak termasuk 
ujicoba lapangan kepada petugas kesehatan dan non kesehatan ditingkat 
kecamatan dan para kader dan peserta posyandu.

Dalam Tumpeng Gizi Seimbang (TGS) ada empat  lapis berurutan dari 
bawah ke atas, dan semakin ke atas semakin kecil.  Empat lapis artiny a 
Gizi Seimbang didasarkan pada prinsip 4 pilar yaitu konsumsi 
beranekaragam pangan, aktifitas fisik, kebersihan diri, dan pemantaun 
berat badan untuk mempertahankan berat badan normal. Semakin ke 
atas ukuran tumpeng semakin kecil berarti pangan pada lapis paling atas 
yaitu gula, garam dan lemak dibutuhkan sedikit sekali atau perlu 
dibatasi. Pada setiap kelompok pangan dituliskan berapa jumlah porsi 
setiap kelompok pangan yang dianjurkan. Misalnya pada kelompok 
sayuran tertulis 3-4 porsi sehari, artinya sayuran dianjurkan dikonsumsi 
oleh remaja atau dewasa sejumlah 3-4 mangkuk sehari. Satu mangkuk 
sayuran beratnya sekitar 75 gram, sehingga perlu makan sayur sekitar 
300 gram sehari. Sebelah kanan  tumpeng ada tanda tambah (+) diikuti 
dengan visual segelas air putih dan tulisan 8 gelas.  Ini artinya dalam 
sehari  setiap orang remaja atau dewasa dianjurkan untuk minum air 
putih sekitar 8 gelas sehari. 
Selain makanan dan minuman dalam visual TGS ini juga ada pesan 
cuci tangan sebelum dan sesudah makan yang divisualkan oleh gambar 
cuci tangan menggunakan air mengalir; juga berbagai siluet aktifitas fisik 
(termasuk olahraga), dan kegiatan menimbang berat badan. Kegiatan fisik 
dianjurkan untuk dilakukan paling tidak tiga kali seminggu dan 
memantau berat badan setiap bulan.

PIRING MAKANKU: SAJIAN SEKALI MAKAN, dimaksudkan sebagai 
panduan yang menunjukkan sajian makanan dan minuman pada setiap 
kali makan (misal sarapan, makan siang dan makan malam). Visual Piring 
Makanku ini menggambarkan anjuran makan sehat dimana separoh 
(50%)  dari total jumlah makanan setiap kali makan adalah sayur dan 
buah, dan separoh (50%) lagi adalah makanan pokok dan lauk-pauk. 
Piring Makanku juga menganjurkan makan bahwa porsi sayuran harus 
lebih banyak dari porsi buah, dan porsi makanan pokok lebih banyak dari 
porsi lauk-pauk. Piring makanku juga menganjurkan perlu minum setiap 
kali makan,  bisa sebelum, ketika atau setelah makan. Meskipun gambar 
gelas hanya satu buah dalam visual ini, tidak berarti bahwa minum dalam 
satu kali makan hanya satu gelas, bisa saja disesuaikan dengan 
kebutuhan, misalnya segelas sebelum makan dan segelas  lagi setelah 
makan. 
Makan dan minum tidak ada artinya bila tidak bersih dan aman 
termasuk tangan dan peralatan makan. Oleh karena itu sejalan dengan 
prinsip gizi seimbang makan dalam visual Piring Makanku juga 
dianjurkan untuk cuci tangan sebelum dan sesudah makan.  Karena 
Piring Makanku adalah panduan setiap kali makan, maka tidak 
diperlukan anjuran aktivitas fisik dan pemantauan berat badan. Kedua 
hal ini cukup divisualkan pada gambar Tumpeng Gizi Seimbang.

BAB  V 
STRATEGI DAN IMPLEMENTASI KOMUNIKASI, INFORMASI DAN EDUKASI 
GIZI SEIMBANG 
 
A. Komunikasi, Informasi dan Edukasi (KIE) Gizi Seimbang 
1. Sasaran 
Tujuan dari kegiatan Komunikasi, Informasi dan Edukasi (KIE) 
adalah untuk merubah perilaku sesuai dengan pesan yang 
disampaikan. Agar penyampaian pesan dapat terlaksana dengan 
berhasil guna dan berdaya guna (efisien dan efektif) maka tahap awal 
dari kegiatan tersebut adalah menentukan siapa sasaran yang akan 
dituju. Prinsip dalam menentukan sasaran KIE Gizi Seimbang adalah 
“Sasaran bukan hanya sebagai objek saja tetapi juga sebagai subjek”. 
Dalam kaitan dengan tujuan KIE Gizi Seimbang  untuk merubah 
perilaku seluruh lapisan masyarakat, maka sasaran dari KIE Gizi 
Seimbang adalah : 
a. Sasaran utama : 
1) Masyarakat dari berbagai kelompok usia 
2) Masyarakat dari berbagai lapisan ekonomi 
3) Masyarakat dari berbagai lapisan pendidikan 
b. Sasaran antara : 
1) Penentu kebijakan 
2) Pengelola Program 
3) Lembaga Swadaya Masyarakat 
4) Kader 
5) Organisasi Profesi 
6) Media Massa 
7) Dunia Usaha 
8) Mitra Pembangunan Internasional 
9) Lembaga pendidikan: 
(a)  Sekolah : TK, SD, SMP, SMA/SMK, Perguruan Tinggi 
(b)  Madrasah : RA, MI, MTs., MA, PTAI 
(c) Pondok Pesantren  
10) Lembaga sosial dankeagamaan 
11) Kelompok Komunitas

2. Metode 
Setelah sasaran ditentukan, tahap selanjutnya adalah 
menentukan metode yang tepat agar proses penyampaian pesan 
dapat berjalan dengan baik dan benar. Metode yang  dipilih adalah 
metode yang dapat mengembangkan prinsip “komunikasi 
partisipatif/komunikasi dua arah” yang dilaksanakan baik secara 
formal maupun informal. Jenis metode yang perlu dilaksanakan 
dalam KIE Gizi Seimbang adalah : 
a. Penyampaian secara langsung yaitu : 
1) Social marketing /pemasaran sosial seperti kampanye, 
penyuluhan, pencanangan, siaran melalui media, 
penyebaran melalui media cetak, penyebar luasan melalui 
media sosial misalnya facebook, twitter dan Internet 
2) Melalui lomba  
3) Sayembara  
4) Pengangkatan seorang duta Gizi Seimbang sebagai panutan 
untuk memotivasi perubahan perilaku 
b. Penyampaian secara tidak langsung seperti : 
1) Pelatihan dan pendidikan secara berjenjang 
2) Semiloka/lokakarya/sarahsehan 
3) Pembentukan kelompok diskusi terarah (Focus Group 
Discussion) 
 
3. Media dan Alat 
Agar metode yang dipilih dapat berjalan efektif dan efisien, perlu 
didukung dengan media dan alat yang tepat. Berbagai media dan alat 
yang tersedia di masyarakat dapat digunakan secara optimal. Media 
yang dapat dapat digunakan dalam kegiatan KIE Gizi Seimbang 
adalah : 
a. Media elektronik seperti radio, televisi, bioskop, telepon dan video 
b. Media cetak seperti koran, majalah, brosur, leaflet, booklet, 
kalender, lembar balik dan buku saku 
c. Media online seperti web, facebook, twitter dan youtube 
d. Media audio seperti lagu, jingle dan yel-yel. 
 
4. Lingkup Materi  
Sesuai dengan tujuan KIE untuk mengubah perilaku maka 
lingkup materi sebagai pesan yang akan disampaikan harus jelas, 
mudah dipahami, mudah dimengerti dan mudah dipraktekkan. 
Dalam kaitan dengan pendidikan Gizi Seimbang yang bertujuan agar 
masyarakat berperilaku Gizi Seimbang, materi yang akan 
disampaikan meliputi :

a. Pengertian dan prinsip Gizi Seimbang 
b. Pesan Gizi Seimbang baik yang bersifat umum maupun khusus 
c. Slogan dan visual Gizi Seimbang 
d. Anjuran jumlah porsi dan Contoh-contoh menu sehat dan bergizi  
 
Tabel Anjuran Jumlah Porsi Menurut Kecukupan Energi untuk 
Berbagai Kelompok Umur 
 
1) Untuk Kelompok Ibu Hamil dan Menyusui 
 
Bahan Makanan 
Ibu Hamil 
2500 kkal 
Ibu Menyusui 
2500 kkal 
Nasi 6p 6p 
Sayuran 4p 4p 
Buah 4p 4p 
Tempe 4p 4p 
Daging 3p 3p 
Susu 1p 1p 
Minyak 6p 6p 
Gula 2p 2p 
 
2) Untuk Kelompok Umur 1-3 tahun dan 4-6 tahun 
 
Bahan Makanan Anak Usia 1-3 tahun 
1125 kkal 
Anak Usia 
4-6 tahun 
1600 kkal 
Nasi 3p 4p 
Sayuran  1,5p 2p 
Buah 3p 3p 
Tempe  1p 2p 
Daging 1p 2p 
ASI Dilanjutkan hingga 
2 tahun 
 
Susu 1p 1p 
Minyak 3p 4p 
Gula 2p 2p


========================================

# Pedoman Angka Kecukupan Gizi (AKG) 2019
**Sumber:** *Peraturan Menteri Kesehatan Republik Indonesia Nomor 28 Tahun 2019 tentang Angka Kecukupan Gizi yang Dianjurkan untuk Masyarakat Indonesia*

---

## 1. Definisi dan Ketentuan Umum
Mengingat  :   1.  Undang-Undang Nomor 36 Tahun 2009 tentang 
Kesehatan (Lembaran Negara Republik Indonesia Tahun 
2009 Nomor 144, Tambahan Lembaran Negara Republik 
Indonesia Nomor 5063); 
2. Undang-Undang Nomor 18 Tahun 2012 tentang Pangan 
(Lembaran Negara Republik Indonesia Tahun 2012 
Nomor 227, Tambahan Lembaran Negara Republik 
Indonesia Nomor 5360);  
3. Peraturan Pemerintah Nomor 28 Tahun 2004 tentang 
Keamanan, Mutu dan Gizi Pangan (Lembaran Negara 
Republik Indonesia Tahun 2004 Nomor 107, Tambahan 
Lembaran Negara Republik Indonesia Nomor 4424); 
4. Peraturan Presiden Nomor 35 Tahun 2015 tentang 
Kementerian Kesehatan (Lembaran Negara Republik 
Indonesia Tahun 2015 Nomor 59); 
5. Peraturan Menteri Kesehatan Nomor 23 Tahun 2014 
tentang Upaya Perbaikan Gizi (Berita Negara Republik 
Indonesia Tahun 2014 Nomor 967); 
6. Peraturan Menteri Kesehatan Nomor 64 Tahun 2015 
tentang Organisasi dan Tata Kerja Kementerian 
Nomor 1508) sebagaimana telah diubah dengan 
Peraturan Menteri Kesehatan Nomor 30 Tahun 2018 
tentang Perubahan atas Peraturan Menteri Kesehatan 
Nomor 64 Tahun 2015 tentang Organisasi dan Tata Kerja 
Kementerian Kesehatan (Berita Negara Republik 
Indonesia Tahun 2018 Nomor 945);  
 
MEMUTUSKAN: 
Menetapkan   : PERATURAN MENTERI KESEHATAN TENTANG ANGKA  
KECUKUPAN GIZI YANG DIANJURKAN UNTUK MASYARAKAT 
INDONESIA.

Pasal 1 
Angka Kecukupan Gizi yang Dianjurkan untuk Masyarakat 
Indonesia yang selanjutnya disingkat AKG adalah suatu nilai 
yang menunjukkan kebutuhan rata-rata zat gizi tertentu yang 
harus dipenuhi setiap hari bagi hampir semua orang dengan 
karakteristik tertentu yang meliputi umur, jenis kelamin, 
tingkat aktivitas fisik, dan kondisi fisiologis, untuk hidup 
sehat.  
 
Pasal 2 
AKG digunakan pada tingkat konsumsi yang meliputi 
kecukupan energi, protein, lemak, karbohidrat, serat, air, 
vitamin, dan mineral. 
 
Pasal 3 
(1) Untuk melakukan evaluasi, perencanaan konsumsi dan 
ketersediaan pangan dalam rang ka pemenuhan 
kebutuhan penduduk rata-rata secara makro nasional 
dan berbagai kebutuhan lainnya, dalam AKG ditetapkan 
estimasi rata-rata angka kecukupan energi dan rata-rata 
angka kecukupan protein bagi masyarakat Indonesia. 
(2) Rata-rata angka kecukupan energi bagi masyarakat 
Indonesia sebagaimana dimaksud pada ayat (1) sebesar 
2100 (dua ribu seratus) kilo kalori per orang per hari 
pada tingkat konsumsi. 
(3) Rata-rata angka kecukupan protein bagi masyarakat 
Indonesia sebagaimana dimaksud pada ayat (1) sebesar  
57 (lima puluh tujuh) gram per orang per hari pada 
tingkat konsumsi. 
 
Pasal 4 
Tabel AKG sebagaimana dimaksud dalam Pasal 2 tercantum 
dalam Lampiran I yang merupakan bagian tidak terpisahkan 
dari Peraturan Menteri ini.

Pasal 5 
AKG digunakan sebagai acuan bagi  pemerintah pusat, 
pemerintah daerah, dan pemangku kepentingan untuk: 
a. menghitung kecukupan gizi penduduk di daerah; 
b. menyusun pedoman konsumsi pangan; 
c. menilai konsumsi pangan pada penduduk dengan 
karakteristik tertentu; 
d. menghitung kebutuhan pangan bergizi pada 
penyelenggaraan makanan institusi; 
e. menghitung kebutuhan pangan bergizi pada situasi 
darurat; 
f. menetapkan Acuan Label Gizi (ALG); 
g. mengembangkan indeks mutu konsumsi pangan; 
h. mengembangkan produk pangan olahan; 
i. menentukan garis kemiskinan; 
j. menentukan besaran biaya minimal untuk pangan  
bergizi dalam program jaminan sosial pangan;  
k. menentukan upah minimum; dan 
l. kebutuhan lainnya.  
 
Pasal 6 
(1) Penggunaan AKG sebagaimana dimaksud dalam Pasal 5  
harus memperhatikan prinsip dan tata cara penggunaan 
AKG. 
(2) penggunaan AKG sebagaimana dimaksud pada ayat (1) 
dilaksanakan sesuai dengan Pedoman Penggunaan AKG 
sebagaimana tercantum dalam Lampiran II yang 
merupakan bagian tidak terpisahkan dari Peraturan 
Menteri ini. 
 
Pasal 7 
Pada saat Peraturan Menteri ini mulai berlaku, Peraturan 
Menteri Kesehatan Nomor 75 Tahun 2013 tentang Angka 
Kecukupan Gizi yang Dianjurkan Bagi Bangsa Indonesia  
dicabut dan dinyatakan tidak berlaku.

Pasal 8 
Peraturan Menteri ini mulai berlaku pada tanggal 
diundangkan. 
 
Agar setiap orang mengetahuinya, memerintahkan 
pengundangan Peraturan Menteri ini dengan penempatannya 
 
 
Ditetapkan di Jakarta 
pada tanggal 20 Agustus 2019 
 
MENTERI KESEHATAN 
REPUBLIK INDONESIA, 
 
                ttd 
 
NILA FARID MOELOEK 
 
Diundangkan di Jakarta 
pada tanggal 26 Agustus 2019 
 
DIREKTUR JENDERAL  
PERATURAN PERUNDANG-UNDANGAN 
KEMENTERIAN HUKUM DAN HAK ASASI MANUSIA 
REPUBLIK INDONESIA, 
 
                ttd 
 
WIDODO EKATJAHJANA

---

## 2. Tabel Angka Kecukupan Gizi Rata-rata yang Dianjurkan (Per Orang Per Hari)
LAMPIRAN I 
PERATURAN MENTERI KESEHATAN REPUBLIK INDONESIA 
NOMOR 28 TAHUN 2019  
TENTANG  
ANGKA KECUKUPAN GIZI YANG DIANJURKAN UNTUK 
MASYARAKAT INDONESIA 
 
 
TABEL ANGKA KECUKUPAN GIZI  
 
I. Angka Kecukupan Energi, Protein, Lemak, Karbohidrat, Serat, dan Air yang Dianjurkan (Per Orang Per Hari) 
 
Tabel 1 
Angka Kecukupan Energi, Protein, Lemak, Karbohidrat, Serat, dan Air yang dianjurkan (per orang per hari) 
 
Kelompok Umur Berat 
Badan 
(kg) 
Tinggi 
Badan 
(cm) 
Energi  
(kkal) 
Protein  
(g) 
Lemak (g) Karbohidrat  
(g) 
Serat  
(g) 
Air  
(ml) Total Omega 3 Omega 6 
Bayi /Anak           
0 – 5  bulan1 6 60 550 9 31 0.5 4.4 59 0 700 
6 – 11 bulan 9 72 800 15 35 0.5 4.4 105 11 900

Kelompok Umur Berat 
Badan 
(kg) 
Tinggi 
Badan 
(cm) 
Energi  
(kkal) 
Protein  
(g) 
Lemak (g) Karbohidrat  
(g) 
Serat  
(g) 
Air  
(ml) Total Omega 3 Omega 6 
1 – 3 tahun  13 92 1350 20 45 0.7 7 215 19 1150 
4 – 6 tahun  19 113 1400 25 50 0.9 10 220 20 1450 
7 – 9 tahun  27 130 1650 40 55 0.9 10 250 23 1650 
Laki-laki           
10 – 12 tahun 36 145 2000 50 65 1.2 12 300 28 1850 
13 – 15 tahun 50 163 2400 70 80 1.6 16 350 34 2100 
16 – 18 tahun 60 168 2650 75 85 1.6 16 400 37 2300 
19 – 29 tahun 60 168 2650 65 75 1.6 17 430 37 2500 
30 – 49 tahun 60 166 2550 65 70 1.6 17 415 36 2500 
50 – 64 tahun 60 166 2150 65 60 1.6 14 340 30 2500 
65 – 80 tahun 58 164 1800 64 50 1.6 14 275 25 1800 
80+ tahun 58 164 1600 64 45 1.6 14 235 22 1600 
Perempuan           
10 – 12 tahun 38 147 1900 55 65 1.0 10 280 27 1850 
13 – 15 tahun 48 156 2050 65 70 1.1 11 300 29 2100 
16 – 18 tahun 52 159 2100 65 70 1.1 11 300 29 2150 
19 – 29 tahun 55 159 2250 60 65 1.1 12 360 32 2350

Kelompok Umur Berat 
Badan 
(kg) 
Tinggi 
Badan 
(cm) 
Energi  
(kkal) 
Protein  
(g) 
Lemak (g) Karbohidrat  
(g) 
Serat  
(g) 
Air  
(ml) Total Omega 3 Omega 6 
30 – 49 tahun 56 158 2150 60 60 1.1 12 340 30 2350 
50 – 64 tahun 56 158 1800 60 50 1.1 11 280 25 2350 
65 – 80 tahun 53 157 1550 58 45 1.1 11 230 22 1550 
80+ tahun 53 157 1400 58 40 1.1 11 200 20 1400 
Hamil (+an)           
Trimester 1   +180 +1 +2.3 +0.3 +2 +25 +3 +300 
Trimester 2   +300 +10 +2.3 +0.3 +2 +40 +4 +300 
Trimester 3   +300 +30 +2.3 +0.3 +2 +40 +4 +300 
Menyusui (+an)           
6 bln pertama   +330 +20 +2.2 +0.2 +2 +45 +5 +800 
6 bln kedua   +400 +15 +2.2 +0.2 +2 +55 +6 +650 
1 Pemenuhan kebutuhan gizi bayi 0-5 bulan bersumber dari pemberian ASI Eksklusif 
2 Energi untuk aktifitas fisik dihitung menggunakan faktor aktifitas fisik untuk masing-masing kelompok umur yaitu 1.1 bagi anak 
hingga umur 1 tahun,  1.14 bagi anak 1-3 tahun, dan 1.26 bagi anak dan dewasa 4-64 tahun, serta 1,12 bagi usia lanjut

II. Angka Kecukupan Vitamin yang Dianjurkan (Per Orang Per Hari) 
 
Tabel 2 
Angka Kecukupan Vitamin yang Dianjurkan (per orang per hari) 
 
Kelompok Umur Vit A 
(RE) 
Vit D 
(mcg) 
Vit E 
(mcg) 
Vit K 
(mcg) 
Vit 
B1 
(mg) 
Vit 
B2 
(mg) 
Vit 
B3 
(mg) 
Vit B5 
(Pantotenat) 
(mg) 
Vit 
B6 
(mg) 
Folat 
(mcg) 
Vit 
B12 
(mcg) 
Biotin 
(mcg) 
Kolin 
(mg) 
Vit C 
(mg) 
Bayi /Anak               
0 – 5  bulan1 375 10 4 5 0.2 0.3 2 1.7 0.1 80 0.4 5 125 40 
6 – 11 bulan 400 10 5 10 0.3 0.4 4 1.8 0.3 80 1.5 6 150 50 
1 – 3 tahun  400 15 6 15 0.5 0.5 6 2.0 0.5 160 1.5 8 200 40 
4 – 6 tahun  450 15 7 20 0.6 0.6 8 3.0 0.6 200 1.5 12 250 45 
7 – 9 tahun  500 15 8 25 0.9 0.9 10 4.0 1.0 300 2.0 12 375 45 
Laki-laki               
10 – 12 tahun 600 15 11 35 1.1 1.3 12 5.0 1.3 400 3.5 20 375 50 
13 – 15 tahun 600 15 15 55 1.2 1.3 16 5.0 1.3 400 4.0 25 550 75 
16 – 18 tahun 700 15 15 55 1.2 1.3 16 5.0 1.3 400 4.0 30 550 90 
19 – 29 tahun 650 15 15 65 1.2 1.3 16 5.0 1.3 400 4.0 30 550 90 
30 – 49 tahun 650 15 15 65 1.2 1.3 16 5.0 1.3 400 4.0 30 550 90 
50 – 64 tahun 650 15 15 65 1.2 1.3 16 5.0 1.7 400 4.0 30 550 90

Kelompok Umur Vit A 
(RE) 
Vit D 
(mcg) 
Vit E 
(mcg) 
Vit K 
(mcg) 
Vit 
B1 
(mg) 
Vit 
B2 
(mg) 
Vit 
B3 
(mg) 
Vit B5 
(Pantotenat) 
(mg) 
Vit 
B6 
(mg) 
Folat 
(mcg) 
Vit 
B12 
(mcg) 
Biotin 
(mcg) 
Kolin 
(mg) 
Vit C 
(mg) 
65 – 80 tahun 650 20 15 65 1.2 1.3 16 5.0 1.7 400 4.0 30 550 90 
80+ tahun 650 20 15 65 1.2 1.3 16 5.0 1.7 400 4.0 30 550 90 
Perempuan               
10 – 12 tahun 600 15 15 35 1.0 1.0 12 5.0 1.2 400 3.5 20 375 50 
13 – 15 tahun 600 15 15 55 1.1 1.0 14 5.0 1.2 400 4.0 25 400 65 
16 – 18 tahun 600 15 15 55 1.1 1.0 14 5.0 1.2 400 4.0 30 425 75 
19 – 29 tahun 600 15 15 55 1.1 1.1 14 5.0 1.3 400 4.0 30 425 75 
30 – 49 tahun 600 15 15 55 1.1 1.1 14 5.0 1.3 400 4.0 30 425 75 
50 – 64 tahun 600 15 15 55 1.1 1.1 14 5.0 1.5 400 4.0 30 425 75 
65 – 80 tahun 600 20 20 55 1.1 1.1 14 5.0 1.5 400 4.0 30 425 75 
80+ tahun 600 20 20 55 1.1 1.1 14 5.0 1.5 400 4.0 30 425 75 
Hamil (+an)               
Trimester 1 +300 +0 +0 +0 +0.3 +0.3 +4 +1 +0.6 +200 +0.5 +0 +25 +10 
Trimester 2 +300 +0 +0 +0 +0.3 +0.3 +4 +1 +0.6 +200 +0.5 +0 +25 +10 
Trimester 3 +300 +0 +0 +0 +0.3 +0.3 +4 +1 +0.6 +200 +0.5 +0 +25 +10

Kelompok Umur Vit A 
(RE) 
Vit D 
(mcg) 
Vit E 
(mcg) 
Vit K 
(mcg) 
Vit 
B1 
(mg) 
Vit 
B2 
(mg) 
Vit 
B3 
(mg) 
Vit B5 
(Pantotenat) 
(mg) 
Vit 
B6 
(mg) 
Folat 
(mcg) 
Vit 
B12 
(mcg) 
Biotin 
(mcg) 
Kolin 
(mg) 
Vit C 
(mg) 
Menyusui (+an)               
6 bln pertama +350 +0 +4 +0 +0.4 +0.5 +3 +2 +0.6 +100 +1.0 +5 +125 +45 
6 bln kedua +350 +0 +4 +0 +0.4 +0.5 +3 +2 +0.6 +100 +1.0 +5 +125 +45 
1 Pemenuhan kebutuhan gizi bayi 0-5 bulan bersumber dari pemberian ASI Eksklusif

III. Angka Kecukupan Mineral yang Dianjurkan (per orang per hari) 
 
Tabel 3 
Angka Kecukupan Mineral yang dianjurkan (per orang per hari) 
 
Kelompok Umur 
Kalsi
um 
(mg) 
Fosfor 
(mg) 
Magne
sium 
(mg) 
Besi2 
(mg) 
Iodium 
(mcg) 
Seng3 
(mg) 
Sele
nium 
(mcg) 
Man
gan 
(mg) 
Fluor 
(mg) 
Kromi
um 
(mcg) 
Kalium 
(mg) 
Natrium 
(mg) 
Klor 
(mg) 
Tem
baga 
(mcg) 
Bayi /Anak               
0 –5  bulan1 200 100 30 0.3 90 1.1 7 0.00
0.01 0.2 400 120 180 200 
6 – 11 bulan 270 275 55 11 120 3 10 0.7 0.5 6 700 370 570 220 
1 – 3 tahun  650 460 65 7 90 3 18 1.2 0.7 14 2600 800 1200 340 
4 – 6 tahun  1000 500 95 10 120 5 21 1.5 1.0 16 2700 900 1300 440 
7 – 9 tahun  1000 500 135 10 120 5 22 1.7 1.4 21 3200 1000 1500 570 
Laki-laki               
10 – 12 tahun 1200 1250 160 8 120 8 22 1.9 1.8 28 3900 1300 1900 700 
13 – 15 tahun 1200 1250 225 11 150 11 30 2.2 2.5 36 4800 1500 2300 795 
16 – 18 tahun 1200 1250 270 11 150 11 36 2.3 4.0 41 5300 1700 2500 890 
19 – 29 tahun 1000 700 360 9 150 11 30 2.3 4.0 36 4700 1500 2250 900

---

## 3. Petunjuk Penggunaan AKG Individu dan Kelompok
LAMPIRAN II  
PERATURAN MENTERI KESEHATAN  
REPUBLIK INDONESIA  
NOMOR 28 TAHUN 2019.... 
TENTANG ANGKA  KECUKUPAN GIZI 
YANG DIANJURKAN UNTUK 
MASYARAKAT INDONESIA 
 
 
PEDOMAN PENGGUNAAN ANGKA KECUKUPAN GIZI 
 
I. Latar Belakang  
Undang-Undang Nomor 36 Tahun 2009 tentang Kesehatan telah 
mengamanatkan bahwa setiap kegiatan pembangunan harus dilandasi 
dengan wawasan kesehatan. Kesehatan merupakan hak asasi manusia 
dan salah satu unsur kesejahteraan yang harus diwujudkan sesuai 
dengan amanat Undang-Undang Dasar 1945. Upaya untuk memelihara 
dan meningkatkan derajat kesehatan harus dilaksanakan secara merata 
dalam rangka membentuk sumber daya manusia Indonesia yang 
berkualitas dan berdaya saing. Dalam Undang-Undang Nomor 36 Tahun 
2009 tentang Kesehatan dinyatakan bahwa kesehatan meliputi sehat 
secara fisik, mental, spiritual, maupun sosial yang memungkinkan setiap 
orang untuk hidup produktif. Salah satu bagian dari peningkatan derajat 
kesehatan yang menjadi tanggung jawab pemerintah adalah melalui 
upaya perbaikan gizi. 
Upaya perbaikan gizi sangat erat kaitannya dengan pemenuhan 
kualitas dan kuantitas konsumsi pangan masyarakat. Acuan untuk 
merencanakan dan menilai pemenuhan konsumsi gizi seseorang disebut 
kebutuhan gizi (nutrient requirement ), sedangkan acuan untuk 
merencanakan dan menilai konsumsi pangan kelompok orang atau 
masyarakat di suatu daerah/wilayah disebut kecukupan gizi (nutrient 
allowances atau Recommended Dietary Allowances/RDA). 
Di Indonesia, recommended dietary allowances disebut juga dengan 
Angka Kecukupan Gizi (AKG). AKG pertama kali ditetapkan pada tahun 
1968, selanjutnya diperbaharui melalui Widyakarya Nasional Pangan dan 
Gizi (WNPG). AKG yang pertama terdiri dari energi, protein, 5 vitamin dan 
2 mineral. AKG tahun 2018 mencakup energi, semua zat gizi makro

(protein, lemak dan karbohidrat serta air), 14 vitamin,  dan 14 mineral 
termasuk elektrolit.  
Pada dasarnya penggunaan AKG dapat dibagi menjadi dua kategori 
besar yaitu untuk penilaian asupan zat gizi dari konsumsi pangan dan 
untuk perencanaan konsumsi pangan (Gambar1).  
 
 
 
 
 
Sejak ditetapkannya AKG dan pembaharuannya secara berkala 
hingga kini, berbagai kebijakan dan program telah menggunakan AKG, 
antara lain perencanaan penyediaan pangan, penggunaan AKG untuk 
penetapan garis kemiskinan, penggunaan AKG untuk penetapan upah 
minimum, penggunaan AKG untuk penetapan skor Pola Pangan Harapan 
(PPH), penggunaan AKG untuk penetapan panduan gizi seimbang, dan 
penggunaan AKG untuk Penetapan Acuan Label Gizi (ALG).  
 
II. Tujuan 
AKG digunakan sebagai acuan bagi pemerintah pusat, pemerintah daerah, 
dan pemangku kepentingan untuk : 
a. menghitung kecukupan gizi penduduk di daerah 
b. menyusun pedoman konsumsi pangan 
Asupan 
Gizi* 
Kecukupan 
Gizi 
Penilaian    
asupan              
gizi 
Perencanaan 
konsumsi 
pangan 
Kelompok Daerah/ 
Wilayah Kelompok 
Daerah/ 
Wilayah 
 
Gambar 1.  
Penggunaan Angka Kecukupan Gizi untuk Penilaian 
Asupan Gizi dan Perencanaan Konsumsi Pangan 
Sumber : Institue of Medicine, 2005

c. menilai konsumsi pangan pada penduduk dengan karakteristik 
tertentu 
d. menghitung kebutuhan pangan bergizi pada penyelenggaraan 
makanan institusi 
e. menghitung kebutuhan pangan bergizi pada situasi darurat 
f. menetapkan Acuan Label Gizi  
g. mengembangkan indeks mutu konsumsi pangan 
h. mengembangkan produk pangan olahan 
i. menentukan garis kemiskinan 
j. menentukan biaya minimal untuk pangan bergizi dalam program 
jaminan sosial pangan 
k. menentukan upah minimum  
l. kebutuhan lainnya  
 
III. Prinsip dan Tata Cara Penggunaan Angka Kecukupan Gizi  
A. Penggunaan Angka Kecukupan Gizi untuk Menghitung Kecukupan 
Gizi Penduduk  di Daerah 
Prinsip dan tata cara penentuan rata-rata AKG dari penduduk di 
suatu daerah: 
1. Menghitung persentase (%) penduduk menurut jenis kelamin 
dan umur sesuai dengan pengelompokan umur pada tabel AKG. 
2. Mengalikan nilai AKG pada tiap kelompok umur dan jenis 
kelamin, dengan persentase penduduk (%) di suatu daerah pada 
kelompok umur dan jenis kelamin yang sesuai. 
3. Hasil dari perkalian tersebut kemudian dijumlahkan kebawah 
untuk setiap zat gizi, kemudian dibagi 100.  
4. Maka didapatkan rerata AKG (misal AKE dan AKP) penduduk di 
daerah tersebut. 
 
B. Penggunaan Angka Kecukupan Gizi untuk Menyusun Pedoman 
Konsumsi Pangan  
Konsumsi pangan penduduk Indonesia diarahkan untuk 
mengacu pada Pedoman Umum Gizi Seimbang. Prinsip dan tata cara 
penggunaan AKG untuk menyusun pedoman konsumsi pangan: 
1. Menggunakan AKG per kelompok umur sesuai pengelompokan 
umur pada pedoman gizi seimbang. 
2. Menerjemahkan jumlah energi dan zat gizi menggunakan Tabel

Komposisi Pangan Indonesia (TKPI) menjadi kuantitas pangan 
dalam satuan gram pangan untuk setiap kelompok pangan 
(makanan pokok, lauk pauk, sayur, buah dan air). 
3. Menerjemahkan kuantitas gram masing-masing kelompok 
pangan menjadi satuan porsi atau ukuran Ukuran Rumah 
Tangga (URT). 
4. Prinsip ini bisa dilakukan untuk setiap kelompok umur, dengan 
pembagian porsi sebagaimana contoh menu “isi piringku” pada 
Pedoman Umum Gizi Seimbang. 
 
C. Penggunaan Angka Kecukupan Gizi untuk Menilai Konsumsi Pangan 
pada Penduduk dengan Karakteristik Tertentu 
Konsumsi pangan suatu penduduk menunjukkan tingkat 
asupan energi, protein, vitamin, dan mineral yang dapat digunakan 
sebagai indikator untuk menentukan tingkat gizi masyarakat dan 
juga keberhasilan pemerintah dalam pembangunan pangan, 
pertanian, kesehatan, dan sosial ekonomi secara terintegrasi. 
Prinsip dan tata cara penggunaan AKG untuk penilaian 
konsumsi pangan pada penduduk dengan karakteristik tertentu: 
1. Menetapkan kelompok penduduk yang akan dilakukan 
penilaiannya misalnya bedasarkan umur, jenis kelamin atau 
status fisiologis tertentu. 
2. Menghitung kandungan energi dan zat gizi dari pangan yang 
dikonsumsi menggunakan TKPI. 
3. Menghitung rata-rata asupan energi dan zat gizi pada kelompok 
tersebut. 
4. Nilai rata rata asupan tersebut dibandingkan dengan AKG pada 
kelompok umur dan jenis kelamin yang sesuai dan dinyatakan 
dalam persentase (%), untuk mengetahui tingkat asupan gizi. 
 
D. Penggunaan Angka Kecukupan Gizi untuk Menghitung Kebutuhan 
Pangan Bergizi pada Penyelenggaraan Makanan Insitusi  
Pedoman penggunaan AKG untuk menghitung kebutuhan 
pangan bergizi pada penyelenggaraan makanan insitusi diperuntukan 
pada institusi sekolah, tempat kerja, asrama, pesantren, panti, pusat 
pemasyarakatan, dan pelayanan haji. Gizi institusi adalah 
kecukupan gizi didasarkan pada hitungan dengan memperhatikan,

antara lain angka kecukupan gizi, aktivitas tubuh, umur, penyakit, 
dan jenis kelamin. Penyelenggaraan makanan institusi dapat berupa 
pemberian makanan untuk memenuhi kebutuhan sehari atau untuk 
memenuhi sebagian dari kebutuhan gizi harian seperti sarapan, 
makan siang, makan malam, atau kudapan. 
Pedoman ini dapat digunakan untuk penilaian asupan gizi, 
pengadaan makanan, perencanaan makan, pengaturan tingkat gizi 
karakteristik dan kelompok sasaran.  
Prinsip dan tata cara penggunaan AKG untuk menghitung 
kebutuhan pangan bergizi pada penyelenggaraan makanan insitusi  
sebagai berikut:  
1. Menetapkan kelompok sasaran sesuai pengelompokan umur dan 
jenis kelamin dalam tabel AKG.   
2. Menggunakan AKG pada kelompok tersebut untuk 
merencanakan kebutuhan konsumsi pangan. 
3. Menerjemahkan hasil perhitungan kebutuhan gizi menjadi 
kuantitas (gram) dan porsi makanan (prioritas pada energi, 
protein, karbohidrat, lemak, vitamin A, vitamin C, zat besi dan 
zink) sesuai kelompok pangan berdasarkan gizi seimbang dalam 
kualitas dan kuantitas. 
4. Menghitung kebutuhan jumlah makanan untuk seluruh sasaran 
di institusi tersebut (termasuk penambahan 10%). 
Penyelenggaraan makanan pada institusi khusus seperti militer 
dan kepolisian perlu memperhatikan kecukupan gizi yang didasarkan 
kepada hitungan lebih spesifik dengan memperhatikan AKG, aktivitas 
tubuh, usia, suhu lingkungan, penyakit, jenis kelamin, dan sifat 
penugasan. Pedoman ini dapat digunakan untuk penilaian asupan 
gizi kelompok, pengadaan makanan dan perencanaan makan, 
pengaturan tingkat gizi ransum militer, serta untuk distribusi, dan 
pengembangan materi pendidikan gizi untuk personil militer dan 
kepolisian.  
Prinsip dan tata cara penggunaan AKG untuk menghitung 
kebutuhan pangan bergizi pada penyelenggaraan makanan insitusi  
khusus tersebut, sebagai berikut:  
1. Perhitungan kebutuhan menggunakan rerata AKG pada 
kelompok berdasarkan kelompok umur 19-29 tahun, 30-49 
tahun, dan 50-64 tahun dengan menjumlahkan kebutuhan jenis

laki-laki dan perempuan yang dirata-ratakan. 
2. Menyesuaikan AKG pada angka 1 dengan memperhatikan faktor 
tingkat aktivitas fisik, suhu lingkungan, jenis kelamin, stres, dan 
sifat penugasan yang dihadapi prajurit. 
3. Mengonversi kebutuhan gizi pada angka 2 menjadi jumlah dan 
komposisi anjuran konsumsi makanan dan minuman mengikuti 
prinsip gizi seimbang.  
Contoh Kebutuhan zat gizi untuk militer awak pesawat terbang: 
a. Kebutuhan karbohidrat sebesar 60-65% dari energi, 
diberikan sebelum terbang sebesar 60-65% dari energi, 
dalam kondisi terbang sebesar  60-65% dari energi, sesudah 
terbang  ± 55%  dari energi.   
b. Kebutuhan protein  diperlukan sebanyak 65% hewani, 35% 
nabati, sebelum terbang sebesar 10 -15% dari energi, 
kondisi dalam terbang sebesar 10-15% dari energi, sesudah 
terbang ± 13%  dari energi. 
c. Kebutuhan lemak berkisar 20-25% dari energi. sebelum 
terbang sebanyak sebesar 20-25% dari energi, kondisi 
dalam terbang sebesar 20-25% dari energi, kondisi sesudah 
terbang ± 32% dari energi. 
d. Kebutuhan vitamin dan mineral, dan air disesuaikan 
dengan kebutuhan zat gizi makro dengan memperhatikan 
kondisi fisiologis dan  lingkungan kerja/penugasan. 
 
E. Penggunaan Angka Kecukupan Gizi untuk Menghitung Kebutuhan 
Pangan Bergizi Pada Situasi Darurat  
Upaya penanganan gizi dalam situasi bencana merupakan 
rangkaian kegiatan yang dimulai sejak sebelum terjadinya bencana 
(pra bencana), pada saat tanggap darurat bencana, dan pasca 
bencana. Tahap awal pemberian makanan bertujuan agar pengungsi 
tidak lapar serta dapat mempertahankan dan memperbaiki status 
gizi, serta menanggulangi masalah gizi melalui intervensi sesuai 
permasalahan yang ditemukan. 
Dalam koordinasi penanganan bencana melalui pendekatan 
kluster, gizi merupakan salah satu subkluster yang berada dibawah 
kluster kesehatan dan mempunyai tugas dan fungsi terkait 
penyelenggaraan makanan yang bertujuan untuk menyediakan

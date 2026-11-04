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

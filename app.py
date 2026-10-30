import time, os, string, datetime, pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from streamlit_drawable_canvas import st_canvas
import numpy as np

# ========== 1. FUNGSI BACA TULIS PASSWORD, HITUNG LUAS ==========
FILE_USERNAME = "admin"
def baca_user():
    if os.path.exists(FILE_USERNAME):
        with open(FILE_USERNAME, "r") as f:
            return f.read().strip()
    return "admin"

FILE_PASSWORD = "password.txt"
def baca_password():
    if os.path.exists(FILE_PASSWORD):
        with open(FILE_PASSWORD, "r") as f: return f.read().strip()
    return "admin123"

def simpan_password(pw_baru):
    with open(FILE_PASSWORD, "w") as f: f.write(pw_baru)

def hitung_luas(panjang, lebar): return panjang * lebar

# =========================================================================
# ========== 2. SETUP AWAL SESSION STATE (LACI MEMORI CIPTAKANKAN DULU) ====
# =========================================================================
if "login" not in st.session_state: st.session_state.login = False
if "riwayat" not in st.session_state: st.session_state.riwayat = []
if "hasil_psikologi" not in st.session_state: st.session_state.hasil_psikologi = "Belum dianalisis"
if "user" not in st.session_state: st.session_state.user = baca_user()
if "password_saat_ini" not in st.session_state: st.session_state.password_saat_ini = baca_password()

# SET PAGE - Diletakkan di bawah inisialisasi awal agar aman
st.set_page_config(page_title="PersonaArch Budget", layout="centered")

# =========================================================================
# ========== 3. ZONA CSS GLOBAL (DI LUAR IF LOGIN - KEBAL KEDIP MERAH) =====
# =========================================================================
# Saat rerun perpindahan halaman terjadi, instruksi biru tidak akan putus!
st.markdown("""
    <style>
    /* Mengunci warna SEMUA tombol utama (primary) di aplikasi agar selalu BIRU GRADASI */
    .stApp button[kind="primary"], [data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #1E73E6 0%, #1A237E 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0px !important;
        box-shadow: 0 4px 15px rgba(30, 115, 230, 0.3) !important;
    }
    .stApp button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(26, 35, 126, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# ========== 4. HALAMAN LOGIN (LOG IN PAGE) ===============================
# =========================================================================
if not st.session_state.get("login", False):
    # CSS hanya aktif saat pengguna berada di halaman login depan saja - bg login page
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #EBF3FC 0%, #C2DCFF 100%) !important;
    }
    div[data-testid="stColumn"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.94) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        padding: 42px 35px !important;
        box-shadow: 0 15px 45px rgba(30, 115, 230, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.7) !important;
    }
    /* Setelan kolom input teks Username & Password */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid #7AB8FF !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Render Gambar Logo Biru di Atas Tengah
    _, img_col, _ = st.columns([1.5, 5, 1.5])
    with img_col:
        st.image("logo_line.png", use_container_width=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # 3. Struktur Kolom Tengah pembungkus Card
    _, card_col, _ = st.columns([1, 4, 1]) 

    # 4. CONTAINER MASUK KE DALAM KOLOM
    with card_col:
        with st.container(border=True):
            st.markdown("""
                <h2 style='text-align:center; color:#1E73E6; font-family: "Segoe UI", sans-serif; font-weight: 800; margin-bottom: 5px; margin-top: 0px;'>
                Welcome <span style='color:#1A237E;'>Back</span>
                </h2>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                <p style='text-align:center; color:#1A237E; font-size: 14px; font-family: "Segoe UI", sans-serif; opacity: 0.85; margin-top: -20px; margin-bottom: 25px; line-height: 1.4;'>
                Where architectural vision meets your personality
                </p>
                """, unsafe_allow_html=True)

            st.markdown("""
                <p style='text-align:left; color:#1A237E; font-size: 13px; font-family: "Helvetica", sans-serif; font-weight: 600; margin-bottom: 5px; opacity: 0.9;'>
                Username
                </p>
                """, unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Input Username", label_visibility="collapsed")

            st.markdown("""
                <p style='text-align:left; color:#1A237E; font-size: 13px; font-family: "Segoe UI", sans-serif; font-weight: 600; margin-bottom: 5px; opacity: 0.9;'>
                Password
                </p>
                """, unsafe_allow_html=True)
            pw = st.text_input("Password", type="password", placeholder="Masukkan Password Akses", label_visibility="collapsed")
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            # Tombol Sign In
            if st.button("Sign In", type="primary", use_container_width=True):
                if (username == st.session_state.user and pw == st.session_state.password_saat_ini):
                    st.session_state.login = True
                    st.session_state.login_error = False
                    st.rerun()
                else:
                    st.session_state.login_error = True

            if "login_error" in st.session_state and st.session_state.login_error:
                st.markdown("""
                    <div style='background-color: #FDE8E8; border: 1px solid #F8B4B4; border-radius: 12px; padding: 12px 15px; margin-top: 15px; text-align: left;'>
                        <span style='color: #9B1C1C; font-weight: 700; font-size: 14px; display: block; margin-bottom: 2px;'>An Error Occurred.</span>
                        <span style='color: #C81E1E; font-weight: 400; font-size: 13px;'>Incorrect password. Please try again.</span>
                    </div>
                """, unsafe_allow_html=True)

    st.stop()
    
# =========================================================================
# ========== 3. HALAMAN UTAMA (DASHBOARD PEMILIHAN & ESTIMASI) ==========
# =========================================================================

# FUNGSI RESET FORM 
def reset_form():
    # Mengosongkan memori variabel hitungan utama
    if 'total_biaya_global' in st.session_state: 
        del st.session_state['total_biaya_global']
    if 'df_rab' in st.session_state: 
        del st.session_state['df_rab']
    if 'path_denah' in st.session_state: 
        del st.session_state['path_denah']
    if 'path_ttd' in st.session_state: 
        del st.session_state['path_ttd']
    if 'hasil_psikologi' in st.session_state:
        st.session_state.hasil_psikologi = "Belum dianalisis"
        
    # UI: Memaksa Streamlit membersihkan sisa isian di komponen layar
    # Hapus kunci widget-nya dari memori agar kembali ke nilai awal bawaan (default)
    kunci_widget = ['panjang', 'lebar', 'jumlah_kamar', 'jumlah_gedung', 'jumlah_kamar_gedung', 'nama', 'alamat']
    for kunci in kunci_widget:
        if kunci in st.session_state:
            del st.session_state[kunci]

# CSS Kustom untuk Mengubah Seluruh Tombol Menjadi Biru & Merapikan Tampilan
st.markdown("""
    <style>
    /* Ubah semua tombol utama bawaan Streamlit (Type Primary) menjadi Biru Gradasi */
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #1E73E6 0%, #1A237E 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(30, 115, 230, 0.2) !important;
    }
    
    /* Ubah semua tombol sekunder bawaan Streamlit menjadi Biru Soft Terang */
    div.stButton > button[data-testid="baseButton-secondary"] {
        background: #F0F4FA !important;
        color: #1E73E6 !important;
        border: 1px solid #C2DCFF !important;
    }
    div.stButton > button[data-testid="baseButton-secondary"]:hover {
        background: #EBF3FC !important;
        color: #1A237E !important;
        border: 1px solid #1E73E6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Opening Banner - Gradasi Biru Langit 
st.markdown("""
    <div style='background: linear-gradient(135deg, #EBF3FC 0%, #C2DCFF 100%); padding: 20px; border-radius: 20px; border-left: 6px solid #1E73E6; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(30, 115, 230, 0.06);'>
        <h2 style='margin: 0; color: #1A237E; font-family: "Segoe UI", sans-serif; font-weight: 700;'>Dashboard</h2>
        <p style='margin: 5px 0 0 0; color: #1A237E; margin-top: -5px; margin-bottom: 5px; font-size: 14px; line-height: 1.5; font-family: "Segoe UI", sans-serif; opacity: 0.85;'>
            An integrated spatial budgeting system tailored to your technical dimensions and personality profiling
        </p>
    </div>
""", unsafe_allow_html=True)

# ========== UPLOADER SETTING APP DI SIDEBAR ==========
st.sidebar.title("⚙️ Settings")
tampilkan_draft = st.sidebar.checkbox("Watermark DRAFT", value=True, key="draft")
uploaded_logo = st.sidebar.file_uploader("Upload Logo Perusahaan", type=["png", "jpg", "jpeg"])
logo_path = None
if uploaded_logo is not None:
    with open("temp_logo.png", "wb") as f:
        f.write(uploaded_logo.getbuffer())
        logo_path = "temp_logo.png"
        st.sidebar.success("Logo berhasil diupload!")

with st.sidebar.expander("🔐 Security & Account"):
    st.subheader("Authentication Settings")
    pass_lama = st.text_input("Current Password", type="password", key="plama")
    pass_baru = st.text_input("New Password", type="password", key="pbaru")
    pass_baru_2 = st.text_input("Confirm New Password", type="password", key="pbaru2")
    if st.button("Update Access Password", use_container_width=True):
        if pass_lama != st.session_state.password_saat_ini: st.error("Current password incorrect!")
        elif pass_baru != pass_baru_2: st.error("Passwords do not match!")
        elif len(pass_baru) < 8: st.error("Password must be at least 8 characters!")
        elif not any(char.isdigit() for char in pass_baru): st.error("Password must contain a number!")
        elif not any(char.isupper() for char in pass_baru): st.error("Password must contain an uppercase letter!")
        elif not any(char in string.punctuation for char in pass_baru): st.error("Password must contain a special character!")
        else:
            simpan_password(pass_baru)
            st.session_state.password_saat_ini = pass_baru
            st.success("Password updated successfully!") 

# Jarak indentasi rapi agar sejajar dengan blok expander di atasnya
with st.sidebar.expander("🚪 Session Control"):
    st.write("Selesai menggunakan aplikasi?")
    if st.button("Log Out From App", type="secondary", use_container_width=True, key="btn_logout"):
        # Reset status login memori aplikasi kembali ke awal
        st.session_state.login = False
        if "login_error" in st.session_state:
            st.session_state.login_error = False
        
        # PENTING: st.rerun() harus MASUK 8 spasi ke dalam (DI DALAM tanda kurung tombol button)
        st.rerun()           

# Input Dimensi Bangunan
st.markdown("### 🏗️ Proyeksi Spasial & Dimensi Bangunan")

col_mode, col_diskon = st.columns(2)
with col_mode:
    mode = st.radio("Kategori Objek Pembangunan:", ["Rumah", "Hotel", "Kompleks"], horizontal=True, key="mode")
with col_diskon:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    pakai_diskon = st.checkbox("Terapkan Diskon Khusus (50%)", value=False, key="pakai_diskon")

st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    panjang = st.number_input("Panjang Unit (meter)", min_value=0.0, format="%.2f", key="panjang")
with c2:
    lebar = st.number_input("Lebar Unit (meter)", min_value=0.0, format="%.2f", key="lebar")
with c3:
    harga_per_m2 = st.number_input("Biaya Standard per m² (Rp)", min_value=0, value=2500000, step=100000, key="harga_per_m2")

if mode == "Rumah" or mode == "Hotel":
    jumlah_kamar = st.number_input(f"Jumlah Kamar pada {mode}", min_value=1, value=1, key="jumlah_kamar")
    jumlah_gedung = 1
    jumlah_kamar_per_gedung = 1
else:
    cc1, cc2 = st.columns(2)
    with cc1:
        jumlah_gedung = st.number_input("Total Unit Gedung dalam Kompleks", min_value=1, value=1, key="jumlah_gedung")
    with cc2:
        jumlah_kamar_per_gedung = st.number_input("Kapasitas Kamar per Unit Gedung", min_value=1, value=1, key="jumlah_kamar_gedung")
    jumlah_kamar = 1

pilihan = st.radio(
    "Metode Perhitungan Volume Proyek:", 
    ["Hitung Berdasarkan Luas Standard", "Hitung Berdasarkan Akumulasi Kamar"], horizontal=True, key="pilihan")

# =========================================================================
# ========== 4. ANALISIS PSIKOLOGI SPASIAL (SISI PSIKOLOGI LINGKUNGAN) =====
# =========================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("### 🔮 Pendekatan Psikologi Spasial & Profiling Karakter")

# Membagi baris menjadi 3 kolom agar input kuesioner rapi dan sejajar horizontal
cp1, cp2, cp3 = st.columns(3)
with cp1:
    warna = st.selectbox("Palet Warna Dominan Ruangan:", ["Biru", "Kuning", "Hijau", "Putih", "Abu-abu"], key="warna")
with cp2:
    pencahayaan = st.selectbox("Preferensi Sistem Pencahayaan:", ["Sinar Alami / Bukaan Besar", "Cahaya Hangat / Redup Syahdu", "Cahaya Terang / Fokus"], key="pencahayaan")
with cp3:
    fungsi_utama = st.selectbox("Fungsi Utama Pemanfaatan Ruang:", ["Sosialisasi / Interaksi Keluarga", "Menyendiri / Memulihkan Energi", "Fokus Bekerja / Cari Inspirasi"], key="fungsi_utama")

# Slider ditaruh di bawahnya melebar penuh sebagai parameter pelengkap luas spasial
luas_ideal = st.slider("Ekspektasi Luas Kamar/Ruang Ideal (m²):", 8, 40, 15, key="luas_ideal")

# 🧬 MESIN UTAMA RUMUS PSIKOLOGI SPASIAL (Membaca kombinasi 3 Variabel + Parameter Luas)
def analisis_kepribadian(warna, cahaya, fungsi, luas):
    if warna == "Biru" and fungsi == "Menyendiri / Memulihkan Energi":
        return "The Deep Introspective Sanctuary (Karakter tenang dengan tingkat stimulasi kognitif rendah. Sangat ideal untuk memulihkan kelelahan mental, menekan tingkat kecemasan, dan merangsang pemikiran reflektif mendalam)."
    elif warna == "Kuning" and cahaya == "Sinar Alami / Bukaan Besar" and fungsi == "Sosialisasi / Interaksi Keluarga":
        return "The High-Energy Communal Oasis (Sangat menstimulasi hormon kebahagiaan dan dopamin. Desain ruang terbuka yang memicu antusiasme, kehangatan komunikasi, serta mempererat ikatan hubungan antarmanusia)."
    elif warna == "Hijau" and fungsi == "Fokus Bekerja / Cari Inspirasi":
        return "The Biophilic Productivity Zone (Kombinasi elemen alam spasial yang ampuh mereduksi stres kognitif. Meningkatkan daya fokus visual, stabilitas emosi, serta memicu munculnya ide-ide kreatif baru)."
    elif warna == "Putih" and luas > 20:
        return "The Minimalist Zenith (Menawarkan kebebasan persepsi spasial yang mutlak. Minim gangguan visual sehingga otak bisa fokus penuh pada fungsionalitas, keteraturan kognitif, dan efisiensi mental)."
    else:
        # Pilihan default jika kombinasi pengguna sangat unik
        return "The Harmonious Adaptable Space (Desain ruang seimbang yang fleksibel. Mengutamakan kenyamanan emosional yang ramah terhadap perubahan aktivitas, serta memberikan ketenangan psikologis yang stabil)."

# Tombol Pemicu Analisis
if st.button("Jalankan Analisis Psikologi Ruang", type="secondary", use_container_width=True, key="btn_psiko"):
    hasil = analisis_kepribadian(warna, pencahayaan, fungsi_utama, luas_ideal)
    st.session_state.hasil_psikologi = hasil
    st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 18px; border-radius: 14px; border: 1px solid #A5D6A7; color: #2E7D32; font-family: "Segoe UI", sans-serif; font-size: 15px; line-height: 1.5;'>
            <strong>🧬 Hasil Profiling & Karakter Spasial:</strong><br>{hasil}
        </div>
    """, unsafe_allow_html=True)


# ========== 5. DOKUMENTASI & VALIDASI DATA LAPORAN ==========
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("### 📝 Validasi Administratif Laporan")

cl1, cl2 = st.columns(2)
with cl1:
    nama = st.text_input("Nama Pemilik / Klien Proyek", placeholder="Contoh: Dr. Ari Gunawan", key="nama")
with cl2:
    alamat = st.text_input("Lokasi Geografis Proyek", placeholder="Contoh: Jl. Nusa Permai No.1, Semarang", key="alamat")

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
st.caption("Tanda Tangan Digital sebagai Validasi Dokumen:")

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)", 
    stroke_width=3, 
    stroke_color="#1A237E", 
    background_color="#ffffff", 
    height=150, 
    width=400, 
    drawing_mode="freedraw", 
    key="canvas", 
    update_streamlit=True, 
)

if canvas_result is not None and canvas_result.json_data is not None:
    if len(canvas_result.json_data["objects"]) > 0:
        img = Image.fromarray(np.uint8(canvas_result.image_data))
        img = img.convert("RGBA")
        img.save("ttd.png")
        st.session_state['path_ttd'] = "ttd.png"

# ========== 6. EKSEKUSI UTAMA (PROSES KALKULASI RAB) ==========
st.markdown("<br>", unsafe_allow_html=True)

# ========== Tombol Hitung Utama ==========
if st.button("📊 ESTIMASI BIAYA & RAB", type="primary", use_container_width=True, key="btn_hitung"):
    if panjang == 0 or lebar == 0: 
        st.warning("⚠️ Lengkapi nilai dimensi Panjang dan Lebar unit terlebih dahulu.")
    else:
        luas_mentah = hitung_luas(panjang, lebar)

        if mode == "Kompleks":
            hasil_total = luas_mentah * jumlah_kamar_per_gedung * jumlah_gedung
            jumlah_gambar_final = jumlah_gedung * jumlah_kamar_per_gedung
        else:
            # MEMISAHKAN LOGIKA RUMUS RUMAH / HOTEL BERDASARKAN OPSI USER
            if pilihan == "Hitung Berdasarkan Luas Standard":
                # Metode 1: Panjang x Lebar adalah LUAS TOTAL RUMAH (Tidak dikali kamar)
                hasil_total = luas_mentah
                jumlah_gambar_final = jumlah_kamar
            else:
                # Metode 2: Akumulasi Kamar (Luas 1 Kamar x Banyaknya Kamar)
                hasil_total = luas_mentah * jumlah_kamar
                jumlah_gambar_final = jumlah_kamar
            
        # Perhitungan total biaya akhir & aplikasi diskon kustom
        total_biaya = hasil_total * harga_per_m2
        if pakai_diskon:
            total_biaya = total_biaya * 0.5

        # Menyimpan seluruh hasil kalkulasi yang valid ke dalam memori aplikasi
        st.session_state['total_biaya_global'] = total_biaya
        st.session_state['luas_total_render'] = hasil_total
        st.session_state['jumlah_gambar_final_render'] = jumlah_gambar_final
        
        # Menyiapkan kamus data RAB untuk tabel visual
        rab_data = {
            "Komponen Pekerjaan Arsitektur": [
                "Struktur Pondasi & Tanah (15%)", 
                "Struktur Inti & Pasangan Dinding (30%)", 
                "Konstruksi Rangka Atap & Plafond (15%)", 
                "Pekerjaan Finishing & Arsitektural (25%)", 
                "Instalasi Mekanikal, Elektrikal & Saniter (15%)"
            ], 
            "Bobot (%)": [15, 30, 15, 25, 15]
        }
        st.session_state['df_rab'] = rab_data
        st.success("✅ Anggaran Proyek Berhasil Dikalkulasi!")

# BAGIAN RENDER VISUAL (Hanya muncul jika memori hitungan terisi)
if 'total_biaya_global' in st.session_state:
    total_biaya = st.session_state['total_biaya_global']
    hasil_total = st.session_state.get('luas_total_render', 0)
    jumlah_gambar_final = st.session_state.get('jumlah_gambar_final_render', 1)
    
    st.markdown(f"""
        <div style='background-color: #EBF3FC; padding: 20px; border-radius: 16px; border: 1px solid #C2DCFF; text-align: center; margin-bottom: 25px;'>
            <p style='margin: 0; color: #1E73E6; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Total Estimasi Anggaran Biaya</p>
            <h1 style='margin: 5px 0 0 0; color: #1A237E; font-size: 36px; font-weight: 800;'>Rp {total_biaya:,.0f}</h1>
            <p style='margin: 5px 0 0 0; color: #555; font-size: 13px;'>Volume Total Bangunan: <strong>{hasil_total:.2f} m²</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Render Tabel RAB
    if 'df_rab' in st.session_state:
        rab_data = st.session_state['df_rab']
        df_tampil = pd.DataFrame(rab_data)

        df_tampil["Alokasi Anggaran (Rp)"] = [f"Rp {total_biaya * p / 100:,.0f}" for p in rab_data["Bobot (%)"]]
        st.markdown("#### 📊 Distribusi Anggaran Pekerjaan (RAB)")
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        # =========================================================================
        # ==== 🗺️ PROYEKSI VISUAL: DIAGRAM LINGKARAN (PIE CHART) RAB DINAMIS =====
        # =========================================================================
        st.markdown("#### 📊 Visualisasi Distribusi Anggaran Proyek")
            
        # 1. Menentukan Palet Warna Diagram Berdasarkan Variabel Psikologi Warna User
        # Kita gunakan kombinasi gradasi warna yang selaras agar visualnya mewah
        if warna == "Biru":
                palet_warna = ['#1A237E', '#1E73E6', '#4A90E2', '#7AB8FF', '#C2DCFF'] # Gradasi Navy ke Biru Muda
        elif warna == "Kuning":
                palet_warna = ['#B7791F', '#D69E2E', '#ECC94B', '#F6E05E', '#FEFCBF'] # Gradasi Emas ke Kuning Pastel
        elif warna == "Hijau":
                palet_warna = ['#276749', '#38A169', '#48BB78', '#68D391', '#C6F6D5'] # Gradasi Hijau Hutan ke Mint
        elif warna == "Abu-abu":
                palet_warna = ['#2D3748', '#4A5568', '#718096', '#A0AEC0', '#E2E8F0'] # Gradasi Monokrom Elegan
        else: # Putih / Default
                palet_warna = ['#2B6CB0', '#4299E1', '#63B3ED', '#90CDF4', '#EBF8FF'] # Biru Soft Universal
            
        # 2. Siapkan Data untuk Diagram
        labels = [
                "Struktur Pondasi (15%)", 
                "Dinding & Struktur Inti (30%)", 
                "Rangka Atap & Plafond (15%)", 
                "Finishing & Arsitektural (25%)", 
                "Mekanikal & Elektrikal (15%)"
        ]
        sizes = [15, 30, 15, 25, 15]
            
        # 3. Proses Penggambaran Menggunakan Matplotlib
        fig, ax = plt.subplots(figsize=(6, 5))
            
        # Gambar diagram lingkaran dengan efek bayangan dan gaya minimalis modern
        wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=palet_warna,
                autopct='%1.0f%%', # Menampilkan angka persentase bulat
                startangle=140,    # Sudut kemiringan awal diagram
                shadow=False,       # Matikan shadow bawaan matplotlib agar tidak kaku
                textprops=dict(color="#2D3748", fontname="sans-serif", fontsize=9), # Gaya teks label
                pctdistance=0.75   # Mengatur posisi teks persentase agar pas di dalam potongan
            )
            
        # Membuat teks persentase di dalam lingkaran menjadi tebal berwarna putih agar kontras
        for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
                
        # Menambahkan lingkaran putih di tengah untuk efek "Donut Chart" 
        centre_circle = plt.Circle((0,0), 0.50, fc='white', linewidth=0)
        fig.gca().add_artist(centre_circle)
            
        ax.axis('equal')  # Memastikan lingkaran berbentuk bulat sempurna
        plt.tight_layout()
            
        # 4. Simpan Gambar Sementara untuk Lampiran PDF Halaman 2
        fig.savefig("denah_temp.png", dpi=300, bbox_inches='tight', transparent=True)
        st.session_state['path_denah'] = "denah_temp.png"
            
        # Render visual diagram langsung ke layar dashboard 
        st.pyplot(fig)
        plt.close(fig)      

# =========================================================================
# ========== 7. PANEL EKSEKUSI LAPORAN & DOKUMEN ==========================
# =========================================================================
# 1. CETAKAN FUNGSI PDF (Wajib ditaruh di atas sebelum tombol memanggilnya)
def buat_pdf(
        nama, alamat, luas, biaya, logo_file, mode, jumlah_gedung=1, jumlah_kamar_per_gedung=1, 
        jml_gambar=1, hasil_analisis="Belum dianalisis", show_draft=True, warna="Biru", pencahayaan="Sinar Alami", fungsi_utama="Sosialisasi"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(595, 842)) # Ukuran kertas A4
    
    # Fungsi Watermark Draft
    if show_draft:
        c.saveState()
        c.setFont("Helvetica-Bold", 70)
        c.setFillColorRGB(0.7, 0, 0, alpha=0.06)
        c.translate(300, 420)
        c.rotate(45)
        c.drawString(-110, 0, "DRAFT")
        c.restoreState()

    # Pemrosesan Header Logo
    try:
        if logo_file is not None and os.path.exists(logo_file):
            logo_reader = ImageReader(logo_file)
            c.drawImage(logo_reader, 40, 740, width=150, height=60, preserveAspectRatio=True, mask='auto')
        else:
            c.setFont("Helvetica-Bold", 18)
            c.setFillColorRGB(0.11, 0.45, 0.90)
            c.drawString(40, 760, "PersonaArch")
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.1, 0.14, 0.49)
            c.drawString(40, 745, "Spatial Budgeting & Psychology")
    except:
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(0.11, 0.45, 0.90)
        c.drawString(40, 760, "PersonaArch")

    hari_ini = datetime.date.today().strftime("%d %B %Y")
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(400, 760, f"Tanggal Penerbitan: {hari_ini}")

    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(1)
    c.line(40, 725, 555, 725)

    # =========================================================================
    # ========== BLOK INFORMASI ADMINISTRATIF (TATA LETAK PRESISI) ============
    # =========================================================================
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.1, 0.14, 0.49)
    y = 700
    c.drawString(40, y, "DATA SPESIFIKASI & ESTIMASI ANGGARAN"); y -= 22

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    
    # --- KOLOM KIRI (Klien, Lokasi, Warna, Fungsi, PENCAHAYAAN PINDAH KE SINI) ---
    # Langkah 1: Gambar Label Kolom Kiri di x=40
    c.drawString(40, y, "Klien / Pemilik Proyek")
    c.drawString(40, y-16, "Lokasi Geografis")
    c.drawString(40, y-32, "Palet Warna Pilihan")
    c.drawString(40, y-48, "Pemanfaatan Ruang")
    c.drawString(40, y-64, "Sistem Pencahayaan") 
    
    # Langkah 2: Gambar Isi Data Kolom Kiri Secara Tegak Lurus Sejajar di x=155
    c.drawString(155, y, f":   {nama if nama else '-'}")
    c.drawString(155, y-16, f":   {alamat if alamat else '-'}")
    c.drawString(155, y-32, f":   {warna}")
    c.drawString(155, y-48, f":   {fungsi_utama}")
    c.drawString(155, y-64, f":   {pencahayaan}") 

    # --- KOLOM KANAN (Data naik ke atas, lebih longgar dan lapang) ---
    # Langkah 3: Gambar Label Kolom Kanan di x=330
    c.drawString(330, y, "Kategori Objek")
    c.drawString(330, y-16, "Target Standar Kamar")
    c.drawString(330, y-32, "Luas Total Akumulasi")
    c.drawString(330, y-48, "Volume Unit")
    
    # Langkah 4: Gambar Isi Data Kolom Kanan Secara Tegak Lurus Sejajar di x=460
    c.drawString(460, y, f":   {mode}")
    c.drawString(460, y-16, f":   {st.session_state.get('luas_ideal', 15)} m² (Ideal)")
    c.drawString(460, y-32, f":   {luas:,.2f} m²")
    
    if mode == "Kompleks":
        c.drawString(460, y-48, f":   {jumlah_gedung} Gedung x {jumlah_kamar_per_gedung} Kamar")
    else:
        c.drawString(460, y-48, f":   {jml_gambar} Kamar / Ruang")

    # Menurunkan posisi garis pembatas agar aman dari baris teks paling bawah
    y -= 85
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(1)
    c.line(40, y, 555, y)
    y -= 25
    
    # Nilai Investasi & Diskon
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.1, 0.14, 0.49)
    c.drawString(40, y, "PROYEKSI NILAI INVESTASI BANGUNAN"); y -= 20
    
    pakai_diskon = st.session_state.get('pakai_diskon', False)
    if pakai_diskon:
        harga_asli = biaya * 2
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        teks_asli = f"Biaya Normal Standar: Rp {harga_asli:,.0f}"
        c.drawString(40, y, teks_asli)
        panjang_teks = c.stringWidth(teks_asli, "Helvetica", 10)
        c.setStrokeColorRGB(0.8, 0, 0)
        c.line(40, y+3, 40+panjang_teks, y+3)
        y -= 18
        
        c.setFillColorRGB(0.8, 0, 0)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, y, f"Nilai Investasi Akhir (Diskon Khusus 50%): Rp {biaya:,.0f}")
        y -= 30
    else:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(40, y, f"Total Alokasi Investasi: Rp {biaya:,.0f}")
        y -= 25

    # Tabel RAB
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.1, 0.14, 0.49)
    c.drawString(40, y, "RENCANA ANGGARAN BIAYA (RAB) TERINTEGRASI"); y -= 18
    
    rab = st.session_state.get('df_rab', None)
    if rab:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(0.92, 0.94, 0.98)
        c.rect(40, y-4, 515, 18, fill=1, stroke=1)
        c.setFillColorRGB(0.1, 0.14, 0.49)
        c.drawString(45, y, "Komponen Pekerjaan Arsitektural & Inti")
        c.drawString(340, y, "Bobot (%)")
        c.drawString(430, y, "Alokasi Anggaran (Rp)")
        y -= 18
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0, 0, 0)

        for i in range(len(rab["Komponen Pekerjaan Arsitektur"])):
            c.rect(40, y-4, 515, 18, stroke=1)
            c.drawString(45, y, str(rab['Komponen Pekerjaan Arsitektur'][i]))
            c.drawString(355, y, f"{rab['Bobot (%)'][i]}%")
            nilai = biaya * rab['Bobot (%)'][i] / 100
            c.drawString(430, y, f"Rp {nilai:,.0f}")
            y -= 18
    
    # Blok Psikologi Spasial & Cat Dinding
    y -= 12
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.1, 0.14, 0.49)
    c.drawString(40, y, "HASIL PROFILING & PSIKOLOGI SPASIAL"); y -= 16
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(40, y, f"Rekomendasi Palet Warna Utama  :  {warna} (Cat Dinding Objek)"); y -= 16
    
    max_width = 515
    text = str(hasil_analisis)
    words = text.split(' ')
    line = ""
    for word in words:
        test_line = line + word + " "
        if c.stringWidth(test_line, "Helvetica", 10) < max_width:
            line = test_line
        else:
            c.drawString(40, y, line.strip())
            y -= 14
            line = word + " "
    c.drawString(40, y, line.strip())

    # Tanda Tangan Validasi
    y = 160
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(40, y, 555, y)
    y -= 25
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(60, y, "Disetujui & Divalidasi Oleh,")
    c.drawString(390, y, "Diterbitkan Oleh,")
    y -= 75
    
    if 'path_ttd' in st.session_state and os.path.exists(st.session_state['path_ttd']):
        ttd = ImageReader(st.session_state['path_ttd'])
        c.drawImage(ttd, 60, y+10, width=110, height=55, preserveAspectRatio=True, mask='auto')
        
    y -= 10
    c.line(60, y, 200, y)
    c.line(390, y, 530, y)
    y -= 14
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.drawString(60, y, f"{nama if nama else 'Klien Proyek'}")
    c.drawString(390, y, "PersonaArch Analytica")

    # ========== LAMPIRAN GRAFIK ANGGARAN (HALAMAN 2) ==========
    c.showPage()
    
    # 🔒 PENGAMAN SINKRONISASI SIDEBAR: Hanya cetak draft jika tombol di sidebar bernilai True (ON)
    if show_draft:
        c.saveState()
        c.setFont("Helvetica-Bold", 70)
        c.setFillColorRGB(0.7, 0, 0, alpha=0.04) # Opasitas 4% (sangat halus)
        c.translate(300, 420)
        c.rotate(45)
        c.drawString(-130, 0, "DRAFT")
        c.restoreState()
    
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.1, 0.14, 0.49)
    # Teks diubah dari "LAYOUT SPASIAL (DENAH)" menjadi "STRUKTUR ANGGARAN"
    c.drawString(40, 800, f"LAMPIRAN PROYEKSI STRUKTUR ANGGARAN (GRAFIK)")
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(40, 785, f"Spesifikasi Objek Proyek: Kategori {mode} | Kapasitas Akumulasi: {jml_gambar} Unit")
    c.drawString(40, 772, f"Alamat Lokasi: {alamat if alamat else '-'}")
    c.line(40, 762, 555, 762)

    # Sistem akan otomatis menarik gambar Donut Chart baru untuk dicetak ke halaman 2!
    if 'path_denah' in st.session_state and os.path.exists(st.session_state['path_denah']):
        c.drawImage(st.session_state['path_denah'], 40, 320, width=515, height=380, preserveAspectRatio=True, mask='auto')
    elif os.path.exists("denah_temp.png"):
        c.drawImage("denah_temp.png", 40, 360, width=515, height=380, preserveAspectRatio=True, mask='auto')
    
    c.save()
    return buffer.getvalue(), hari_ini

# =========================================================================
# ============= TOMBOL AKSI UTAMA & INJEKSI CSS WARNA BARU ================
# =========================================================================
st.markdown("<br>", unsafe_allow_html=True)

# 🎨 SUNTIKAN CSS DI-UPGRADE: Memaksa tombol hitung DAN tombol download menjadi Biru Premium
st.markdown("""
    <style>
    /* Ubah SEMUA tombol utama (st.button jenis primary DAN st.download_button) menjadi Biru Gradasi */
    .stButton button[kind="primary"], .stDownloadButton button {
        background: linear-gradient(90deg, #1E73E6 0%, #1A237E 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(30, 115, 230, 0.25) !important;
    }
    
    /* Mengubah semua tombol sekunder (Secondary / Reset) menjadi Biru Soft */
    .stButton button[kind="secondary"] {
        background: #F0F4FA !important;
        color: #1E73E6 !important;
        border: 1px solid #C2DCFF !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: #EBF3FC !important;
        color: #1A237E !important;
        border: 1px solid #1E73E6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# ============= PANEL EKSEKUSI LAPORAN & DOKUMEN ==========================
# =========================================================================
# 1. MENAMPILKAN MENU DROPDOWN FORMAT EKSPOR LAPORAN
st.markdown("##### 📁 Export Document:")
format_ekspor = st.selectbox(
    "Format Ekspor",
    ["Laporan Terintegrasi (PDF)", "Spreadsheets Rincian Anggaran (Excel)"],
    label_visibility="collapsed",
    key="format_ekspor"
)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# Tombol Aksi Utama: Memproses Data Masuk ke Memori
if st.button("📄 GENERATE COMPLIANCE REPORT", type="primary", use_container_width=True, key="btn_proses_dokumen"):
    if nama == "" or alamat == "":
        st.warning("⚠️ Proses dibatalkan. Mohon lengkapi data Nama Klien dan Alamat Proyek terlebih dahulu.")
    elif 'total_biaya_global' not in st.session_state:
        st.error("❌ Silakan klik tombol 'ESTIMASI BIAYA & RAB' terlebih dahulu sebelum memproses dokumen.")
    else:
        # Menarik data penting dari memori dashboard
        luas_total = st.session_state['luas_total_render']
        jml_gambar_final = st.session_state['jumlah_gambar_final_render']
        total_biaya = st.session_state['total_biaya_global']
        hasil_psiko = st.session_state.get('hasil_psikologi', "Belum dianalisis")
        rab = st.session_state.get('df_rab', None)

        # A. JIKA PENGGUNA MEMILIH FORMAT PDF
        if format_ekspor == "Laporan Terintegrasi (PDF)":
            # Ditambahkan ', pencahayaan, fungsi_utama' di bagian paling belakang parameter
            pdf_data, tanggal_file = buat_pdf(
                nama, alamat, luas_total, total_biaya, logo_path, mode, jumlah_gedung, 
                jumlah_kamar_per_gedung, jml_gambar_final, hasil_psiko, tampilkan_draft, warna, pencahayaan, fungsi_utama)
            
            st.session_state['file_siap_unduh'] = pdf_data
            st.session_state['nama_file_unduh'] = f"Laporan_Anggaran_PersonaArch_{nama.replace(' ', '_')}.pdf"
            st.session_state['mime_file_unduh'] = "application/pdf"

        # B. JIKA PENGGUNA MEMILIH FORMAT EXCEL
        else:
            # Membuat struktur data Excel premium menggunakan Pandas DataFrame
            if rab:
                df_excel = pd.DataFrame({
                    "Komponen Pekerjaan Arsitektur": rab["Komponen Pekerjaan Arsitektur"],
                    "Bobot Pekerjaan (%)": rab["Bobot (%)"],
                    "Alokasi Anggaran (Rupiah)": [total_biaya * p / 100 for p in rab["Bobot (%)"]]
                })
                
                # Menambahkan baris total akhir di bagian paling bawah tabel Excel
                baris_total = pd.DataFrame({
                    "Komponen Pekerjaan Arsitektur": ["TOTAL NILAI INVESTASI BANGUNAN"],
                    "Bobot Pekerjaan (%)":[100], # <--- Kurung siku diisi angka 100 tunggal, bukan dari list rab
                    "Alokasi Anggaran (Rupiah)": [total_biaya]})
                
                df_excel = pd.concat([df_excel, baris_total], ignore_index=True)
                
                # Mengonversi DataFrame menjadi byte data Excel (.xlsx) di memori
                output_excel = BytesIO()
                with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                    df_excel.to_excel(writer, index=False, sheet_name="RAB PersonaArch")
                excel_data = output_excel.getvalue()
                
                st.session_state['file_siap_unduh'] = excel_data
                st.session_state['nama_file_unduh'] = f"RAB_Spreadsheet_PersonaArch_{nama.replace(' ', '_')}.xlsx"
                st.session_state['mime_file_unduh'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        # Log History
        st.session_state.riwayat.append(
            f"🏡 {mode} | Vol: {luas_total:.2f}m² | 💰 Rp {total_biaya:,.0f} | "
            f"🎨 Palet: {warna} | 💡 Cahaya: {pencahayaan.split(' / ')[0]} | "
            f"🎯 Fungsi: {fungsi_utama.split(' / ')[0]}"
        )
        st.success("✅ Berkas berhasil diproses! Silakan klik tombol unduh di bawah ini.")

# 2. SATU TOMBOL UNDUH SERBAGUNA (Otomatis berubah nama & tipe file mengikuti dropdown)
if 'file_siap_unduh' in st.session_state:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    # Menyesuaikan label teks pada tombol secara dinamis
    label_tombol = "📥 DOWNLOAD LAPORAN (PDF)" if "pdf" in st.session_state['mime_file_unduh'] else "📥 DOWNLOAD SPREADSHEET EXCEL)"
    
    st.download_button(
        label=label_tombol,
        data=st.session_state['file_siap_unduh'],
        file_name=st.session_state['nama_file_unduh'],
        mime=st.session_state['mime_file_unduh'],
        use_container_width=True,
        key="dl_serbaguna"
    )

# =========================================================================
# ========== 8. ARSIP & LOG HISTORI PERHITUNGAN ===========================
# =========================================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("### 📜 Log History")

# 1. RENDER RIWAYAT (Jika ada data histori)
if st.session_state.riwayat:
    for i, item in enumerate(st.session_state.riwayat):
        st.markdown(f"""
            <div style='background-color: white; padding: 10px 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 8px; font-family: "Segoe UI", sans-serif; font-size: 14px;'>
                <strong>Arsip #{i+1}:</strong> {item}
            </div>
        """, unsafe_allow_html=True)
else:
    # Teks info ini dipindahkan ke sini agar HANYA muncul jika riwayat benar-benar kosong
    st.info("Belum ada rekam jejak perhitungan proyek yang tersimpan pada sesi ini.")

# Memberi jarak halus sebelum tombol di paling bawah
st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# 2. STRUKTUR TOMBOL BERSEBELAHAN DI PALING BAWAH
# Membagi baris menjadi 2 kolom sama rata (1:1) secara bersih tanpa tumpang tindih
col_bawah_1, col_bawah_2 = st.columns(2)

with col_bawah_1:
    # Tombol Reset Dashboard di sebelah kiri
    if st.button("🔁 RESET DASHBOARD DATA", type="secondary", use_container_width=True, key="btn_reset"):
        if 'pdf_siap_unduh' in st.session_state: 
            del st.session_state['pdf_siap_unduh']
        reset_form()
        st.rerun()

with col_bawah_2:
    # Tombol Delete History di sebelah kanan
    if st.button("🗑️ DELETE HISTORY", type="secondary", use_container_width=True, key="hapus_riwayat"):
        st.session_state.riwayat = []
        st.rerun()








            
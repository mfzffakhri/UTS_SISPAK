import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
# Data CF dari pakar
cf_pakar = {
    'P1': {'G1': 0.8, 'G2': 0.2, 'G3': 0.8, 'G4': 0.6, 'G7': 0.4, 'G12': 0.2, 'G13': 0.8, 'G16': 0.2},
    'P2': {'G1': 0.8, 'G2': 0.8, 'G3': 0.4, 'G4': 0.8, 'G5': 0.6, 'G6': 0.4, 'G8': 0.8, 'G12': 0.6, 'G13': 0.4, 'G16': 0.4},
    'P3': {'G2': 0.4, 'G4': 0.4, 'G5': 0.4, 'G6': 0.8, 'G7': 0.4, 'G9': 0.8, 'G13': 0.8, 'G16': 0.4, 'G17': 0.4},
    'P4': {'G4': 0.8, 'G5': 0.6, 'G7': 0.8, 'G11': 0.2, 'G12': 0.8, 'G13': 0.8, 'G16': 0.6, 'G17': 0.8},
    'P5': {'G1': 0.6, 'G2': 0.8, 'G3': 0.6, 'G4': 0.8, 'G6': 0.4, 'G7': 0.4, 'G8': 0.6, 'G9': 0.6},
    'P6': {'G1': 0.6, 'G5': 0.6, 'G6': 0.8, 'G7': 0.6, 'G9': 0.4, 'G10': 0.8, 'G13': 0.4, 'G14': 0.4},
    'P7': {'G3': 0.6, 'G4': 0.4, 'G12': 0.8, 'G15': 0.4, 'G16': 0.4, 'G17': 0.4},
    'P8': {'G1': 0.8, 'G4': 0.8, 'G7': 0.8, 'G11': 0.2, 'G12': 0.6, 'G16': 0.2, 'G17': 0.8}
}

gejala_per_penyakit = {
    'P1': ['G1', 'G3', 'G4', 'G7', 'G12', 'G13', 'G16'],
    'P2': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G8', 'G12', 'G13', 'G16'],
    'P3': ['G2', 'G4', 'G5', 'G6', 'G7', 'G9', 'G13', 'G16', 'G17'],
    'P4': ['G4', 'G5', 'G7', 'G11', 'G12', 'G13', 'G16', 'G17'],
    'P5': ['G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'G9'],
    'P6': ['G1', 'G5', 'G6', 'G7', 'G9', 'G10', 'G13', 'G14'],
    'P7': ['G3', 'G4', 'G12', 'G15', 'G16', 'G17'],
    'P8': ['G1', 'G4', 'G7', 'G11', 'G12', 'G16', 'G17']
}

nama_penyakit = {
    'P1': 'Gastritis',
    'P2': 'Gastric',
    'P3': 'Gastric',
    'P4': 'Tumor Benign Gastric',
    'P5': 'Dyspepsia',
    'P6': 'GERD',
    'P7': 'Gastroperesis',
    'P8': 'Gastronteritis'
}

# Fungsi untuk menghitung certainty factor gabungan
def combine_cf(cf1, cf2):
    return cf1 + cf2 - (cf1 * cf2)

# Halaman Login
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login/Register')
        
        # Layout utama
        layout = QVBoxLayout()

        self.label = QLabel("Login or Register", self)
        layout.addWidget(self.label)
        
        # Input untuk username
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # Input untuk password
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Tombol Login
        login_btn = QPushButton('Login', self)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        # Tombol Register
        register_btn = QPushButton('Register', self)
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
    
    # Fungsi Login
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.check_credentials(username, password):
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.open_main_menu()  # Buka halaman utama
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials!')
    
    # Fungsi Register
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.username_exists(username):
            QMessageBox.warning(self, 'Error', 'Username already exists!')
        else:
            self.save_user(username, password)
            QMessageBox.information(self, 'Success', 'Registration successful!')
    
    # Mengecek apakah username sudah terdaftar
    def username_exists(self, username):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    saved_username, _ = line.strip().split(',')
                    if saved_username == username:
                        return True
        return False

    # Menyimpan user baru ke file
    def save_user(self, username, password):
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")

    # Mengecek kredensial login
    def check_credentials(self, username, password):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    saved_username, saved_password = line.strip().split(',')
                    if saved_username == username and saved_password == password:
                        return True
        return False

    # Buka halaman utama jika login berhasil
    def open_main_menu(self):
        self.main_menu = MyApp()
        self.main_menu.show()
        self.close()

# Kelas GUI untuk input dan diagnosis
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.login_window = login_window  # Simpan referensi ke halaman login

        # Peta antara deskripsi dan nilai numerik
        self.value_map = {
            "": 0.0,
            "Tidak yakin sama sekali": 0.0,
            "Tidak sepertinya": 0.3,
            "Setengah yakin": 0.5,
            "Sepertinya iya": 0.8,
            "Sangat yakin": 1.0
        }

        # List untuk menyimpan combo boxes
        self.comboboxes = []
        self.numbers = []  # Inisialisasi array (list) untuk menyimpan angka

        # Deskripsi kondisi gejala
        self.condition_descriptions = [
            "Perut terasa kembung", "Mengalami nyeri pada ulu hati", "Mudah kenyang", "Mual dan muntah",
            "Timbulnya pendarahan di lambung", "Sering sendawa", "Rasa sakit atau tidak nyaman di perut bagian atas",
            "Rasa panas di dada dan perut", "Gas asam keluar dari mulut", "Rasa sakit dan tidak nyaman saat menelan",
            "Sakit kepala dan demam", "Nyeri di dada", "Masalah pencernaan dan perubahan feses", "Sering batuk",
            "Gula darah rendah", "Nafsu makan rendah dan penurunan berat badan", "Mudah lelah"
        ]

        # Inisialisasi UI
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Membuat 17 combo boxes dengan label di samping
        for i in range(17):
            # Membuat layout horizontal untuk label dan combo box
            h_layout = QHBoxLayout()

            # Menambahkan label untuk kondisi
            label = QLabel(f"{i + 1}. {self.condition_descriptions[i]}")
            h_layout.addWidget(label)  # Menambahkan label ke layout horizontal

            # Membuat combo box
            combobox = QComboBox(self)
            combobox.addItems(list(self.value_map.keys()))  # Menambahkan deskripsi ke combo box
            self.comboboxes.append(combobox)  # Menambahkan combo box ke dalam list
            h_layout.addWidget(combobox)  # Menambahkan combo box ke layout horizontal

            # Menambahkan layout horizontal ke layout utama
            layout.addLayout(h_layout)

        # Membuat tombol "Save"
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.on_save)

        # Membuat tombol "Reset"
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.on_reset)

        # Label untuk menampilkan hasil
        self.label = QLabel(self)

        # Menambahkan tombol dan label ke layout
        layout.addWidget(self.save_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.label)

        # Tombol Logout
        logout_btn = QPushButton('Logout', self)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        # Mengatur layout
        self.setLayout(layout)
        
        # Mengatur window
        self.setWindowTitle('Descriptive Input with Multiple QComboBoxes')
        self.show()

    # Fungsi logout, kembali ke halaman login
    def logout(self):
        self.close()  # Tutup main menu
        self.login_window.show()  # Kembali ke halaman login

    def on_save(self):
        # Mendapatkan nilai dari semua combo boxes
        user_cf = {}
        for i, combobox in enumerate(self.comboboxes):
            selected_text = combobox.currentText()
            gejala = f"G{i+1}"  # Gejala dari G1 hingga G17
            if selected_text in self.value_map:
                user_cf[gejala] = self.value_map[selected_text]

        # Hitung CF berdasarkan input user
        hasil_cf = self.hitung_cf(user_cf)

        # Menampilkan hasil diagnosis
        hasil_str = "\nHasil diagnosis:\n"
        highest_cf = 0
        most_likely_disease = ""

        for penyakit, cf_value in hasil_cf.items():
            nama = nama_penyakit.get(penyakit, penyakit)  # Dapatkan nama penyakit atau default ke kode
            hasil_str += f"{nama}: Certainty Factor = {cf_value:.2f}\n"
            # Menyimpan penyakit dengan CF terbesar
            if cf_value > highest_cf:
                highest_cf = cf_value
                most_likely_disease = nama

        self.label.setText(hasil_str)
        
        # Menampilkan kesimpulan penyakit yang paling berpotensi
        if most_likely_disease:
            kesimpulan = f"\nKesimpulan: Penyakit yang paling berpotensi adalah {most_likely_disease} dengan CF = {highest_cf:.2f}"
            self.label.setText(hasil_str + kesimpulan)
        else:
            self.label.setText(hasil_str + "\nKesimpulan: Tidak ada penyakit yang berpotensi.")

    def on_reset(self):
        # Reset nilai semua combo boxes ke pilihan pertama (index 0)
        for combobox in self.comboboxes:
            combobox.setCurrentIndex(0)

        # Reset label hasil
        self.label.setText("")

    # Fungsi untuk menghitung CF total untuk setiap penyakit
    def hitung_cf(self, user_cf):
        cf_hasil = {}
        for penyakit, gejala_list in gejala_per_penyakit.items():
            cf_total = 0
            for gejala in gejala_list:
                cf_gejala = cf_pakar[penyakit][gejala] * user_cf.get(gejala, 0)  # Kalikan dengan CF user
                if cf_total == 0:
                    cf_total = cf_gejala
                else:
                    cf_total = combine_cf(cf_total, cf_gejala)
            cf_hasil[penyakit] = cf_total
        return cf_hasil

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = MyApp()
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


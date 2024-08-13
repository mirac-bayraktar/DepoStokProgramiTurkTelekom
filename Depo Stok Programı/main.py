import os
import sys
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
import sqlite3
import pandas as pd
from datetime import datetime
from PyQt5.uic import loadUi

current_dir = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QMainWindow = loadUiType(str(current_dir) + "\depoStok.ui")

id_index = 0
malzeme_cinsi_index = 1
poz_no_index = 2
malzeme_adi_index = 3
makara_no_index = 4
irsaliye_tarihi_index = 5
birim_index = 6
gelen_miktar_index = 7
kullanilan_miktar_index = 8
sevk_miktari_index = 9
kalan_miktar_index = 10
konum_index = 11
aciklama_index = 12

numara = 0

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Depo Stok Programi")         
        self.cmbMalzemeCinsi.currentIndexChanged.connect(self.update_malzeme_combobox)
        self.icon_path = os.path.join(current_dir, "excell.png")
        self.excel_icon = QIcon(self.icon_path)
        self.btnExcel.setIcon(self.excel_icon)
        self.setup_database()
        self.kayit_listele()
        self.load_konum_data()        
        self.a = ""
        self.sevkEkipleri= []
        self.btnMalzemeEkle.clicked.connect(self.kayit_ekle)
        self.btnTumunuListele.clicked.connect(self.kayit_listele)
        self.btnMalzemeSil.clicked.connect(self.kayit_sil)
        self.btnKonumaGoreListele.clicked.connect(self.konuma_gore_listele)
        self.btnMalzemeCinsiListele.clicked.connect(self.malzeme_cinsine_gore_listele)
        self.btnMalzemeListele.clicked.connect(self.malzemeye_gore_listele)
        self.btnExcel.clicked.connect(self.export_to_excel)
        self.btnMakaraSorgula.clicked.connect(self.makara_sorgula)
        self.btnKullanimDetayi.clicked.connect(self.kullanim_detay_penceresi)
        self.btnMalzemeGonder.clicked.connect(self.malzeme_cikart)
        self.btnEkipEkle.clicked.connect(self.ekip_ekle)
        self.btnEkipCikart.clicked.connect(self.ekip_cikart)
        self.btnKonumEkle.clicked.connect(self.konum_ekle)
        self.btnKonumCikart.clicked.connect(self.konum_cikart)
        self.btnGuncelle.clicked.connect(self.sayim_ekle)

       
    def show_warning_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Uyarı")
        msg.exec_()    

    def temizle(self):
        self.lneAciklama.clear()
        self.lneCikanMiktar.clear()
        self.lneCikisTarihi.clear()
        self.lneGelenMiktar.clear()
        self.lneIrsaliyeNo.clear()
        self.lneIrsaliyeTarihi.clear()
        self.lneMakaraNo.clear()
        self.lneProjeNo.clear()
        self.lneCikanMiktar.clear()
        self.lneCikisTarihi.clear()
        self.lneKrokiNo.clear()
        self.lneEklenecekKonum.clear()
        self.lneEklenecekEkip.clear()

    def setup_database(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()

        # stok tablosunu oluştur
        self.islem.execute("""
            CREATE TABLE IF NOT EXISTS stok (
                id INTEGER PRIMARY KEY,
                malzemeCinsi TEXT,
                pozNo TEXT,
                malzemeAdi TEXT,
                irsaliyeTarihi TEXT,
                makaraNo TEXT,
                birim TEXT,
                gelenMiktar INTEGER,
                kullanilanMiktar INTEGER,
                sevkMiktari INTEGER,
                kalanMiktar INTEGER,
                konum TEXT,
                aciklama TEXT,
                sayim INTEGER
            )
        """)
        
        self.baglanti.commit()
        
        self.islem.execute("""CREATE TABLE IF NOT EXISTS ekipler (ekipAdi TEXT, sevkEkibi INTEGER)""")
        self.baglanti.commit()
        self.islem.execute("""CREATE TABLE IF NOT EXISTS konumlar (konumAdi TEXT)""")
        self.baglanti.commit()
        
    def update_malzeme_combobox(self, index):
        self.cmbMalzeme.clear()
        if index == 0:
            self.cmbMalzeme.addItems(['FO-H 4', 'FO-H 6', 'FO-H 12', 'FO-H 24', 'FO-H 36', 'FO-H 48', 'FO-Y 4', 'FO-Y 6', 'FO-Y 12', 'FO-Y 24', 'FO-Y 36', 'FO-Y 48', 'FO-Y 60', 'FO-Y 72', 'FO-Y 96', 'FO-Y 144', 'FO-Y 192', 'FO-Y 288', 'FO-NM 4', 'FO-NM 6', 'FO-NM 12', 'FO-NM 24', 'FO-NM 36', 'FO-NM 48', 'FO-NM 60', 'FO-NM 72', 'FO-NM 96', 'FO-M 6', 'FO-M 12', 'FO-M 24', 'FO-M 36', 'FO-M 48', 'FO-M 60', 'FO-M 72', 'FO-M 96', 'FO-M 144', 'FO-M 192', 'FO-M 288'])
        elif index == 1:
            self.cmbMalzeme.addItems(['KPDF-APA 20-0.4', 'KPDF-APA 30-0.4', 'KPDF-APA 50-0.4', 'KPDF-APA 100-0.4', 'KPDF-APA 150-0.4', 'KPDF-APA 200-0.4', 'KPDF-APA 6-0.5', 'KPDF-APA 10-0.5', 'KPDF-APA 20-0.5', 'KPDF-APA 30-0.5', 'KPDF-APA 50-0.5', 'KPDF-APA 100-0.5', 'KPDF-APA 150-0.5', 'KPDF-APA 200-0.5', 'KPDF-APA 20-0.6', 'KPDF-APA 30-0.6', 'KPDF-APA 50-0.6', 'KPDF-APA 100-0.6', 'KPDF-APA 150-0.6', 'KPDF-APA 200-0.6', 'KPDF-APA 6-0.9', 'KPDF-APA 10-0.9', 'KPDF-APA 20-0.9', 'KPDF-APA 30-0.9', 'KPDF-APA 50-0.9', 'KPDF-APA 100-0.9', 'KPDF-AP 20-0.4', 'KPDF-AP 30-0.4', 'KPDF-AP 50-0.4', 'KPDF-AP 100-0.4', 'KPDF-AP 150-0.4', 'KPDF-AP 200-0.4', 'KPDF-AP 300-0.4', 'KPDF-AP 400-0.4', 'KPDF-AP 20-0.5', 'KPDF-AP 30-0.5', 'KPDF-AP 50-0.5', 'KPDF-AP 100-0.5', 'KPDF-AP 150-0.5', 'KPDF-AP 200-0.5', 'KPDF-AP 300-0.5', 'KPDF-AP 400-0.5', 'KPDF-AP 20-0.6', 'KPDF-AP 30-0.6', 'KPDF-AP 50-0.6', 'KPDF-AP 100-0.6', 'KPDF-AP 150-0.6', 'KPDF-AP 200-0.6', 'KPDF-AP 300-0.6', 'KPDF-AP 20-0.9', 'KPDF-AP 30-0.9', 'KPDF-AP 50-0.9', 'KPDF-AP 100-0.9', 'KPDF-AP 150-0.9', 'KPDF-AP 200-0.9', 'KPDF-AP 300-0.9', 'KPD-PAP 600-0.4', 'KPD-PAP 900-0.4', 'KPD-PAP 1200-0.4', 'KPD-PAP 1500-0.4', 'KPD-PAP 1800-0.4', 'KPD-PAP 600-0.5', 'KPD-PAP 900-0.5', 'KPD-PAP 1200-0.5', 'KPDF-PAP 600-0.4', 'KPDF-PAP 900-0.4', 'KPDF-PAP 1200-0.4', 'KPDF-PAP 1500-0.4', 'KPDF-PAP 1800-0.4', 'KPDF-PAP 600-0.5', 'KPDF-PAP 900-0.5', 'KPDF-PAP 1200-0.5', 'KPD-P-A 2-0.5', 'KPD-P-A 4-0.5', 'KPD-P-A 6-0.5', 'KPD-P-A 10-0.5', '(K)PDF-AP 200-05 KABLO (250m)', '(K)PDF-AP 150-05 KABLO (250m)', '(K)PDF-AP 100-05 KABLO (250m)', '(K)PDF-AP 50-05 KABLO (500m)', '(K)PDF-AP 30-05 KABLO (500m)', '(K)PDF-AP 20-05 KABLO (500m)', '(K)PDF-APA 200-05 KABLO (250m)', '(K)PDF-APA 150-05 KABLO (250m)', '(K)PDF-APA 100-05 KABLO (250m)', '(K)PDF-APA 50-05 KABLO (500m)', '(K)PDF-APA 30-05 KABLO (500m)', '(K)PDF-APA 20-05 KABLO (500m)', 'PD-P-A (KPD-PA) 10-05 KABLO (500m)', 'PD-P-A (KPD-PA) 6-05 KABLO (500m)', 'PD-P-A (KPD-PA) 4-05 KABLO (500m)', 'PD-P-A (KPD-PA) 2-05 KABLO (250m)'])
        elif index == 2:
            self.cmbMalzeme.addItems(['Çift cidarlı HDPE boru (110)', 'Çift cidarlı HDPE boru için birleştirme manşonu (110)', 'Çift cidarlı HDPE boru (90)', 'Çift cidarlı HDPE boru için birleştirme manşonu (90)', 'Çift cidarlı HDPE Boru (75)', 'Çift cidarlı HDPE boru için birleştirme manşonu (75)', 'Çift cidarlı HDPE Boru (50)', 'Çift cidarlı HDPE boru için birleştirme manşonu (50)', '1x1 HDPE boru', '2x1 HDPE boru', '3x1 HDPE boru', 'HDPE ikili göz çoklayıcı boru (Tıkama parçası dahil)', 'HDPE üçlü göz çokl. boru (Tıkama parç. ve kanal ağzı tut. dahil)', 'Çift cidarlı HDPE boru için HDPE tamir manşonu', 'Çift cidarlı HDPE boru için PVC parçalı tamir manşonu(iki parça)', 'Çift cidarlı HDPE boru için HDPE boru adaptörü', 'Çift cidarlı HDPE boru için HDPE boru tıpası', "Çift cidarlı HDPE boru için PVC boru destekleri(2' li)", 'Mikroboru 1 Gözlü', 'Mikroboru 2 Gözlü', 'Mikroboru 4 Gözlü', 'Mikroboru 7 Gözlü', 'Tip-1 Prefabrik beton menhol', 'Tip-2 Prefabrik beton ek odası', 'Kompozit Ek Odası Kapağı', 'Kompozit Ek Odası Çerçevesi', 'Kompozit Menhol Kapağı', 'Kompozit Menhol Çerçevesi', 'Kompozit Ek Odası Yükseltme Halkası', 'Kompozit Menhol Yükseltme Halkası', 'Ek Odası H41 (Kompozit)', 'Ek Odası H65 (Kompozit)', 'Ek Odası H75 (Kompozit)', 'Ek Odası Kapağı H65-H41 (Kompozit)', 'Ek Odası Kapağı H75 (Kompozit)', 'Ek Odası Çerçevesi H65-H41 (Kompozit)', 'Ek Odası Ara Yükseltme Çerçevesi H75 (Kompozit)', 'Ek Odası Ara Yükseltme Çerçevesi H65-H41 (Kompozit)', 'Ek Odası Çerçevesi H75 (Kompozit)', 'Prefabrik menhol yükseltme parçası', 'FTTx küçük tip kabin (Tip 7, 11, 13, 15 ve 23) beton kaidesi', 'Andezit Parke', 'Granit Parke', 'Bazalt Parke', 'Beton Parke', 'Mermer', 'Granit', 'Beton Bordür', 'Karosiman', 'C20/25 beton', "Rak pabucu (25'lik ve 50'lik)", 'Tıkama malzemesi (protolin)', 'Menhol kanalı tıkama malzemesi (Dolu göz için)', 'Menhol kanalı tıkama malzemesi (Boş göz için, mekanik tip)'])
        elif index == 3:
            self.cmbMalzeme.addItems(['F/O Ek Kutusu (3 Kasetli)', 'F/O Ek Kutusu (6 Kasetli)', 'F/O Ek Kutusu (12 Kasetli)', 'F/O Ek Kutusu (16 Kasetli)', 'F/O Ek Kutusu (3 Kasetli) Tip 2', 'OB 1x2', 'OB 1X4', 'OB 1X8', 'OB 1X2 SC', 'OB 1X4 SC', 'OB 1X8 SC', 'OB 1X16 SC', 'OB 1X32 SC', 'OFDK-M 1X8', 'OFDK-M 1X16', 'OFDK-M 1X32', 'OFDP 1X2', 'OFDP 1X4', 'OFDP 1X8', 'OFDP 1X16', 'OFDP 1X32', 'OFDÇ 12U ', 'OFDÇ 24U ', 'OFDÇ 42U ', 'OFSB-12', 'OFSB-24', 'OFSB-72', 'OFSD 24U', 'OFSD 24U Çelik', 'OFSD 12U', 'OFSK-P 1x1', '1x2 OBK (Outdoor + Zırhlı)', '1x2 OBK (Çelik + askı tel)', '1x2 OBK (FRP + askı tel)', '1x1 OBK (400N)', '1x1 OBK (outdoor)', 'Riser Kablo (2*6)', 'Riser Kablo (2*12)', 'Riser Kablo (2*24)', 'Riser Kablo (2*48)', 'Riser Kablo Yönlendirme kutusu', 'OFSK-P 1x2', 'OFSK-P 1x4', 'OFDK-P 1X4', 'OFDK-P 1X8', 'OFDK-P 1X16', 'OFDK-P 1X32', 'OFDK-P 1X8 K', 'OFDK-P Askı Aparatı', 'Harici OFDK-P', 'Harici OFDK Bağlantı Aparatı', 'T25', 'FAOC Kutusu', 'TK-OBF SC 2 m', '1x24 TK-OBK SC 5 m', '1x24 TK-OBK SC 10 m', '1x24 TK-OBK SC 20 m', '1x1 K-OBK SC-SC 1 m', '1x1 K-OBK SC-SC 2 m', '1x1 K-OBK SC-SC 3 m', '1x1 K-OBK SC-SC 5 m', '1x1 K-OBK SC-SC 10 m', '1x1 K-OBK SC-SC 20 m', '1x1 K-OBK SC-SC 30 m', '1x1 K-OBK SC-SC 40 m', '1x1 K-OBK SC-SC 50 m', '1x1 K-OBK LC-LC 1 m', '1x1 K-OBK LC-LC 2 m', '1x1 K-OBK LC-LC 3 m', '1x1 K-OBK LC-LC 5 m', '1x1 K-OBK LC-LC 10 m', '1x1 K-OBK LC-LC 20 m', '1x1 K-OBK LC-LC 30 m', '1x1 K-OBK LC-LC 40 m', '1x1 K-OBK LC-LC 50 m', '1x1 K-OBK SC-LC 1 m', '1x1 K-OBK SC-LC 2 m', '1x1 K-OBK SC-LC 3 m', '1x1 K-OBK SC-LC 5 m', '1x1 K-OBK SC-LC 10 m', '1x1 K-OBK SC-LC 20 m', '1x1 K-OBK SC-LC 30 m', '1x1 K-OBK SC-LC 40 m', '1x1 K-OBK SC-LC 50 m', '1x1 K-OBK SC-A/SC 1 m', '1x1 K-OBK SC-A/SC 2 m', '1x1 K-OBK SC-A/SC 3 m', '1x1 K-OBK SC-A/SC 5 m', '1x1 K-OBK SC-A/SC 10 m', '1x1 K-OBK SC-A/SC 20 m', '1x1 K-OBK SC-A/SC 30 m', '1x1 K-OBK SC-A/SC 40 m', '1x1 K-OBK SC-A/SC 50 m', '1x2 K-OBK SC-SC 1 m', '1x2 K-OBK SC-SC 2 m', '1x2 K-OBK SC-SC 3 m', '1x2 K-OBK SC-SC 5 m', '1x2 K-OBK SC-SC 10 m', '1x2 K-OBK SC-SC 20 m', '1x2 K-OBK SC-SC 30 m', '1x2 K-OBK SC-SC 40 m', '1x2 K-OBK SC-SC 50 m', '1x2 K-OBK LC-LC 1 m', '1x2 K-OBK LC-LC 2 m', '1x2 K-OBK LC-LC 3 m', '1x2 K-OBK LC-LC 5 m', '1x2 K-OBK LC-LC 10 m', '1x2 K-OBK LC-LC 20 m', '1x2 K-OBK LC-LC 30 m', '1x2 K-OBK LC-LC 40 m', '1x2 K-OBK LC-LC 50 m', '1x2 K-OBK SC-LC 1 m', '1x2 K-OBK SC-LC 2 m', '1x2 K-OBK SC-LC 3 m', '1x2 K-OBK SC-LC 5 m', '1x2 K-OBK SC-LC 10 m', '1x2 K-OBK SC-LC 20 m', '1x2 K-OBK SC-LC 30 m', '1x2 K-OBK SC-LC 40 m', '1x2 K-OBK SC-LC 50 m', '1x12 K-OBK SC-SC 5 m', '1x12 K-OBK SC-SC 10 m', '1x12 K-OBK SC-SC 15 m', '1x12 K-OBK SC-SC 20 m', '1x12 K-OBK SC-SC 25 m', '1x12 K-OBK SC-SC 30 m', '1x12 K-OBK SC-SC 35 m', '1x12 K-OBK SC-SC 40 m', '1x12 K-OBK SC-SC 45 m', '1x12 K-OBK SC-SC 50 m', '1x12 K-OBK LC-LC 5 m', '1x12 K-OBK LC-LC 10 m', '1x12 K-OBK LC-LC 15 m', '1x12 K-OBK LC-LC 20 m', '1x12 K-OBK LC-LC 25 m', '1x12 K-OBK LC-LC 30 m', '1x12 K-OBK LC-LC 35 m', '1x12 K-OBK LC-LC 40 m', '1x12 K-OBK LC-LC 45 m', '1x12 K-OBK LC-LC 50 m', '1x12 K-OBK SC-LC 5 m', '1x12 K-OBK SC-LC 10 m', '1x12 K-OBK SC-LC 15 m', '1x12 K-OBK SC-LC 20 m', '1x12 K-OBK SC-LC 25 m', '1x12 K-OBK SC-LC 30 m', '1x12 K-OBK SC-LC 35 m', '1x12 K-OBK SC-LC 40 m', '1x12 K-OBK SC-LC 45 m', '1x12 K-OBK SC-LC 50 m', '1x24 K-OBK SC-SC 5 m', '1x24 K-OBK SC-SC 10 m', '1x24 K-OBK SC-SC 15 m', '1x24 K-OBK SC-SC 20 m', '1x24 K-OBK SC-SC 25 m', '1x24 K-OBK SC-SC 30 m', '1x24 K-OBK SC-SC 35 m', '1x24 K-OBK SC-SC 40 m', '1x24 K-OBK SC-SC 45 m', '1x24 K-OBK SC-SC 50 m', '1x24 K-OBK SC-SC 60 m', '1x24 K-OBK SC-SC 70 m', '1x24 K-OBK SC-SC 80 m', '1x24 K-OBK SC-SC 90 m', '1x24 K-OBK SC-SC 100 m', '1x24 K-OBK SC-SC 150 m', '1x24 K-OBK LC-LC 5 m', '1x24 K-OBK LC-LC 10 m', '1x24 K-OBK LC-LC 15 m', '1x24 K-OBK LC-LC 20 m', '1x24 K-OBK LC-LC 25 m', '1x24 K-OBK LC-LC 30 m', '1x24 K-OBK LC-LC 35 m', '1x24 K-OBK LC-LC 40 m', '1x24 K-OBK LC-LC 45 m', '1x24 K-OBK LC-LC 50 m', '1x24 K-OBK SC-LC 5 m', '1x24 K-OBK SC-LC 10 m', '1x24 K-OBK SC-LC 15 m', '1x24 K-OBK SC-LC 20 m', '1x24 K-OBK SC-LC 25 m', '1x24 K-OBK SC-LC 30 m', '1x24 K-OBK SC-LC 35 m', '1x24 K-OBK SC-LC 40 m', '1x24 K-OBK SC-LC 45 m', '1x24 K-OBK SC-LC 50 m', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 0,6 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 1 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 3 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 5 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 7 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 10 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 15 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 20 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 30 M', 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 40 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 0,6 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 1 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 3 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 5 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 7 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 10 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 15 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 20 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 25 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 30 M', 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 40 M', 'PATCHCORD FC/UPC-SC/UPC DUBLEX 12 M', 'PATCHCORD FC/UPC-LC/UPC DUBLEX 5 M', 'PATCHCORD FC/UPC-LC/UPC DUBLEX 10 M', 'PATCHCORD FC/UPC-LC/UPC DUBLEX 15 M', 'PATCHCORD FC/UPC-LC/UPC DUBLEX 20 M', 'PATCHCORD FC/UPC-LC/UPC DUBLEX 25 M', 'PATCHCORD FC/UPC-MU/UPC SIMPLEX 0,6 M', 'PATCHCORD FC/UPC-MU/UPC SIMPLEX 3 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 0,3 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 0,6 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 7 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 8 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 13 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 15 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 17 M', 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 25 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 6 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 7 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 9 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 12 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 15 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 18 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 22 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 25 M', 'PATCHCORD SC/UPC-SC/UPC DUBLEX 28 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 0,6 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 3 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 5 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 7 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 10 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 15 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 20 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 25 M', 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 30 M', 'PATCHCORD SC/UPC-MU/UPC DUBLEX 10 M', 'PATCHCORD SC/UPC-MU/UPC DUBLEX 15 M', 'PATCHCORD SC/UPC-MU/UPC DUBLEX 20 M', 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 5 M', 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 10 M', 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 15 M', 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 20 M', 'PATCHCORD SC/UPC-E2000/UPC SIMPLEX 5 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 1 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 3 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 5 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 7 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 10 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 15 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 20 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 25 M', 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 30 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 0,6 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 7 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 8 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 12 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 15 M', 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 25 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 4 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 6 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 7 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 8 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 9 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 10,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 11M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 11,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 12 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 12,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 13 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 13,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 14 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 14,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 15 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 15,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 16 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 16,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 17 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 17,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 18 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 18,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 19 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 19,5 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 21 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 22 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 25 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 28 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 33 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 35 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 38 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 45 M', 'PATCHCORD LC/UPC-SC/UPC DUBLEX 55 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,3 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,5 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,6 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 1,2 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 7 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 8 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 12 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 15 M', 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 25 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,15 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,20 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,30 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 7 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 8 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 12 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 13 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 14 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 15 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 16 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 17 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 18 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 23 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 25 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 28 M', 'PATCHCORD LC/UPC-LC/UPC DUBLEX 35 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 1 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 3 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 7 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 10 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 15 M', 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 20 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 0,3 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 0,6 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 1 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 3 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 5 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 7 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 10 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 15 M', 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 20 M', 'PATCHCORD MU/UPC-MU/UPC DUBLEX 0,6 M', 'PATCHCORD ST/UPC-LC/UPC DUBLEX 5 M', 'PATCHCORD ST/UPC-LC/UPC DUBLEX 10 M', 'PATCHCORD ST/UPC-LC/UPC DUBLEX 20 M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 10M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 15M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 20M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 25M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 30M', 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 40M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 10M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 15M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 20M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 25M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 30M', 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 40M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 10M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 15M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 20M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 25M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 30M', 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 40M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 10M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 15M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 20M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 25M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 30M', 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 40M', 'Z-OABK SC-SC 0,6m 3dB', 'Z-OABK SC-SC 0,6m 5dB', 'Z-OABK SC-SC 0,6m 10dB', 'Z-OABK LC-LC 0,6m 3dB', 'Z-OABK LC-LC 0,6m 5dB', 'Z-OABK LC-LC 0,6m 10dB', 'Z-OABK MU-MU 0,6m 3dB', 'Z-OABK MU-MU 0,6m 5dB', 'Z-OABK MU-MU 0,6m 10dB', 'U-LINK SIMPLEX FC UPC/SC UPC', 'U-LINK SIMPLEX FC UPC/LC UPC', 'U-LINK SIMPLEX MU UPC/MU UPC', 'U-LINK SIMPLEX LC UPC/SC UPC', 'U-LINK SIMPLEX LC UPC/LC UPC', 'U-LINK DUBLEX LC UPC/LC UPC', 'U-LINK SIMPLEX FC UPC/FC UPC', 'U-LINK SIMPLEX SC UPC/SC UPC', 'U-LINK SIMPLEX E-2000 APC / E-2000 APC', 'U-LINK SIMPLEX E-2000 UPC / E-2000 UPC', 'ZAYIFLATICI SC PLUG-IN TİPİ 5 dB', 'ZAYIFLATICI SC PLUG-IN TİPİ 3 dB', 'ZAYIFLATICI SC PLUG-IN TİPİ 7 dB', 'ZAYIFLATICI SC PLUG-IN TİPİ 10 dB', 'ZAYIFLATICI SC PLUG-IN TİPİ 15dB', 'ZAYIFLATICI LC PLUG-IN TİPİ 3 dB', 'ZAYIFLATICI LC PLUG-IN TİPİ 5 dB', 'ZAYIFLATICI LC PLUG-IN TİPİ 7 dB', 'ZAYIFLATICI LC PLUG-IN TİPİ 10 dB', 'ZAYIFLATICI LC PLUG-IN TİPİ 15 dB', 'ZAYIFLATICI FC PLUG-IN TİPİ 3 dB', 'ZAYIFLATICI FC PLUG-IN TİPİ 5 dB', 'ZAYIFLATICI FC PLUG-IN TİPİ 7dB', 'ZAYIFLATICI FC PLUG-IN TİPİ 10 dB', 'ZAYIFLATICI MU PLUG-IN TİPİ 3 dB', 'ZAYIFLATICI MU PLUG-IN TİPİ 5 dB', 'ZAYIFLATICI MU PLUG-IN TİPİ 7 dB', 'ZAYIFLATICI MU PLUG-IN TİPİ 10 dB', 'ZAYIFLATICI MU PLUG-IN TİPİ 15 dB', '1x24 TK-OBK SC 2 m', '1x24 TK-OBK SC 3 m', '1x32 TK-OBK SC 10 m', '1x1 K-OBK SC-A/LC 3 M', '1x16 K-OBK SC-SC 5 m', '1x16 K-OBK SC-SC 10 m', '1x16 K-OBK SC-SC 20 m', '1x32 K-OBK SC-SC 5 m', '1x32 K-OBK SC-SC 10 m', '1x32 K-OBK SC-SC 20 m'])
        elif index == 4:
            self.cmbMalzeme.addItems(['Ağaç telefon direği (7 Mt)', 'Ağaç telefon direği (8 Mt)', 'Ağaç telefon direği (9 Mt)', '10 luk kesmeli modül ', '10 luk kesmesiz modül ', 'BEKT A', 'BEKT B', 'BEKT C', 'Çatal ek kiti', 'Topraklama kiti', 'İzoleli Çelik spiral boru 9 mm', 'İzoleli Çelik spiral boru 11 mm', 'İzoleli Çelik spiral boru 14 mm', 'İzoleli Çelik spiral boru 16 mm', 'İzoleli Çelik spiral boru 18 mm', 'İzoleli Çelik spiral boru 26 mm', 'İzoleli Çelik spiral boru 29 mm', 'İzoleli Çelik spiral boru 32 mm', 'İzoleli Çelik spiral boru 37 mm', 'İzoleli Çelik spiral boru 42 mm', 'İzoleli Çelik spiral boru 50 mm', 'İzoleli Çelik spiral boru 63 mm', 'Galvanizli boru 1/2"', 'Galvanizli boru 3/4"', 'Galvanizli boru 1"', 'Galvanizli boru 1 1/4"', 'Galvanizli boru 1 1/2"', 'Galvanizli boru 2"', 'Galvanizli boru 2 1/2"', 'Galvanizli boru 3"', 'Galvanizli boru 4"', 'Çelik spiral boru 9 mm', 'Çelik spiral boru 11 mm', 'Çelik spiral boru 14 mm', 'Çelik spiral boru 16 mm', 'Çelik spiral boru 18 mm', 'Çelik spiral boru 21 mm', 'Çelik spiral boru 26 mm', 'Çelik spiral boru 29 mm', 'Çelik spiral boru 32 mm', 'Çelik spiral boru 37 mm', 'Çelik spiral boru 42 mm', 'Çelik spiral boru 50 mm', 'Çelik spiral boru 63 mm', 'Plastik spiral boru 14 mm', 'Plastik spiral boru 16 mm', 'Plastik spiral boru 18 mm', 'Plastik spiral boru 20 mm', 'Plastik spiral boru 26 mm', 'Plastik spiral boru 32 mm', 'Plastik spiral boru 40 mm', 'Plastik spiral boru 50 mm', 'Halojen free alev yaymaz Plastik spiral boru 16 mm', 'Halojen free alev yaymaz Plastik spiral boru 20 mm', 'Halojen free alev yaymaz Plastik spiral boru 25 mm', 'Halojen free alev yaymaz Plastik spiral boru 32 mm', 'Halojen free alev yaymaz Plastik spiral boru 40 mm', 'Halojen free alev yaymaz Plastik spiral boru 50 mm', '5cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '10cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '20cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '30cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '40cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '50cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '60cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)', '10cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', '20cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', '30cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', '40cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', '50cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', '60cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)', 'Topraklama levhası (0,7x0,7/0,5x1 3mm)', 'Topraklama çubuğu (150cm)', '3 mm lik Bakır Tel', '6 mm2 topraklama iletkeni (NYY)', '10 mm2 topraklama iletkeni (NYY)', '16 mm2 topraklama iletkeni (NYY)', '25 mm2 topraklama iletkeni (NYY)', '50 mm2 topraklama iletkeni (NYY)', '6 mm2 topraklama iletkeni (Çıplak bakır)', '10 mm2 topraklama iletkeni (Çıplak bakır)', '16 mm2 topraklama iletkeni (Çıplak bakır)', '25 mm2 topraklama iletkeni (Çıplak bakır)', '50 mm2 topraklama iletkeni (Çıplak bakır)', '12x12 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '16x16 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '25x16 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '25x25 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '40x25 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '40x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '60x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '60x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '80x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '80x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '100x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '100x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '120x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)', '22,5x45 telefon prizi', '22,5x45 data prizi', '45x45 UPS topraklı priz', '45x45 Topraklı priz', 'UTP CAT6 Sıva Üstü Tekli Priz', 'UTP CAT6 Sıva Üstü İkili Priz', 'UTP CAT6 Sıva Altı Tekli Priz', 'UTP CAT6 Sıva Altı İkili Priz', '3lü Topraklı klemensli grup priz', 'RJ45 konnektör', 'RJ11 konnektör', "Sac pano (0,1 m2'ye kadar, 0,1 dahil)", 'Sac pano (0,1-0,2 m2, 0,2 dahil)', 'Sac pano (0,2-0,3 m2, 0,3 dahil)', '1 Fazlı Nötr Kesmeli Anahtarlı Otomatik Sigorta (40 A.e kadar)', 'Yangın koruma rölesi 2x40A 300mA', 'Yangın koruma rölesi 2x25A 300mA', 'Kaçak akım koruma rölesi 30mA (40 A.e kadar)', '6U dikey kablo düzenleyici (tek taraf)', '9U dikey kablo düzenleyici (tek taraf)', '12U dikey kablo düzenleyici (tek taraf)', '6U 19" kabinet', '9U 19" kabinet', '12U 19" kabinet', 'Sabit raf', 'Hareketli raf', 'Termostatlı fan modülü 2 fanlı', 'Termostatlı fan modülü 4 fanlı', '19" rack tipi 4lü grup priz sigortalı', '19" rack tipi 6lı grup priz sigortalı', '19" rack tipi 8li grup priz sigortalı', 'Saha dolabı 2400 lük (8 adet modül bağlantı sacı dahil)', 'Direk tipi saha dolabı 600 lük ( 2 adet modül bağlantı sacı dahil)', 'BDDK-1 (AKEK) Abone Kablo Ek Kutusu', 'BDDK-3 Bina Dışı Dağıtım kutusu (modülsüz)', 'BİDK-2 Bina İçi Dağıtım kutusu 30-50 lik (modülsüz)', 'BİDK-2 Bina İçi Dağıtım kutusu 100 lük (modülsüz)', '300 çiftlik modül bağlantı çatısı', 'Wifi Projesi SW Kutusu (Outdoor Kabinet)', 'Wifi Projesi Sistem Kutusu (Indoor Kabinet)', 'POE Kutusu (Plastik Kutu)', '10G Main Router', 'PTP AP', 'Outdoor AP', '10G Pole Switch', '10G Main Switch', 'Wifi Spot Loglama Cihazı', '3x120+70 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil) ', '3x70+35 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil)', '4x16 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil)', '4x16 AG reçineli ek mufu (Montaj için gerekli malzemeler dahil) ', 'İstavroz demiri', '3U Kabin', "2400'lük Saha dolabı çatısı", '40x60 FTTB Dağıtım kutusu', '60x80 FTTB Dağıtım kutusu', '4x6 NYY 1KV', '4x10 NYY 1KV', '2x6 NYY 1KV', '2x10 NYY 1KV', '3x2,5 NVV', '3x4 NVV ', '2x6 NVV ', '4x6 NVV ', '4x10 YVOV (NYRY): NYF GBY 1KV', '4x16 YVOV (NYRY): NYF GBY 1KV', 'UTP CAT6 LS0H Patch Cord 0,5m', 'UTP CAT6 LS0H Patch Cord 1m', 'UTP CAT6 LS0H Patch Cord 2m', 'UTP CAT6 LS0H Patch Cord 3m', 'UTP CAT6 LS0H Patch Cord 5m', 'CAT6 20 cm F/UTP', 'CAT6 100 cm F/UTP'])

    def kayit_listele(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(("Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"))

        if not self.cbxSecim.isChecked():
            
            self.sorgu = "select * from stok"
            self.islem.execute(self.sorgu)
        
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        
        else:         
            self.sorgu = "select * from stok where kalanMiktar != 0"
            self.islem.execute(self.sorgu)
            
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
    
    def kayit_ekle(self):
        malzemeCinsi = self.cmbMalzemeCinsi.currentText()
        malzemeAdi = self.cmbMalzeme.currentText()
        irsaliyeNo = str(self.lneIrsaliyeNo.text())
        makaraNo = str(self.lneMakaraNo.text())
        irsaliyeTarihi = str(self.lneIrsaliyeTarihi.text())
        birim = self.cmbBirim.currentText()
        konum = self.cmbKonum.currentText()
        aciklama = self.lneAciklama.text()
        try:
            gelenMiktar = int(self.lneGelenMiktar.text())
        except:
            self.show_warning_message("LUTFEN GELEN MIKTAR'A SAYISAL DEGER GIRINIZ") 
            return           

        proje_Adi= str(self.lneProjeNo.text())
        kullanan_Ekip= self.cmbKullananEkip.currentText()
        kroki_No= str(self.lneKrokiNo.text())
        hakedis_durumu= self.cmbHakedis.currentText()        
        guncellemeTarihi = datetime.now().strftime("%Y-%m-%d")
        
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()  
                      
        if not aciklama:
            aciklama = "-"
        if not makaraNo:
            makaraNo= "-"
        if not kroki_No:
            kroki_No="-"
        if not proje_Adi:
            proje_Adi="-"
            
        self.mapping= {'KPDF-APA 20-0.4': 676, 'KPDF-APA 30-0.4': 677, 'KPDF-APA 50-0.4': 678, 'KPDF-APA 100-0.4': 679, 'KPDF-APA 150-0.4': 680, 
                       'KPDF-APA 200-0.4': 681, 'KPDF-APA 6-0.5': 682, 'KPDF-APA 10-0.5': 683, 'KPDF-APA 20-0.5': 684, 'KPDF-APA 30-0.5': 685, 
                       'KPDF-APA 50-0.5': 686, 'KPDF-APA 100-0.5': 687, 'KPDF-APA 150-0.5': 688, 'KPDF-APA 200-0.5': 689, 'KPDF-APA 20-0.6': 690, 
                       'KPDF-APA 30-0.6': 691, 'KPDF-APA 50-0.6': 692, 'KPDF-APA 100-0.6': 693, 'KPDF-APA 150-0.6': 694, 'KPDF-APA 200-0.6': 695, 
                       'KPDF-APA 6-0.9': 696, 'KPDF-APA 10-0.9': 697, 'KPDF-APA 20-0.9': 698, 'KPDF-APA 30-0.9': 699, 'KPDF-APA 50-0.9': 700, 
                       'KPDF-APA 100-0.9': 701, 'KPDF-AP 20-0.4': 702, 'KPDF-AP 30-0.4': 703, 'KPDF-AP 50-0.4': 704, 'KPDF-AP 100-0.4': 705, 
                       'KPDF-AP 150-0.4': 706, 'KPDF-AP 200-0.4': 707, 'KPDF-AP 300-0.4': 708, 'KPDF-AP 400-0.4': 709, 'KPDF-AP 20-0.5': 710, 
                       'KPDF-AP 30-0.5': 711, 'KPDF-AP 50-0.5': 712, 'KPDF-AP 100-0.5': 713, 'KPDF-AP 150-0.5': 714, 'KPDF-AP 200-0.5': 715, 
                       'KPDF-AP 300-0.5': 716, 'KPDF-AP 400-0.5': 717, 'KPDF-AP 20-0.6': 718, 'KPDF-AP 30-0.6': 719, 'KPDF-AP 50-0.6': 720, 
                       'KPDF-AP 100-0.6': 721, 'KPDF-AP 150-0.6': 722, 'KPDF-AP 200-0.6': 723, 'KPDF-AP 300-0.6': 724, 'KPDF-AP 20-0.9': 725, 
                       'KPDF-AP 30-0.9': 726, 'KPDF-AP 50-0.9': 727, 'KPDF-AP 100-0.9': 728, 'KPDF-AP 150-0.9': 729, 'KPDF-AP 200-0.9': 730, 
                       'KPDF-AP 300-0.9': 731, 'KPD-PAP 600-0.4': 732, 'KPD-PAP 900-0.4': 733, 'KPD-PAP 1200-0.4': 734, 'KPD-PAP 1500-0.4': 735, 
                       'KPD-PAP 1800-0.4': 736, 'KPD-PAP 600-0.5': 737, 'KPD-PAP 900-0.5': 738, 'KPD-PAP 1200-0.5': 739, 'KPDF-PAP 600-0.4': 740, 
                       'KPDF-PAP 900-0.4': 741, 'KPDF-PAP 1200-0.4': 742, 'KPDF-PAP 1500-0.4': 743, 'KPDF-PAP 1800-0.4': 744, 'KPDF-PAP 600-0.5': 745, 'KPDF-PAP 900-0.5': 746, 
                       'KPDF-PAP 1200-0.5': 747, 'KPD-P-A 2-0.5': 748, 'KPD-P-A 4-0.5': 749, 'KPD-P-A 6-0.5': 750, 'KPD-P-A 10-0.5': 751, 
                       '(K)PDF-AP 200-05 KABLO (250m)': 752, '(K)PDF-AP 150-05 KABLO (250m)': 753, '(K)PDF-AP 100-05 KABLO (250m)': 754, 
                       '(K)PDF-AP 50-05 KABLO (500m)': 755, '(K)PDF-AP 30-05 KABLO (500m)': 756, '(K)PDF-AP 20-05 KABLO (500m)': 757, 
                       '(K)PDF-APA 200-05 KABLO (250m)': 758, '(K)PDF-APA 150-05 KABLO (250m)': 759, '(K)PDF-APA 100-05 KABLO (250m)': 760, 
                       '(K)PDF-APA 50-05 KABLO (500m)': 761, '(K)PDF-APA 30-05 KABLO (500m)': 762, '(K)PDF-APA 20-05 KABLO (500m)': 763, 'PD-P-A (KPD-PA) 10-05 KABLO (500m)': 764, 
                       'PD-P-A (KPD-PA) 6-05 KABLO (500m)': 765, 'PD-P-A (KPD-PA) 4-05 KABLO (500m)': 766, 'PD-P-A (KPD-PA) 2-05 KABLO (250m)': 767, 'Ağaç telefon direği (7 Mt)': 55, 
                       'Ağaç telefon direği (8 Mt)': 56, 'Ağaç telefon direği (9 Mt)': 57, '10 luk kesmeli modül ': 58, '10 luk kesmesiz modül ': 59, 'BEKT A': 60, 'BEKT B': 61, 'BEKT C': 62, 
                       'Çatal ek kiti': 63, 'Topraklama kiti': 64, 'İzoleli Çelik spiral boru 9 mm': 65, 'İzoleli Çelik spiral boru 11 mm': 66, 'İzoleli Çelik spiral boru 14 mm': 67, 
                       'İzoleli Çelik spiral boru 16 mm': 68, 'İzoleli Çelik spiral boru 18 mm': 69, 'İzoleli Çelik spiral boru 26 mm': 70, 'İzoleli Çelik spiral boru 29 mm': 71, 
                       'İzoleli Çelik spiral boru 32 mm': 72, 'İzoleli Çelik spiral boru 37 mm': 73, 'İzoleli Çelik spiral boru 42 mm': 74, 'İzoleli Çelik spiral boru 50 mm': 75, 
                       'İzoleli Çelik spiral boru 63 mm': 76, 'Galvanizli boru 1/2"': 77, 'Galvanizli boru 3/4"': 78, 'Galvanizli boru 1"': 79, 'Galvanizli boru 1 1/4"': 80, 'Galvanizli boru 1 1/2"': 81, 
                       'Galvanizli boru 2"': 82, 'Galvanizli boru 2 1/2"': 83, 'Galvanizli boru 3"': 84, 'Galvanizli boru 4"': 85, 'Çelik spiral boru 9 mm': 86, 'Çelik spiral boru 11 mm': 87, 
                       'Çelik spiral boru 14 mm': 88, 'Çelik spiral boru 16 mm': 89, 'Çelik spiral boru 18 mm': 90, 'Çelik spiral boru 21 mm': 91, 'Çelik spiral boru 26 mm': 92, 'Çelik spiral boru 29 mm': 93, 
                       'Çelik spiral boru 32 mm': 94, 'Çelik spiral boru 37 mm': 95, 'Çelik spiral boru 42 mm': 96, 'Çelik spiral boru 50 mm': 97, 'Çelik spiral boru 63 mm': 98, 'Plastik spiral boru 14 mm': 99, 
                       'Plastik spiral boru 16 mm': 100, 'Plastik spiral boru 18 mm': 101, 'Plastik spiral boru 20 mm': 102, 'Plastik spiral boru 26 mm': 103, 'Plastik spiral boru 32 mm': 104, 'Plastik spiral boru 40 mm': 105, 
                       'Plastik spiral boru 50 mm': 106, 'Halojen free alev yaymaz Plastik spiral boru 16 mm': 107, 'Halojen free alev yaymaz Plastik spiral boru 20 mm': 108, 'Halojen free alev yaymaz Plastik spiral boru 25 mm': 109, 
                       'Halojen free alev yaymaz Plastik spiral boru 32 mm': 110, 'Halojen free alev yaymaz Plastik spiral boru 40 mm': 111, 'Halojen free alev yaymaz Plastik spiral boru 50 mm': 112, 
                       '5cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 113, '10cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 114, '20cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 115, 
                       '30cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 116, '40cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 117, '50cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 118, 
                       '60cmlik Kablo tavası (Montaj için gerekli malzemeler dahil)': 119, '10cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 120, '20cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 121, 
                       '30cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 122, '40cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 123, '50cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 124, 
                       '60cmlik Kablo merdiveni (Montaj için gerekli malzemeler dahil)': 125, 'Topraklama levhası (0,7x0,7/0,5x1 3mm)': 126, 'Topraklama çubuğu (150cm)': 127, '3 mm lik Bakır Tel': 128, '6 mm2 topraklama iletkeni (NYY)': 129, '10 mm2 topraklama iletkeni (NYY)': 130, '16 mm2 topraklama iletkeni (NYY)': 131, '25 mm2 topraklama iletkeni (NYY)': 132, '50 mm2 topraklama iletkeni (NYY)': 133, '6 mm2 topraklama iletkeni (Çıplak bakır)': 134, '10 mm2 topraklama iletkeni (Çıplak bakır)': 135, '16 mm2 topraklama iletkeni (Çıplak bakır)': 136, '25 mm2 topraklama iletkeni (Çıplak bakır)': 137, '50 mm2 topraklama iletkeni (Çıplak bakır)': 138, '12x12 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 139, '16x16 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 140, '25x16 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 141, '25x25 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 142, '40x25 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 143, '40x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 144, '60x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 145, '60x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 146, '80x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 147, '80x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 148, '100x40 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 149, '100x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 150, '120x60 Kablo kanalı (Montaj için gerekli iç köşe, dirsek vb. malzemeler dahil)': 151, '22,5x45 telefon prizi': 152, '22,5x45 data prizi': 153, '45x45 UPS topraklı priz': 154, '45x45 Topraklı priz': 155, 'UTP CAT6 Sıva Üstü Tekli Priz': 156, 'UTP CAT6 Sıva Üstü İkili Priz': 157, 'UTP CAT6 Sıva Altı Tekli Priz': 158, 'UTP CAT6 Sıva Altı İkili Priz': 159, '3lü Topraklı klemensli grup priz': 160, 'RJ45 konnektör': 161, 'RJ11 konnektör': 162, "Sac pano (0,1 m2'ye kadar, 0,1 dahil)": 163, 'Sac pano (0,1-0,2 m2, 0,2 dahil)': 164, 'Sac pano (0,2-0,3 m2, 0,3 dahil)': 165, 
                       '1 Fazlı Nötr Kesmeli Anahtarlı Otomatik Sigorta (40 A.e kadar)': 166, 'Yangın koruma rölesi 2x40A 300mA': 167, 
                       'Yangın koruma rölesi 2x25A 300mA': 168, 'Kaçak akım koruma rölesi 30mA (40 A.e kadar)': 169, '6U dikey kablo düzenleyici (tek taraf)': 170, '9U dikey kablo düzenleyici (tek taraf)': 171, '12U dikey kablo düzenleyici (tek taraf)': 172, 
                       '6U 19" kabinet': 173, '9U 19" kabinet': 174, '12U 19" kabinet': 175, 'Sabit raf': 176, 'Hareketli raf': 177, 'Termostatlı fan modülü 2 fanlı': 178, 'Termostatlı fan modülü 4 fanlı': 179, '19" rack tipi 4lü grup priz sigortalı': 180, 
                       '19" rack tipi 6lı grup priz sigortalı': 181, '19" rack tipi 8li grup priz sigortalı': 182, 'Saha dolabı 2400 lük (8 adet modül bağlantı sacı dahil)': 183, 'Direk tipi saha dolabı 600 lük ( 2 adet modül bağlantı sacı dahil)': 184, 
                       'BDDK-1 (AKEK) Abone Kablo Ek Kutusu': 185, 'BDDK-3 Bina Dışı Dağıtım kutusu (modülsüz)': 186, 'BİDK-2 Bina İçi Dağıtım kutusu 30-50 lik (modülsüz)': 187, 'BİDK-2 Bina İçi Dağıtım kutusu 100 lük (modülsüz)': 188, '300 çiftlik modül bağlantı çatısı': 189, 'Wifi Projesi SW Kutusu (Outdoor Kabinet)': 190, 'Wifi Projesi Sistem Kutusu (Indoor Kabinet)': 191, 
                       'POE Kutusu (Plastik Kutu)': 192, '10G Main Router': 193, 'PTP AP': 194, 'Outdoor AP': 195, '10G Pole Switch': 196, '10G Main Switch': 197, 'Wifi Spot Loglama Cihazı': 198, '3x120+70 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil) ': 199, '3x70+35 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil)': 200, 
                       '4x16 AG ısı büzüşmeli ek mufu paket (Montaj için gerekli malzemeler dahil)': 201, '4x16 AG reçineli ek mufu (Montaj için gerekli malzemeler dahil) ': 202, 'İstavroz demiri': 203, '3U Kabin': 204, "2400'lük Saha dolabı çatısı": 205, '40x60 FTTB Dağıtım kutusu': 206, '60x80 FTTB Dağıtım kutusu': 207, '4x6 NYY 1KV': 208, '4x10 NYY 1KV': 209, '2x6 NYY 1KV': 210, 
                       '2x10 NYY 1KV': 211, '3x2,5 NVV': 212, '3x4 NVV ': 213, '2x6 NVV ': 214, '4x6 NVV ': 215, '4x10 YVOV (NYRY): NYF GBY 1KV': 216, '4x16 YVOV (NYRY): NYF GBY 1KV': 217, 'UTP CAT6 LS0H Patch Cord 0,5m': 218, 'UTP CAT6 LS0H Patch Cord 1m': 219, 
                       'UTP CAT6 LS0H Patch Cord 2m': 220, 'UTP CAT6 LS0H Patch Cord 3m': 221, 'UTP CAT6 LS0H Patch Cord 5m': 222, 'CAT6 20 cm F/UTP': 223, 'CAT6 100 cm F/UTP': 224, 'FO-H 4': 638, 'FO-H 6': 639, 'FO-H 12': 640, 'FO-H 24': 641, 'FO-H 36': 642, 
                       'FO-H 48': 643, 'FO-Y 4': 644, 'FO-Y 6': 645, 'FO-Y 12': 646, 'FO-Y 24': 647, 'FO-Y 36': 648, 'FO-Y 48': 649, 'FO-Y 60': 650, 'FO-Y 72': 651, 'FO-Y 96': 652, 'FO-Y 144': 653, 'FO-Y 192': 654, 'FO-Y 288': 655, 'FO-NM 4': 656, 'FO-NM 6': 657, 'FO-NM 12': 658, 'FO-NM 24': 659, 'FO-NM 36': 660, 'FO-NM 48': 661, 'FO-NM 60': 662, 'FO-NM 72': 663, 'FO-NM 96': 664, 'FO-M 6': 665, 'FO-M 12': 666, 'FO-M 24': 667, 'FO-M 36': 668, 'FO-M 48': 669, 'FO-M 60': 670, 'FO-M 72': 671, 'FO-M 96': 672, 'FO-M 144': 673, 'FO-M 192': 674, 'FO-M 288': 675, 'F/O Ek Kutusu (3 Kasetli)': 225, 'F/O Ek Kutusu (6 Kasetli)': 226, 'F/O Ek Kutusu (12 Kasetli)': 227, 'F/O Ek Kutusu (16 Kasetli)': 228, 'F/O Ek Kutusu (3 Kasetli) Tip 2': 229, 'OB 1x2': 230, 'OB 1X4': 231, 'OB 1X8': 232, 'OB 1X2 SC': 233, 'OB 1X4 SC': 234, 'OB 1X8 SC': 235, 'OB 1X16 SC': 236, 'OB 1X32 SC': 237, 'OFDK-M 1X8': 238, 'OFDK-M 1X16': 239, 'OFDK-M 1X32': 240, 'OFDP 1X2': 241, 'OFDP 1X4': 242, 'OFDP 1X8': 243, 'OFDP 1X16': 244, 'OFDP 1X32': 245, 'OFDÇ 12U ': 246, 'OFDÇ 24U ': 247, 'OFDÇ 42U ': 248, 'OFSB-12': 249, 'OFSB-24': 250, 'OFSB-72': 251, 'OFSD 24U': 252, 'OFSD 24U Çelik': 253, 'OFSD 12U': 254, 'OFSK-P 1x1': 255, '1x2 OBK (Outdoor + Zırhlı)': 256, '1x2 OBK (Çelik + askı tel)': 257, '1x2 OBK (FRP + askı tel)': 258, '1x1 OBK (400N)': 259, '1x1 OBK (outdoor)': 260, 'Riser Kablo (2*6)': 261, 'Riser Kablo (2*12)': 262, 'Riser Kablo (2*24)': 263, 'Riser Kablo (2*48)': 264, 'Riser Kablo Yönlendirme kutusu': 265, 'OFSK-P 1x2': 266, 'OFSK-P 1x4': 267, 'OFDK-P 1X4': 268, 'OFDK-P 1X8': 269, 'OFDK-P 1X16': 270, 'OFDK-P 1X32': 271, 'OFDK-P 1X8 K': 272, 'OFDK-P Askı Aparatı': 273, 'Harici OFDK-P': 274, 'Harici OFDK Bağlantı Aparatı': 275, 'T25': 276, 'FAOC Kutusu': 277, 'TK-OBF SC 2 m': 278, '1x24 TK-OBK SC 5 m': 279, '1x24 TK-OBK SC 10 m': 280, '1x24 TK-OBK SC 20 m': 281, '1x1 K-OBK SC-SC 1 m': 282, '1x1 K-OBK SC-SC 2 m': 283, '1x1 K-OBK SC-SC 3 m': 284, '1x1 K-OBK SC-SC 5 m': 285, '1x1 K-OBK SC-SC 10 m': 286, '1x1 K-OBK SC-SC 20 m': 287, '1x1 K-OBK SC-SC 30 m': 288, '1x1 K-OBK SC-SC 40 m': 289, '1x1 K-OBK SC-SC 50 m': 290, '1x1 K-OBK LC-LC 1 m': 291, '1x1 K-OBK LC-LC 2 m': 292, '1x1 K-OBK LC-LC 3 m': 293, '1x1 K-OBK LC-LC 5 m': 294, '1x1 K-OBK LC-LC 10 m': 295, '1x1 K-OBK LC-LC 20 m': 296, '1x1 K-OBK LC-LC 30 m': 297, '1x1 K-OBK LC-LC 40 m': 298, '1x1 K-OBK LC-LC 50 m': 299, '1x1 K-OBK SC-LC 1 m': 300, '1x1 K-OBK SC-LC 2 m': 301, '1x1 K-OBK SC-LC 3 m': 302, '1x1 K-OBK SC-LC 5 m': 303, '1x1 K-OBK SC-LC 10 m': 304, '1x1 K-OBK SC-LC 20 m': 305, '1x1 K-OBK SC-LC 30 m': 306, '1x1 K-OBK SC-LC 40 m': 307, '1x1 K-OBK SC-LC 50 m': 308, '1x1 K-OBK SC-A/SC 1 m': 309, '1x1 K-OBK SC-A/SC 2 m': 310, '1x1 K-OBK SC-A/SC 3 m': 311, '1x1 K-OBK SC-A/SC 5 m': 312, '1x1 K-OBK SC-A/SC 10 m': 313, '1x1 K-OBK SC-A/SC 20 m': 314, '1x1 K-OBK SC-A/SC 30 m': 315, '1x1 K-OBK SC-A/SC 40 m': 316, '1x1 K-OBK SC-A/SC 50 m': 317, '1x2 K-OBK SC-SC 1 m': 318, '1x2 K-OBK SC-SC 2 m': 319, '1x2 K-OBK SC-SC 3 m': 320, '1x2 K-OBK SC-SC 5 m': 321, '1x2 K-OBK SC-SC 10 m': 322, '1x2 K-OBK SC-SC 20 m': 323, '1x2 K-OBK SC-SC 30 m': 324, '1x2 K-OBK SC-SC 40 m': 325, '1x2 K-OBK SC-SC 50 m': 326, '1x2 K-OBK LC-LC 1 m': 327, '1x2 K-OBK LC-LC 2 m': 328, '1x2 K-OBK LC-LC 3 m': 329, '1x2 K-OBK LC-LC 5 m': 330, '1x2 K-OBK LC-LC 10 m': 331, '1x2 K-OBK LC-LC 20 m': 332, '1x2 K-OBK LC-LC 30 m': 333, '1x2 K-OBK LC-LC 40 m': 334, '1x2 K-OBK LC-LC 50 m': 335, '1x2 K-OBK SC-LC 1 m': 336, '1x2 K-OBK SC-LC 2 m': 337, '1x2 K-OBK SC-LC 3 m': 338, '1x2 K-OBK SC-LC 5 m': 339, '1x2 K-OBK SC-LC 10 m': 340, '1x2 K-OBK SC-LC 20 m': 341, '1x2 K-OBK SC-LC 30 m': 342, '1x2 K-OBK SC-LC 40 m': 343, '1x2 K-OBK SC-LC 50 m': 344, '1x12 K-OBK SC-SC 5 m': 345, '1x12 K-OBK SC-SC 10 m': 346, '1x12 K-OBK SC-SC 15 m': 347, '1x12 K-OBK SC-SC 20 m': 348, '1x12 K-OBK SC-SC 25 m': 349, '1x12 K-OBK SC-SC 30 m': 350, '1x12 K-OBK SC-SC 35 m': 351, '1x12 K-OBK SC-SC 40 m': 352, '1x12 K-OBK SC-SC 45 m': 353, '1x12 K-OBK SC-SC 50 m': 354, '1x12 K-OBK LC-LC 5 m': 355, '1x12 K-OBK LC-LC 10 m': 356, '1x12 K-OBK LC-LC 15 m': 357, '1x12 K-OBK LC-LC 20 m': 358, '1x12 K-OBK LC-LC 25 m': 359, '1x12 K-OBK LC-LC 30 m': 360, '1x12 K-OBK LC-LC 35 m': 361, '1x12 K-OBK LC-LC 40 m': 362, '1x12 K-OBK LC-LC 45 m': 363, '1x12 K-OBK LC-LC 50 m': 364, '1x12 K-OBK SC-LC 5 m': 365, '1x12 K-OBK SC-LC 10 m': 366, '1x12 K-OBK SC-LC 15 m': 367, '1x12 K-OBK SC-LC 20 m': 368, '1x12 K-OBK SC-LC 25 m': 369, '1x12 K-OBK SC-LC 30 m': 370, '1x12 K-OBK SC-LC 35 m': 371, '1x12 K-OBK SC-LC 40 m': 372, '1x12 K-OBK SC-LC 45 m': 373, '1x12 K-OBK SC-LC 50 m': 374, '1x24 K-OBK SC-SC 5 m': 375, '1x24 K-OBK SC-SC 10 m': 376, '1x24 K-OBK SC-SC 15 m': 377, '1x24 K-OBK SC-SC 20 m': 378, '1x24 K-OBK SC-SC 25 m': 379, '1x24 K-OBK SC-SC 30 m': 380, '1x24 K-OBK SC-SC 35 m': 381, '1x24 K-OBK SC-SC 40 m': 382, '1x24 K-OBK SC-SC 45 m': 383, '1x24 K-OBK SC-SC 50 m': 384, '1x24 K-OBK SC-SC 60 m': 385, '1x24 K-OBK SC-SC 70 m': 386, '1x24 K-OBK SC-SC 80 m': 387, '1x24 K-OBK SC-SC 90 m': 388, '1x24 K-OBK SC-SC 100 m': 389, '1x24 K-OBK SC-SC 150 m': 390, '1x24 K-OBK LC-LC 5 m': 391, '1x24 K-OBK LC-LC 10 m': 392, '1x24 K-OBK LC-LC 15 m': 393, '1x24 K-OBK LC-LC 20 m': 394, '1x24 K-OBK LC-LC 25 m': 395, '1x24 K-OBK LC-LC 30 m': 396, '1x24 K-OBK LC-LC 35 m': 397, '1x24 K-OBK LC-LC 40 m': 398, '1x24 K-OBK LC-LC 45 m': 399, '1x24 K-OBK LC-LC 50 m': 400,'1x24 K-OBK SC-LC 5 m': 401, '1x24 K-OBK SC-LC 10 m': 402, '1x24 K-OBK SC-LC 15 m': 403, '1x24 K-OBK SC-LC 20 m': 404, '1x24 K-OBK SC-LC 25 m': 405, '1x24 K-OBK SC-LC 30 m': 406, '1x24 K-OBK SC-LC 35 m': 407, '1x24 K-OBK SC-LC 40 m': 408, '1x24 K-OBK SC-LC 45 m': 409, '1x24 K-OBK SC-LC 50 m': 410, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 0,6 M': 411, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 1 M': 412, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 3 M': 413, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 5 M': 414,'PATCHCORD FC/UPC-FC/UPC SIMPLEX 7 M': 415, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 10 M': 416, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 15 M': 417, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 20 M': 418, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 30 M': 419, 'PATCHCORD FC/UPC-FC/UPC SIMPLEX 40 M': 420, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 0,6 M': 421, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 1 M': 422, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 3 M': 423, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 5 M': 424, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 7 M': 425, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 10 M': 426, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 15 M': 427, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 20 M': 428, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 25 M': 429, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 30 M': 430, 'PATCHCORD FC/UPC-SC/UPC SIMPLEX 40 M': 431, 'PATCHCORD FC/UPC-SC/UPC DUBLEX 12 M': 432, 'PATCHCORD FC/UPC-LC/UPC DUBLEX 5 M': 433, 'PATCHCORD FC/UPC-LC/UPC DUBLEX 10 M': 434, 'PATCHCORD FC/UPC-LC/UPC DUBLEX 15 M': 435, 'PATCHCORD FC/UPC-LC/UPC DUBLEX 20 M': 436,'PATCHCORD FC/UPC-LC/UPC DUBLEX 25 M': 437, 'PATCHCORD FC/UPC-MU/UPC SIMPLEX 0,6 M': 438, 'PATCHCORD FC/UPC-MU/UPC SIMPLEX 3 M': 439, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 0,3 M': 440, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 0,6 M': 441, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 7 M': 442, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 8 M': 443, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 13 M': 444, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 15 M': 445, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 17 M': 446, 'PATCHCORD SC/UPC-SC/UPC SIMPLEX 25 M': 447,'PATCHCORD SC/UPC-SC/UPC DUBLEX 6 M': 448, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 7 M': 449, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 9 M': 450, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 12 M': 451, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 15 M': 452, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 18 M': 453, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 22 M': 454, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 25 M': 455, 'PATCHCORD SC/UPC-SC/UPC DUBLEX 28 M': 456, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 0,6 M': 457, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 3 M': 458,'PATCHCORD SC/UPC-MU/UPC SIMPLEX 5 M': 459, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 7 M': 460, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 10 M': 461, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 15 M': 462, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 20 M': 463, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 25 M': 464, 'PATCHCORD SC/UPC-MU/UPC SIMPLEX 30 M': 465, 'PATCHCORD SC/UPC-MU/UPC DUBLEX 10 M': 466, 'PATCHCORD SC/UPC-MU/UPC DUBLEX 15 M': 467, 'PATCHCORD SC/UPC-MU/UPC DUBLEX 20 M': 468, 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 5 M': 469, 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 10 M': 470, 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 15 M': 471, 'PATCHCORD SC/UPC-E2000/APC SIMPLEX 20 M': 472, 'PATCHCORD SC/UPC-E2000/UPC SIMPLEX 5 M': 473, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 1 M': 474, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 3 M': 475, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 5 M': 476, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 7 M': 477, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 10 M': 478, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 15 M': 479, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 20 M': 480, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 25 M': 481, 'PATCHCORD LC/UPC-FC/UPC SIMPLEX 30 M': 482, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 0,6 M': 483, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 7 M': 484, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 8 M': 485, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 12 M': 486, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 15 M': 487, 'PATCHCORD LC/UPC-SC/UPC SIMPLEX 25 M': 488, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 4 M': 489, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 6 M': 490, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 7 M': 491, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 8 M': 492, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 9 M': 493, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 10,5 M': 494, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 11M': 495, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 11,5 M': 496, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 12 M': 497, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 12,5 M': 498,'PATCHCORD LC/UPC-SC/UPC DUBLEX 13 M': 499, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 13,5 M': 500, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 14 M': 501, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 14,5 M': 502, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 15 M': 503, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 15,5 M': 504, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 16 M': 505, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 16,5 M': 506, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 17 M': 507, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 17,5 M': 508, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 18 M': 509, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 18,5 M': 510, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 19 M': 511, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 19,5 M': 512, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 21 M': 513, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 22 M': 514, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 25 M': 515, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 28 M': 516, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 33 M': 517, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 35 M': 518, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 38 M': 519, 'PATCHCORD LC/UPC-SC/UPC DUBLEX 45 M': 520,'PATCHCORD LC/UPC-SC/UPC DUBLEX 55 M': 521, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,3 M': 522, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,5 M': 523, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 0,6 M': 524, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 1,2 M': 525, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 7 M': 526, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 8 M': 527, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 12 M': 528, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 15 M': 529, 'PATCHCORD LC/UPC-LC/UPC SIMPLEX 25 M': 530, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,15 M': 531, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,20 M': 532, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 0,30 M': 533, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 7 M': 534, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 8 M': 535, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 12 M': 536, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 13 M': 537, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 14 M': 538, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 15 M': 539, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 16 M': 540, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 17 M': 541, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 18 M': 542, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 23 M': 543, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 25 M': 544, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 28 M': 545, 'PATCHCORD LC/UPC-LC/UPC DUBLEX 35 M': 546, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 1 M': 547, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 3 M': 548, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 7 M': 549, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 10 M': 550, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 15 M': 551, 'PATCHCORD LC/UPC-MU/UPC SIMPLEX 20 M': 552, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 0,3 M': 553,'PATCHCORD MU/UPC-MU/UPC SIMPLEX 0,6 M': 554, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 1 M': 555, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 3 M': 556, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 5 M': 557, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 7 M': 558, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 10 M': 559, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 15 M': 560, 'PATCHCORD MU/UPC-MU/UPC SIMPLEX 20 M': 561, 'PATCHCORD MU/UPC-MU/UPC DUBLEX 0,6 M': 562, 'PATCHCORD ST/UPC-LC/UPC DUBLEX 5 M': 563, 'PATCHCORD ST/UPC-LC/UPC DUBLEX 10 M': 564, 'PATCHCORD ST/UPC-LC/UPC DUBLEX 20 M': 565, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 10M': 566, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 15M': 567, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 20M': 568, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 25M': 569, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 30M': 570, 'PATCHCORD SC/UPC-SC/UPC 4X1 BREAKOUT 40M': 571, 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 10M': 572, 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 15M': 573, 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 20M': 574,'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 25M': 575, 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 30M': 576, 'PATCHCORD SC/UPC-SC/UPC 12X1BREAKOUT 40M': 577, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 10M': 578, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 15M': 579, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 20M': 580, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 25M': 581, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 30M': 582, 'PATCHCORD LC/UPC-SC/UPC 4X1 BREAKOUT 40M': 583, 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 10M': 584,'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 15M': 585, 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 20M': 586, 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 25M': 587, 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 30M': 588, 'PATCHCORD LC/UPC-SC/UPC 12X1BREAKOUT 40M': 589, 'Z-OABK SC-SC 0,6m 3dB': 590, 'Z-OABK SC-SC 0,6m 5dB': 591, 'Z-OABK SC-SC 0,6m 10dB': 592, 'Z-OABK LC-LC 0,6m 3dB': 593, 'Z-OABK LC-LC 0,6m 5dB': 594, 'Z-OABK LC-LC 0,6m 10dB': 595, 'Z-OABK MU-MU 0,6m 3dB': 596, 'Z-OABK MU-MU 0,6m 5dB': 597, 'Z-OABK MU-MU 0,6m 10dB': 598,'U-LINK SIMPLEX FC UPC/SC UPC': 599, 'U-LINK SIMPLEX FC UPC/LC UPC': 600, 'U-LINK SIMPLEX MU UPC/MU UPC': 601, 'U-LINK SIMPLEX LC UPC/SC UPC': 602, 'U-LINK SIMPLEX LC UPC/LC UPC': 603, 'U-LINK DUBLEX LC UPC/LC UPC': 604, 'U-LINK SIMPLEX FC UPC/FC UPC': 605, 'U-LINK SIMPLEX SC UPC/SC UPC': 606, 'U-LINK SIMPLEX E-2000 APC / E-2000 APC': 607, 'U-LINK SIMPLEX E-2000 UPC / E-2000 UPC': 608, 'ZAYIFLATICI SC PLUG-IN TİPİ 5 dB': 609, 'ZAYIFLATICI SC PLUG-IN TİPİ 3 dB': 610, 'ZAYIFLATICI SC PLUG-IN TİPİ 7 dB': 611, 'ZAYIFLATICI SC PLUG-IN TİPİ 10 dB': 612, 'ZAYIFLATICI SC PLUG-IN TİPİ 15dB': 613, 'ZAYIFLATICI LC PLUG-IN TİPİ 3 dB': 614, 'ZAYIFLATICI LC PLUG-IN TİPİ 5 dB': 615, 'ZAYIFLATICI LC PLUG-IN TİPİ 7 dB': 616, 'ZAYIFLATICI LC PLUG-IN TİPİ 10 dB': 617, 'ZAYIFLATICI LC PLUG-IN TİPİ 15 dB': 618, 'ZAYIFLATICI FC PLUG-IN TİPİ 3 dB': 619, 'ZAYIFLATICI FC PLUG-IN TİPİ 5 dB': 620, 'ZAYIFLATICI FC PLUG-IN TİPİ 7dB': 621, 'ZAYIFLATICI FC PLUG-IN TİPİ 10 dB': 622, 'ZAYIFLATICI MU PLUG-IN TİPİ 3 dB': 623, 'ZAYIFLATICI MU PLUG-IN TİPİ 5 dB': 624, 'ZAYIFLATICI MU PLUG-IN TİPİ 7 dB': 625, 'ZAYIFLATICI MU PLUG-IN TİPİ 10 dB': 626, 'ZAYIFLATICI MU PLUG-IN TİPİ 15 dB': 627, '1x24 TK-OBK SC 2 m': 628, '1x24 TK-OBK SC 3 m': 629, '1x32 TK-OBK SC 10 m': 630, '1x1 K-OBK SC-A/LC 3 M': 631, '1x16 K-OBK SC-SC 5 m': 632, '1x16 K-OBK SC-SC 10 m': 633, '1x16 K-OBK SC-SC 20 m': 634, '1x32 K-OBK SC-SC 5 m': 635, '1x32 K-OBK SC-SC 10 m': 636, '1x32 K-OBK SC-SC 20 m': 637, 'Çift cidarlı HDPE boru (110)': 1, 'Çift cidarlı HDPE boru için birleştirme manşonu (110)': 2, 'Çift cidarlı HDPE boru (90)': 3, 'Çift cidarlı HDPE boru için birleştirme manşonu (90)': 4, 'Çift cidarlı HDPE Boru (75)': 5, 'Çift cidarlı HDPE boru için birleştirme manşonu (75)': 6, 'Çift cidarlı HDPE Boru (50)': 7, 'Çift cidarlı HDPE boru için birleştirme manşonu (50)': 8, '1x1 HDPE boru': 9, '2x1 HDPE boru': 10, '3x1 HDPE boru': 11, 'HDPE ikili göz çoklayıcı boru (Tıkama parçası dahil)': 12, 'HDPE üçlü göz çokl. boru (Tıkama parç. ve kanal ağzı tut. dahil)': 13, 'Çift cidarlı HDPE boru için HDPE tamir manşonu': 14, 'Çift cidarlı HDPE boru için PVC parçalı tamir manşonu(iki parça)': 15, 'Çift cidarlı HDPE boru için HDPE boru adaptörü': 16, 'Çift cidarlı HDPE boru için HDPE boru tıpası': 17, "Çift cidarlı HDPE boru için PVC boru destekleri(2' li)": 18, 'Mikroboru 1 Gözlü': 19, 'Mikroboru 2 Gözlü': 20, 'Mikroboru 4 Gözlü': 21, 'Mikroboru 7 Gözlü': 22, 'Tip-1 Prefabrik beton menhol': 23, 'Tip-2 Prefabrik beton ek odası': 24, 'Kompozit Ek Odası Kapağı': 25, 'Kompozit Ek Odası Çerçevesi': 26, 'Kompozit Menhol Kapağı': 27, 'Kompozit Menhol Çerçevesi': 28, 'Kompozit Ek Odası Yükseltme Halkası': 29, 'Kompozit Menhol Yükseltme Halkası': 30, 'Ek Odası H41 (Kompozit)': 31, 'Ek Odası H65 (Kompozit)': 32, 'Ek Odası H75 (Kompozit)': 33, 'Ek Odası Kapağı H65-H41 (Kompozit)': 34, 'Ek Odası Kapağı H75 (Kompozit)': 35, 'Ek Odası Çerçevesi H65-H41 (Kompozit)': 36, 'Ek Odası Ara Yükseltme Çerçevesi H75 (Kompozit)': 37, 'Ek Odası Ara Yükseltme Çerçevesi H65-H41 (Kompozit)': 38, 'Ek Odası Çerçevesi H75 (Kompozit)': 39, 'Prefabrik menhol yükseltme parçası': 40, 'FTTx küçük tip kabin (Tip 7, 11, 13, 15 ve 23) beton kaidesi': 41, 'Andezit Parke': 42, 'Granit Parke': 43, 'Bazalt Parke': 44, 'Beton Parke': 45, 'Mermer': 46, 'Granit': 47, 'Beton Bordür': 48, 'Karosiman': 49, 'C20/25 beton': 50, "Rak pabucu (25'lik ve 50'lik)": 51, 'Tıkama malzemesi (protolin)': 52, 'Menhol kanalı tıkama malzemesi (Dolu göz için)': 53, 'Menhol kanalı tıkama malzemesi (Boş göz için, mekanik tip)': 54}
        
        
        if not irsaliyeNo or not irsaliyeTarihi or not gelenMiktar or not malzemeAdi:
            self.show_warning_message("Eksik bilgi girdiniz. Lutfen istenilen tum bilgileri eksiksiz giriniz!!")
        else:
            try:
                if malzemeCinsi == "Fiber Kablo" or malzemeCinsi == "Bakir Kablo":
                    en_son_id_sorgu = "SELECT Id FROM stok ORDER BY Id DESC LIMIT 1"
                    self.islem.execute(en_son_id_sorgu)
                    en_son_id = self.islem.fetchone()
                    
                    self.a= "k" + str(malzemeAdi).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower() + "" +str(makaraNo).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower()

                    if en_son_id:
                        id = en_son_id[-1] + 1
                    else:
                        id = 1

                    pozNo = self.mapping.get(malzemeAdi)
                    ekle = "insert into stok (id, malzemeCinsi, pozNo, malzemeAdi, irsaliyeTarihi, makaraNo, birim, gelenMiktar, kullanilanMiktar, sevkMiktari, kalanMiktar, konum, aciklama, sayim) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    self.islem.execute(ekle, (id, malzemeCinsi, pozNo, malzemeAdi, irsaliyeTarihi, makaraNo, birim, gelenMiktar, 0,0,gelenMiktar, konum, aciklama, 0))
                    self.baglanti.commit()
                    
                    self.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)

                    self.islem.execute("create table if not exists " + str(self.a) + " (islemNo int, islemTuru text, makaraNo text, irsaliyeNo text, irsaliyeTarihi text, cikisTarihi text, projeAdi text, krokiNo text, kullananEkip text, sevkMiktari int, aciklama text, hakedis text, guncellemeTarihi text, cbsid1 int, cbsid2 int, cbsid3 int, cbsid4 int, cbsid5 int)")
                    self.baglanti.commit()

                    islemNo_son = "SELECT islemNo FROM " + str(self.a) + " ORDER BY islemNo DESC LIMIT 1"
                    self.islem.execute(islemNo_son,)
                    islemNo_son = self.islem.fetchone()
                    
                    if islemNo_son:
                        islemNo = islemNo_son[-1] + 1
                    else:
                        islemNo = 1      
                    ekle2="insert into " + str(self.a) +" (islemNo, islemTuru, makaraNo, irsaliyeNo, irsaliyeTarihi, cikisTarihi, projeAdi, krokiNo, kullananEkip, sevkMiktari, aciklama, hakedis, guncellemeTarihi, cbsid1, cbsid2, cbsid3, cbsid4, cbsid5) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            
                    self.islem.execute(ekle2, (islemNo, "GIRIS", makaraNo, irsaliyeNo, irsaliyeTarihi, "-", proje_Adi, kroki_No, kullanan_Ekip, gelenMiktar, aciklama,hakedis_durumu, guncellemeTarihi, 0, 0, 0, 0, 0))
                    self.baglanti.commit()
                                        
                    self.kayit_listele()
                    self.temizle()
                    id = id + 1
                    islemNo= islemNo + 1
                else:
                    self.gozlem = False
                    self.rowdeg = 0
                    self.a= "m" + str(malzemeAdi).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower()
                 
                    for row in range(self.tableWidget.rowCount()):
                        item = str(self.tableWidget.item(row, 3).text()) if self.tableWidget.item(row, 3) is not None else ""
                        if item == str(malzemeAdi):
                            self.gozlem = True
                            self.rowdeg= row
                            break
                        
                        if item == "":
                            break
                        
                    if self.gozlem == True:
                        
                        self.id2 = int(self.tableWidget.item(self.rowdeg, 0).text())
                        self.sorgu = "select * from stok where id = ?"
                        self.islem.execute(self.sorgu, (self.id2,))
                        a = self.islem.fetchone()

                        if a:
                            a_list = list(a)

                            a_list[gelen_miktar_index] += int(gelenMiktar)
                        else:
                            a_list[gelen_miktar_index] = int(gelenMiktar)
                        
                        a_list[kalan_miktar_index] += int(gelenMiktar)
                        a_updated = tuple(a_list)
                        update_sorgu = """
                            UPDATE stok
                            SET gelenMiktar = ?,
                            kalanMiktar = ?
                            WHERE id = ?
                            """
                        self.islem.execute(update_sorgu, (a_updated[gelen_miktar_index], a_updated[kalan_miktar_index],self.id2))
                        self.baglanti.commit()
                        
                        self.islem.execute("create table if not exists " + str(self.a) + " (islemNo int, islemTuru text, makaraNo text, irsaliyeNo text, irsaliyeTarihi text, cikisTarihi text, projeAdi text, krokiNo text, kullananEkip text, sevkMiktari int, aciklama text, hakedis text, guncellemeTarihi text, cbsid1 int, cbsid2 int, cbsid3 int, cbsid4 int, cbsid5 int)")

                        islemNo_son = "SELECT islemNo FROM " + str(self.a) + " ORDER BY islemNo DESC LIMIT 1"
                        self.islem.execute(islemNo_son,)
                        islemNo_son = self.islem.fetchone()
                        
                        if islemNo_son:
                            islemNo = islemNo_son[-1] + 1
                        else:
                            islemNo = 1      
                        ekle2="insert into " + str(self.a) +" ( islemNo, islemTuru, makaraNo, irsaliyeNo, irsaliyeTarihi, cikisTarihi, projeAdi, krokiNo, kullananEkip, sevkMiktari, aciklama, hakedis, guncellemeTarihi, cbsid1, cbsid2, cbsid3, cbsid4, cbsid5) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                                
                        self.islem.execute(ekle2, (islemNo, "GIRIS", "-", irsaliyeNo, irsaliyeTarihi,"-", proje_Adi, kroki_No, kullanan_Ekip, gelenMiktar, aciklama,hakedis_durumu, guncellemeTarihi, 0, 0, 0, 0, 0))
                        self.baglanti.commit()                        
                            
                        self.kayit_listele()
                        self.temizle()
                        self.gozlem= False
                    else:    
                        en_son_id_sorgu = "SELECT Id FROM stok ORDER BY Id DESC LIMIT 1"
                        self.islem.execute(en_son_id_sorgu)
                        en_son_id = self.islem.fetchone()
                        
                        if en_son_id:
                            id = en_son_id[-1] + 1
                        else:
                            id = 1
                        pozNo = self.mapping.get(malzemeAdi)
                        ekle = "insert into stok (id, malzemeCinsi, pozNo, malzemeAdi, irsaliyeTarihi, makaraNo, birim, gelenMiktar, kullanilanMiktar, sevkMiktari, kalanMiktar, konum, aciklama, sayim) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                        self.islem.execute(ekle, (id, malzemeCinsi, pozNo, malzemeAdi, irsaliyeTarihi, "-", birim, gelenMiktar, 0,0,gelenMiktar, konum, aciklama, 0))
                        self.baglanti.commit()
                        self.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)

                        self.islem.execute("create table if not exists " + str(self.a) + " (islemNo int, islemTuru text, makaraNo text, irsaliyeNo text, irsaliyeTarihi text, cikisTarihi text, projeAdi text, krokiNo text, kullananEkip text, sevkMiktari int, aciklama text, hakedis text, guncellemeTarihi text, cbsid1 int, cbsid2 int, cbsid3 int, cbsid4 int, cbsid5 int)")
                        self.baglanti.commit()

                        islemNo_son = "SELECT islemNo FROM " + str(self.a) + " ORDER BY islemNo DESC LIMIT 1"
                        self.islem.execute(islemNo_son,)
                        islemNo_son = self.islem.fetchone()
                        
                        if islemNo_son:
                            islemNo = islemNo_son[-1] + 1
                        else:
                            islemNo = 1      
                        ekle2="insert into " + str(self.a) +" ( islemNo, islemTuru, makaraNo, irsaliyeNo, irsaliyeTarihi, cikisTarihi, projeAdi, krokiNo, kullananEkip, sevkMiktari, aciklama, hakedis, guncellemeTarihi, cbsid1, cbsid2, cbsid3, cbsid4, cbsid5) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                        self.islem.execute(ekle2, (islemNo, "GIRIS", "-", irsaliyeNo, irsaliyeTarihi, "-", proje_Adi, kroki_No, "-", gelenMiktar, aciklama,hakedis_durumu, guncellemeTarihi,0,0,0,0,0))
                        self.baglanti.commit()   
                                                
                        self.kayit_listele()
                        self.temizle()
                        id = id+1   
                        islemNo = islemNo + 1
                        
            except Exception as e:
                self.show_warning_message("Bir hata oluştu. Lütfen tekrar deneyin.")

    def malzeme_cikart(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        proje_Adi= str(self.lneProjeNo.text())
        kullanan_Ekip= self.cmbKullananEkip.currentText()
        kroki_No= str(self.lneKrokiNo.text())
        hakedis_durumu= self.cmbHakedis.currentText()        
        guncellemeTarihi = datetime.now().strftime("%Y-%m-%d")
        self.id_No= int(self.lneIdNo.text())
        

        try:
            cikan_Miktar = int(self.lneCikanMiktar.text())
        except:
            self.show_warning_message("LUTFEN CIKAN MIKTAR'A SAYISAL DEGER GIRINIZ") 
            return   
        cikis_Tarihi= str(self.lneCikisTarihi.text())
        aciklama= str(self.lneAciklama.text())
        
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        
        if not proje_Adi:
            proje_Adi= "-"
        
        if not kroki_No:
            kroki_No= "-"
        
        if not self.id_No:
            self.show_warning_message("Islem yapilacak malzemenin Id No'sunu giriniz!!")            

        self.sorgu = "select * from stok where id = ?"
        self.islem.execute(self.sorgu, (self.id_No,))
        b = self.islem.fetchone()
        
        if b:
            a_list = list(b)
        else:
            return
        
        

        if a_list[malzeme_cinsi_index] == "Fiber Kablo" or a_list[malzeme_cinsi_index] == "Bakir Kablo":   
            self.a= "k"+str(a_list[3]).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower() + "" +str(a_list[5]).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower()
        else:
            self.a= "m"+str(a_list[3]).replace("/","").replace("+","").replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").lower()
        
        self.baglanti.commit()
                
        islemNo_son = "SELECT islemNo FROM " + str(self.a) + " ORDER BY islemNo DESC LIMIT 1"
        self.islem.execute(islemNo_son)
        islemNo_son = self.islem.fetchone()
        
        if islemNo_son:
            islemNo = islemNo_son[-1] + 1
        else:
            islemNo = 1      

        cikart="insert into " + str(self.a) +" ( islemNo, islemTuru, makaraNo, irsaliyeNo, irsaliyeTarihi, cikisTarihi, projeAdi, krokiNo, kullananEkip, sevkMiktari, aciklama, hakedis, guncellemeTarihi, cbsid1, cbsid2, cbsid3, cbsid4, cbsid5) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self.islem.execute(cikart, (islemNo, "CIKIS", a_list[makara_no_index], "-", "-", cikis_Tarihi, proje_Adi, kroki_No, kullanan_Ekip, 0-int(cikan_Miktar), aciklama, hakedis_durumu, guncellemeTarihi,0,0,0,0,0))
        self.baglanti.commit()
    

        self.islem.execute("SELECT ekipAdi FROM ekipler WHERE sevkEkibi = 1")
        sevk_ekipleri = [ekip[0] for ekip in self.islem.fetchall()]
        
        sevk_ekipleri = str(sevk_ekipleri)[1:-1]
        self.baglanti.commit()
        
        sorgu1 = "SELECT SUM(SevkMiktari) FROM "+str(self.a)+" WHERE KullananEkip IN ("+ sevk_ekipleri +") AND IslemTuru = 'CIKIS'"


        self.islem.execute(sorgu1)
        
        toplam_eregliye_sevk_miktari = self.islem.fetchone()[0]
        if toplam_eregliye_sevk_miktari is None:
            toplam_eregliye_sevk_miktari = 0
        else:
            toplam_eregliye_sevk_miktari = int(int(toplam_eregliye_sevk_miktari) * (-1))
        
        
        sorgu2 = "SELECT SUM(SevkMiktari) FROM "+ str(self.a) +" WHERE IslemTuru = 'CIKIS'"

        
        self.islem.execute(sorgu2)
        toplam_kullanilan_miktar = self.islem.fetchone()[0]
        if toplam_kullanilan_miktar is None:
            toplam_kullanilan_miktar = 0
        else:      
            toplam_kullanilan_miktar = int(toplam_kullanilan_miktar)* (-1)
            toplam_kullanilan_miktar = toplam_kullanilan_miktar - toplam_eregliye_sevk_miktari
        
        a_list[sevk_miktari_index] = toplam_eregliye_sevk_miktari

        a_list[kullanilan_miktar_index] = toplam_kullanilan_miktar

        a_list[kalan_miktar_index] = int(a_list[gelen_miktar_index]) - toplam_eregliye_sevk_miktari - toplam_kullanilan_miktar

        update_sorgu = """
            UPDATE stok
            SET kullanilanMiktar = ?,
            sevkMiktari = ?,
            kalanMiktar = ?
            WHERE id = ?
            """
        self.islem.execute(update_sorgu, (a_list[kullanilan_miktar_index],a_list[sevk_miktari_index], a_list[kalan_miktar_index],self.id_No))
        self.baglanti.commit()
        
        global numara
        numara = self.id_No
        
        self.statusbar.showMessage("Malzeme Sevk Islemi Basarili !!", 10000)
        self.kayit_listele()

    def kayit_sil(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Lütfen silmek istediğiniz satırı seçin!!")
            msg.setWindowTitle("Uyarı")
            msg.exec_()
        else:   
            result = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)
            
            if result == QMessageBox.Yes:               
                if selected_row != -1:
                    secilen_id = self.tableWidget.item(selected_row, 0).text()  # İd'nin bulunduğu sütun indeksi
                    try:
                        silme_sorgu = "DELETE FROM stok WHERE id = ?"
                        self.islem.execute(silme_sorgu, (secilen_id,))
                        self.baglanti.commit()
                        self.statusbar.showMessage("Kayıt Silme İşlemi Başarılı", 10000)
                        self.kayit_listele()

                    except Exception as error:
                        self.statusbar.showMessage("Kayıt Silinirken Hata Oluştu === " + str(error))

            else:
                self.statusbar.showMessage("Silme İşlemi İptal Edildi")

    def konuma_gore_listele(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(("Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"))

        listelenecek_konum = self.cmbKonum.currentText()
            
                
        if not self.cbxSecim.isChecked():
            
            sorgu = "select * from stok where konum = ?"
            self.islem.execute(sorgu,(listelenecek_konum,))    
        
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        
        else:
            
            sorgu = "select * from stok where kalanMiktar != 0 and konum = ?"
            self.islem.execute(sorgu,(listelenecek_konum,))
            
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

    def malzeme_cinsine_gore_listele(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(("Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"))
        listelenecek_malzeme_cinsi = self.cmbMalzemeCinsi.currentText()
            
                
        if not self.cbxSecim.isChecked():
            
            sorgu = "select * from stok where malzemeCinsi = ?"
            self.islem.execute(sorgu,(listelenecek_malzeme_cinsi,))    
        
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        
        else:
            
            sorgu = "select * from stok where kalanMiktar != 0 and malzemeCinsi = ?"
            self.islem.execute(sorgu,(listelenecek_malzeme_cinsi,))
            
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

    def malzemeye_gore_listele(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(("Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"))
        listelenecek_malzeme = self.cmbMalzeme.currentText()
            
                
        if not self.cbxSecim.isChecked():
            
            sorgu = "select * from stok where malzemeAdi = ?"
            self.islem.execute(sorgu,(listelenecek_malzeme,))    
        
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        
        else:
            
            sorgu = "select * from stok where kalanMiktar != 0 and malzemeAdi = ?"
            self.islem.execute(sorgu,(listelenecek_malzeme,))
            
            for indexSatir, kayitNumarasi in enumerate(self.islem):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

    def makara_sorgula(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        try:
            sorgulanan_makara = self.lneMakaraNo.text()
            self.islem2= self.islem
            sorgu = "select * from stok where makaraNo = ?"
            self.islem2.execute(sorgu,(sorgulanan_makara,))
            sonuc = self.islem2.fetchall()
            
            if not sonuc:
                self.show_warning_message("ARAMANIZLA ESLESEN MAKARA BULUNAMAMISTIR!!")
            
            else:
                self.tableWidget.clear()
                self.tableWidget.setHorizontalHeaderLabels(("Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"))
                sorgu = "select * from stok where makaraNo = ?"
                self.islem.execute(sorgu,(sorgulanan_makara,))
                
                for indexSatir, kayitNumarasi in enumerate(self.islem):
                    for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                        self.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

        except Exception as error:
            self.statusbar.showMessage("Makara Sorgulanirken Hata === " + str(error))

    def export_to_excel(self):
        # Sadece görünen verileri al
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        veriler = []

        for row in range(rows):
            veri = []
            for col in range(columns):
                item = self.tableWidget.item(row, col)
                if item is not None:
                    veri.append(item.text())
                else:
                    veri.append('')
            veriler.append(veri)

        if not veriler:
            self.show_warning_message("Veri bulunamadi.")
            return

        columns = ["Id", "Malzeme Cinsi", "Poz No", "Malzeme Adi","Son Irsaliye Tarihi","Makara No","Birim","Gelen Miktar","Kullanilan Miktar","Sevk Miktari","Kalan Miktar","Konumu","Aciklama","Sayim"]
        
        df = pd.DataFrame(veriler, columns=columns)

        bugunun_tarihi = datetime.now().strftime("%Y-%m-%d")

        dosya_adi, _ = QFileDialog.getSaveFileName(self, "Excel Dosyasını Kaydet", f"Depo Stok ({bugunun_tarihi}).xlsx", "Excel Dosyası (*.xlsx)")

        if not dosya_adi:
            return

        df.to_excel(dosya_adi, index=False)

        QMessageBox.information(self, "Başarılı", "Veriler Excel dosyasına başarıyla kaydedildi.")

    def load_ekip_data(self):
        self.cmbKullananEkip.clear()

        self.islem.execute("SELECT ekipAdi FROM ekipler")
        ekipler = self.islem.fetchall()

        for ekip in ekipler:
            self.cmbKullananEkip.addItem(ekip[0])

        self.baglanti.commit()      

    def kullanim_detay_penceresi(self):
        try:
            self.baglanti = sqlite3.connect("urunler.db")
            self.islem = self.baglanti.cursor()
            selected_row = self.tableWidget.currentRow()
            if selected_row == -1:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Lutfen Detayini Gormek Istediginiz Malzemeyi Tablodan Seciniz!!")
                msg.setWindowTitle("Uyari")
                msg.exec_()
            else:   

                global deneme
                if self.tableWidget.item(selected_row, 1).text() == "Fiber Kablo" or self.tableWidget.item(selected_row, 1).text() == "Bakir Kablo":
                    self.a= "k"+str(self.tableWidget.item(selected_row, 3).text()).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").lower() + "" +str(self.tableWidget.item(selected_row, 5).text()).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower()
                    deneme = self.a
                else:
                    self.a= "m"+str(self.tableWidget.item(selected_row, 3).text()).replace(" ", "").replace("-","").replace(".","").replace(",","").replace("x","").replace("(","").replace(")","").replace("/","").replace("+","").lower()
                    deneme = self.a   
                    
                self.yeni_pencere= App2()
                self.yeni_pencere.show()
        except:
            self.show_warning_message("LUTFEN KULLANIM DETAYINI GORMEK ISTEDIGINIZ MALZEMEYI TABLODAN SECINIZ")
            
    def load_konum_data(self):
        self.cmbKonum.clear()

        self.islem.execute("SELECT konumAdi FROM konumlar")
        konumlar = self.islem.fetchall()

        for konum in konumlar:
            self.cmbKonum.addItem(konum[0])

        self.baglanti.commit() 
           
    def konum_ekle(self):
        konumadi= self.lneEklenecekKonum.text()        
        if konumadi == "":
            self.show_warning_message("LUTFEN BIR KONUM GIRINIZ!!")
            return
        
        self.islem.execute("SELECT konumAdi FROM konumlar WHERE konumAdi = ?", (konumadi,))
        konum = self.islem.fetchone()

        if konum:
            self.show_warning_message("BOYLE BIR KONUM MEVCUT!!")

            
        else:
            self.islem.execute("INSERT INTO konumlar (konumAdi) VALUES (?)", (konumadi,))
            self.baglanti.commit()   
            self.statusbar.showMessage("Konum Ekleme İşlemi Başarılı", 10000)
            self.load_konum_data()
        
        self.temizle()

    def konum_cikart(self):
        try:
            silinmek_istenen_metin = self.lneEklenecekKonum.text()
            self.islem.execute("SELECT * FROM konumlar WHERE konumAdi = ?", (silinmek_istenen_metin,))
            konum = self.islem.fetchone()

            if konum:
                self.islem.execute("DELETE FROM konumlar WHERE konumAdi = ?", (silinmek_istenen_metin,))
                self.baglanti.commit()
                self.statusbar.showMessage("Konum Silme İşlemi Başarılı", 10000)
                self.load_konum_data()
                self.temizle()
            else:
                self.show_warning_message("KONUM BULUNAMADI!!")

        except:
            self.show_warning_message("KONUM BULUNAMADI!!")
            self.temizle()

    def ekip_ekle(self):
        try:
            ekipadi= self.lneEklenecekEkip.text()        
            if ekipadi == "":
                self.show_warning_message("LUTFEN BIR EKIP ADI GIRINIZ!!")
                return
            
            self.islem.execute("SELECT ekipAdi FROM ekipler WHERE ekipAdi = ?", (ekipadi,))
            ekip = self.islem.fetchone()

            if ekip:
                self.show_warning_message("BOYLE BIR EKIP MEVCUT!!")

            
            else:
                if self.cbxEkip.isChecked():
                    sevk_ekibi_degeri = 1
                else:
                    sevk_ekibi_degeri = 0
            ekipekle="insert into ekipler (ekipAdi, sevkEkibi) values(?,?)"
            self.islem.execute(ekipekle,(ekipadi,sevk_ekibi_degeri)) 

            self.statusbar.showMessage("Ekip Ekleme İşlemi Başarılı", 10000)
            self.load_ekip_data()
            
            self.temizle()
        except:
            self.show_warning_message("EKIP BULUNAMADI!!")
            self.temizle()

    def ekip_cikart(self):
        try:
            silinmek_istenen_metin = self.lneEklenecekEkip.text()
            self.islem.execute("SELECT * FROM ekipler WHERE ekipAdi = ?", (silinmek_istenen_metin,))
            konum = self.islem.fetchone()

            if konum:
                self.islem.execute("DELETE FROM ekipler WHERE ekipAdi = ?", (silinmek_istenen_metin,))
                self.baglanti.commit()
                self.statusbar.showMessage("Ekip Silme Islemi Basarili", 10000)
                self.load_konum_data()
                self.temizle()
            else:
                self.show_warning_message("EKIP BULUNAMADI!!")

        except:
            self.show_warning_message("EKIP BULUNAMADI!!")

    def sayim_ekle(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        id_no2= self.lneIdNo_2.text()
        sayim= self.lneSayim.text()
        update_sorgu = """
                            UPDATE stok
                            SET sayim = ?
                            WHERE id = ?
                            """
        self.islem.execute(update_sorgu, (sayim, id_no2))
        self.baglanti.commit()
        self.kayit_listele()       

class App2(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('kullanimDetay.ui', self)
        self.setWindowTitle("Kullanim Icerigi")
        self.kayit_listele()
        self.icon_path = os.path.join(current_dir, "excell.png")
        self.excel_icon = QIcon(self.icon_path)
        self.btnExcell.setIcon(self.excel_icon)
        self.btnExcell.clicked.connect(self.export_to_excel)
        self.btnGuncelle.clicked.connect(self.guncelle)
        self.pushButton_2.clicked.connect(self.kullanim_sil)
        
    def kayit_listele(self):
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.tblDetay.clear()
        self.tblDetay.setHorizontalHeaderLabels(("Islem No","Islem Turu","Makara No", "Irsaliye No", "IrsaliyeTarihi", "Cikis Tarihi", "Proje Adi", "Kroki No", "Kullanan Ekip", "Sevk Miktari","Aciklama","Hakedis", "Son Guncelleme Tarihi","Cbs Id1","Cbs Id2","Cbs Id3","Cbs Id4","Cbs Id5"))
        global deneme
        self.sorgu = "select * from " + deneme
        self.islem.execute(self.sorgu,)
        
        for indexSatir, kayitNumarasi in enumerate(self.islem):
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.tblDetay.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

        self.islem.execute("SELECT ekipAdi FROM ekipler WHERE sevkEkibi = 1")
        sevk_ekipleri = [ekip[0] for ekip in self.islem.fetchall()]
        
        sevk_ekipleri = str(sevk_ekipleri)[1:-1]
        self.baglanti.commit()
        sorgu1 = "SELECT SUM(SevkMiktari) FROM "+deneme+" WHERE KullananEkip IN ("+ sevk_ekipleri +") AND IslemTuru = 'CIKIS'"
        self.islem.execute(sorgu1)
        
        toplam_eregliye_sevk_miktari = self.islem.fetchone()[0]
        
        if toplam_eregliye_sevk_miktari is None:
            toplam_eregliye_sevk_miktari = 0
        else:
            toplam_eregliye_sevk_miktari = int(int(toplam_eregliye_sevk_miktari) * (-1))
        
        sorgu2 = "SELECT SUM(SevkMiktari) FROM "+ str(deneme) +" WHERE IslemTuru = 'CIKIS'"
        self.islem.execute(sorgu2)
        
        toplam_kullanilan_miktar = self.islem.fetchone()[0]
        if toplam_kullanilan_miktar is None:
            toplam_kullanilan_miktar = 0
        else:      
            toplam_kullanilan_miktar = int(toplam_kullanilan_miktar)* (-1)
            toplam_kullanilan_miktar = toplam_kullanilan_miktar - toplam_eregliye_sevk_miktari
        
        sevk = toplam_eregliye_sevk_miktari
        kullanilan = toplam_kullanilan_miktar
        
        sorgu3 = "SELECT SUM(SevkMiktari) FROM "+ str(deneme) +" WHERE IslemTuru = 'GIRIS'"
        self.islem.execute(sorgu3)
        
        toplam = int(self.islem.fetchone()[0])
        
        kalan= toplam - sevk - kullanilan
        # kalan = int(a_list[gelen_miktar_index]) - toplam_eregliye_sevk_miktari - toplam_kullanilan_miktar
        self.baglanti.commit()
        global numara
        
        update_sorgu = "UPDATE stok SET kullanilanMiktar=?,  sevkMiktari=?, kalanMiktar=? WHERE id= ?"
        self.islem.execute(update_sorgu, (kullanilan, sevk, kalan, int(numara)))
        self.baglanti.commit()
        
    def kullanim_sil(self):
        global deneme
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        selected_row = self.tblDetay.currentRow()
        if selected_row == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Lütfen silmek istediğiniz satırı seçin!!")
            msg.setWindowTitle("Uyarı")
            msg.exec_()
        else:   
            result = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)
            
            if result == QMessageBox.Yes:               
                if selected_row != -1:
                    secilen_id = self.tblDetay.item(selected_row, 0).text()  # İd'nin bulunduğu sütun indeksi
                    try:
                        silme_sorgu = "DELETE FROM "+deneme+" WHERE islemNo = ?"
                        self.islem.execute(silme_sorgu, (secilen_id,))
                        self.baglanti.commit()
                        self.statusbar.showMessage("Kayıt Silme İşlemi Başarılı", 10000)
                        self.kayit_listele()
                        MyApp().kayit_listele()

                    except Exception as error:
                        self.statusbar.showMessage("Kayıt Silinirken Hata Oluştu === " + str(error))

            else:
                self.statusbar.showMessage("Silme İşlemi İptal Edildi")
                
    def guncelle(self):
        
        islemNo= self.lneIslemNo.text()
        krokiNo= self.lneKrokiNo.text()
        hakedis= self.cmbHakedis.currentText()
        cbsid= self.lneIslemNo_2.text()
        aciklama= self.lineEdit.text()
        global deneme
        
        if krokiNo is None:
            krokiNo ="-"
        if cbsid is None:
            cbsid=0
        if aciklama is None:
            aciklama = ""
        self.sorgu = "select * from "+str(deneme)+" where islemNo = ?"
        self.islem.execute(self.sorgu, (islemNo,))
        b = self.islem.fetchone()
        
        if b:
            a_list = list(b)
        else:
            return
        
        if a_list[4] != "-":
            krokiNo = a_list[4]
        
        aciklama += str(a_list[10])
        
        cbsid1= a_list[13]
        cbsid2= a_list[14]
        cbsid3= a_list[15]
        cbsid4= a_list[16]
        cbsid5= a_list[17]
        
        
        if cbsid1 == 0:
            cbsid1 = cbsid
        elif cbsid1 != 0 and cbsid2 == 0:
            cbsid2 = cbsid
        elif cbsid1 != 0 and cbsid2 != 0 and cbsid3 == 0:
            cbsid3 = cbsid
        elif cbsid1 != 0 and cbsid2 != 0 and cbsid3 != 0 and cbsid4 == 0:
            cbsid4 = cbsid
        elif cbsid1 != 0 and cbsid2 != 0 and cbsid3 != 0 and cbsid4 != 0 and cbsid5 == 0:
            cbsid5 = cbsid
        else:
            self.statusbar.showMessage("CBS ID KISMI DOLMUSTUR... KAYIT EKLENEMEZ")
        
        guncelleme = "UPDATE "+ str(deneme)+" SET krokiNo= ?, aciklama = ?, hakedis= ?, cbsid1= ?, cbsid2= ?, cbsid3= ?, cbsid4= ?, cbsid5= ? where islemNo = ? "        
        self.islem.execute(guncelleme, (krokiNo, aciklama, hakedis, cbsid1, cbsid2, cbsid3, cbsid4, cbsid5, islemNo))
        self.baglanti.commit()
      
        self.kayit_listele()
        
    def export_to_excel(self):
        global deneme
        rows = self.tblDetay.rowCount()
        columns = self.tblDetay.columnCount()
        veriler = []

        for row in range(rows):
            veri = []
            for col in range(columns):
                item = self.tblDetay.item(row, col)
                if item is not None:
                    veri.append(item.text())
                else:
                    veri.append('')
            veriler.append(veri)

        if not veriler:
            self.show_warning_message("Veri bulunamadi.")
            return

        columns = ["Islem No","Islem Turu","Makara No", "Irsaliye No", "IrsaliyeTarihi", "Cikis Tarihi", "Proje Adi", "Kroki No", "Kullanan Ekip", "Sevk Miktari","Aciklama","Hakedis", "Son Guncelleme Tarihi","Cbs Id1","Cbs Id2","Cbs Id3","Cbs Id4","Cbs Id5"]
        
        df = pd.DataFrame(veriler, columns=columns)
        bugunun_tarihi = datetime.now().strftime("%Y-%m-%d")

        dosya_adi, _ = QFileDialog.getSaveFileName(self, "Excel Dosyasını Kaydet", str(deneme)+ " kullanim detayi ("+ str(bugunun_tarihi) +").xlsx", "Excel Dosyası (*.xlsx)")

        if not dosya_adi:
            return

        df.to_excel(dosya_adi, index=False)
        QMessageBox.information(self, "Başarılı", "Veriler Excel dosyasına başarıyla kaydedildi.")

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.load_ekip_data()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
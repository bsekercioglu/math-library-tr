"""
Doğal Dil Parser - Matematik Kütüphanesi
========================================

Bu modül kullanıcının doğal dilde yazdığı matematik sorularını
ayrıştırır ve ilgili modül ve fonksiyona yönlendirir.

Yazar: Matematik Kütüphanesi
"""

import re
from typing import Dict, List, Tuple, Optional


class DoğalDilParser:
    """Doğal dil sorgularını ayrıştıran sınıf"""
    
    def __init__(self):
        # Konu anahtar kelimeleri
        self.konu_anahtarlari = {
            "cebir": ["cebir", "denklem", "kök", "çarpan", "polinom", "faktör", "çöz", "=", "x²", "x^2", "kuadratik"],
            "geometri": ["geometri", "üçgen", "kare", "daire", "alan", "çevre", "hacim", "pisagor", "pitagor", "hipotenüs", 
                        "kenar", "kosinüs kuralı", "cosinus", "sinus kuralı", "dikdörtgen", "küp", "silindir", "küre",
                        "üçüncü kenar", "dik üçgen", "yay", "kesit", "koordinat"],
            "trigonometri": ["trigonometri", "sinüs", "kosinüs", "tanjant", "açı", "sin", "cos", "tan", "arcsin", "arccos", "arctan", "derece", "radyan"],
            "analiz": ["analiz", "türev", "integral", "limit", "sürekli"],
            "olasılık": ["olasılık", "istatistik", "dağılım", "ortalama", "varyans"]
        }
        
        # Alt konu anahtar kelimeleri
        self.alt_konu_anahtarlari = {
            "cebir": {
                "ikinci_dereceden": ["ikinci dereceden", "kuadratik", "x²", "x^2", "kök bul"],
                "carpanlara_ayirma": ["çarpan", "faktör", "çarpanlara ayır", "faktörel"]
            },
            "geometri": {
                "ucgen_hesaplama": ["üçgen", "pisagor", "pitagor", "hipotenüs", "dik üçgen", "üçüncü kenar", "kosinüs kuralı", "sinus kuralı"],
                "dortgen_hesaplama": ["kare", "dikdörtgen", "yamuk", "paralelkenar", "eşkenar dörtgen"],
                "daire_hesaplama": ["daire", "çember", "yay", "kesit", "yarıçap", "çap"],
                "alan_hesaplama": ["alan", "yüzey", "m²", "metrekare"],
                "cevre_hesaplama": ["çevre", "kenar", "uzunluk"],
                "hacim_hesaplama": ["hacim", "küp", "silindir", "küre", "prizma", "piramit", "m³"],
                "koordinat_geometri": ["koordinat", "nokta", "doğru", "eğim", "mesafe"]
            },
            "trigonometri": {
                "fonksiyon_hesaplama": ["sin", "cos", "tan", "sinüs", "kosinüs", "tanjant"],
                "ters_fonksiyon": ["arcsin", "arccos", "arctan", "ters"],
                "aci_donusumu": ["derece", "radyan", "dönüştür", "çevir"],
                "denklem_cozme": ["denklem", "çöz", "=", "sin(x)", "cos(x)", "tan(x)"],
                "ifade_hesaplama": ["hesapla", "+", "-", "*", "/", "toplam", "fark"],
                "karma_denklem_cozme": ["sin(x)", "cos(x)", "tan(x)", "ise", "x hesapla"],
                "turev_integral": ["türev", "integral", "d/dx", "∫"]
            },
            "analiz": {
                "turev": ["türev", "diferansiyel", "d/dx", "türevini al"],
                "integral": ["integral", "∫", "integrali", "belirsiz", "belirli"],
                "limit": ["limit", "yaklaşır", "sonsuza", "∞"]
            },
            "olasılık": {
                "faktoriyel": ["faktöriyel", "n!", "!"],
                "permutasyon": ["permutasyon", "düzenleme", "P(", "sıralama"],
                "kombinasyon": ["kombinasyon", "seçim", "C(", "choose"],
                "temel_olasilik": ["olasılık", "şans", "ihtimal", "/"],
                "binom_dagilimi": ["binom", "dağılım", "deneme", "başarı"]
            }
        }
        
        # İşlem anahtar kelimeleri
        self.islem_anahtarlari = {
            "çöz": ["çöz", "bul", "hesapla", "kök", "sonuç"],
            "çarpanlara_ayır": ["çarpan", "faktör", "ayır"],
            "grafikle": ["çiz", "grafik", "görselleştir"],
            "trigonometrik_hesapla": ["hesapla", "değer", "sin", "cos", "tan"],
            "geometri_hesapla": ["alan", "çevre", "hacim", "kenar", "hipotenüs", "üçüncü kenar", "pisagor", "kosinüs kuralı"],
            "ters_trigonometrik": ["arcsin", "arccos", "arctan", "ters"],
            "aci_donustur": ["dönüştür", "çevir", "derece", "radyan"],
            "trigonometrik_ifade_hesapla": ["hesapla", "+", "-", "toplam", "fark", "ifade"],
            "turev_hesapla": ["türev", "türevini", "d/dx", "diferansiyel"],
            "integral_hesapla": ["integral", "integrali", "∫", "belirsiz", "belirli"],
            "faktoriyel_hesapla": ["faktöriyel", "n!", "!"],
            "permutasyon_hesapla": ["permutasyon", "düzenleme", "P(", "sıralama"],
            "kombinasyon_hesapla": ["kombinasyon", "seçim", "C(", "choose"],
            "olasilik_hesapla": ["olasılık", "şans", "ihtimal"],
            "geometri_hesapla": ["alan", "çevre", "hacim", "pisagor"]
        }
    
    def sorgu_analiz_et(self, kullanici_girisi: str) -> Dict[str, any]:
        """
        Kullanıcı girdisini analiz eder ve hangi modül/fonksiyona 
        yönlendirileceğini belirler.
        
        Args:
            kullanici_girisi (str): Kullanıcının yazdığı soru
        
        Returns:
            Dict: Analiz sonuçları
        """
        girdi_temiz = kullanici_girisi.lower().strip()
        
        # Denklem tespit et
        denklem = self._denklem_tespit_et(girdi_temiz)
        
        # Trigonometri değer tespit et
        trig_ifade = self._trigonometri_tespit_et(girdi_temiz)
        
        # Konu tespit et
        konu = self._konu_tespit_et(girdi_temiz)
        
        # Alt konu tespit et
        alt_konu = self._alt_konu_tespit_et(girdi_temiz, konu)
        
        # İşlem tespit et
        islem = self._islem_tespit_et(girdi_temiz)
        
        # Güven skoru hesapla
        guven_skoru = self._guven_skoru_hesapla(girdi_temiz, konu, alt_konu, islem)
        
        return {
            "orijinal_girdi": kullanici_girisi,
            "konu": konu,
            "alt_konu": alt_konu,
            "islem": islem,
            "denklem": denklem,
            "trig_ifade": trig_ifade,
            "guven_skoru": guven_skoru,
            "oneri": self._oneri_olustur(konu, alt_konu, islem, denklem or trig_ifade, kullanici_girisi)
        }
    
    def _denklem_tespit_et(self, metin: str) -> Optional[str]:
        """Metinden matematik denklemini çıkarır (cebir için)"""
        # Trigonometrik fonksiyonlar varsa, buradan tespit etme
        if any(trig in metin for trig in ["sin", "cos", "tan", "sinüs", "kosinüs", "tanjant"]):
            return None
            
        # Eşittir işareti varsa, basit yaklaşım kullan
        if "=" in metin:
            # = ile böl ve sol tarafı al
            parts = metin.split("=")
            if len(parts) >= 2:
                sol_taraf = parts[0].strip()
                sag_taraf = parts[1].split()[0].strip() if parts[1].strip() else "0"
                
                # Matematik ifadesi kontrol et (sadece cebir için)
                if any(char in sol_taraf for char in ["x", "²", "^"]) and not any(trig in sol_taraf for trig in ["sin", "cos", "tan"]):
                    return f"{sol_taraf} = {sag_taraf}"
        
        # Çarpanlara ayırma için ifade tespit et (= olmadan)
        if any(kelime in metin for kelime in ["çarpan", "faktör", "ayır"]):
            # x² - 9 gibi ifadeleri bul
            carpan_kaliplari = [
                r'[x-z]²[\s]*[\+\-][\s]*[\d]+',  # x² - 9
                r'[\d]*[x-z]²[\s]*[\+\-][\s]*[\d]+',  # 2x² - 8
                r'[x-z]\^2[\s]*[\+\-][\s]*[\d]+',  # x^2 - 9
                r'[\d]*[x-z]\^2[\s]*[\+\-][\s]*[\d]+',  # 2x^2 - 8
            ]
            
            for kalip in carpan_kaliplari:
                eslesen = re.search(kalip, metin)
                if eslesen:
                    return eslesen.group().strip()
        
        return None
    
    def _trigonometri_tespit_et(self, metin: str) -> Optional[str]:
        """Metinden trigonometrik ifadeleri çıkarır"""
        # ÖNCE karmaşık trigonometrik ifade arama (birden fazla fonksiyon)
        trig_fonksiyonlar = ['sin', 'cos', 'tan', 'sinüs', 'kosinüs', 'tanjant']
        fonksiyon_sayisi = 0
        for fonk in trig_fonksiyonlar:
            fonksiyon_sayisi += len(re.findall(fonk, metin))
        
        # = varsa ve x içeriyorsa, karma denklem kontrolü yapılmalı
        if "=" in metin and "x" in metin:
            # Bu karma denklem olabilir, devam et
            pass
        elif fonksiyon_sayisi > 1 or any(op in metin for op in ["+", "-", "*", "/"]):
            # Karmaşık ifade - tüm metni döndür
            if "=" in metin:
                return metin.split("=")[0].strip()
            else:
                return metin.strip()
        
        # Karma trigonometrik denklem arama (x + sabit fonksiyonlar)
        karma_denklem_kaliplari = [
            r'(sin|cos|tan)\s*\(\s*x\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*\d+\s*\)\s*=\s*[\d.]+',  # sin(x) + cos(45) = 1.20
            r'(sin|cos|tan)\s*\(\s*\d+\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*x\s*\)\s*=\s*[\d.]+',  # cos(45) + sin(x) = 1.20
        ]
        
        for kalip in karma_denklem_kaliplari:
            eslesen = re.search(kalip, metin)
            if eslesen:
                # Karma denklem tespit edildi - tüm denklemi döndür
                if "=" in metin:
                    # = işaretinden önce ve sonrasını al
                    return metin.strip()
                else:
                    return metin.strip()
        
        # Basit trigonometrik denklem arama
        trig_denklem_kaliplari = [
            r'(sin|cos|tan)\s*\(\s*x\s*\)\s*=\s*[\d.-]+',  # sin(x) = 0.5
            r'(sin|cos|tan)\s*x\s*=\s*[\d.-]+',  # sinx = 0.5
        ]
        
        for kalip in trig_denklem_kaliplari:
            eslesen = re.search(kalip, metin)
            if eslesen:
                return eslesen.group().strip()
        
        # Tekil trigonometrik fonksiyon kalıpları
        trig_kaliplari = [
            r'(sin|cos|tan|sinüs|kosinüs|tanjant)\s*\(\s*(\d+)\s*\)',  # sin(30)
            r'(sin|cos|tan|sinüs|kosinüs|tanjant)\s*(\d+)',  # sin30
            r'(arcsin|arccos|arctan|asin|acos|atan)\s*\(\s*([\d.,]+)\s*\)',  # arcsin(0.5)
            r'(\d+)\s*(derece|°)\s*(radyan|rad)',  # 90 derece radyan
            r'(\d+)\s*(radyan|rad)\s*(derece|°)',  # 1.57 radyan derece
        ]
        
        for kalip in trig_kaliplari:
            eslesen = re.search(kalip, metin)
            if eslesen:
                return eslesen.group().strip()
        
        # Basit trigonometrik fonksiyon arama
        for fonk in trig_fonksiyonlar + ['arcsin', 'arccos', 'arctan']:
            if fonk in metin:
                # Sayı ara
                sayi_eslesen = re.search(r'\d+(?:\.\d+)?', metin)
                if sayi_eslesen:
                    return f"{fonk}({sayi_eslesen.group()})"
        
        return None
    
    def _fonksiyon_cikar(self, metin: str) -> str:
        """Metinden matematik fonksiyonunu çıkarır"""
        # Türev/integral kelimelerini temizle
        temiz_metin = metin.lower()
        gereksiz_kelimeler = ["türevini", "türev", "al", "integralini", "integrini", "integral", "hesapla", "nin", "nın", "bul", "çöz"]
        for kelime in gereksiz_kelimeler:
            temiz_metin = temiz_metin.replace(kelime, "")
        
        temiz_metin = temiz_metin.strip()
        
        # x² -> x**2 gibi dönüşümler
        temiz_metin = temiz_metin.replace("²", "**2")
        temiz_metin = temiz_metin.replace("³", "**3")
        
        return temiz_metin if temiz_metin else "x"
    
    def _sayi_cikar(self, metin: str) -> int:
        """Metinden sayı çıkarır"""
        import re
        # ! işaretinden önceki sayıyı bul
        eslesen = re.search(r'(\d+)!', metin)
        if eslesen:
            return int(eslesen.group(1))
        
        # Genel sayı arama
        eslesen = re.search(r'\d+', metin)
        if eslesen:
            return int(eslesen.group())
        
        return 5  # Varsayılan
    
    def _nr_cikar(self, metin: str) -> tuple:
        """Metinden n,r değerlerini çıkarır"""
        import re
        
        # P(n,r) veya C(n,r) formatı
        eslesen = re.search(r'[PC]\((\d+),(\d+)\)', metin)
        if eslesen:
            return int(eslesen.group(1)), int(eslesen.group(2))
        
        # Sayıları bul
        sayilar = re.findall(r'\d+', metin)
        if len(sayilar) >= 2:
            return int(sayilar[0]), int(sayilar[1])
        elif len(sayilar) == 1:
            return int(sayilar[0]), int(sayilar[0])//2
        
        return 5, 3  # Varsayılan
    
    def _geometri_parametreleri_cikar(self, metin: str) -> dict:
        """Metinden geometri parametrelerini çıkarır"""
        import re
        parametreler = {}
        
        # Sayıları bul
        sayilar = re.findall(r'\d+(?:\.\d+)?', metin)
        sayilar = [float(s) for s in sayilar]
        
        # Açı değerlerini tespit et (derece)
        aci_kaliplari = [r'(\d+(?:\.\d+)?)°', r'(\d+(?:\.\d+)?)\s*derece', r'C=(\d+(?:\.\d+)?)']
        for kalip in aci_kaliplari:
            eslesen = re.search(kalip, metin, re.IGNORECASE)
            if eslesen:
                parametreler['aci_c'] = float(eslesen.group(1))
                break
        
        # Dik üçgen tespiti
        if any(kelime in metin.lower() for kelime in ['dik üçgen', 'pisagor', 'pitagor']):
            parametreler['dik_ucgen'] = True
        
        # Kenar parametreleri
        if len(sayilar) >= 2:
            parametreler['a'] = sayilar[0]
            parametreler['b'] = sayilar[1]
            if len(sayilar) >= 3:
                parametreler['c'] = sayilar[2]
        elif len(sayilar) == 1:
            # Tek sayı varsa (kare alan, daire yarıçapı vb.)
            if any(kelime in metin.lower() for kelime in ['kare', 'alan']):
                parametreler['kenar'] = sayilar[0]
            elif any(kelime in metin.lower() for kelime in ['daire', 'yarıçap', 'r=']):
                parametreler['yaricap'] = sayilar[0]
            elif any(kelime in metin.lower() for kelime in ['çap']):
                parametreler['cap'] = sayilar[0]
            else:
                parametreler['a'] = sayilar[0]
        
        # Spesifik parametreler için pattern matching
        r_pattern = re.search(r'r=(\d+(?:\.\d+)?)', metin, re.IGNORECASE)
        if r_pattern:
            parametreler['yaricap'] = float(r_pattern.group(1))
        
        a_pattern = re.search(r'a=(\d+(?:\.\d+)?)', metin, re.IGNORECASE)
        if a_pattern:
            parametreler['a'] = float(a_pattern.group(1))
            
        b_pattern = re.search(r'b=(\d+(?:\.\d+)?)', metin, re.IGNORECASE)
        if b_pattern:
            parametreler['b'] = float(b_pattern.group(1))
        
        return parametreler
    
    def _konu_tespit_et(self, metin: str) -> str:
        """Metinden ana konuyu tespit eder"""
        # Öncelikli analiz tespit edilecek kelimeler
        analiz_oncelikli = ["türev", "türevini", "integral", "integralini", "d/dx", "∫"]
        for kelime in analiz_oncelikli:
            if kelime in metin.lower():
                return "analiz"
        
        # Olasılık öncelikli tespit
        olasilik_oncelikli = ["faktöriyel", "!", "permutasyon", "kombinasyon", "P(", "C("]
        for kelime in olasilik_oncelikli:
            if kelime in metin:
                return "olasılık"
        
        # Normal konu tespiti
        en_yuksek_skor = 0
        tespit_edilen_konu = "belirsiz"
        
        for konu, anahtarlar in self.konu_anahtarlari.items():
            skor = 0
            for anahtar in anahtarlar:
                if anahtar in metin:
                    skor += 1
            
            if skor > en_yuksek_skor:
                en_yuksek_skor = skor
                tespit_edilen_konu = konu
        
        return tespit_edilen_konu
    
    def _alt_konu_tespit_et(self, metin: str, ana_konu: str) -> str:
        """Metinden alt konuyu tespit eder"""
        if ana_konu == "belirsiz" or ana_konu not in self.alt_konu_anahtarlari:
            return "belirsiz"
        
        en_yuksek_skor = 0
        tespit_edilen_alt_konu = "belirsiz"
        
        for alt_konu, anahtarlar in self.alt_konu_anahtarlari[ana_konu].items():
            skor = 0
            for anahtar in anahtarlar:
                if anahtar in metin:
                    skor += 1
            
            if skor > en_yuksek_skor:
                en_yuksek_skor = skor
                tespit_edilen_alt_konu = alt_konu
        
        return tespit_edilen_alt_konu
    
    def _islem_tespit_et(self, metin: str) -> str:
        """Metinden yapılacak işlemi tespit eder"""
        # Öncelikli kontroller
        if "integral" in metin.lower():
            return "integral_hesapla"
        if "türev" in metin.lower():
            return "turev_hesapla"
        if "!" in metin:
            return "faktoriyel_hesapla"
        if "P(" in metin:
            return "permutasyon_hesapla"
        if "C(" in metin:
            return "kombinasyon_hesapla"
        
        # Normal işlem tespiti
        en_yuksek_skor = 0
        tespit_edilen_islem = "belirsiz"
        
        for islem, anahtarlar in self.islem_anahtarlari.items():
            skor = 0
            for anahtar in anahtarlar:
                if anahtar in metin:
                    skor += 1
            
            if skor > en_yuksek_skor:
                en_yuksek_skor = skor
                tespit_edilen_islem = islem
        
        return tespit_edilen_islem
    
    def _guven_skoru_hesapla(self, metin: str, konu: str, alt_konu: str, islem: str) -> float:
        """Analiz güvenilirlik skoru hesaplar (0-1 arası)"""
        skor = 0.0
        
        # Konu tespit skoru
        if konu != "belirsiz":
            skor += 0.3
        
        # Alt konu tespit skoru
        if alt_konu != "belirsiz":
            skor += 0.3
        
        # İşlem tespit skoru
        if islem != "belirsiz":
            skor += 0.2
        
        # Denklem/trigonometri ifade varlığı skoru
        if self._denklem_tespit_et(metin) or self._trigonometri_tespit_et(metin):
            skor += 0.2
        
        return min(skor, 1.0)
    
    def _oneri_olustur(self, konu: str, alt_konu: str, islem: str, ifade: Optional[str], orijinal_girdi: str) -> Dict[str, any]:
        """Analiz sonucuna göre işlem önerisi oluşturur"""
        
        # ÖNCELİKLE analiz konusu kontrol et
        if konu == "analiz" or islem in ["turev_hesapla", "integral_hesapla"]:
            if islem == "integral_hesapla" or "integral" in str(ifade).lower():
                # İntegral işlemi
                return {
                    "modül": "analiz", 
                    "fonksiyon": "integral_hesapla",
                    "parametreler": {},
                    "açıklama": "Fonksiyonun integrali hesaplanacak"
                }
            elif islem == "turev_hesapla" or "türev" in str(ifade).lower():
                # Türev işlemi
                return {
                    "modül": "analiz",
                    "fonksiyon": "turev_hesapla",
                    "parametreler": {},
                    "açıklama": "Fonksiyonun türevi hesaplanacak"
                }
            else:
                # Analiz alt konusuna göre karar ver
                if alt_konu == "integral":
                    return {
                        "modül": "analiz",
                        "fonksiyon": "integral_hesapla",
                        "parametreler": {},
                        "açıklama": "Fonksiyonun integrali hesaplanacak"
                    }
                else:
                    # Varsayılan türev
                    return {
                        "modül": "analiz",
                        "fonksiyon": "turev_hesapla",
                        "parametreler": {},
                        "açıklama": "Fonksiyonun türevi hesaplanacak"
                    }
        
        # Olasılık konusu kontrol et
        elif konu == "olasılık" or islem in ["faktoriyel_hesapla", "permutasyon_hesapla", "kombinasyon_hesapla"]:
            if islem == "faktoriyel_hesapla" or "faktöriyel" in islem or "!" in str(ifade):
                # Ana sistemde orijinal girdiden çıkaracağız
                return {
                    "modül": "olasılık",
                    "fonksiyon": "faktoriyel",
                    "parametreler": {},
                    "açıklama": "Faktöriyel hesaplanacak"
                }
            elif islem == "permutasyon_hesapla" or "permutasyon" in islem or "P(" in str(ifade):
                # Ana sistemde orijinal girdiden çıkaracağız
                return {
                    "modül": "olasılık",
                    "fonksiyon": "permutasyon",
                    "parametreler": {},
                    "açıklama": "Permutasyon hesaplanacak"
                }
            elif islem == "kombinasyon_hesapla" or "kombinasyon" in islem or "C(" in str(ifade):
                # Ana sistemde orijinal girdiden çıkaracağız
                return {
                    "modül": "olasılık",
                    "fonksiyon": "kombinasyon",
                    "parametreler": {},
                    "açıklama": "Kombinasyon hesaplanacak"
                }
        
        # Önce KARMA trigonometrik denklem kontrol et
        if ifade and "=" in str(ifade):
            import re
            karma_denklem_kaliplari = [
                r'(sin|cos|tan)\s*\(\s*x\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*\d+\s*\)',  # sin(x) + cos(45)
                r'(sin|cos|tan)\s*\(\s*\d+\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*x\s*\)',  # cos(45) + sin(x)
            ]
            
            for kalip in karma_denklem_kaliplari:
                if re.search(kalip, str(ifade)):
                    return {
                        "modül": "trigonometri",
                        "fonksiyon": "karma_trigonometrik_denklem_coz",
                        "parametreler": {"denklem": ifade},
                        "açıklama": "Karma trigonometrik denklem çözülecek"
                    }
        
        # Sonra basit trigonometrik denklem kontrol et
        if ifade and any(trig in str(ifade) for trig in ["sin(x)", "cos(x)", "tan(x)", "sinx", "cosx", "tanx"]) and "=" in str(ifade):
            return {
                "modül": "trigonometri",
                "fonksiyon": "trigonometrik_denklem_coz",
                "parametreler": {"denklem": ifade},
                "açıklama": "Trigonometrik denklem çözülecek"
            }
        
        if konu == "cebir" and ifade:
            if islem == "çarpanlara_ayır" or "çarpan" in islem or "faktör" in islem:
                return {
                    "modül": "cebir", 
                    "fonksiyon": "carpanlara_ayir",
                    "parametreler": {"ifade": ifade},
                    "açıklama": "İfade çarpanlarına ayrılacak"
                }
            elif "=" in str(ifade) or islem == "çöz":
                return {
                    "modül": "cebir",
                    "fonksiyon": "ikinci_dereceden_coz", 
                    "parametreler": {"denklem": ifade},
                    "açıklama": "İkinci dereceden denklem çözülecek"
                }
        
        elif konu == "trigonometri" and ifade:
            # ÖNCELİKLE karma trigonometrik denklem kontrolü
            karma_denklem_kaliplari = [
                r'(sin|cos|tan)\s*\(\s*x\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*\d+\s*\)',  # sin(x) + cos(45)
                r'(sin|cos|tan)\s*\(\s*\d+\s*\)\s*[\+\-]\s*(sin|cos|tan)\s*\(\s*x\s*\)',  # cos(45) + sin(x)
            ]
            
            # Karma denklem kontrolü
            for kalip in karma_denklem_kaliplari:
                if re.search(kalip, str(ifade)) and "=" in str(ifade):
                    return {
                        "modül": "trigonometri",
                        "fonksiyon": "karma_trigonometrik_denklem_coz",
                        "parametreler": {"denklem": ifade},
                        "açıklama": "Karma trigonometrik denklem çözülecek"
                    }
            
            # Karmaşık ifade kontrolü (birden fazla trigonometrik fonksiyon)
            trig_fonksiyonlar = ['sin', 'cos', 'tan', 'sinüs', 'kosinüs', 'tanjant']
            fonksiyon_sayisi = 0
            for fonk in trig_fonksiyonlar:
                fonksiyon_sayisi += len(re.findall(fonk, str(ifade)))
            
            if fonksiyon_sayisi > 1 and "=" not in str(ifade):
                return {
                    "modül": "trigonometri",
                    "fonksiyon": "trigonometrik_ifade_hesapla",
                    "parametreler": {"ifade": ifade},
                    "açıklama": "Karmaşık trigonometrik ifade hesaplanacak"
                }
            elif "=" in str(ifade) and any(x in str(ifade) for x in ["sin(x)", "cos(x)", "tan(x)", "sinx", "cosx", "tanx"]):
                return {
                    "modül": "trigonometri",
                    "fonksiyon": "trigonometrik_denklem_coz",
                    "parametreler": {"denklem": ifade},
                    "açıklama": "Trigonometrik denklem çözülecek"
                }
            elif alt_konu == "ters_fonksiyon" or any(x in str(ifade) for x in ["arcsin", "arccos", "arctan"]):
                return {
                    "modül": "trigonometri",
                    "fonksiyon": "ters_trigonometrik_hesapla",
                    "parametreler": {"ifade": ifade},
                    "açıklama": "Ters trigonometrik fonksiyon hesaplanacak"
                }
            elif alt_konu == "aci_donusumu" or any(x in str(ifade) for x in ["derece", "radyan", "dönüştür", "çevir"]):
                return {
                    "modül": "trigonometri",
                    "fonksiyon": "aci_donustur",
                    "parametreler": {"ifade": ifade},
                    "açıklama": "Açı birim dönüşümü yapılacak"
                }
            else:
                return {
                    "modül": "trigonometri",
                    "fonksiyon": "trigonometrik_hesapla",
                    "parametreler": {"ifade": ifade},
                    "açıklama": "Trigonometrik fonksiyon hesaplanacak"
                }
        
        # Geometri konusu kontrol et
        elif konu == "geometri" or islem == "geometri_hesapla":
            parametreler = self._geometri_parametreleri_cikar(orijinal_girdi)
            
            # Üçgen hesaplamaları
            if any(kelime in orijinal_girdi.lower() for kelime in ['pisagor', 'pitagor', 'hipotenüs', 'dik üçgen']):
                if parametreler.get('dik_ucgen') or 'dik' in orijinal_girdi.lower():
                    return {
                        "modül": "geometri",
                        "fonksiyon": "ucgen_hesaplama",
                        "parametreler": {"hesaplama_turu": "pisagor", **parametreler},
                        "açıklama": "Pisagor teoremi ile hipotenüs hesaplanacak"
                    }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['üçüncü kenar', '3. kenar', 'kosinüs kuralı']):
                return {
                    "modül": "geometri", 
                    "fonksiyon": "ucgen_hesaplama",
                    "parametreler": {"hesaplama_turu": "ucuncu_kenar", **parametreler},
                    "açıklama": "Üçüncü kenar hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['üçgen alan', 'triangle area']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "ucgen_hesaplama", 
                    "parametreler": {"hesaplama_turu": "alan", **parametreler},
                    "açıklama": "Üçgen alanı hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['üçgen çevre']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "ucgen_hesaplama",
                    "parametreler": {"hesaplama_turu": "cevre", **parametreler},
                    "açıklama": "Üçgen çevresi hesaplanacak"
                }
            
            # Dörtgen hesaplamaları
            elif any(kelime in orijinal_girdi.lower() for kelime in ['kare alan']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "dortgen_hesaplama",
                    "parametreler": {"sekil": "kare", "hesaplama": "alan", **parametreler},
                    "açıklama": "Kare alanı hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['kare çevre']):
                return {
                    "modül": "geometri", 
                    "fonksiyon": "dortgen_hesaplama",
                    "parametreler": {"sekil": "kare", "hesaplama": "cevre", **parametreler},
                    "açıklama": "Kare çevresi hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['dikdörtgen alan']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "dortgen_hesaplama", 
                    "parametreler": {"sekil": "dikdortgen", "hesaplama": "alan", **parametreler},
                    "açıklama": "Dikdörtgen alanı hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['dikdörtgen çevre']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "dortgen_hesaplama",
                    "parametreler": {"sekil": "dikdortgen", "hesaplama": "cevre", **parametreler}, 
                    "açıklama": "Dikdörtgen çevresi hesaplanacak"
                }
            
            # Daire hesaplamaları
            elif any(kelime in orijinal_girdi.lower() for kelime in ['daire alan']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "daire_hesaplama",
                    "parametreler": {"hesaplama": "alan", **parametreler},
                    "açıklama": "Daire alanı hesaplanacak"
                }
            
            elif any(kelime in orijinal_girdi.lower() for kelime in ['daire çevre']):
                return {
                    "modül": "geometri",
                    "fonksiyon": "daire_hesaplama", 
                    "parametreler": {"hesaplama": "cevre", **parametreler},
                    "açıklama": "Daire çevresi hesaplanacak"
                }
            
            # Genel geometri
            else:
                return {
                    "modül": "geometri",
                    "fonksiyon": "genel_hesaplama",
                    "parametreler": parametreler,
                    "açıklama": "Geometri hesaplama yapılacak"
                }
        
        return {
            "modül": "belirsiz",
            "fonksiyon": "belirsiz", 
            "parametreler": {},
            "açıklama": "Uygun işlem tespit edilemedi"
        }
    
    def ornek_sorgular_onerisi(self) -> List[str]:
        """Kullanıcıya örnek sorgular önerir"""
        return [
            "x² - 5x + 6 = 0 denkleminin köklerini bul",
            "2x² + 3x - 2 = 0 çöz",
            "x² - 9 çarpanlarına ayır",
            "x² + 4x + 4 faktörlerine ayır"
        ]


# Kullanım kolaylığı için global fonksiyon
def sorgu_analiz_et(kullanici_girisi: str) -> Dict[str, any]:
    """Kullanıcı girdisini analiz eder"""
    parser = DoğalDilParser()
    return parser.sorgu_analiz_et(kullanici_girisi)


# Test fonksiyonu
if __name__ == "__main__":
    # Test örnekleri
    test_sorguları = [
        "x² - 5x + 6 = 0 denkleminin köklerini bul",
        "ikinci dereceden denklem çöz: 2x² + 3x - 2 = 0",
        "x² - 9 çarpanlarına ayır",
        "kuadratik denklem köklerini hesapla"
    ]
    
    parser = DoğalDilParser()
    
    for sorgu in test_sorguları:
        print(f"\n--- Test: {sorgu} ---")
        sonuc = parser.sorgu_analiz_et(sorgu)
        
        print(f"Konu: {sonuc['konu']}")
        print(f"Alt Konu: {sonuc['alt_konu']}")
        print(f"İşlem: {sonuc['islem']}")
        print(f"Denklem: {sonuc['denklem']}")
        print(f"Güven Skoru: {sonuc['guven_skoru']}")
        print(f"Öneri: {sonuc['oneri']}")


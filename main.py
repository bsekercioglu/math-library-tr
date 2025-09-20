"""
Matematik Kütüphanesi - Ana Program
===================================

Bu program, kullanıcıların doğal dilde matematik soruları sormasına
ve adım adım çözümler almasına olanak tanır.

Desteklenen Konular:
- Cebir (İkinci dereceden denklemler, Çarpanlara ayırma)
- Geometri (Planlanan)
- Trigonometri (Planlanan)
- Analiz (Planlanan)
- Olasılık (Planlanan)

Yazar: Matematik Kütüphanesi
Sürüm: 1.0.0
"""

import sys
import os
from typing import Dict, Any

# Modül yollarını ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.cebir import ikinci_dereceden_coz, carpanlara_ayir
from modules.trigonometri import (trigonometrik_hesapla, ters_trigonometrik_hesapla, aci_donustur, 
                                 trigonometrik_denklem_coz, trigonometrik_ifade_hesapla, 
                                 karma_trigonometrik_denklem_coz, trigonometrik_turev_integral)
from modules.analiz import turev_hesapla, integral_hesapla, trigonometrik_analiz
from modules.olasilik import faktoriyel, permutasyon, kombinasyon, olasilik_hesapla, binom_dagilimi
from modules.geometri import ucgen_hesapla, dortgen_hesapla
from utils.parser import sorgu_analiz_et, DoğalDilParser
from utils.formatter import cozum_formatla, kisa_ozet, hata_mesaji_formatla


class MatematikKutuphanesi:
    """Ana matematik kütüphanesi sınıfı"""
    
    def __init__(self):
        self.parser = DoğalDilParser()
        self.surum = "1.0.0"
        self.desteklenen_konular = ["cebir", "trigonometri", "geometri", "analiz", "olasılık"]
        self.aktif = True
    
    def hosgeldin_mesaji(self):
        """Hoşgeldin mesajını gösterir"""
        print("=" * 60)
        print("   🧮 MATEMATİK KÜTÜPHANESİ 🧮")
        print(f"   Sürüm: {self.surum}")
        print("=" * 60)
        print()
        print("Merhaba! Matematik sorularınızı doğal dilde yazabilirsiniz.")
        print("Örnek sorular:")
        
        ornekler = self.parser.ornek_sorgular_onerisi()
        for i, ornek in enumerate(ornekler, 1):
            print(f"  {i}. {ornek}")
        
        print()
        print("Çıkmak için 'çıkış', 'exit' veya 'q' yazabilirsiniz.")
        print("Yardım için 'yardım' veya 'help' yazabilirsiniz.")
        print("=" * 60)
        print()
    
    def yardim_goster(self):
        """Yardım mesajını gösterir"""
        print("\n📚 YARDIM MENÜSÜ")
        print("-" * 40)
        print("🔹 Desteklenen Konular:")
        for konu in self.desteklenen_konular:
            durum = "✅" if konu in ["cebir", "trigonometri", "analiz", "olasılık"] else "🚧"
            print(f"   {durum} {konu.capitalize()}")
        
        print("\n🔹 Örnek Kullanım:")
        print("   Cebir:")
        print("   - 'x² - 5x + 6 = 0 denkleminin köklerini bul'")
        print("   - '2x² + 3x - 2 = 0 çöz'")
        print("   - 'x² - 9 çarpanlarına ayır'")
        print("   Trigonometri:")
        print("   - 'sin(30) hesapla'")
        print("   - 'cos 45 derece'")
        print("   - 'arcsin(0.5) bul'")
        print("   - '90 derece radyana çevir'")
        print("   - 'sin(x) = 0.5 çöz'")
        print("   - 'cos(x) = 0 denklemini çöz'")
        print("   - 'sin(30) + cos(45) hesapla'")
        print("   - 'sin(x) + cos(45) = 1.20 ise x hesapla'")
        print("   Analiz:")
        print("   - 'x² türevini al'")
        print("   - 'sin(x) integralini hesapla'")
        print("   Olasılık:")
        print("   - '5! hesapla'")
        print("   - 'C(10,3) kombinasyonu'")
        print("   - 'P(5,2) permutasyonu'")
        
        print("\n🔹 Komutlar:")
        print("   - 'çıkış' / 'exit' / 'q': Programdan çık")
        print("   - 'yardım' / 'help': Bu yardım menüsünü göster")
        print("   - 'temizle' / 'clear': Ekranı temizle")
        print("-" * 40)
    
    def ekran_temizle(self):
        """Ekranı temizler"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def sorgu_isle(self, kullanici_girisi: str) -> str:
        """
        Kullanıcı sorgusunu işler ve sonucu döndürür.
        
        Args:
            kullanici_girisi (str): Kullanıcının yazdığı soru
        
        Returns:
            str: Formatlanmış çözüm veya hata mesajı
        """
        try:
            # Girdiyi analiz et
            analiz = self.parser.sorgu_analiz_et(kullanici_girisi)
            
            # Güven skorunu kontrol et
            if analiz["guven_skoru"] < 0.3:
                oneriler = [
                    "Sorunuzu daha açık yazın",
                    "Matematik denklemini tam olarak yazın",
                    "Örnek sorulardan yararlanın",
                    "'yardım' yazarak desteklenen konuları görün"
                ]
                return hata_mesaji_formatla(
                    "Sorunuzu anlayamadım. Lütfen daha açık bir şekilde yazın.",
                    oneriler
                )
            
            # Öneriyi al
            oneri = analiz["oneri"]
            
            if oneri["modül"] == "belirsiz":
                return hata_mesaji_formatla(
                    "Bu tür soruları henüz çözemiyorum.",
                    ["Şu an sadece cebir konusunu destekliyorum",
                     "İkinci dereceden denklem soruları sorabilirsiniz"]
                )
            
            # Modüle göre işle
            if oneri["modül"] == "cebir":
                return self._cebir_isle(oneri, analiz)
            elif oneri["modül"] == "trigonometri":
                return self._trigonometri_isle(oneri, analiz)
            elif oneri["modül"] == "analiz":
                return self._analiz_isle(oneri, analiz)
            elif oneri["modül"] == "olasılık":
                return self._olasilik_isle(oneri, analiz)
            elif oneri["modül"] == "geometri":
                return self._geometri_isle(oneri, analiz)
            else:
                return hata_mesaji_formatla(
                    f"{oneri['modül'].capitalize()} modülü henüz hazır değil.",
                    ["Desteklenen modüller: cebir, trigonometri, analiz, olasılık"]
                )
        
        except Exception as e:
            return hata_mesaji_formatla(
                f"İşlem sırasında beklenmeyen bir hata oluştu: {str(e)}",
                ["Sorunuzu daha basit bir şekilde yazın",
                 "Matematik sembollerini kontrol edin"]
            )
    
    def _cebir_isle(self, oneri: Dict[str, Any], analiz: Dict[str, Any]) -> str:
        """Cebir modülü işlemlerini yönetir"""
        fonksiyon = oneri["fonksiyon"]
        parametreler = oneri["parametreler"]
        
        if fonksiyon == "ikinci_dereceden_coz":
            denklem = parametreler.get("denklem")
            if not denklem:
                return hata_mesaji_formatla(
                    "Denklem tespit edilemedi.",
                    ["Denklemi = işareti ile tam olarak yazın",
                     "Örnek: x² - 5x + 6 = 0"]
                )
            
            sonuc = ikinci_dereceden_coz(denklem)
            return cozum_formatla(sonuc, "İkinci Dereceden Denklem Çözümü")
        
        elif fonksiyon == "carpanlara_ayir":
            ifade = parametreler.get("ifade")
            if not ifade or ifade == "belirsiz":
                return hata_mesaji_formatla(
                    "Çarpanlarına ayrılacak ifade tespit edilemedi.",
                    ["İfadeyi açık bir şekilde yazın",
                     "Örnek: x² - 9"]
                )
            
            sonuc = carpanlara_ayir(ifade)
            return cozum_formatla(sonuc, "Çarpanlara Ayırma İşlemi")
        
        else:
            return hata_mesaji_formatla(
                f"'{fonksiyon}' fonksiyonu henüz desteklenmiyor."
            )
    
    def _trigonometri_isle(self, oneri: Dict[str, Any], analiz: Dict[str, Any]) -> str:
        """Trigonometri modülü işlemlerini yönetir"""
        fonksiyon = oneri["fonksiyon"]
        parametreler = oneri["parametreler"]
        ifade = parametreler.get("ifade", "")
        
        try:
            if fonksiyon == "trigonometrik_hesapla":
                # sin(30), cos(45) gibi ifadeleri ayrıştır
                import re
                eslesen = re.search(r'(sin|cos|tan|sinüs|kosinüs|tanjant)\s*\(?(\d+(?:\.\d+)?)\)?', ifade)
                if eslesen:
                    fonk_adi = eslesen.group(1)
                    aci = float(eslesen.group(2))
                    sonuc = trigonometrik_hesapla(fonk_adi, aci, "derece")
                    return cozum_formatla(sonuc, "Trigonometrik Fonksiyon Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "Trigonometrik fonksiyon formatı tanınamadı.",
                        ["Örnek: sin(30), cos 45, tan(60)"]
                    )
            
            elif fonksiyon == "ters_trigonometrik_hesapla":
                # arcsin(0.5) gibi ifadeleri ayrıştır
                import re
                eslesen = re.search(r'(arcsin|arccos|arctan|asin|acos|atan)\s*\(?([\d.,]+)\)?', ifade)
                if eslesen:
                    fonk_adi = eslesen.group(1)
                    deger = float(eslesen.group(2).replace(',', '.'))
                    sonuc = ters_trigonometrik_hesapla(fonk_adi, deger)
                    return cozum_formatla(sonuc, "Ters Trigonometrik Fonksiyon Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "Ters trigonometrik fonksiyon formatı tanınamadı.",
                        ["Örnek: arcsin(0.5), arccos(0.707)"]
                    )
            
            elif fonksiyon == "aci_donustur":
                # 90 derece radyan, 1.57 radyan derece gibi ifadeleri ayrıştır
                import re
                # Derece → Radyan
                eslesen = re.search(r'(\d+(?:\.\d+)?)\s*(derece|°).*?(radyan|rad)', ifade)
                if eslesen:
                    aci = float(eslesen.group(1))
                    sonuc = aci_donustur(aci, "derece", "radyan")
                    return cozum_formatla(sonuc, "Açı Dönüşümü")
                
                # Radyan → Derece
                eslesen = re.search(r'(\d+(?:\.\d+)?)\s*(radyan|rad).*?(derece|°)', ifade)
                if eslesen:
                    aci = float(eslesen.group(1))
                    sonuc = aci_donustur(aci, "radyan", "derece")
                    return cozum_formatla(sonuc, "Açı Dönüşümü")
                
                return hata_mesaji_formatla(
                    "Açı dönüşüm formatı tanınamadı.",
                    ["Örnek: 90 derece radyan, 1.57 radyan derece"]
                )
            
            elif fonksiyon == "trigonometrik_denklem_coz":
                # Denklem parametrelerinden denklemi al
                denklem = parametreler.get("denklem", ifade)
                if denklem:
                    sonuc = trigonometrik_denklem_coz(denklem)
                    return cozum_formatla(sonuc, "Trigonometrik Denklem Çözümü")
                else:
                    return hata_mesaji_formatla(
                        "Trigonometrik denklem tespit edilemedi.",
                        ["Örnek: sin(x) = 0.5, cos(x) = 0, tan(x) = 1"]
                    )
            
            elif fonksiyon == "trigonometrik_ifade_hesapla":
                # Karmaşık trigonometrik ifadeyi hesapla
                if ifade:
                    sonuc = trigonometrik_ifade_hesapla(ifade)
                    return cozum_formatla(sonuc, "Trigonometrik İfade Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "Trigonometrik ifade tespit edilemedi.",
                        ["Örnek: sin(30) + cos(45), tan(60) - sin(90)"]
                    )
            
            elif fonksiyon == "karma_trigonometrik_denklem_coz":
                # Karma trigonometrik denklem çöz
                denklem = parametreler.get("denklem", ifade)
                if denklem:
                    sonuc = karma_trigonometrik_denklem_coz(denklem)
                    return cozum_formatla(sonuc, "Karma Trigonometrik Denklem Çözümü")
                else:
                    return hata_mesaji_formatla(
                        "Karma trigonometrik denklem tespit edilemedi.",
                        ["Örnek: sin(x) + cos(45) = 1.20, cos(x) - sin(30) = 0.5"]
                    )
            
            else:
                return hata_mesaji_formatla(
                    f"'{fonksiyon}' fonksiyonu henüz desteklenmiyor."
                )
        
        except Exception as e:
            return hata_mesaji_formatla(
                f"Trigonometri hesaplaması sırasında hata oluştu: {str(e)}",
                ["Açı değerini kontrol edin",
                 "Fonksiyon adını doğru yazdığınızdan emin olun"]
            )
    
    def _analiz_isle(self, oneri: Dict[str, Any], analiz: Dict[str, Any]) -> str:
        """Analiz modülü işlemlerini yönetir"""
        fonksiyon = oneri["fonksiyon"]
        parametreler = oneri["parametreler"]
        orijinal_girdi = analiz.get("orijinal_girdi", "")
        
        try:
            if fonksiyon == "turev_hesapla":
                # Türev hesapla
                fonksiyon_str = parametreler.get("fonksiyon")
                if not fonksiyon_str:
                    # Orijinal girdiden fonksiyonu çıkar
                    from utils.parser import DoğalDilParser
                    parser = DoğalDilParser()
                    fonksiyon_str = parser._fonksiyon_cikar(orijinal_girdi)
                
                if fonksiyon_str:
                    sonuc = turev_hesapla(fonksiyon_str)
                    return cozum_formatla(sonuc, "Türev Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "Türev alınacak fonksiyon tespit edilemedi.",
                        ["Örnek: x², sin(x), 2x+3"]
                    )
            
            elif fonksiyon == "integral_hesapla":
                # İntegral hesapla
                fonksiyon_str = parametreler.get("fonksiyon")
                if not fonksiyon_str:
                    # Orijinal girdiden fonksiyonu çıkar
                    from utils.parser import DoğalDilParser
                    parser = DoğalDilParser()
                    fonksiyon_str = parser._fonksiyon_cikar(orijinal_girdi)
                
                if fonksiyon_str:
                    sonuc = integral_hesapla(fonksiyon_str)
                    return cozum_formatla(sonuc, "İntegral Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "İntegral alınacak fonksiyon tespit edilemedi.",
                        ["Örnek: x², sin(x), 2x+3"]
                    )
            
            else:
                return hata_mesaji_formatla(
                    f"'{fonksiyon}' analiz fonksiyonu henüz desteklenmiyor."
                )
        
        except Exception as e:
            return hata_mesaji_formatla(
                f"Analiz hesaplaması sırasında hata oluştu: {str(e)}",
                ["Fonksiyon formatını kontrol edin",
                 "Matematiksel ifadeyi doğru yazdığınızdan emin olun"]
            )
    
    def _olasilik_isle(self, oneri: Dict[str, Any], analiz: Dict[str, Any]) -> str:
        """Olasılık modülü işlemlerini yönetir"""
        fonksiyon = oneri["fonksiyon"]
        parametreler = oneri["parametreler"]
        orijinal_girdi = analiz.get("orijinal_girdi", "")
        
        try:
            if fonksiyon == "faktoriyel":
                # Faktöriyel hesapla
                n = parametreler.get("n")
                if not n:
                    # Orijinal girdiden sayı çıkar
                    from utils.parser import DoğalDilParser
                    parser = DoğalDilParser()
                    n = parser._sayi_cikar(orijinal_girdi)
                
                sonuc = faktoriyel(n)
                return cozum_formatla(sonuc, "Faktöriyel Hesaplama")
            
            elif fonksiyon == "permutasyon":
                # Permutasyon hesapla
                n = parametreler.get("n")
                r = parametreler.get("r")
                if not n or not r:
                    # Orijinal girdiden n,r çıkar
                    from utils.parser import DoğalDilParser
                    parser = DoğalDilParser()
                    n, r = parser._nr_cikar(orijinal_girdi)
                
                sonuc = permutasyon(n, r)
                return cozum_formatla(sonuc, "Permutasyon Hesaplama")
            
            elif fonksiyon == "kombinasyon":
                # Kombinasyon hesapla
                n = parametreler.get("n")
                r = parametreler.get("r")
                if not n or not r:
                    # Orijinal girdiden n,r çıkar
                    from utils.parser import DoğalDilParser
                    parser = DoğalDilParser()
                    n, r = parser._nr_cikar(orijinal_girdi)
                
                sonuc = kombinasyon(n, r)
                return cozum_formatla(sonuc, "Kombinasyon Hesaplama")
            
            else:
                return hata_mesaji_formatla(
                    f"'{fonksiyon}' olasılık fonksiyonu henüz desteklenmiyor."
                )
        
        except Exception as e:
            return hata_mesaji_formatla(
                f"Olasılık hesaplaması sırasında hata oluştu: {str(e)}",
                ["Sayı değerlerini kontrol edin",
                 "Permutasyon/kombinasyon formatını doğrulayın"]
            )
    
    def _geometri_isle(self, oneri: Dict[str, Any], analiz: Dict[str, Any]) -> str:
        """Geometri modülü işlemlerini yönetir"""
        fonksiyon = oneri["fonksiyon"]
        parametreler = oneri["parametreler"]
        orijinal_girdi = analiz.get("orijinal_girdi", "")
        
        try:
            from modules.geometri import GeometriCozucu
            
            geo = GeometriCozucu()
            
            if fonksiyon == "ucgen_hesaplama":
                hesaplama_turu = parametreler.pop("hesaplama_turu", "alan")
                sonuc = geo.ucgen_hesaplama(hesaplama_turu, **parametreler)
                return cozum_formatla(sonuc, f"Üçgen {hesaplama_turu.title()} Hesaplama")
            
            elif fonksiyon == "dortgen_hesaplama":
                sekil = parametreler.pop("sekil", "kare")
                hesaplama = parametreler.pop("hesaplama", "alan")
                sonuc = geo.dortgen_hesaplama(sekil, hesaplama, **parametreler)
                return cozum_formatla(sonuc, f"{sekil.title()} {hesaplama.title()} Hesaplama")
            
            elif fonksiyon == "daire_hesaplama":
                hesaplama = parametreler.pop("hesaplama", "alan")
                sonuc = geo.daire_hesaplama(hesaplama, **parametreler)
                return cozum_formatla(sonuc, f"Daire {hesaplama.title()} Hesaplama")
            
            elif fonksiyon == "genel_hesaplama":
                # Genel geometri hesaplama - kullanıcı girdisine göre belirlenir
                if any(kelime in orijinal_girdi.lower() for kelime in ['pisagor', 'pitagor', 'hipotenüs']):
                    sonuc = geo.ucgen_hesaplama("pisagor", **parametreler)
                    return cozum_formatla(sonuc, "Pisagor Teoremi")
                elif any(kelime in orijinal_girdi.lower() for kelime in ['üçgen', 'alan']):
                    sonuc = geo.ucgen_hesaplama("alan", **parametreler)
                    return cozum_formatla(sonuc, "Üçgen Alan Hesaplama")
                else:
                    return hata_mesaji_formatla(
                        "Belirtilen geometri hesaplama türü tespit edilemedi.",
                        ["Desteklenen hesaplamalar: pisagor teoremi, üçgen alanı, kare/dikdörtgen alan/çevre, daire alan/çevre"]
                    )
            
            else:
                return hata_mesaji_formatla(
                    f"'{fonksiyon}' geometri fonksiyonu henüz desteklenmiyor.",
                    ["Desteklenen fonksiyonlar: ucgen_hesaplama, dortgen_hesaplama, daire_hesaplama"]
                )
        
        except Exception as e:
            return hata_mesaji_formatla(
                f"Geometri hesaplaması sırasında hata oluştu: {str(e)}",
                ["Parametreleri kontrol edin",
                 "Sayı değerlerinin doğru olduğundan emin olun",
                 "Desteklenen geometri şekillerini kullanın"]
            )
    
    def calistir(self):
        """Ana programı çalıştırır"""
        self.hosgeldin_mesaji()
        
        while self.aktif:
            try:
                # Kullanıcı girdisi al
                kullanici_girisi = input("🤔 Matematik sorunuz: ").strip()
                
                if not kullanici_girisi:
                    continue
                
                # Çıkış komutları
                if kullanici_girisi.lower() in ['çıkış', 'exit', 'q', 'quit']:
                    print("\n👋 Görüşmek üzere! Matematik kütüphanesini kullandığınız için teşekkürler.")
                    self.aktif = False
                    break
                
                # Yardım komutları
                elif kullanici_girisi.lower() in ['yardım', 'help', 'h']:
                    self.yardim_goster()
                    continue
                
                # Ekran temizleme komutları
                elif kullanici_girisi.lower() in ['temizle', 'clear', 'cls']:
                    self.ekran_temizle()
                    self.hosgeldin_mesaji()
                    continue
                
                # Soru işle
                print("\n🔄 İşleniyor...")
                sonuc = self.sorgu_isle(kullanici_girisi)
                print(sonuc)
                print()
            
            except KeyboardInterrupt:
                print("\n\n👋 Program sonlandırıldı. Görüşmek üzere!")
                self.aktif = False
            except EOFError:
                print("\n\n👋 Program sonlandırıldı. Görüşmek üzere!")
                self.aktif = False
            except Exception as e:
                print(f"\n❌ Beklenmeyen hata: {str(e)}")
                print("Lütfen tekrar deneyin veya programı yeniden başlatın.\n")


def main():
    """Ana fonksiyon"""
    # Gerekli kütüphaneleri kontrol et
    try:
        import sympy
        import numpy
    except ImportError as e:
        print("❌ Gerekli kütüphaneler yüklenmemiş!")
        print("Lütfen şu komutu çalıştırın: pip install -r requirements.txt")
        print(f"Eksik kütüphane: {str(e)}")
        return
    
    # Kütüphaneyi başlat
    kutuhane = MatematikKutuphanesi()
    kutuhane.calistir()


if __name__ == "__main__":
    main()


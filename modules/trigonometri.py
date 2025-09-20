"""
Trigonometri Modülü - Matematik Kütüphanesi
===========================================

Bu modül trigonometrik işlemler için fonksiyonlar içerir.
Desteklenen işlemler:
- Trigonometrik fonksiyon hesaplama (sin, cos, tan)
- Ters trigonometrik fonksiyonlar (arcsin, arccos, arctan)
- Açı dönüşümleri (derece ↔ radyan)
- Trigonometrik denklem çözme

Yazar: Matematik Kütüphanesi
"""

import sympy as sp
import math
import re
from typing import Dict, List, Tuple, Optional


class TrigonometriCozucu:
    """Trigonometri problemlerini çözen ana sınıf"""
    
    def __init__(self):
        self.x = sp.Symbol('x')
        self.pi = sp.pi
        
        # Açı birimleri
        self.derece_modu = True  # Default olarak derece
        
        # Trigonometrik fonksiyonlar
        self.trig_fonksiyonlari = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'sinüs': sp.sin,
            'kosinüs': sp.cos,
            'tanjant': sp.tan,
            'cotanjant': sp.cot,
            'cot': sp.cot,
            'sekant': sp.sec,
            'sec': sp.sec,
            'kosekant': sp.csc,
            'csc': sp.csc
        }
        
        # Ters trigonometrik fonksiyonlar
        self.ters_trig_fonksiyonlari = {
            'arcsin': sp.asin,
            'arccos': sp.acos,
            'arctan': sp.atan,
            'asin': sp.asin,
            'acos': sp.acos,
            'atan': sp.atan
        }
    
    def fonksiyon_hesapla(self, fonksiyon: str, aci: float, birim: str = "derece") -> Dict[str, any]:
        """
        Trigonometrik fonksiyon değerini hesaplar.
        
        Args:
            fonksiyon (str): Trigonometrik fonksiyon adı (sin, cos, tan)
            aci (float): Açı değeri
            birim (str): Açı birimi ("derece" veya "radyan")
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Hesaplanacak: {fonksiyon}({aci}°)" if birim == "derece" else f"Hesaplanacak: {fonksiyon}({aci} radyan)")
            
            # Açıyı radyana çevir
            if birim == "derece":
                aci_radyan = math.radians(aci)
                adimlar.append(f"Açıyı radyana çevir: {aci}° = {aci_radyan:.4f} radyan")
            else:
                aci_radyan = aci
            
            # Fonksiyon hesapla
            fonksiyon_temiz = fonksiyon.lower().replace("ü", "u").replace("ı", "i")
            
            if fonksiyon_temiz in self.trig_fonksiyonlari:
                trig_func = self.trig_fonksiyonlari[fonksiyon_temiz]
                sonuc = float(trig_func(aci_radyan))
                
                # Özel açılar kontrolü
                ozel_deger = self._ozel_aci_kontrol(fonksiyon_temiz, aci)
                if ozel_deger:
                    adimlar.append(f"Bu özel bir açıdır: {ozel_deger}")
                
                adimlar.append(f"{fonksiyon}({aci}°) = {sonuc:.6f}" if birim == "derece" else f"{fonksiyon}({aci}) = {sonuc:.6f}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "fonksiyon": fonksiyon,
                    "aci": aci,
                    "birim": birim,
                    "sonuc": sonuc,
                    "aci_radyan": aci_radyan
                }
            else:
                return {
                    "basarili": False,
                    "hata": f"Bilinmeyen trigonometrik fonksiyon: {fonksiyon}",
                    "adimlar": []
                }
                
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Hesaplama sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }
    
    def ters_fonksiyon_hesapla(self, fonksiyon: str, deger: float) -> Dict[str, any]:
        """
        Ters trigonometrik fonksiyon hesaplar.
        
        Args:
            fonksiyon (str): Ters trigonometrik fonksiyon (arcsin, arccos, arctan)
            deger (float): Fonksiyon değeri
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Hesaplanacak: {fonksiyon}({deger})")
            
            fonksiyon_temiz = fonksiyon.lower()
            
            if fonksiyon_temiz in self.ters_trig_fonksiyonlari:
                ters_func = self.ters_trig_fonksiyonlari[fonksiyon_temiz]
                
                # Değer aralığı kontrolü
                if fonksiyon_temiz in ['arcsin', 'asin'] and abs(deger) > 1:
                    return {
                        "basarili": False,
                        "hata": f"arcsin için değer [-1, 1] aralığında olmalı. Girilen: {deger}",
                        "adimlar": []
                    }
                elif fonksiyon_temiz in ['arccos', 'acos'] and abs(deger) > 1:
                    return {
                        "basarili": False,
                        "hata": f"arccos için değer [-1, 1] aralığında olmalı. Girilen: {deger}",
                        "adimlar": []
                    }
                
                aci_radyan = float(ters_func(deger))
                aci_derece = math.degrees(aci_radyan)
                
                adimlar.append(f"{fonksiyon}({deger}) = {aci_radyan:.6f} radyan")
                adimlar.append(f"Dereceye çevir: {aci_derece:.2f}°")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "fonksiyon": fonksiyon,
                    "deger": deger,
                    "aci_radyan": aci_radyan,
                    "aci_derece": aci_derece
                }
            else:
                return {
                    "basarili": False,
                    "hata": f"Bilinmeyen ters trigonometrik fonksiyon: {fonksiyon}",
                    "adimlar": []
                }
                
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Hesaplama sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }
    
    def trigonometrik_ifade_hesapla(self, ifade_str: str) -> Dict[str, any]:
        """
        Karmaşık trigonometrik ifadeleri hesaplar.
        
        Args:
            ifade_str (str): Trigonometrik ifade (örn: "sin(30) + cos(45)")
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Verilen trigonometrik ifade: {ifade_str}")
            
            # İfadeyi temizle
            ifade_temiz = ifade_str.lower()
            
            # Gereksiz kelimeleri çıkar
            gereksiz_kelimeler = ["hesapla", "bul", "çöz", "değer", "sonuç"]
            for kelime in gereksiz_kelimeler:
                ifade_temiz = ifade_temiz.replace(kelime, "")
            
            # Boşlukları temizle
            ifade_temiz = ifade_temiz.replace(" ", "")
            
            # = işareti varsa sol tarafı al
            if "=" in ifade_temiz:
                ifade_temiz = ifade_temiz.split("=")[0]
            
            # Trigonometrik fonksiyonları tespit et ve hesapla
            import re
            
            # Tüm trigonometrik fonksiyonları bul
            trig_eslesmeler = re.findall(r'(sin|cos|tan|sinüs|kosinüs|tanjant)\s*\(?(\d+(?:\.\d+)?)\)?', ifade_temiz)
            
            if not trig_eslesmeler:
                return {
                    "basarili": False,
                    "hata": "Trigonometrik fonksiyon tespit edilemedi",
                    "adimlar": []
                }
            
            # Her fonksiyonu hesapla ve değiştir
            hesaplanan_ifade = ifade_temiz
            fonksiyon_hesaplamalari = {}
            
            for fonksiyon, aci_str in trig_eslesmeler:
                aci = float(aci_str)
                
                # Fonksiyonu hesapla
                sonuc_hesaplama = self.fonksiyon_hesapla(fonksiyon, aci, "derece")
                
                if sonuc_hesaplama["basarili"]:
                    deger = sonuc_hesaplama["sonuc"]
                    fonksiyon_hesaplamalari[f"{fonksiyon}({aci})"] = deger
                    
                    # Adım ekle
                    adimlar.append(f"{fonksiyon}({aci}°) = {deger:.6f}")
                    
                    # İfadede değiştir - daha güvenli replacement
                    eski_ifade = f"{fonksiyon}({aci_str})"
                    if eski_ifade in hesaplanan_ifade:
                        hesaplanan_ifade = hesaplanan_ifade.replace(eski_ifade, f"({deger})")
                    else:
                        eski_ifade = f"{fonksiyon}{aci_str}"
                        if eski_ifade in hesaplanan_ifade:
                            hesaplanan_ifade = hesaplanan_ifade.replace(eski_ifade, f"({deger})")
                else:
                    return {
                        "basarili": False,
                        "hata": f"{fonksiyon}({aci}) hesaplanırken hata oluştu",
                        "adimlar": adimlar
                    }
            
            # Matematiksel ifadeyi değerlendir
            try:
                # Güvenli değerlendirme için sadece sayısal işlemler
                import ast
                import operator as op
                
                # Desteklenen operatörler
                operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                           ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                           ast.USub: op.neg}
                
                def eval_expr(expr):
                    return eval_(ast.parse(expr, mode='eval').body)
                
                def eval_(node):
                    if isinstance(node, ast.Num):
                        return node.n
                    elif isinstance(node, ast.BinOp):
                        return operators[type(node.op)](eval_(node.left), eval_(node.right))
                    elif isinstance(node, ast.UnaryOp):
                        return operators[type(node.op)](eval_(node.operand))
                    else:
                        raise TypeError(node)
                
                # Basit eval kullan (sadece sayısal ifadeler için güvenli)
                nihai_sonuc = eval(hesaplanan_ifade)
                
                adimlar.append(f"İfade değerlendirmesi: {hesaplanan_ifade}")
                adimlar.append(f"Nihai sonuç: {nihai_sonuc:.6f}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "orijinal_ifade": ifade_str,
                    "hesaplanan_ifade": hesaplanan_ifade,
                    "fonksiyon_hesaplamalari": fonksiyon_hesaplamalari,
                    "nihai_sonuc": nihai_sonuc
                }
                
            except Exception as e:
                return {
                    "basarili": False,
                    "hata": f"İfade değerlendirmesi sırasında hata: {str(e)}",
                    "adimlar": adimlar
                }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Trigonometrik ifade hesaplaması sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }

    def karma_trigonometrik_denklem_coz(self, denklem_str: str) -> Dict[str, any]:
        """
        Karma trigonometrik denklem çözer (değişken + sabit değerler).
        
        Args:
            denklem_str (str): Karma trigonometrik denklem (örn: "sin(x) + cos(45) = 1.20")
        
        Returns:
            Dict: Çözüm adımları ve sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Verilen karma trigonometrik denklem: {denklem_str}")
            
            # Denklemi temizle ve ayrıştır
            denklem_temiz = denklem_str.lower()
            
            # Önce "x hesapla" gibi bileşik ifadeleri çıkar
            denklem_temiz = denklem_temiz.replace("x hesapla", "")
            denklem_temiz = denklem_temiz.replace("ise x", "")
            
            # Sonra tekil kelimeleri çıkar
            gereksiz_kelimeler = ["ise", "hesapla", "bul", "çöz", "değer", "sonuç"]
            for kelime in gereksiz_kelimeler:
                denklem_temiz = denklem_temiz.replace(kelime, "")
            
            denklem_temiz = denklem_temiz.replace(" ", "")
            
            if "=" not in denklem_temiz:
                return {
                    "basarili": False,
                    "hata": "Denklemde eşittir işareti bulunamadı",
                    "adimlar": []
                }
            
            sol_taraf, sag_taraf = denklem_temiz.split("=", 1)
            hedef_deger = float(sag_taraf)
            
            adimlar.append(f"Sol taraf: {sol_taraf}")
            adimlar.append(f"Hedef değer: {hedef_deger}")
            
            # Sabit trigonometrik fonksiyonları hesapla ve çıkar
            import re
            
            # Sabit fonksiyonları bul (sayı içeren)
            sabit_fonksiyonlar = re.findall(r'(sin|cos|tan)\((\d+(?:\.\d+)?)\)', sol_taraf)
            
            sol_taraf_hesaplanan = sol_taraf
            sabit_toplam = 0
            
            for fonksiyon, aci_str in sabit_fonksiyonlar:
                aci = float(aci_str)
                
                # Fonksiyonu hesapla
                sonuc_hesaplama = self.fonksiyon_hesapla(fonksiyon, aci, "derece")
                
                if sonuc_hesaplama["basarili"]:
                    deger = sonuc_hesaplama["sonuc"]
                    adimlar.append(f"{fonksiyon}({aci}°) = {deger:.6f}")
                    
                    # İfadeden çıkar
                    fonksiyon_ifadesi = f"{fonksiyon}({aci_str})"
                    if f"+{fonksiyon_ifadesi}" in sol_taraf_hesaplanan:
                        sol_taraf_hesaplanan = sol_taraf_hesaplanan.replace(f"+{fonksiyon_ifadesi}", "")
                        sabit_toplam += deger
                    elif f"-{fonksiyon_ifadesi}" in sol_taraf_hesaplanan:
                        sol_taraf_hesaplanan = sol_taraf_hesaplanan.replace(f"-{fonksiyon_ifadesi}", "")
                        sabit_toplam -= deger
                    elif sol_taraf_hesaplanan.startswith(fonksiyon_ifadesi):
                        sol_taraf_hesaplanan = sol_taraf_hesaplanan.replace(fonksiyon_ifadesi, "")
                        sabit_toplam += deger
                else:
                    return {
                        "basarili": False,
                        "hata": f"{fonksiyon}({aci}) hesaplanırken hata oluştu",
                        "adimlar": adimlar
                    }
            
            # Kalan ifade sadece x içeren fonksiyon olmalı
            sol_taraf_hesaplanan = sol_taraf_hesaplanan.strip("+-")
            
            # x için hedef değeri hesapla
            x_hedef_degeri = hedef_deger - sabit_toplam
            
            adimlar.append(f"Sabit fonksiyonların toplamı: {sabit_toplam:.6f}")
            adimlar.append(f"Kalan denklem: {sol_taraf_hesaplanan} = {x_hedef_degeri:.6f}")
            
            # X içeren fonksiyonu çöz
            x_fonksiyon_eslesen = re.search(r'(sin|cos|tan)\(x\)', sol_taraf_hesaplanan)
            
            if not x_fonksiyon_eslesen:
                return {
                    "basarili": False,
                    "hata": "x değişkenli trigonometrik fonksiyon bulunamadı",
                    "adimlar": adimlar
                }
            
            x_fonksiyon = x_fonksiyon_eslesen.group(1)
            
            # Değer aralığı kontrolü
            if x_fonksiyon in ['sin', 'cos'] and abs(x_hedef_degeri) > 1:
                return {
                    "basarili": False,
                    "hata": f"{x_fonksiyon}(x) = {x_hedef_degeri:.6f} denkleminin çözümü yok (|{x_hedef_degeri}| > 1)",
                    "adimlar": adimlar
                }
            
            # x değerlerini hesapla
            cozumler = []
            
            if x_fonksiyon == "sin":
                if abs(x_hedef_degeri) <= 1:
                    ana_aci = math.degrees(math.asin(x_hedef_degeri))
                    aci1 = ana_aci % 360
                    aci2 = (180 - ana_aci) % 360
                    
                    adimlar.append(f"sin(x) = {x_hedef_degeri:.6f}")
                    adimlar.append(f"Ana açı: arcsin({x_hedef_degeri:.6f}) = {ana_aci:.2f}°")
                    adimlar.append(f"Çözümler: x = {aci1:.2f}° veya x = {aci2:.2f}°")
                    
                    cozumler = [aci1, aci2]
            
            elif x_fonksiyon == "cos":
                if abs(x_hedef_degeri) <= 1:
                    ana_aci = math.degrees(math.acos(x_hedef_degeri))
                    aci1 = ana_aci % 360
                    aci2 = (360 - ana_aci) % 360
                    
                    adimlar.append(f"cos(x) = {x_hedef_degeri:.6f}")
                    adimlar.append(f"Ana açı: arccos({x_hedef_degeri:.6f}) = {ana_aci:.2f}°")
                    adimlar.append(f"Çözümler: x = {aci1:.2f}° veya x = {aci2:.2f}°")
                    
                    cozumler = [aci1, aci2]
            
            elif x_fonksiyon == "tan":
                ana_aci = math.degrees(math.atan(x_hedef_degeri))
                if ana_aci < 0:
                    ana_aci += 180
                aci1 = ana_aci % 360
                aci2 = (ana_aci + 180) % 360
                
                adimlar.append(f"tan(x) = {x_hedef_degeri:.6f}")
                adimlar.append(f"Ana açı: arctan({x_hedef_degeri:.6f}) = {ana_aci:.2f}°")
                adimlar.append(f"Çözümler: x = {aci1:.2f}° veya x = {aci2:.2f}°")
                
                cozumler = [aci1, aci2]
            
            # Çözümleri doğrula
            adimlar.append("")
            adimlar.append("Çözümleri doğrulama:")
            for i, x_degeri in enumerate(cozumler, 1):
                # Orijinal denklemi x değeri ile hesapla
                dogrulama_sonucu = 0
                
                # Sabit fonksiyonları ekle
                dogrulama_sonucu += sabit_toplam
                
                # x fonksiyonunu ekle
                if x_fonksiyon == "sin":
                    dogrulama_sonucu += math.sin(math.radians(x_degeri))
                elif x_fonksiyon == "cos":
                    dogrulama_sonucu += math.cos(math.radians(x_degeri))
                elif x_fonksiyon == "tan":
                    dogrulama_sonucu += math.tan(math.radians(x_degeri))
                
                adimlar.append(f"x = {x_degeri:.2f}° için: {dogrulama_sonucu:.6f} ≈ {hedef_deger}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "denklem": denklem_str,
                "x_fonksiyon": x_fonksiyon,
                "hedef_deger": hedef_deger,
                "sabit_toplam": sabit_toplam,
                "x_hedef_degeri": x_hedef_degeri,
                "cozumler": cozumler,
                "cozum_sayisi": len(cozumler)
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Karma trigonometrik denklem çözümü sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }

    def trigonometrik_denklem_coz(self, denklem_str: str) -> Dict[str, any]:
        """
        Trigonometrik denklem çözer.
        
        Args:
            denklem_str (str): Trigonometrik denklem (örn: "sin(x) = 0.5")
        
        Returns:
            Dict: Çözüm adımları ve sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Verilen trigonometrik denklem: {denklem_str}")
            
            # Denklemi temizle ve ayrıştır
            denklem_temiz = denklem_str.lower().replace(" ", "")
            
            # Denklem tiplerini tespit et
            if "=" not in denklem_temiz:
                return {
                    "basarili": False,
                    "hata": "Denklemde eşittir işareti bulunamadı",
                    "adimlar": []
                }
            
            sol_taraf, sag_taraf = denklem_temiz.split("=", 1)
            
            # Temel trigonometrik denklem çözümü
            cozumler = []
            
            # sin(x) = değer formatı
            sin_eslesen = re.search(r'sin\s*\(\s*([x])\s*\)', sol_taraf)
            if sin_eslesen and sag_taraf.replace(".", "").replace("-", "").isdigit():
                deger = float(sag_taraf)
                if abs(deger) <= 1:
                    adimlar.append(f"sin(x) = {deger} denklemini çözelim")
                    
                    # Ana açı bulma
                    if deger == 0:
                        ana_aci = 0
                        adimlar.append("sin(x) = 0 için ana çözümler: x = 0°, 180°")
                        cozumler = [0, 180]
                    elif deger == 1:
                        ana_aci = 90
                        adimlar.append("sin(x) = 1 için çözüm: x = 90°")
                        cozumler = [90]
                    elif deger == -1:
                        ana_aci = 270
                        adimlar.append("sin(x) = -1 için çözüm: x = 270°")
                        cozumler = [270]
                    elif deger == 0.5:
                        adimlar.append("sin(x) = 0.5 için ana açı: arcsin(0.5) = 30°")
                        adimlar.append("Genel çözümler: x = 30° + 360°k veya x = 150° + 360°k")
                        cozumler = [30, 150]
                    elif deger == -0.5:
                        adimlar.append("sin(x) = -0.5 için ana açı: arcsin(-0.5) = -30°")
                        adimlar.append("Genel çözümler: x = 210° + 360°k veya x = 330° + 360°k")
                        cozumler = [210, 330]
                    elif abs(deger) == sp.sqrt(2)/2:
                        if deger > 0:
                            adimlar.append("sin(x) = √2/2 için ana açı: 45°")
                            adimlar.append("Genel çözümler: x = 45° + 360°k veya x = 135° + 360°k")
                            cozumler = [45, 135]
                        else:
                            adimlar.append("sin(x) = -√2/2 için ana açı: -45°")
                            adimlar.append("Genel çözümler: x = 225° + 360°k veya x = 315° + 360°k")
                            cozumler = [225, 315]
                    elif abs(deger) == sp.sqrt(3)/2:
                        if deger > 0:
                            adimlar.append("sin(x) = √3/2 için ana açı: 60°")
                            adimlar.append("Genel çözümler: x = 60° + 360°k veya x = 120° + 360°k")
                            cozumler = [60, 120]
                        else:
                            adimlar.append("sin(x) = -√3/2 için ana açı: -60°")
                            adimlar.append("Genel çözümler: x = 240° + 360°k veya x = 300° + 360°k")
                            cozumler = [240, 300]
                    else:
                        # Genel durum - arcsin kullan
                        ana_aci = math.degrees(math.asin(deger))
                        adimlar.append(f"sin(x) = {deger} için ana açı: arcsin({deger}) = {ana_aci:.2f}°")
                        aci1 = ana_aci % 360
                        aci2 = (180 - ana_aci) % 360
                        adimlar.append(f"Genel çözümler: x = {aci1:.2f}° + 360°k veya x = {aci2:.2f}° + 360°k")
                        cozumler = [aci1, aci2]
                        
                else:
                    return {
                        "basarili": False,
                        "hata": f"sin(x) = {deger} denkleminin çözümü yok (|{deger}| > 1)",
                        "adimlar": []
                    }
            
            # cos(x) = değer formatı
            cos_eslesen = re.search(r'cos\s*\(\s*([x])\s*\)', sol_taraf)
            if cos_eslesen and sag_taraf.replace(".", "").replace("-", "").isdigit():
                deger = float(sag_taraf)
                if abs(deger) <= 1:
                    adimlar.append(f"cos(x) = {deger} denklemini çözelim")
                    
                    if deger == 0:
                        adimlar.append("cos(x) = 0 için çözümler: x = 90°, 270°")
                        cozumler = [90, 270]
                    elif deger == 1:
                        adimlar.append("cos(x) = 1 için çözüm: x = 0°")
                        cozumler = [0]
                    elif deger == -1:
                        adimlar.append("cos(x) = -1 için çözüm: x = 180°")
                        cozumler = [180]
                    elif deger == 0.5:
                        adimlar.append("cos(x) = 0.5 için ana açı: arccos(0.5) = 60°")
                        adimlar.append("Genel çözümler: x = 60° + 360°k veya x = 300° + 360°k")
                        cozumler = [60, 300]
                    elif deger == -0.5:
                        adimlar.append("cos(x) = -0.5 için ana açı: arccos(-0.5) = 120°")
                        adimlar.append("Genel çözümler: x = 120° + 360°k veya x = 240° + 360°k")
                        cozumler = [120, 240]
                    else:
                        # Genel durum
                        ana_aci = math.degrees(math.acos(deger))
                        adimlar.append(f"cos(x) = {deger} için ana açı: arccos({deger}) = {ana_aci:.2f}°")
                        aci1 = ana_aci % 360
                        aci2 = (360 - ana_aci) % 360
                        adimlar.append(f"Genel çözümler: x = {aci1:.2f}° + 360°k veya x = {aci2:.2f}° + 360°k")
                        cozumler = [aci1, aci2]
                else:
                    return {
                        "basarili": False,
                        "hata": f"cos(x) = {deger} denkleminin çözümü yok (|{deger}| > 1)",
                        "adimlar": []
                    }
            
            # tan(x) = değer formatı
            tan_eslesen = re.search(r'tan\s*\(\s*([x])\s*\)', sol_taraf)
            if tan_eslesen and sag_taraf.replace(".", "").replace("-", "").isdigit():
                deger = float(sag_taraf)
                adimlar.append(f"tan(x) = {deger} denklemini çözelim")
                
                if deger == 0:
                    adimlar.append("tan(x) = 0 için çözümler: x = 0°, 180°")
                    cozumler = [0, 180]
                elif deger == 1:
                    adimlar.append("tan(x) = 1 için ana açı: 45°")
                    adimlar.append("Genel çözüm: x = 45° + 180°k")
                    cozumler = [45, 225]
                elif deger == -1:
                    adimlar.append("tan(x) = -1 için ana açı: -45°")
                    adimlar.append("Genel çözüm: x = 135° + 180°k")
                    cozumler = [135, 315]
                elif abs(deger) == sp.sqrt(3):
                    if deger > 0:
                        adimlar.append("tan(x) = √3 için ana açı: 60°")
                        adimlar.append("Genel çözüm: x = 60° + 180°k")
                        cozumler = [60, 240]
                    else:
                        adimlar.append("tan(x) = -√3 için ana açı: -60°")
                        adimlar.append("Genel çözüm: x = 120° + 180°k")
                        cozumler = [120, 300]
                elif abs(deger) == sp.sqrt(3)/3:
                    if deger > 0:
                        adimlar.append("tan(x) = √3/3 için ana açı: 30°")
                        adimlar.append("Genel çözüm: x = 30° + 180°k")
                        cozumler = [30, 210]
                    else:
                        adimlar.append("tan(x) = -√3/3 için ana açı: -30°")
                        adimlar.append("Genel çözüm: x = 150° + 180°k")
                        cozumler = [150, 330]
                else:
                    # Genel durum
                    ana_aci = math.degrees(math.atan(deger))
                    if ana_aci < 0:
                        ana_aci += 180
                    adimlar.append(f"tan(x) = {deger} için ana açı: arctan({deger}) = {ana_aci:.2f}°")
                    aci1 = ana_aci % 360
                    aci2 = (ana_aci + 180) % 360
                    adimlar.append(f"Genel çözüm: x = {aci1:.2f}° + 180°k")
                    cozumler = [aci1, aci2]
            
            if not cozumler:
                return {
                    "basarili": False,
                    "hata": "Denklem formatı tanınamadı veya desteklenmiyor",
                    "adimlar": adimlar
                }
            
            # [0°, 360°) aralığındaki çözümleri göster
            adimlar.append("")
            adimlar.append("[0°, 360°) aralığındaki çözümler:")
            for i, cozum in enumerate(cozumler, 1):
                adimlar.append(f"  x₍{i}₎ = {cozum}°")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "denklem": denklem_str,
                "cozumler": cozumler,
                "cozum_sayisi": len(cozumler)
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Trigonometrik denklem çözümü sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }

    def aci_donusumu(self, aci: float, kaynak_birim: str, hedef_birim: str) -> Dict[str, any]:
        """
        Açı birim dönüşümü yapar.
        
        Args:
            aci (float): Açı değeri
            kaynak_birim (str): Kaynak birim ("derece" veya "radyan")
            hedef_birim (str): Hedef birim ("derece" veya "radyan")
        
        Returns:
            Dict: Dönüşüm sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Dönüştürülecek: {aci} {kaynak_birim} → {hedef_birim}")
            
            if kaynak_birim == hedef_birim:
                return {
                    "basarili": True,
                    "adimlar": ["Birimler aynı, dönüşüm gerekmez"],
                    "sonuc": aci
                }
            
            if kaynak_birim == "derece" and hedef_birim == "radyan":
                sonuc = math.radians(aci)
                adimlar.append(f"Formül: radyan = derece × π/180")
                adimlar.append(f"{aci}° × π/180 = {sonuc:.6f} radyan")
            elif kaynak_birim == "radyan" and hedef_birim == "derece":
                sonuc = math.degrees(aci)
                adimlar.append(f"Formül: derece = radyan × 180/π")
                adimlar.append(f"{aci} × 180/π = {sonuc:.2f}°")
            else:
                return {
                    "basarili": False,
                    "hata": f"Desteklenmeyen birim dönüşümü: {kaynak_birim} → {hedef_birim}",
                    "adimlar": []
                }
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "kaynak_aci": aci,
                "kaynak_birim": kaynak_birim,
                "hedef_birim": hedef_birim,
                "sonuc": sonuc
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Dönüşüm sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }
    
    def _ozel_aci_kontrol(self, fonksiyon: str, aci_derece: float) -> Optional[str]:
        """Özel açıları kontrol eder ve değerlerini döndürür"""
        ozel_aciler = {
            0: {"sin": "0", "cos": "1", "tan": "0"},
            30: {"sin": "1/2", "cos": "√3/2", "tan": "√3/3"},
            45: {"sin": "√2/2", "cos": "√2/2", "tan": "1"},
            60: {"sin": "√3/2", "cos": "1/2", "tan": "√3"},
            90: {"sin": "1", "cos": "0", "tan": "∞"},
            180: {"sin": "0", "cos": "-1", "tan": "0"},
            270: {"sin": "-1", "cos": "0", "tan": "∞"},
            360: {"sin": "0", "cos": "1", "tan": "0"}
        }
        
        # Açıyı 0-360 aralığına indir
        aci_normalize = aci_derece % 360
        
        if aci_normalize in ozel_aciler and fonksiyon in ozel_aciler[aci_normalize]:
            return f"{fonksiyon}({aci_derece}°) = {ozel_aciler[aci_normalize][fonksiyon]}"
        
        return None


# Kullanım kolaylığı için global fonksiyonlar
def trigonometrik_hesapla(fonksiyon: str, aci: float, birim: str = "derece") -> Dict[str, any]:
    """Trigonometrik fonksiyon hesaplar"""
    cozucu = TrigonometriCozucu()
    return cozucu.fonksiyon_hesapla(fonksiyon, aci, birim)


def ters_trigonometrik_hesapla(fonksiyon: str, deger: float) -> Dict[str, any]:
    """Ters trigonometrik fonksiyon hesaplar"""
    cozucu = TrigonometriCozucu()
    return cozucu.ters_fonksiyon_hesapla(fonksiyon, deger)


def aci_donustur(aci: float, kaynak_birim: str, hedef_birim: str) -> Dict[str, any]:
    """Açı birim dönüşümü yapar"""
    cozucu = TrigonometriCozucu()
    return cozucu.aci_donusumu(aci, kaynak_birim, hedef_birim)


def trigonometrik_denklem_coz(denklem: str) -> Dict[str, any]:
    """Trigonometrik denklem çözer"""
    cozucu = TrigonometriCozucu()
    return cozucu.trigonometrik_denklem_coz(denklem)


def trigonometrik_ifade_hesapla(ifade: str) -> Dict[str, any]:
    """Karmaşık trigonometrik ifadeleri hesaplar"""
    cozucu = TrigonometriCozucu()
    return cozucu.trigonometrik_ifade_hesapla(ifade)


def karma_trigonometrik_denklem_coz(denklem: str) -> Dict[str, any]:
    """Karma trigonometrik denklem çözer"""
    cozucu = TrigonometriCozucu()
    return cozucu.karma_trigonometrik_denklem_coz(denklem)


def trigonometrik_turev_integral(islem: str, fonksiyon: str) -> Dict[str, any]:
    """Trigonometrik fonksiyonların türev ve integrallerini hesaplar"""
    try:
        adimlar = []
        
        # Temel trigonometrik fonksiyonların türev ve integralleri
        trig_turevler = {
            "sin(x)": "cos(x)",
            "cos(x)": "-sin(x)", 
            "tan(x)": "sec²(x) = 1/cos²(x)",
            "cot(x)": "-csc²(x) = -1/sin²(x)",
            "sec(x)": "sec(x)tan(x)",
            "csc(x)": "-csc(x)cot(x)",
            "sinüs(x)": "kosinüs(x)",
            "kosinüs(x)": "-sinüs(x)",
            "tanjant(x)": "sekant²(x)"
        }
        
        trig_integraller = {
            "sin(x)": "-cos(x)",
            "cos(x)": "sin(x)",
            "tan(x)": "-ln|cos(x)|",
            "cot(x)": "ln|sin(x)|", 
            "sec(x)": "ln|sec(x) + tan(x)|",
            "csc(x)": "-ln|csc(x) + cot(x)|",
            "sinüs(x)": "-kosinüs(x)",
            "kosinüs(x)": "sinüs(x)",
            "tanjant(x)": "-ln|kosinüs(x)|"
        }
        
        # Fonksiyonu normalize et
        fonksiyon_temiz = fonksiyon.lower().strip()
        
        if islem.lower() in ["türev", "turev"]:
            adimlar.append(f"Trigonometrik türev hesaplanıyor: {fonksiyon}")
            
            if fonksiyon_temiz in trig_turevler:
                sonuc = trig_turevler[fonksiyon_temiz]
                adimlar.append(f"Trigonometrik türev kuralı:")
                adimlar.append(f"d/dx[{fonksiyon}] = {sonuc}")
                
                # Açıklama ekle
                if "sin" in fonksiyon_temiz:
                    adimlar.append("Sinüs fonksiyonunun türevi kosinüs fonksiyonudur")
                elif "cos" in fonksiyon_temiz:
                    adimlar.append("Kosinüs fonksiyonunun türevi negatif sinüs fonksiyonudur")
                elif "tan" in fonksiyon_temiz:
                    adimlar.append("Tanjant fonksiyonunun türevi sekant karesine eşittir")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "fonksiyon": fonksiyon,
                    "islem": "türev",
                    "sonuc": sonuc
                }
            else:
                return {
                    "basarili": False,
                    "hata": f"Bilinmeyen trigonometrik fonksiyon: {fonksiyon}",
                    "adimlar": adimlar
                }
        
        elif islem.lower() == "integral":
            adimlar.append(f"Trigonometrik integral hesaplanıyor: ∫{fonksiyon} dx")
            
            if fonksiyon_temiz in trig_integraller:
                sonuc = trig_integraller[fonksiyon_temiz]
                adimlar.append(f"Trigonometrik integral kuralı:")
                adimlar.append(f"∫{fonksiyon} dx = {sonuc} + C")
                
                # Açıklama ekle
                if "sin" in fonksiyon_temiz:
                    adimlar.append("Sinüs fonksiyonunun integrali negatif kosinüstür")
                elif "cos" in fonksiyon_temiz:
                    adimlar.append("Kosinüs fonksiyonunun integrali sinüstür")
                elif "tan" in fonksiyon_temiz:
                    adimlar.append("Tanjant fonksiyonunun integrali -ln|cos(x)|'tır")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "fonksiyon": fonksiyon,
                    "islem": "integral",
                    "sonuc": sonuc
                }
            else:
                return {
                    "basarili": False,
                    "hata": f"Bilinmeyen trigonometrik fonksiyon: {fonksiyon}",
                    "adimlar": adimlar
                }
        
        else:
            return {
                "basarili": False,
                "hata": f"Desteklenmeyen işlem: {islem}. 'türev' veya 'integral' kullanın",
                "adimlar": []
            }
            
    except Exception as e:
        return {
            "basarili": False,
            "hata": f"Trigonometrik analiz sırasında hata: {str(e)}",
            "adimlar": []
        }


# Test fonksiyonu
if __name__ == "__main__":
    # Test örnekleri
    test_hesaplamalari = [
        ("sin", 30, "derece"),
        ("cos", 45, "derece"),
        ("tan", 60, "derece"),
        ("sin", 90, "derece")
    ]
    
    cozucu = TrigonometriCozucu()
    
    print("🔺 TRİGONOMETRİ MODÜLÜ TEST")
    print("=" * 50)
    
    for fonksiyon, aci, birim in test_hesaplamalari:
        print(f"\n--- Test: {fonksiyon}({aci}°) ---")
        sonuc = cozucu.fonksiyon_hesapla(fonksiyon, aci, birim)
        
        if sonuc["basarili"]:
            for adim in sonuc["adimlar"]:
                print(adim)
            print(f"Sonuç: {sonuc['sonuc']:.6f}")
        else:
            print(f"Hata: {sonuc['hata']}")
    
    # Ters fonksiyon testi
    print(f"\n--- Test: arcsin(0.5) ---")
    ters_sonuc = cozucu.ters_fonksiyon_hesapla("arcsin", 0.5)
    if ters_sonuc["basarili"]:
        for adim in ters_sonuc["adimlar"]:
            print(adim)
    
    # Açı dönüşümü testi
    print(f"\n--- Test: 90° → radyan ---")
    donusum_sonuc = cozucu.aci_donusumu(90, "derece", "radyan")
    if donusum_sonuc["basarili"]:
        for adim in donusum_sonuc["adimlar"]:
            print(adim)
    
    # Trigonometrik denklem testleri
    trig_denklemler = [
        "sin(x) = 0.5",
        "cos(x) = 0",
        "tan(x) = 1"
    ]
    
    print(f"\n{'='*50}")
    print("TRİGONOMETRİK DENKLEM TESTLERİ")
    print(f"{'='*50}")
    
    for denklem in trig_denklemler:
        print(f"\n--- Test: {denklem} ---")
        sonuc = cozucu.trigonometrik_denklem_coz(denklem)
        
        if sonuc["basarili"]:
            for adim in sonuc["adimlar"]:
                print(adim)
            print(f"Çözüm sayısı: {sonuc['cozum_sayisi']}")
        else:
            print(f"Hata: {sonuc['hata']}")

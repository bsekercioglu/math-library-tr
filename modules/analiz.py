#!/usr/bin/env python3
"""
Analiz Modülü - Türkçe Matematik Kütüphanesi

Bu modül matematik analizini içerir:
- Türev hesaplamaları
- İntegral hesaplamaları
- Trigonometrik fonksiyonların türev ve integralleri
- Limit hesaplamaları
- Temel analiz kuralları
"""

import math
import sympy as sp
from typing import Dict, List, Tuple, Optional, Any
import re


class AnalizCozucu:
    """Ana analiz çözücü sınıfı"""
    
    def __init__(self):
        self.x = sp.Symbol('x')
        self.t = sp.Symbol('t')
        
    def turev_hesapla(self, fonksiyon_str: str, degisken: str = 'x') -> Dict[str, Any]:
        """
        Fonksiyonun türevini hesaplar.
        
        Args:
            fonksiyon_str (str): Türevi alınacak fonksiyon
            degisken (str): Türev değişkeni (varsayılan: x)
        
        Returns:
            Dict: Türev hesaplama sonuçları
        """
        try:
            adimlar = []
            adimlar.append(f"Verilen fonksiyon: f({degisken}) = {fonksiyon_str}")
            
            # Fonksiyonu temizle ve sympy formatına çevir
            fonksiyon_temiz = self._fonksiyon_temizle(fonksiyon_str)
            adimlar.append(f"Temizlenmiş fonksiyon: {fonksiyon_temiz}")
            
            # Sympy ifadesi oluştur
            if degisken == 'x':
                var = self.x
            elif degisken == 't':
                var = self.t
            else:
                var = sp.Symbol(degisken)
            
            try:
                fonksiyon = sp.sympify(fonksiyon_temiz)
                adimlar.append(f"SymPy ifadesi: {fonksiyon}")
            except Exception as e:
                return {
                    "basarili": False,
                    "hata": f"Fonksiyon ayrıştırılamadı: {str(e)}",
                    "adimlar": adimlar
                }
            
            # Türev hesapla
            turev = sp.diff(fonksiyon, var)
            adimlar.append(f"Türev kuralları uygulanıyor...")
            
            # Türev kurallarını açıkla
            self._turev_kurallari_acikla(fonksiyon, var, adimlar)
            
            adimlar.append(f"f'({degisken}) = {turev}")
            
            # Basitleştir
            turev_basit = sp.simplify(turev)
            if turev != turev_basit:
                adimlar.append(f"Basitleştirilmiş: f'({degisken}) = {turev_basit}")
            
            # Sonuçları daha okunabilir hale getir
            turev_okunabilir = self._matematik_sembolleri_donustur(str(turev))
            turev_basit_okunabilir = self._matematik_sembolleri_donustur(str(turev_basit))
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "orijinal_fonksiyon": fonksiyon_str,
                "temizlenmis_fonksiyon": fonksiyon_temiz,
                "sympy_fonksiyon": str(fonksiyon),
                "turev": turev_okunabilir,
                "turev_basit": turev_basit_okunabilir,
                "degisken": degisken
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Türev hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def integral_hesapla(self, fonksiyon_str: str, degisken: str = 'x', belirli: bool = False, 
                        alt_sinir: Optional[float] = None, ust_sinir: Optional[float] = None) -> Dict[str, Any]:
        """
        Fonksiyonun integralini hesaplar.
        
        Args:
            fonksiyon_str (str): İntegrali alınacak fonksiyon
            degisken (str): İntegral değişkeni (varsayılan: x)
            belirli (bool): Belirli integral mi?
            alt_sinir (float): Alt sınır (belirli integral için)
            ust_sinir (float): Üst sınır (belirli integral için)
        
        Returns:
            Dict: İntegral hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if belirli and (alt_sinir is None or ust_sinir is None):
                return {
                    "basarili": False,
                    "hata": "Belirli integral için alt ve üst sınır gerekli",
                    "adimlar": []
                }
            
            if belirli:
                adimlar.append(f"Belirli integral: ∫[{alt_sinir}→{ust_sinir}] {fonksiyon_str} d{degisken}")
            else:
                adimlar.append(f"Belirsiz integral: ∫ {fonksiyon_str} d{degisken}")
            
            # Fonksiyonu temizle ve sympy formatına çevir
            fonksiyon_temiz = self._fonksiyon_temizle(fonksiyon_str)
            adimlar.append(f"Temizlenmiş fonksiyon: {fonksiyon_temiz}")
            
            # Sympy ifadesi oluştur
            if degisken == 'x':
                var = self.x
            elif degisken == 't':
                var = self.t
            else:
                var = sp.Symbol(degisken)
            
            try:
                fonksiyon = sp.sympify(fonksiyon_temiz)
                adimlar.append(f"SymPy ifadesi: {fonksiyon}")
            except Exception as e:
                return {
                    "basarili": False,
                    "hata": f"Fonksiyon ayrıştırılamadı: {str(e)}",
                    "adimlar": adimlar
                }
            
            # İntegral hesapla
            if belirli:
                integral = sp.integrate(fonksiyon, (var, alt_sinir, ust_sinir))
                adimlar.append(f"Belirli integral hesaplanıyor: ∫[{alt_sinir}→{ust_sinir}] {fonksiyon} d{degisken}")
                
                # Önce belirsiz integrali bul
                belirsiz_integral = sp.integrate(fonksiyon, var)
                adimlar.append(f"Önce belirsiz integral: ∫ {fonksiyon} d{degisken} = {belirsiz_integral}")
                
                # Sınırları uygula
                adimlar.append(f"Sınırlar uygulanıyor: [{belirsiz_integral}]_{alt_sinir}^{ust_sinir}")
                adimlar.append(f"= ({belirsiz_integral})|_{degisken}={ust_sinir} - ({belirsiz_integral})|_{degisken}={alt_sinir}")
                
                # Sayısal değeri hesapla
                try:
                    sayisal_deger = float(integral.evalf())
                    adimlar.append(f"= {integral} = {sayisal_deger:.6f}")
                except:
                    sayisal_deger = None
                    adimlar.append(f"= {integral}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "orijinal_fonksiyon": fonksiyon_str,
                    "temizlenmis_fonksiyon": fonksiyon_temiz,
                    "sympy_fonksiyon": str(fonksiyon),
                    "integral_turu": "belirli",
                    "belirsiz_integral": str(belirsiz_integral),
                    "integral": str(integral),
                    "sayisal_deger": sayisal_deger,
                    "alt_sinir": alt_sinir,
                    "ust_sinir": ust_sinir,
                    "degisken": degisken
                }
            
            else:
                integral = sp.integrate(fonksiyon, var)
                adimlar.append(f"İntegral kuralları uygulanıyor...")
                
                # İntegral kurallarını açıkla
                self._integral_kurallari_acikla(fonksiyon, var, adimlar)
                
                # Karmaşık integraller için açıklama ekle
                integral_str = str(integral)
                if any(term in integral_str.lower() for term in ['fresnels', 'fresnelc', 'gamma', 'erf', 'ei', 'li']):
                    adimlar.append("Bu integral karmaşık özel fonksiyonlar içerir:")
                    
                    if 'fresnels' in integral_str.lower():
                        adimlar.append("• Fresnel S(x) fonksiyonu: ∫₀ˣ sin(πt²/2) dt integrali")
                        adimlar.append("• Bu fonksiyon optik ve difraksiyon problemlerinde kullanılır")
                        adimlar.append("• Notasyon: S(x) = Fresnel sinüs integrali")
                    
                    if 'fresnelc' in integral_str.lower():
                        adimlar.append("• Fresnel C(x) fonksiyonu: ∫₀ˣ cos(πt²/2) dt integrali")
                        adimlar.append("• Notasyon: C(x) = Fresnel kosinüs integrali")
                    
                    if 'gamma' in integral_str.lower():
                        adimlar.append("• Gamma fonksiyonu: faktöriyelin genelleştirilmiş hali")
                        adimlar.append("• Γ(n) = (n-1)! (pozitif tam sayılar için)")
                    
                    if 'erf' in integral_str.lower():
                        adimlar.append("• Hata fonksiyonu: ∫e^(-t²)dt integrali")
                        adimlar.append("• İstatistik ve olasılık hesaplamalarında kullanılır")
                    
                    adimlar.append("Bu integral basit cebirsel fonksiyonlarla ifade edilemez.")
                    adimlar.append("Sayısal hesaplama veya özel fonksiyon tabloları gerekir.")
                
                adimlar.append(f"∫ {fonksiyon} d{degisken} = {integral} + C")
                
                # Basitleştir
                integral_basit = sp.simplify(integral)
                if integral != integral_basit:
                    adimlar.append(f"Basitleştirilmiş: ∫ {fonksiyon} d{degisken} = {integral_basit} + C")
                
                # Sonuçları daha okunabilir hale getir
                integral_okunabilir = self._matematik_sembolleri_donustur(str(integral))
                integral_basit_okunabilir = self._matematik_sembolleri_donustur(str(integral_basit))
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "orijinal_fonksiyon": fonksiyon_str,
                    "temizlenmis_fonksiyon": fonksiyon_temiz,
                    "sympy_fonksiyon": str(fonksiyon),
                    "integral_turu": "belirsiz",
                    "integral": integral_okunabilir,
                    "integral_basit": integral_basit_okunabilir,
                    "degisken": degisken,
                    "karmasik_integral": any(term in str(integral).lower() for term in ['fresnels', 'fresnelc', 'gamma', 'erf', 'ei', 'li'])
                }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"İntegral hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def trigonometrik_turev_integral(self, islem: str, fonksiyon: str) -> Dict[str, Any]:
        """
        Trigonometrik fonksiyonların türev ve integrallerini hesaplar.
        
        Args:
            islem (str): 'turev' veya 'integral'
            fonksiyon (str): Trigonometrik fonksiyon
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            adimlar = []
            
            # Temel trigonometrik fonksiyonların türev ve integralleri
            trig_turevler = {
                "sin(x)": "cos(x)",
                "cos(x)": "-sin(x)",
                "tan(x)": "sec²(x) = 1/cos²(x)",
                "cot(x)": "-csc²(x) = -1/sin²(x)",
                "sec(x)": "sec(x)tan(x)",
                "csc(x)": "-csc(x)cot(x)"
            }
            
            trig_integraller = {
                "sin(x)": "-cos(x)",
                "cos(x)": "sin(x)",
                "tan(x)": "-ln|cos(x)|",
                "cot(x)": "ln|sin(x)|",
                "sec(x)": "ln|sec(x) + tan(x)|",
                "csc(x)": "-ln|csc(x) + cot(x)|"
            }
            
            if islem == "turev":
                if fonksiyon in trig_turevler:
                    sonuc = trig_turevler[fonksiyon]
                    adimlar.append(f"Trigonometrik türev kuralı:")
                    adimlar.append(f"d/dx[{fonksiyon}] = {sonuc}")
                    
                    # Açıklama ekle
                    if fonksiyon == "sin(x)":
                        adimlar.append("Sinüs fonksiyonunun türevi kosinüstür")
                    elif fonksiyon == "cos(x)":
                        adimlar.append("Kosinüs fonksiyonunun türevi negatif sinüstür")
                    elif fonksiyon == "tan(x)":
                        adimlar.append("Tanjant fonksiyonunun türevi sekant karesine eşittir")
                    
                    return {
                        "basarili": True,
                        "adimlar": adimlar,
                        "fonksiyon": fonksiyon,
                        "islem": "turev",
                        "sonuc": sonuc
                    }
                else:
                    # SymPy ile hesapla
                    return self.turev_hesapla(fonksiyon)
            
            elif islem == "integral":
                if fonksiyon in trig_integraller:
                    sonuc = trig_integraller[fonksiyon]
                    adimlar.append(f"Trigonometrik integral kuralı:")
                    adimlar.append(f"∫ {fonksiyon} dx = {sonuc} + C")
                    
                    # Açıklama ekle
                    if fonksiyon == "sin(x)":
                        adimlar.append("Sinüs fonksiyonunun integrali negatif kosinüstür")
                    elif fonksiyon == "cos(x)":
                        adimlar.append("Kosinüs fonksiyonunun integrali sinüstür")
                    elif fonksiyon == "tan(x)":
                        adimlar.append("Tanjant fonksiyonunun integrali -ln|cos(x)|'tır")
                    
                    return {
                        "basarili": True,
                        "adimlar": adimlar,
                        "fonksiyon": fonksiyon,
                        "islem": "integral",
                        "sonuc": sonuc
                    }
                else:
                    # SymPy ile hesapla
                    return self.integral_hesapla(fonksiyon)
            
            else:
                return {
                    "basarili": False,
                    "hata": f"Desteklenmeyen işlem: {islem}",
                    "adimlar": []
                }
                
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Trigonometrik analiz sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def _fonksiyon_temizle(self, fonksiyon_str: str) -> str:
        """Fonksiyon string'ini SymPy için temizler"""
        fonksiyon_temiz = fonksiyon_str.lower().strip()
        
        # Türkçe fonksiyon isimlerini çevir
        donusumler = {
            "sinüs": "sin",
            "kosinüs": "cos", 
            "tanjant": "tan",
            "kotanjant": "cot",
            "sekant": "sec",
            "kosekant": "csc",
            "ln": "log",
            "üs": "**",
            "^": "**"
        }
        
        for tr_kelime, en_kelime in donusumler.items():
            fonksiyon_temiz = fonksiyon_temiz.replace(tr_kelime, en_kelime)
        
        # Matematiksel ifadeleri düzelt
        fonksiyon_temiz = re.sub(r'(\d)([a-z])', r'\1*\2', fonksiyon_temiz)  # 2x -> 2*x
        fonksiyon_temiz = fonksiyon_temiz.replace("²", "**2")
        fonksiyon_temiz = fonksiyon_temiz.replace("³", "**3")
        
        return fonksiyon_temiz
    
    def _turev_kurallari_acikla(self, fonksiyon, var, adimlar):
        """Türev kurallarını açıklar"""
        if isinstance(fonksiyon, sp.Add):
            adimlar.append("Toplam kuralı: (f + g)' = f' + g'")
        elif isinstance(fonksiyon, sp.Mul):
            adimlar.append("Çarpım kuralı: (fg)' = f'g + fg'")
        elif isinstance(fonksiyon, sp.Pow):
            adimlar.append("Kuvvet kuralı: (x^n)' = n*x^(n-1)")
        elif isinstance(fonksiyon, (sp.sin, sp.cos, sp.tan)):
            adimlar.append("Trigonometrik türev kuralları uygulanıyor")
    
    def _integral_kurallari_acikla(self, fonksiyon, var, adimlar):
        """İntegral kurallarını açıklar"""
        if isinstance(fonksiyon, sp.Add):
            adimlar.append("Toplam kuralı: ∫(f + g)dx = ∫f dx + ∫g dx")
        elif isinstance(fonksiyon, sp.Mul):
            adimlar.append("Sabit çarpan kuralı: ∫c·f dx = c·∫f dx")
        elif isinstance(fonksiyon, sp.Pow):
            adimlar.append("Kuvvet kuralı: ∫x^n dx = x^(n+1)/(n+1) + C")
        elif isinstance(fonksiyon, (sp.sin, sp.cos, sp.tan)):
            adimlar.append("Trigonometrik integral kuralları uygulanıyor")
    
    def _matematik_sembolleri_donustur(self, metin: str) -> str:
        """Matematik ifadelerini daha okunabilir sembollerle değiştirir"""
        # sqrt yerine karekök sembolü
        import re
        
        # sqrt(x) -> √x formatına çevir
        metin = re.sub(r'sqrt\(([^)]+)\)', r'√(\1)', metin)
        
        # Fresnel fonksiyonları için özel gösterim
        metin = re.sub(r'fresnels\(([^)]+)\)', r'S(\1)', metin)  # Fresnel S
        metin = re.sub(r'fresnelc\(([^)]+)\)', r'C(\1)', metin)  # Fresnel C
        
        # Diğer özel fonksiyonlar
        metin = re.sub(r'erf\(([^)]+)\)', r'erf(\1)', metin)      # Hata fonksiyonu (zaten kısa)
        metin = re.sub(r'erfc\(([^)]+)\)', r'erfc(\1)', metin)    # Tamamlayıcı hata fonksiyonu
        metin = re.sub(r'elliptic_f\(([^,]+),([^)]+)\)', r'F(\1|\2)', metin)  # Eliptik integral
        metin = re.sub(r'elliptic_e\(([^,]+),([^)]+)\)', r'E(\1|\2)', metin)  # Eliptik integral
        
        # Diğer matematik sembolleri
        donusumler = {
            'pi': 'π',
            'Pi': 'π', 
            'infinity': '∞',
            'alpha': 'α',
            'beta': 'β',
            'gamma': 'γ',
            'Gamma': 'Γ',
            'delta': 'δ',
            'Delta': 'Δ',
            'theta': 'θ',
            'Theta': 'Θ',
            'lambda': 'λ',
            'mu': 'μ',
            'sigma': 'σ',
            'Sigma': 'Σ',
            'phi': 'φ',
            'Phi': 'Φ',
            'omega': 'ω',
            'Omega': 'Ω'
        }
        
        # Kelime sınırlarında değiştir (başka kelimelerin içindeki harfleri etkilemesin)
        for eski, yeni in donusumler.items():
            metin = re.sub(r'\b' + re.escape(eski) + r'\b', yeni, metin)
        
        return metin


# Global fonksiyonlar
def turev_hesapla(fonksiyon: str, degisken: str = 'x') -> Dict[str, Any]:
    """Fonksiyonun türevini hesaplar"""
    cozucu = AnalizCozucu()
    return cozucu.turev_hesapla(fonksiyon, degisken)


def integral_hesapla(fonksiyon: str, degisken: str = 'x', belirli: bool = False,
                    alt_sinir: Optional[float] = None, ust_sinir: Optional[float] = None) -> Dict[str, Any]:
    """Fonksiyonun integralini hesaplar"""
    cozucu = AnalizCozucu()
    return cozucu.integral_hesapla(fonksiyon, degisken, belirli, alt_sinir, ust_sinir)


def trigonometrik_analiz(islem: str, fonksiyon: str) -> Dict[str, Any]:
    """Trigonometrik fonksiyonların türev ve integrallerini hesaplar"""
    cozucu = AnalizCozucu()
    return cozucu.trigonometrik_turev_integral(islem, fonksiyon)


# Test fonksiyonu
if __name__ == "__main__":
    print("📊 ANALİZ MODÜLÜ TEST")
    print("=" * 50)
    
    # Türev testleri
    print("\n1. Türev Testi (x²):")
    sonuc = turev_hesapla("x**2")
    if sonuc["basarili"]:
        print(f"   Türev: {sonuc['turev']}")
    
    print("\n2. Trigonometrik Türev Testi:")
    sonuc = trigonometrik_analiz("turev", "sin(x)")
    if sonuc["basarili"]:
        print(f"   sin(x)' = {sonuc['sonuc']}")
    
    print("\n3. İntegral Testi (x²):")
    sonuc = integral_hesapla("x**2")
    if sonuc["basarili"]:
        print(f"   İntegral: {sonuc['integral']}")
    
    print("\n4. Belirli İntegral Testi:")
    sonuc = integral_hesapla("x**2", belirli=True, alt_sinir=0, ust_sinir=2)
    if sonuc["basarili"]:
        print(f"   Belirli integral [0,2]: {sonuc['sayisal_deger']}")


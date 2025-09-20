"""
Cebir Modülü - Matematik Kütüphanesi
====================================

Bu modül cebirsel işlemler için fonksiyonlar içerir.
Desteklenen işlemler:
- İkinci dereceden denklem çözme
- Çarpanlara ayırma
- Polinomial işlemler
- Matematik ifadesi hesaplama (faktöriyel, üslü sayılar, vs.)

Yazar: Matematik Kütüphanesi
"""

import sympy as sp
import re
import math
from typing import Dict, List, Tuple, Optional


class CebirCozucu:
    """Cebir problemlerini çözen ana sınıf"""
    
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.z = sp.Symbol('z')
    
    def ikinci_dereceden_coz(self, denklem_str: str) -> Dict[str, any]:
        """
        İkinci dereceden denklemi çözer.
        
        Args:
            denklem_str (str): Denklem string formatında (örn: "x^2 - 5x + 6 = 0")
        
        Returns:
            Dict: Çözüm adımları ve sonuçları içeren sözlük
        """
        try:
            # Denklemi ayrıştır
            denklem_temizlendi = self._denklem_temizle(denklem_str)
            
            # Sympy ile denklemi parse et
            denklem = sp.sympify(denklem_temizlendi)
            
            # Katsayıları al
            a, b, c = self._katsayilari_al(denklem)
            
            # Çözüm adımlarını hesapla
            adimlar = []
            adimlar.append(f"Verilen denklem: {denklem} = 0")
            adimlar.append(f"Standart form: ax² + bx + c = 0")
            adimlar.append(f"Katsayılar: a = {a}, b = {b}, c = {c}")
            
            # Diskriminant hesapla
            diskriminant = b**2 - 4*a*c
            adimlar.append(f"Diskriminant (Δ) = b² - 4ac = ({b})² - 4({a})({c}) = {b**2} - {4*a*c} = {diskriminant}")
            
            # Kökleri hesapla
            kokler = sp.solve(denklem, self.x)
            
            if diskriminant > 0:
                adimlar.append("Δ > 0 olduğu için iki farklı gerçek kök vardır.")
                adimlar.append(f"x₁ = (-b + √Δ) / 2a = ({-b} + √{diskriminant}) / {2*a} = {kokler[0]}")
                adimlar.append(f"x₂ = (-b - √Δ) / 2a = ({-b} - √{diskriminant}) / {2*a} = {kokler[1]}")
            elif diskriminant == 0:
                adimlar.append("Δ = 0 olduğu için bir çift kök vardır.")
                adimlar.append(f"x = -b / 2a = {-b} / {2*a} = {kokler[0]}")
            else:
                adimlar.append("Δ < 0 olduğu için gerçek kök yoktur (karmaşık kökler var).")
                adimlar.append(f"x₁ = {kokler[0]}")
                adimlar.append(f"x₂ = {kokler[1]}")
            
            # Çarpanlara ayırma
            carpanlar = sp.factor(denklem)
            if carpanlar != denklem:
                adimlar.append(f"Çarpanlarına ayrılmış hali: {carpanlar} = 0")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "kokler": kokler,
                "diskriminant": diskriminant,
                "katsayilar": {"a": a, "b": b, "c": c},
                "carpanlar": carpanlar
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Denklem çözülürken hata oluştu: {str(e)}",
                "adimlar": []
            }
    
    def _denklem_temizle(self, denklem_str: str) -> str:
        """Denklem string'ini temizler ve sympy formatına dönüştürür"""
        # Türkçe karakterleri değiştir
        denklem = denklem_str.lower()
        
        # Eşittir işaretinden sonrasını sıfıra al
        if "=" in denklem:
            sol, sag = denklem.split("=", 1)
            denklem = f"({sol}) - ({sag})"
        
        # ² karakterini **2 ile değiştir
        denklem = denklem.replace("²", "**2")
        # ^ karakterini ** ile değiştir  
        denklem = denklem.replace("^", "**")
        
        # Türkçe karakterleri temizle
        denklem = denklem.replace("ü", "u").replace("ğ", "g").replace("ı", "i")
        denklem = denklem.replace("ş", "s").replace("ç", "c").replace("ö", "o")
        
        # Boşlukları temizle
        denklem = re.sub(r'\s+', '', denklem)
        
        # Çarpma işlemlerini düzelt (2x -> 2*x)
        denklem = re.sub(r'(\d)([a-z])', r'\1*\2', denklem)
        
        return denklem
    
    def _katsayilari_al(self, denklem) -> Tuple[float, float, float]:
        """Denklemden a, b, c katsayılarını alır"""
        try:
            expanded = sp.expand(denklem)
            
            # Polinomun katsayılarını al
            poly = sp.Poly(expanded, self.x)
            katsayilar = poly.all_coeffs()
            
            # 2. derece denklemi için a, b, c katsayıları
            if len(katsayilar) == 3:
                return float(katsayilar[0]), float(katsayilar[1]), float(katsayilar[2])
            elif len(katsayilar) == 2:
                return 0.0, float(katsayilar[0]), float(katsayilar[1])
            elif len(katsayilar) == 1:
                return 0.0, 0.0, float(katsayilar[0])
            else:
                return 1.0, 0.0, 0.0
        except:
            # Hata durumunda default değerler
            return 1.0, 0.0, 0.0
    
    def carpanlara_ayir(self, ifade_str: str) -> Dict[str, any]:
        """
        Verilen ifadeyi çarpanlarına ayırır.
        
        Args:
            ifade_str (str): Çarpanlarına ayrılacak ifade
        
        Returns:
            Dict: Çözüm adımları ve sonuçları
        """
        try:
            ifade_temizlendi = self._denklem_temizle(ifade_str)
            ifade = sp.sympify(ifade_temizlendi)
            
            adimlar = []
            adimlar.append(f"Verilen ifade: {ifade}")
            
            # Çarpanlara ayır
            carpanlar = sp.factor(ifade)
            
            if carpanlar != ifade:
                adimlar.append(f"Çarpanlarına ayrılmış hali: {carpanlar}")
            else:
                adimlar.append("Bu ifade daha fazla çarpanlarına ayrılamaz.")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "orijinal": ifade,
                "carpanlar": carpanlar
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Çarpanlara ayırma sırasında hata oluştu: {str(e)}",
                "adimlar": []
            }


# Kullanım kolaylığı için global fonksiyonlar
def ikinci_dereceden_coz(denklem: str) -> Dict[str, any]:
    """İkinci dereceden denklem çözer"""
    cozucu = CebirCozucu()
    return cozucu.ikinci_dereceden_coz(denklem)


def carpanlara_ayir(ifade: str) -> Dict[str, any]:
    """İfadeyi çarpanlarına ayırır"""
    cozucu = CebirCozucu()
    return cozucu.carpanlara_ayir(ifade)


# Test fonksiyonu
if __name__ == "__main__":
    # Test örnekleri
    test_denklemleri = [
        "x^2 - 5x + 6 = 0",
        "2x^2 + 3x - 2 = 0",
        "x^2 - 4 = 0",
        "x^2 + 1 = 0"
    ]
    
    for denklem in test_denklemleri:
        print(f"\n--- Test: {denklem} ---")
        sonuc = ikinci_dereceden_coz(denklem)
        
        if sonuc["basarili"]:
            for adim in sonuc["adimlar"]:
                print(adim)
            print(f"Kökler: {sonuc['kokler']}")
        else:
            print(f"Hata: {sonuc['hata']}")


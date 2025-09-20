#!/usr/bin/env python3
"""
Geometri Modülü - Türkçe Matematik Kütüphanesi

Bu modül tüm geometrik hesaplamaları içerir:
- Üçgen teoremi ve hesaplamaları
- 2D şekillerde alan ve çevre hesaplamaları
- 3D şekillerde hacim ve yüzey alanı hesaplamaları
- Çember, yay ve kesit hesaplamaları
- Koordinat geometrisi
"""

import math
import sympy as sp
from typing import Dict, List, Tuple, Optional, Any
import re


class GeometriCozucu:
    """Ana geometri çözücü sınıfı"""
    
    def __init__(self):
        self.pi = math.pi
        
    def ucgen_hesaplama(self, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
        """
        Üçgen hesaplamaları yapar.
        
        Args:
            hesaplama_turu (str): 'alan', 'cevre', 'ucuncu_kenar', 'pisagor', 'cosinus_kurali', 'sinus_kurali'
            **kwargs: Hesaplama parametreleri
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if hesaplama_turu == "alan":
                return self._ucgen_alan_hesapla(**kwargs)
            elif hesaplama_turu == "cevre":
                return self._ucgen_cevre_hesapla(**kwargs)
            elif hesaplama_turu == "ucuncu_kenar":
                return self._ucuncu_kenar_hesapla(**kwargs)
            elif hesaplama_turu == "pisagor":
                return self._pisagor_teoremi(**kwargs)
            elif hesaplama_turu == "cosinus_kurali":
                return self._cosinus_kurali(**kwargs)
            elif hesaplama_turu == "sinus_kurali":
                return self._sinus_kurali(**kwargs)
            else:
                return {
                    "basarili": False,
                    "hata": f"Desteklenmeyen hesaplama türü: {hesaplama_turu}",
                    "adimlar": []
                }
                
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Üçgen hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def _ucgen_alan_hesapla(self, **kwargs) -> Dict[str, Any]:
        """Üçgen alan hesaplamaları"""
        adimlar = []
        
        # Taban ve yükseklik ile alan
        if "taban" in kwargs and "yukseklik" in kwargs:
            taban = float(kwargs["taban"])
            yukseklik = float(kwargs["yukseklik"])
            
            alan = (taban * yukseklik) / 2
            
            adimlar.append(f"Üçgen alan formülü: Alan = (taban × yükseklik) / 2")
            adimlar.append(f"Verilen: taban = {taban}, yükseklik = {yukseklik}")
            adimlar.append(f"Alan = ({taban} × {yukseklik}) / 2")
            adimlar.append(f"Alan = {taban * yukseklik} / 2")
            adimlar.append(f"Alan = {alan}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "ucgen_alan_taban_yukseklik",
                "taban": taban,
                "yukseklik": yukseklik,
                "alan": alan
            }
        
        # Üç kenar ile alan (Heron formülü)
        elif "a" in kwargs and "b" in kwargs and "c" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            c = float(kwargs["c"])
            
            # Üçgen oluşabilme kontrolü
            if not (a + b > c and a + c > b and b + c > a):
                return {
                    "basarili": False,
                    "hata": f"Bu kenar uzunlukları ile üçgen oluşturulamaz: {a}, {b}, {c}",
                    "adimlar": []
                }
            
            s = (a + b + c) / 2  # Yarı çevre
            alan = math.sqrt(s * (s - a) * (s - b) * (s - c))
            
            adimlar.append(f"Heron formülü: Alan = √[s(s-a)(s-b)(s-c)]")
            adimlar.append(f"Verilen kenarlar: a = {a}, b = {b}, c = {c}")
            adimlar.append(f"Yarı çevre: s = (a + b + c) / 2 = ({a} + {b} + {c}) / 2 = {s}")
            adimlar.append(f"s - a = {s} - {a} = {s - a}")
            adimlar.append(f"s - b = {s} - {b} = {s - b}")
            adimlar.append(f"s - c = {s} - {c} = {s - c}")
            adimlar.append(f"Alan = √[{s} × {s - a} × {s - b} × {s - c}]")
            adimlar.append(f"Alan = √[{s * (s - a) * (s - b) * (s - c)}]")
            adimlar.append(f"Alan = {alan:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "ucgen_alan_heron",
                "kenarlar": {"a": a, "b": b, "c": c},
                "yari_cevre": s,
                "alan": alan
            }
        
        # İki kenar ve aralarındaki açı ile alan
        elif "kenar1" in kwargs and "kenar2" in kwargs and "aci" in kwargs:
            kenar1 = float(kwargs["kenar1"])
            kenar2 = float(kwargs["kenar2"])
            aci = float(kwargs["aci"])  # Derece cinsinden
            
            aci_radyan = math.radians(aci)
            alan = (kenar1 * kenar2 * math.sin(aci_radyan)) / 2
            
            adimlar.append(f"İki kenar ve aralarındaki açı ile alan formülü:")
            adimlar.append(f"Alan = (kenar1 × kenar2 × sin(açı)) / 2")
            adimlar.append(f"Verilen: kenar1 = {kenar1}, kenar2 = {kenar2}, açı = {aci}°")
            adimlar.append(f"Açıyı radyana çevir: {aci}° = {aci_radyan:.6f} radyan")
            adimlar.append(f"sin({aci}°) = {math.sin(aci_radyan):.6f}")
            adimlar.append(f"Alan = ({kenar1} × {kenar2} × {math.sin(aci_radyan):.6f}) / 2")
            adimlar.append(f"Alan = {alan:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "ucgen_alan_iki_kenar_aci",
                "kenar1": kenar1,
                "kenar2": kenar2,
                "aci_derece": aci,
                "aci_radyan": aci_radyan,
                "alan": alan
            }
        
        else:
            return {
                "basarili": False,
                "hata": "Üçgen alanı için yeterli parametre verilmedi. Gerekli: (taban, yükseklik) veya (a, b, c) veya (kenar1, kenar2, açı)",
                "adimlar": []
            }
    
    def _ucgen_cevre_hesapla(self, **kwargs) -> Dict[str, Any]:
        """Üçgen çevre hesaplama"""
        adimlar = []
        
        if "a" in kwargs and "b" in kwargs and "c" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            c = float(kwargs["c"])
            
            cevre = a + b + c
            
            adimlar.append(f"Üçgen çevre formülü: Çevre = a + b + c")
            adimlar.append(f"Verilen kenarlar: a = {a}, b = {b}, c = {c}")
            adimlar.append(f"Çevre = {a} + {b} + {c} = {cevre}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "ucgen_cevre",
                "kenarlar": {"a": a, "b": b, "c": c},
                "cevre": cevre
            }
        else:
            return {
                "basarili": False,
                "hata": "Üçgen çevresi için üç kenar uzunluğu gerekli: a, b, c",
                "adimlar": []
            }
    
    def _ucuncu_kenar_hesapla(self, **kwargs) -> Dict[str, Any]:
        """İki kenar bilinen üçgende üçüncü kenar hesaplama"""
        adimlar = []
        
        # Pisagor teoremi (dik üçgen)
        if "dik_ucgen" in kwargs and kwargs["dik_ucgen"]:
            if "a" in kwargs and "b" in kwargs:
                a = float(kwargs["a"])
                b = float(kwargs["b"])
                
                c = math.sqrt(a**2 + b**2)
                
                adimlar.append(f"Dik üçgen - Pisagor teoremi: c² = a² + b²")
                adimlar.append(f"Verilen dik kenarlar: a = {a}, b = {b}")
                adimlar.append(f"c² = {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2}")
                adimlar.append(f"c = √{a**2 + b**2} = {c:.6f}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "hesaplama_turu": "pisagor_hipotenuse",
                    "dik_kenarlar": {"a": a, "b": b},
                    "hipotenus": c
                }
        
        # Kosinüs kuralı ile
        elif "a" in kwargs and "b" in kwargs and "aci_c" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            aci_c = float(kwargs["aci_c"])  # C açısı (derece)
            
            aci_c_radyan = math.radians(aci_c)
            c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(aci_c_radyan))
            
            adimlar.append(f"Kosinüs kuralı: c² = a² + b² - 2ab cos(C)")
            adimlar.append(f"Verilen: a = {a}, b = {b}, C = {aci_c}°")
            adimlar.append(f"C açısını radyana çevir: {aci_c}° = {aci_c_radyan:.6f} radyan")
            adimlar.append(f"cos({aci_c}°) = {math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c² = {a}² + {b}² - 2×{a}×{b}×{math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c² = {a**2} + {b**2} - {2 * a * b * math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c² = {a**2 + b**2 - 2 * a * b * math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c = √{a**2 + b**2 - 2 * a * b * math.cos(aci_c_radyan):.6f} = {c:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "cosinus_kurali_ucuncu_kenar",
                "bilinen_kenarlar": {"a": a, "b": b},
                "aci_derece": aci_c,
                "aci_radyan": aci_c_radyan,
                "ucuncu_kenar": c
            }
        
        else:
            return {
                "basarili": False,
                "hata": "Üçüncü kenar için: (a, b, dik_ucgen=True) veya (a, b, aci_c) gerekli",
                "adimlar": []
            }
    
    def _pisagor_teoremi(self, **kwargs) -> Dict[str, Any]:
        """Pisagor teoremi hesaplamaları"""
        adimlar = []
        
        # Hipotenüs bulma
        if "a" in kwargs and "b" in kwargs and "aranan" not in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            
            c = math.sqrt(a**2 + b**2)
            
            adimlar.append(f"Pisagor teoremi: a² + b² = c²")
            adimlar.append(f"Verilen dik kenarlar: a = {a}, b = {b}")
            adimlar.append(f"c² = a² + b² = {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2}")
            adimlar.append(f"c = √{a**2 + b**2} = {c:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "pisagor_hipotenus",
                "dik_kenarlar": {"a": a, "b": b},
                "hipotenus": c
            }
        
        # Dik kenar bulma
        elif "c" in kwargs and ("a" in kwargs or "b" in kwargs):
            c = float(kwargs["c"])
            
            if "a" in kwargs:
                a = float(kwargs["a"])
                b = math.sqrt(c**2 - a**2)
                
                adimlar.append(f"Pisagor teoremi: a² + b² = c²")
                adimlar.append(f"b² = c² - a²")
                adimlar.append(f"Verilen: c = {c}, a = {a}")
                adimlar.append(f"b² = {c}² - {a}² = {c**2} - {a**2} = {c**2 - a**2}")
                adimlar.append(f"b = √{c**2 - a**2} = {b:.6f}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "hesaplama_turu": "pisagor_dik_kenar_b",
                    "hipotenus": c,
                    "bilinen_dik_kenar": a,
                    "aranan_dik_kenar": b
                }
            
            else:  # "b" in kwargs
                b = float(kwargs["b"])
                a = math.sqrt(c**2 - b**2)
                
                adimlar.append(f"Pisagor teoremi: a² + b² = c²")
                adimlar.append(f"a² = c² - b²")
                adimlar.append(f"Verilen: c = {c}, b = {b}")
                adimlar.append(f"a² = {c}² - {b}² = {c**2} - {b**2} = {c**2 - b**2}")
                adimlar.append(f"a = √{c**2 - b**2} = {a:.6f}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "hesaplama_turu": "pisagor_dik_kenar_a",
                    "hipotenus": c,
                    "bilinen_dik_kenar": b,
                    "aranan_dik_kenar": a
                }
        
        else:
            return {
                "basarili": False,
                "hata": "Pisagor teoremi için: (a, b) veya (c, a) veya (c, b) gerekli",
                "adimlar": []
            }
    
    def _cosinus_kurali(self, **kwargs) -> Dict[str, Any]:
        """Kosinüs kuralı hesaplamaları"""
        adimlar = []
        
        # Kenar bulma
        if "a" in kwargs and "b" in kwargs and "aci_c" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            aci_c = float(kwargs["aci_c"])
            
            aci_c_radyan = math.radians(aci_c)
            c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(aci_c_radyan))
            
            adimlar.append(f"Kosinüs kuralı: c² = a² + b² - 2ab cos(C)")
            adimlar.append(f"Verilen: a = {a}, b = {b}, C = {aci_c}°")
            adimlar.append(f"cos({aci_c}°) = {math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c² = {a**2} + {b**2} - 2×{a}×{b}×{math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c² = {a**2 + b**2 - 2 * a * b * math.cos(aci_c_radyan):.6f}")
            adimlar.append(f"c = {c:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "cosinus_kurali_kenar",
                "bilinen_kenarlar": {"a": a, "b": b},
                "aci_derece": aci_c,
                "bulunan_kenar": c
            }
        
        # Açı bulma
        elif "a" in kwargs and "b" in kwargs and "c" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            c = float(kwargs["c"])
            
            cos_c = (a**2 + b**2 - c**2) / (2 * a * b)
            aci_c_radyan = math.acos(cos_c)
            aci_c = math.degrees(aci_c_radyan)
            
            adimlar.append(f"Kosinüs kuralı: cos(C) = (a² + b² - c²) / (2ab)")
            adimlar.append(f"Verilen kenarlar: a = {a}, b = {b}, c = {c}")
            adimlar.append(f"cos(C) = ({a**2} + {b**2} - {c**2}) / (2×{a}×{b})")
            adimlar.append(f"cos(C) = {a**2 + b**2 - c**2} / {2 * a * b} = {cos_c:.6f}")
            adimlar.append(f"C = arccos({cos_c:.6f}) = {aci_c:.6f}°")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "cosinus_kurali_aci",
                "kenarlar": {"a": a, "b": b, "c": c},
                "cos_deger": cos_c,
                "aci_derece": aci_c,
                "aci_radyan": aci_c_radyan
            }
        
        else:
            return {
                "basarili": False,
                "hata": "Kosinüs kuralı için: (a, b, aci_c) veya (a, b, c) gerekli",
                "adimlar": []
            }
    
    def _sinus_kurali(self, **kwargs) -> Dict[str, Any]:
        """Sinüs kuralı hesaplamaları"""
        adimlar = []
        
        # a/sin(A) = b/sin(B) = c/sin(C)
        
        # Kenar bulma
        if "a" in kwargs and "aci_a" in kwargs and "aci_b" in kwargs:
            a = float(kwargs["a"])
            aci_a = float(kwargs["aci_a"])
            aci_b = float(kwargs["aci_b"])
            
            aci_a_radyan = math.radians(aci_a)
            aci_b_radyan = math.radians(aci_b)
            
            b = (a * math.sin(aci_b_radyan)) / math.sin(aci_a_radyan)
            
            adimlar.append(f"Sinüs kuralı: a/sin(A) = b/sin(B)")
            adimlar.append(f"Verilen: a = {a}, A = {aci_a}°, B = {aci_b}°")
            adimlar.append(f"b = (a × sin(B)) / sin(A)")
            adimlar.append(f"sin({aci_a}°) = {math.sin(aci_a_radyan):.6f}")
            adimlar.append(f"sin({aci_b}°) = {math.sin(aci_b_radyan):.6f}")
            adimlar.append(f"b = ({a} × {math.sin(aci_b_radyan):.6f}) / {math.sin(aci_a_radyan):.6f}")
            adimlar.append(f"b = {b:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "sinus_kurali_kenar",
                "bilinen_kenar": a,
                "aci_a": aci_a,
                "aci_b": aci_b,
                "bulunan_kenar": b
            }
        
        # Açı bulma
        elif "a" in kwargs and "b" in kwargs and "aci_a" in kwargs:
            a = float(kwargs["a"])
            b = float(kwargs["b"])
            aci_a = float(kwargs["aci_a"])
            
            aci_a_radyan = math.radians(aci_a)
            sin_b = (b * math.sin(aci_a_radyan)) / a
            
            if abs(sin_b) > 1:
                return {
                    "basarili": False,
                    "hata": f"Geçersiz değer: sin(B) = {sin_b:.6f} (|sin(B)| ≤ 1 olmalı)",
                    "adimlar": adimlar
                }
            
            aci_b_radyan = math.asin(sin_b)
            aci_b = math.degrees(aci_b_radyan)
            
            adimlar.append(f"Sinüs kuralı: a/sin(A) = b/sin(B)")
            adimlar.append(f"Verilen: a = {a}, b = {b}, A = {aci_a}°")
            adimlar.append(f"sin(B) = (b × sin(A)) / a")
            adimlar.append(f"sin({aci_a}°) = {math.sin(aci_a_radyan):.6f}")
            adimlar.append(f"sin(B) = ({b} × {math.sin(aci_a_radyan):.6f}) / {a} = {sin_b:.6f}")
            adimlar.append(f"B = arcsin({sin_b:.6f}) = {aci_b:.6f}°")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "sinus_kurali_aci",
                "kenarlar": {"a": a, "b": b},
                "aci_a": aci_a,
                "sin_b": sin_b,
                "aci_b": aci_b
            }
        
        else:
            return {
                "basarili": False,
                "hata": "Sinüs kuralı için: (a, aci_a, aci_b) veya (a, b, aci_a) gerekli",
                "adimlar": []
            }
    
    def dortgen_hesaplama(self, sekil_turu: str, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
        """
        Dörtgen hesaplamaları.
        
        Args:
            sekil_turu (str): 'kare', 'dikdortgen', 'paralel_kenar', 'yamuk', 'eskenar_dortgen'
            hesaplama_turu (str): 'alan', 'cevre'
            **kwargs: Hesaplama parametreleri
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            if sekil_turu == "kare":
                return self._kare_hesapla(hesaplama_turu, **kwargs)
            elif sekil_turu == "dikdortgen":
                return self._dikdortgen_hesapla(hesaplama_turu, **kwargs)
            elif sekil_turu == "paralel_kenar":
                return self._paralel_kenar_hesapla(hesaplama_turu, **kwargs)
            elif sekil_turu == "yamuk":
                return self._yamuk_hesapla(hesaplama_turu, **kwargs)
            elif sekil_turu == "eskenar_dortgen":
                return self._eskenar_dortgen_hesapla(hesaplama_turu, **kwargs)
            else:
                return {
                    "basarili": False,
                    "hata": f"Desteklenmeyen dörtgen türü: {sekil_turu}",
                    "adimlar": []
                }
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Dörtgen hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def _kare_hesapla(self, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
        """Kare hesaplamaları"""
        adimlar = []
        
        if "kenar" not in kwargs:
            return {
                "basarili": False,
                "hata": "Kare hesaplaması için kenar uzunluğu gerekli",
                "adimlar": []
            }
        
        kenar = float(kwargs["kenar"])
        
        if hesaplama_turu == "alan":
            alan = kenar ** 2
            
            adimlar.append(f"Kare alan formülü: Alan = kenar²")
            adimlar.append(f"Verilen kenar: {kenar}")
            adimlar.append(f"Alan = {kenar}² = {alan}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "kare_alan",
                "kenar": kenar,
                "alan": alan
            }
        
        elif hesaplama_turu == "cevre":
            cevre = 4 * kenar
            
            adimlar.append(f"Kare çevre formülü: Çevre = 4 × kenar")
            adimlar.append(f"Verilen kenar: {kenar}")
            adimlar.append(f"Çevre = 4 × {kenar} = {cevre}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "kare_cevre",
                "kenar": kenar,
                "cevre": cevre
            }
        
        else:
            return {
                "basarili": False,
                "hata": f"Desteklenmeyen hesaplama türü: {hesaplama_turu}",
                "adimlar": []
            }
    
    def _dikdortgen_hesapla(self, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
        """Dikdörtgen hesaplamaları"""
        adimlar = []
        
        if "uzun_kenar" not in kwargs or "kisa_kenar" not in kwargs:
            return {
                "basarili": False,
                "hata": "Dikdörtgen hesaplaması için uzun_kenar ve kisa_kenar gerekli",
                "adimlar": []
            }
        
        uzun_kenar = float(kwargs["uzun_kenar"])
        kisa_kenar = float(kwargs["kisa_kenar"])
        
        if hesaplama_turu == "alan":
            alan = uzun_kenar * kisa_kenar
            
            adimlar.append(f"Dikdörtgen alan formülü: Alan = uzun kenar × kısa kenar")
            adimlar.append(f"Verilen: uzun kenar = {uzun_kenar}, kısa kenar = {kisa_kenar}")
            adimlar.append(f"Alan = {uzun_kenar} × {kisa_kenar} = {alan}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "dikdortgen_alan",
                "uzun_kenar": uzun_kenar,
                "kisa_kenar": kisa_kenar,
                "alan": alan
            }
        
        elif hesaplama_turu == "cevre":
            cevre = 2 * (uzun_kenar + kisa_kenar)
            
            adimlar.append(f"Dikdörtgen çevre formülü: Çevre = 2 × (uzun kenar + kısa kenar)")
            adimlar.append(f"Verilen: uzun kenar = {uzun_kenar}, kısa kenar = {kisa_kenar}")
            adimlar.append(f"Çevre = 2 × ({uzun_kenar} + {kisa_kenar}) = 2 × {uzun_kenar + kisa_kenar} = {cevre}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "dikdortgen_cevre",
                "uzun_kenar": uzun_kenar,
                "kisa_kenar": kisa_kenar,
                "cevre": cevre
            }
        
        else:
            return {
                "basarili": False,
                "hata": f"Desteklenmeyen hesaplama türü: {hesaplama_turu}",
                "adimlar": []
            }
    
    def daire_hesaplama(self, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
        """
        Daire hesaplamaları yapar.
        
        Args:
            hesaplama_turu (str): 'alan' veya 'cevre'
            **kwargs: yaricap, cap parametreleri
        
        Returns:
            Dict: Hesaplama sonuçları
        """
        adimlar = []
        
        # Yarıçap belirleme
        yaricap = None
        if "yaricap" in kwargs:
            yaricap = float(kwargs["yaricap"])
        elif "cap" in kwargs:
            cap = float(kwargs["cap"])
            yaricap = cap / 2
            adimlar.append(f"Çaptan yarıçap: r = çap/2 = {cap}/2 = {yaricap}")
        elif "kenar" in kwargs:  # parser bazen kenar olarak algılayabilir
            yaricap = float(kwargs["kenar"])
        else:
            return {
                "basarili": False,
                "hata": "Daire hesaplaması için yarıçap veya çap gerekli",
                "adimlar": []
            }
        
        if hesaplama_turu == "alan":
            alan = math.pi * yaricap * yaricap
            
            adimlar.append(f"Daire alan formülü: A = π × r²")
            adimlar.append(f"Verilen: r = {yaricap}")
            adimlar.append(f"A = π × {yaricap}² = π × {yaricap**2} = {math.pi} × {yaricap**2}")
            adimlar.append(f"A = {alan:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "daire_alan",
                "yaricap": yaricap,
                "alan": round(alan, 2)
            }
        
        elif hesaplama_turu == "cevre":
            cevre = 2 * math.pi * yaricap
            
            adimlar.append(f"Daire çevre formülü: Ç = 2 × π × r")
            adimlar.append(f"Verilen: r = {yaricap}")
            adimlar.append(f"Ç = 2 × π × {yaricap} = 2 × {math.pi} × {yaricap}")
            adimlar.append(f"Ç = {cevre:.6f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "hesaplama_turu": "daire_cevre",
                "yaricap": yaricap,
                "cevre": round(cevre, 2)
            }
        
        else:
            return {
                "basarili": False,
                "hata": f"Desteklenmeyen hesaplama türü: {hesaplama_turu}",
                "adimlar": []
            }


# Global fonksiyonlar
def ucgen_hesapla(hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
    """Üçgen hesaplamaları yapar"""
    cozucu = GeometriCozucu()
    return cozucu.ucgen_hesaplama(hesaplama_turu, **kwargs)


def dortgen_hesapla(sekil_turu: str, hesaplama_turu: str, **kwargs) -> Dict[str, Any]:
    """Dörtgen hesaplamaları yapar"""
    cozucu = GeometriCozucu()
    return cozucu.dortgen_hesaplama(sekil_turu, hesaplama_turu, **kwargs)


# Test fonksiyonu
if __name__ == "__main__":
    print("🔷 GEOMETRİ MODÜLÜ TEST")
    print("=" * 50)
    
    # Üçgen testleri
    print("\n1. Üçgen Alan Testi (Heron):")
    sonuc = ucgen_hesapla("alan", a=3, b=4, c=5)
    if sonuc["basarili"]:
        print(f"   Alan: {sonuc['alan']:.2f}")
    
    print("\n2. Pisagor Teoremi Testi:")
    sonuc = ucgen_hesapla("pisagor", a=3, b=4)
    if sonuc["basarili"]:
        print(f"   Hipotenüs: {sonuc['hipotenus']:.2f}")
    
    print("\n3. Kare Alan Testi:")
    sonuc = dortgen_hesapla("kare", "alan", kenar=5)
    if sonuc["basarili"]:
        print(f"   Alan: {sonuc['alan']}")
    
    print("\n4. Dikdörtgen Çevre Testi:")
    sonuc = dortgen_hesapla("dikdortgen", "cevre", uzun_kenar=8, kisa_kenar=5)
    if sonuc["basarili"]:
        print(f"   Çevre: {sonuc['cevre']}")


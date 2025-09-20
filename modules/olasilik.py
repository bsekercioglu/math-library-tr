#!/usr/bin/env python3
"""
Olasılık Modülü - Türkçe Matematik Kütüphanesi

Bu modül olasılık hesaplamalarını içerir:
- Permutasyon (Düzenlemeler)
- Kombinasyon (Seçimler) 
- Temel olasılık hesaplamaları
- Faktöriyel hesaplamaları
- Binom katsayıları
- Olasılık dağılımları
"""

import math
import sympy as sp
from typing import Dict, List, Tuple, Optional, Any
import re


class OlasililkCozucu:
    """Ana olasılık çözücü sınıfı"""
    
    def __init__(self):
        pass
    
    def faktoriyel_hesapla(self, n: int) -> Dict[str, Any]:
        """
        Faktöriyel hesaplar.
        
        Args:
            n (int): Faktöriyeli alınacak sayı
        
        Returns:
            Dict: Faktöriyel hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if n < 0:
                return {
                    "basarili": False,
                    "hata": "Faktöriyel negatif sayılar için tanımlı değildir",
                    "adimlar": []
                }
            
            adimlar.append(f"Faktöriyel hesaplanıyor: {n}!")
            
            if n == 0 or n == 1:
                sonuc = 1
                adimlar.append(f"{n}! = 1 (tanım gereği)")
            else:
                sonuc = math.factorial(n)
                
                # Adım adım göster (küçük sayılar için)
                if n <= 10:
                    carpim_str = " × ".join([str(i) for i in range(1, n + 1)])
                    adimlar.append(f"{n}! = {carpim_str}")
                    adimlar.append(f"{n}! = {sonuc}")
                else:
                    adimlar.append(f"{n}! = {sonuc} (büyük sayı)")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "n": n,
                "faktoriyel": sonuc
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Faktöriyel hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def permutasyon_hesapla(self, n: int, r: Optional[int] = None) -> Dict[str, Any]:
        """
        Permutasyon (düzenleme) hesaplar.
        
        Args:
            n (int): Toplam eleman sayısı
            r (int): Seçilecek eleman sayısı (None ise n!)
        
        Returns:
            Dict: Permutasyon hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if n < 0:
                return {
                    "basarili": False,
                    "hata": "n negatif olamaz",
                    "adimlar": []
                }
            
            # Tam permutasyon (n!)
            if r is None:
                adimlar.append(f"Tam permutasyon: P({n}) = {n}!")
                faktoriyel_sonuc = self.faktoriyel_hesapla(n)
                
                if not faktoriyel_sonuc["basarili"]:
                    return faktoriyel_sonuc
                
                sonuc = faktoriyel_sonuc["faktoriyel"]
                adimlar.extend(faktoriyel_sonuc["adimlar"])
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "permutasyon_turu": "tam",
                    "n": n,
                    "permutasyon": sonuc
                }
            
            # Kısmi permutasyon P(n,r)
            else:
                if r < 0 or r > n:
                    return {
                        "basarili": False,
                        "hata": f"r değeri 0 ≤ r ≤ n koşulunu sağlamalı (r={r}, n={n})",
                        "adimlar": []
                    }
                
                adimlar.append(f"Kısmi permutasyon: P({n},{r}) = {n}! / ({n}-{r})!")
                adimlar.append(f"P({n},{r}) = {n}! / {n-r}!")
                
                # n! hesapla
                n_fakt = math.factorial(n)
                adimlar.append(f"{n}! = {n_fakt}")
                
                # (n-r)! hesapla
                nr_fakt = math.factorial(n - r)
                adimlar.append(f"{n-r}! = {nr_fakt}")
                
                # Sonuç
                sonuc = n_fakt // nr_fakt
                adimlar.append(f"P({n},{r}) = {n_fakt} / {nr_fakt} = {sonuc}")
                
                # Alternatif gösterim
                if r <= 5 and n <= 15:  # Küçük sayılar için açık gösterim
                    carpim_str = " × ".join([str(i) for i in range(n, n-r, -1)])
                    adimlar.append(f"Alternatif: P({n},{r}) = {carpim_str} = {sonuc}")
                
                return {
                    "basarili": True,
                    "adimlar": adimlar,
                    "permutasyon_turu": "kismi",
                    "n": n,
                    "r": r,
                    "permutasyon": sonuc
                }
                
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Permutasyon hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def kombinasyon_hesapla(self, n: int, r: int) -> Dict[str, Any]:
        """
        Kombinasyon (seçim) hesaplar.
        
        Args:
            n (int): Toplam eleman sayısı
            r (int): Seçilecek eleman sayısı
        
        Returns:
            Dict: Kombinasyon hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if n < 0 or r < 0:
                return {
                    "basarili": False,
                    "hata": "n ve r negatif olamaz",
                    "adimlar": []
                }
            
            if r > n:
                return {
                    "basarili": False,
                    "hata": f"r değeri n'den büyük olamaz (r={r}, n={n})",
                    "adimlar": []
                }
            
            adimlar.append(f"Kombinasyon: C({n},{r}) = {n}! / (r! × ({n}-r)!)")
            adimlar.append(f"C({n},{r}) = {n}! / ({r}! × {n-r}!)")
            
            # Faktöriyelleri hesapla
            n_fakt = math.factorial(n)
            r_fakt = math.factorial(r)
            nr_fakt = math.factorial(n - r)
            
            adimlar.append(f"{n}! = {n_fakt}")
            adimlar.append(f"{r}! = {r_fakt}")
            adimlar.append(f"{n-r}! = {nr_fakt}")
            
            # Sonuç
            sonuc = n_fakt // (r_fakt * nr_fakt)
            adimlar.append(f"C({n},{r}) = {n_fakt} / ({r_fakt} × {nr_fakt})")
            adimlar.append(f"C({n},{r}) = {n_fakt} / {r_fakt * nr_fakt} = {sonuc}")
            
            # Binom katsayısı açıklaması
            adimlar.append(f"Bu aynı zamanda binom katsayısı ({n} choose {r}) olarak da bilinir")
            
            # Simetri özelliği
            if r != n - r:
                adimlar.append(f"Simetri özelliği: C({n},{r}) = C({n},{n-r}) = {sonuc}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "n": n,
                "r": r,
                "kombinasyon": sonuc,
                "binom_katsayisi": sonuc
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Kombinasyon hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def temel_olasilik_hesapla(self, elverişli_durum: int, toplam_durum: int) -> Dict[str, Any]:
        """
        Temel olasılık hesaplar.
        
        Args:
            elverişli_durum (int): Elverişli durum sayısı
            toplam_durum (int): Toplam olası durum sayısı
        
        Returns:
            Dict: Olasılık hesaplama sonuçları
        """
        try:
            adimlar = []
            
            if toplam_durum <= 0:
                return {
                    "basarili": False,
                    "hata": "Toplam durum sayısı pozitif olmalı",
                    "adimlar": []
                }
            
            if elverişli_durum < 0 or elverişli_durum > toplam_durum:
                return {
                    "basarili": False,
                    "hata": f"Elverişli durum sayısı 0 ≤ elverişli ≤ toplam koşulunu sağlamalı",
                    "adimlar": []
                }
            
            adimlar.append(f"Temel olasılık formülü: P(A) = Elverişli durum / Toplam durum")
            adimlar.append(f"Elverişli durum sayısı: {elverişli_durum}")
            adimlar.append(f"Toplam durum sayısı: {toplam_durum}")
            
            # Olasılığı hesapla
            olasilik = elverişli_durum / toplam_durum
            adimlar.append(f"P(A) = {elverişli_durum} / {toplam_durum} = {olasilik:.6f}")
            
            # Yüzde ve kesir gösterimi
            yuzde = olasilik * 100
            adimlar.append(f"Yüzde olarak: %{yuzde:.2f}")
            
            # Kesir olarak basitleştir
            import fractions
            kesir = fractions.Fraction(elverişli_durum, toplam_durum)
            adimlar.append(f"Kesir olarak: {kesir}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "elverisli_durum": elverişli_durum,
                "toplam_durum": toplam_durum,
                "olasilik": olasilik,
                "yuzde": yuzde,
                "kesir": str(kesir)
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Olasılık hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }
    
    def binom_dagılimi(self, n: int, k: int, p: float) -> Dict[str, Any]:
        """
        Binom dağılımı hesaplar.
        
        Args:
            n (int): Deneme sayısı
            k (int): Başarı sayısı
            p (float): Başarı olasılığı
        
        Returns:
            Dict: Binom dağılımı sonuçları
        """
        try:
            adimlar = []
            
            if n < 0 or k < 0 or k > n:
                return {
                    "basarili": False,
                    "hata": "n ≥ 0, k ≥ 0 ve k ≤ n olmalı",
                    "adimlar": []
                }
            
            if not (0 <= p <= 1):
                return {
                    "basarili": False,
                    "hata": "Olasılık 0 ≤ p ≤ 1 aralığında olmalı",
                    "adimlar": []
                }
            
            adimlar.append(f"Binom dağılımı: P(X = k) = C(n,k) × p^k × (1-p)^(n-k)")
            adimlar.append(f"Verilen: n = {n}, k = {k}, p = {p}")
            
            # Kombinasyonu hesapla
            kombinasyon_sonuc = self.kombinasyon_hesapla(n, k)
            if not kombinasyon_sonuc["basarili"]:
                return kombinasyon_sonuc
            
            C_n_k = kombinasyon_sonuc["kombinasyon"]
            adimlar.append(f"C({n},{k}) = {C_n_k}")
            
            # Olasılığı hesapla
            p_k = p ** k
            p_nk = (1 - p) ** (n - k)
            olasilik = C_n_k * p_k * p_nk
            
            adimlar.append(f"p^k = {p}^{k} = {p_k:.6f}")
            adimlar.append(f"(1-p)^(n-k) = {1-p}^{n-k} = {p_nk:.6f}")
            adimlar.append(f"P(X = {k}) = {C_n_k} × {p_k:.6f} × {p_nk:.6f}")
            adimlar.append(f"P(X = {k}) = {olasilik:.6f}")
            
            # Yüzde gösterim
            yuzde = olasilik * 100
            adimlar.append(f"Yüzde olarak: %{yuzde:.2f}")
            
            return {
                "basarili": True,
                "adimlar": adimlar,
                "n": n,
                "k": k,
                "p": p,
                "kombinasyon": C_n_k,
                "olasilik": olasilik,
                "yuzde": yuzde
            }
            
        except Exception as e:
            return {
                "basarili": False,
                "hata": f"Binom dağılımı hesaplaması sırasında hata: {str(e)}",
                "adimlar": []
            }


# Global fonksiyonlar
def faktoriyel(n: int) -> Dict[str, Any]:
    """Faktöriyel hesaplar"""
    cozucu = OlasililkCozucu()
    return cozucu.faktoriyel_hesapla(n)


def permutasyon(n: int, r: Optional[int] = None) -> Dict[str, Any]:
    """Permutasyon hesaplar"""
    cozucu = OlasililkCozucu()
    return cozucu.permutasyon_hesapla(n, r)


def kombinasyon(n: int, r: int) -> Dict[str, Any]:
    """Kombinasyon hesaplar"""
    cozucu = OlasililkCozucu()
    return cozucu.kombinasyon_hesapla(n, r)


def olasilik_hesapla(elverişli: int, toplam: int) -> Dict[str, Any]:
    """Temel olasılık hesaplar"""
    cozucu = OlasililkCozucu()
    return cozucu.temel_olasilik_hesapla(elverişli, toplam)


def binom_dagilimi(n: int, k: int, p: float) -> Dict[str, Any]:
    """Binom dağılımı hesaplar"""
    cozucu = OlasililkCozucu()
    return cozucu.binom_dagılimi(n, k, p)


# Test fonksiyonu
if __name__ == "__main__":
    print("🎲 OLASILIK MODÜLÜ TEST")
    print("=" * 50)
    
    # Faktöriyel testi
    print("\n1. Faktöriyel Testi (5!):")
    sonuc = faktoriyel(5)
    if sonuc["basarili"]:
        print(f"   5! = {sonuc['faktoriyel']}")
    
    # Permutasyon testi
    print("\n2. Permutasyon Testi P(5,3):")
    sonuc = permutasyon(5, 3)
    if sonuc["basarili"]:
        print(f"   P(5,3) = {sonuc['permutasyon']}")
    
    # Kombinasyon testi
    print("\n3. Kombinasyon Testi C(5,3):")
    sonuc = kombinasyon(5, 3)
    if sonuc["basarili"]:
        print(f"   C(5,3) = {sonuc['kombinasyon']}")
    
    # Olasılık testi
    print("\n4. Temel Olasılık Testi (2/6):")
    sonuc = olasilik_hesapla(2, 6)
    if sonuc["basarili"]:
        print(f"   P = {sonuc['olasilik']:.3f} = %{sonuc['yuzde']:.1f}")
    
    # Binom dağılımı testi
    print("\n5. Binom Dağılımı Testi:")
    sonuc = binom_dagilimi(10, 3, 0.3)
    if sonuc["basarili"]:
        print(f"   P(X=3) = {sonuc['olasilik']:.4f}")




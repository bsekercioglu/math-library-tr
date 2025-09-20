"""
Çözüm Formatlayıcısı - Matematik Kütüphanesi
==========================================

Bu modül matematik çözümlerini güzel ve anlaşılır şekilde
formatlar ve kullanıcıya sunar.

Yazar: Matematik Kütüphanesi
"""

from typing import Dict, List, Any
import sympy as sp


class CozumFormatlayicisi:
    """Matematik çözümlerini formatlar"""
    
    def __init__(self):
        self.ayrac = "=" * 50
        self.alt_ayrac = "-" * 30
    
    def cozum_formatla(self, sonuc: Dict[str, Any], baslik: str = "Matematik Çözümü") -> str:
        """
        Çözüm sonucunu güzel bir formatta döndürür.
        
        Args:
            sonuc (Dict): Çözüm sonuçları sözlüğü
            baslik (str): Çözüm başlığı
        
        Returns:
            str: Formatlanmış çözüm metni
        """
        cikti = []
        
        # Başlık
        cikti.append(self.ayrac)
        cikti.append(f" {baslik.upper()} ")
        cikti.append(self.ayrac)
        cikti.append("")
        
        if not sonuc.get("basarili", False):
            cikti.append("❌ HATA:")
            cikti.append(f"   {sonuc.get('hata', 'Bilinmeyen hata oluştu')}")
            cikti.append("")
            return "\n".join(cikti)
        
        # Çözüm adımları
        if "adimlar" in sonuc and sonuc["adimlar"]:
            cikti.append("📋 ÇÖZÜM ADIMLARI:")
            cikti.append(self.alt_ayrac)
            
            for i, adim in enumerate(sonuc["adimlar"], 1):
                cikti.append(f"{i:2d}. {adim}")
            
            cikti.append("")
        
        # Sonuçlar
        cikti.append("✅ SONUÇ:")
        cikti.append(self.alt_ayrac)
        
        if "kokler" in sonuc:
            kokler = sonuc["kokler"]
            if len(kokler) == 0:
                cikti.append("   Gerçek kök bulunamadı.")
            elif len(kokler) == 1:
                cikti.append(f"   x = {kokler[0]}")
            else:
                for i, kok in enumerate(kokler, 1):
                    cikti.append(f"   x₍{i}₎ = {kok}")
        
        if "carpanlar" in sonuc:
            cikti.append(f"   Çarpanlara ayrılmış hali: {sonuc['carpanlar']}")
        
        if "diskriminant" in sonuc:
            delta = sonuc["diskriminant"]
            cikti.append(f"   Diskriminant (Δ): {delta}")
        
        # Trigonometri sonuçları
        if "sonuc" in sonuc and "fonksiyon" in sonuc:
            fonksiyon = sonuc["fonksiyon"]
            deger = sonuc["sonuc"]
            if "aci" in sonuc:
                aci = sonuc["aci"]
                birim = sonuc.get("birim", "derece")
                cikti.append(f"   {fonksiyon}({aci}°) = {deger:.6f}" if birim == "derece" else f"   {fonksiyon}({aci}) = {deger:.6f}")
        
        # Ters trigonometri sonuçları  
        if "aci_derece" in sonuc and "aci_radyan" in sonuc:
            aci_derece = sonuc["aci_derece"]
            aci_radyan = sonuc["aci_radyan"]
            cikti.append(f"   Açı: {aci_derece:.2f}° = {aci_radyan:.6f} radyan")
        
        # Açı dönüşümü sonuçları
        if "kaynak_aci" in sonuc and "kaynak_birim" in sonuc and "hedef_birim" in sonuc:
            kaynak_aci = sonuc["kaynak_aci"]
            kaynak_birim = sonuc["kaynak_birim"]
            hedef_birim = sonuc["hedef_birim"]
            sonuc_deger = sonuc["sonuc"]
            cikti.append(f"   {kaynak_aci} {kaynak_birim} = {sonuc_deger:.6f} {hedef_birim}")
        
        # Trigonometrik denklem çözümleri
        if "cozumler" in sonuc and "cozum_sayisi" in sonuc:
            cozumler = sonuc["cozumler"]
            cozum_sayisi = sonuc["cozum_sayisi"]
            
            if cozum_sayisi == 1:
                cikti.append(f"   Çözüm: x = {cozumler[0]}°")
            else:
                cikti.append(f"   Çözümler ([0°, 360°) aralığında):")
                for i, cozum in enumerate(cozumler, 1):
                    cikti.append(f"   x₍{i}₎ = {cozum}°")
            
            cikti.append(f"   Toplam çözüm sayısı: {cozum_sayisi}")
        
        # Trigonometrik ifade hesaplama sonuçları
        if "nihai_sonuc" in sonuc and "fonksiyon_hesaplamalari" in sonuc:
            nihai_sonuc = sonuc["nihai_sonuc"]
            fonksiyon_hesaplamalari = sonuc["fonksiyon_hesaplamalari"]
            
            cikti.append("   Fonksiyon değerleri:")
            for fonksiyon, deger in fonksiyon_hesaplamalari.items():
                cikti.append(f"   {fonksiyon} = {deger:.6f}")
            
            cikti.append(f"   Nihai sonuç: {nihai_sonuc:.6f}")
        
        # Analiz sonuçları (türev/integral)
        if "turev" in sonuc:
            cikti.append(f"   Türev: {sonuc['turev']}")
            if "turev_basit" in sonuc and sonuc["turev"] != sonuc["turev_basit"]:
                cikti.append(f"   Basitleştirilmiş: {sonuc['turev_basit']}")
        
        if "integral" in sonuc:
            if sonuc.get("integral_turu") == "belirli":
                cikti.append(f"   Belirsiz integral: {sonuc['belirsiz_integral']} + C")
                cikti.append(f"   Belirli integral [{sonuc['alt_sinir']}, {sonuc['ust_sinir']}]: {sonuc['integral']}")
                if sonuc.get("sayisal_deger"):
                    cikti.append(f"   Sayısal değer: {sonuc['sayisal_deger']:.6f}")
            else:
                # Karmaşık integraller için özel açıklama
                if sonuc.get("karmasik_integral", False):
                    cikti.append(f"   📊 Karmaşık İntegral Sonucu:")
                    cikti.append(f"   {sonuc['integral']} + C")
                    if "integral_basit" in sonuc and sonuc["integral"] != sonuc["integral_basit"]:
                        cikti.append(f"   Basitleştirilmiş: {sonuc['integral_basit']} + C")
                    
                    # Pratik bilgi
                    cikti.append("")
                    cikti.append("   💡 Pratik Bilgi:")
                    cikti.append("   Bu integral özel matematiksel fonksiyonlar içerir.")
                    cikti.append("   Sayısal hesaplama yapmak için matematiksel yazılım gerekir.")
                    cikti.append("   Mühendislik uygulamalarında tablolardan değer okunur.")
                else:
                    cikti.append(f"   İntegral: {sonuc['integral']} + C")
                    if "integral_basit" in sonuc and sonuc["integral"] != sonuc["integral_basit"]:
                        cikti.append(f"   Basitleştirilmiş: {sonuc['integral_basit']} + C")
        
        # Olasılık sonuçları
        if "faktoriyel" in sonuc:
            cikti.append(f"   {sonuc['n']}! = {sonuc['faktoriyel']}")
        
        if "permutasyon" in sonuc:
            if sonuc.get("permutasyon_turu") == "tam":
                cikti.append(f"   P({sonuc['n']}) = {sonuc['permutasyon']}")
            else:
                cikti.append(f"   P({sonuc['n']},{sonuc['r']}) = {sonuc['permutasyon']}")
        
        if "kombinasyon" in sonuc:
            cikti.append(f"   C({sonuc['n']},{sonuc['r']}) = {sonuc['kombinasyon']}")
            cikti.append(f"   Binom katsayısı: {sonuc['kombinasyon']}")
        
        if "olasilik" in sonuc:
            cikti.append(f"   Olasılık: {sonuc['olasilik']:.6f}")
            cikti.append(f"   Yüzde: %{sonuc['yuzde']:.2f}")
            cikti.append(f"   Kesir: {sonuc['kesir']}")
        
        # Geometri sonuçları
        if "alan" in sonuc:
            cikti.append(f"   Alan: {sonuc['alan']}")
        
        if "cevre" in sonuc:
            cikti.append(f"   Çevre: {sonuc['cevre']}")
        
        if "hipotenus" in sonuc:
            cikti.append(f"   Hipotenüs: {sonuc['hipotenus']:.6f}")
        
        if "ucuncu_kenar" in sonuc:
            cikti.append(f"   Üçüncü kenar: {sonuc['ucuncu_kenar']:.6f}")
        
        if "hacim" in sonuc:
            cikti.append(f"   Hacim: {sonuc['hacim']:.6f}")
        
        if "yuzey_alani" in sonuc:
            cikti.append(f"   Yüzey alanı: {sonuc['yuzey_alani']:.6f}")
        
        # Geometri hesaplama türü göstergesi
        if "hesaplama_turu" in sonuc:
            hesaplama_turu = sonuc["hesaplama_turu"]
            if hesaplama_turu in ["pisagor_hipotenuse", "cosinus_kurali_ucuncu_kenar"]:
                if "bilinen_kenarlar" in sonuc:
                    kenarlar = sonuc["bilinen_kenarlar"]
                    cikti.append(f"   Bilinen kenarlar: a = {kenarlar.get('a', 'N/A')}, b = {kenarlar.get('b', 'N/A')}")
                if "aci_derece" in sonuc:
                    cikti.append(f"   Kullanılan açı: {sonuc['aci_derece']}°")
        
        # Daire özel sonuçları
        if "yaricap" in sonuc:
            cikti.append(f"   Yarıçap: {sonuc['yaricap']}")
        
        if "cap" in sonuc:
            cikti.append(f"   Çap: {sonuc['cap']}")
        
        # Üçgen özel sonuçları  
        if "kenar_uzunluklari" in sonuc:
            kenarlar = sonuc["kenar_uzunluklari"]
            cikti.append(f"   Kenar uzunlukları: a = {kenarlar.get('a', 'N/A')}, b = {kenarlar.get('b', 'N/A')}, c = {kenarlar.get('c', 'N/A')}")
        
        if "ucgen_turu" in sonuc:
            ucgen_turu = sonuc["ucgen_turu"]
            if ucgen_turu == "dik":
                cikti.append("   Üçgen türü: Dik üçgen")
            elif ucgen_turu == "ikizkenar":
                cikti.append("   Üçgen türü: İkizkenar üçgen")
            elif ucgen_turu == "eszkenar":
                cikti.append("   Üçgen türü: Eşkenar üçgen")
        
        cikti.append("")
        cikti.append(self.ayrac)
        
        return "\n".join(cikti)
    
    def kisa_ozet(self, sonuc: Dict[str, Any]) -> str:
        """Çözümün kısa özetini döndürür"""
        if not sonuc.get("basarili", False):
            return f"❌ Hata: {sonuc.get('hata', 'Bilinmeyen hata')}"
        
        ozet_parcalari = []
        
        if "kokler" in sonuc:
            kokler = sonuc["kokler"]
            if len(kokler) == 0:
                ozet_parcalari.append("Gerçek kök yok")
            elif len(kokler) == 1:
                ozet_parcalari.append(f"x = {kokler[0]}")
            else:
                kok_str = ", ".join([f"x₍{i}₎ = {kok}" for i, kok in enumerate(kokler, 1)])
                ozet_parcalari.append(kok_str)
        
        if "carpanlar" in sonuc and "orijinal" in sonuc:
            if sonuc["carpanlar"] != sonuc["orijinal"]:
                ozet_parcalari.append(f"Çarpanlar: {sonuc['carpanlar']}")
        
        return " | ".join(ozet_parcalari) if ozet_parcalari else "Çözüm tamamlandı"
    
    def adim_adim_goster(self, adimlar: List[str], numara_basla: int = 1) -> str:
        """Adımları numaralı liste olarak formatlar"""
        if not adimlar:
            return "Adım bulunamadı."
        
        formatli_adimlar = []
        for i, adim in enumerate(adimlar, numara_basla):
            formatli_adimlar.append(f"{i:2d}. {adim}")
        
        return "\n".join(formatli_adimlar)
    
    def tablo_formatla(self, basliklar: List[str], satirlar: List[List[str]]) -> str:
        """Verileri tablo formatında gösterir"""
        if not basliklar or not satirlar:
            return "Tablo verisi bulunamadı."
        
        # Sütun genişliklerini hesapla
        sutun_genislikleri = [len(baslik) for baslik in basliklar]
        
        for satir in satirlar:
            for i, hucre in enumerate(satir):
                if i < len(sutun_genislikleri):
                    sutun_genislikleri[i] = max(sutun_genislikleri[i], len(str(hucre)))
        
        # Tablo formatla
        tablo = []
        
        # Başlık satırı
        baslik_satiri = " | ".join([baslik.ljust(genislik) for baslik, genislik in zip(basliklar, sutun_genislikleri)])
        tablo.append(baslik_satiri)
        
        # Ayırıcı çizgi
        ayirici = "-+-".join(["-" * genislik for genislik in sutun_genislikleri])
        tablo.append(ayirici)
        
        # Veri satırları
        for satir in satirlar:
            veri_satiri = " | ".join([str(hucre).ljust(genislik) for hucre, genislik in zip(satir, sutun_genislikleri)])
            tablo.append(veri_satiri)
        
        return "\n".join(tablo)
    
    def hata_mesaji_formatla(self, hata: str, oneriler: List[str] = None) -> str:
        """Hata mesajlarını formatlar"""
        cikti = []
        cikti.append("❌ HATA OLUŞTU!")
        cikti.append(self.alt_ayrac)
        cikti.append(f"Hata: {hata}")
        
        if oneriler:
            cikti.append("")
            cikti.append("💡 ÖNERİLER:")
            for i, oneri in enumerate(oneriler, 1):
                cikti.append(f"{i}. {oneri}")
        
        return "\n".join(cikti)
    
    def basari_mesaji(self, mesaj: str) -> str:
        """Başarı mesajını formatlar"""
        return f"✅ {mesaj}"
    
    def bilgi_mesaji(self, mesaj: str) -> str:
        """Bilgi mesajını formatlar"""
        return f"ℹ️  {mesaj}"
    
    def uyari_mesaji(self, mesaj: str) -> str:
        """Uyarı mesajını formatlar"""
        return f"⚠️  {mesaj}"


# Kullanım kolaylığı için global fonksiyonlar
def cozum_formatla(sonuc: Dict[str, Any], baslik: str = "Matematik Çözümü") -> str:
    """Çözüm sonucunu formatlar"""
    formatter = CozumFormatlayicisi()
    return formatter.cozum_formatla(sonuc, baslik)


def kisa_ozet(sonuc: Dict[str, Any]) -> str:
    """Çözümün kısa özetini döndürür"""
    formatter = CozumFormatlayicisi()
    return formatter.kisa_ozet(sonuc)


def hata_mesaji_formatla(hata: str, oneriler: List[str] = None) -> str:
    """Hata mesajını formatlar"""
    formatter = CozumFormatlayicisi()
    return formatter.hata_mesaji_formatla(hata, oneriler)


# Test fonksiyonu
if __name__ == "__main__":
    # Test için örnek sonuç
    ornek_sonuc = {
        "basarili": True,
        "adimlar": [
            "Verilen denklem: x² - 5x + 6 = 0",
            "Standart form: ax² + bx + c = 0",
            "Katsayılar: a = 1, b = -5, c = 6",
            "Diskriminant (Δ) = b² - 4ac = 25 - 24 = 1",
            "Δ > 0 olduğu için iki farklı gerçek kök vardır.",
            "x₁ = (5 + 1) / 2 = 3",
            "x₂ = (5 - 1) / 2 = 2"
        ],
        "kokler": [3, 2],
        "diskriminant": 1,
        "katsayilar": {"a": 1, "b": -5, "c": 6},
        "latex": "$x^{2} - 5x + 6 = 0$"
    }
    
    formatter = CozumFormatlayicisi()
    print(formatter.cozum_formatla(ornek_sonuc, "İkinci Dereceden Denklem Çözümü"))
    print("\n" + "="*20)
    print("Kısa Özet:", formatter.kisa_ozet(ornek_sonuc))


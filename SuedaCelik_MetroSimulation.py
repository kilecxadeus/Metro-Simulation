from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı yolyı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin                  +
        2. BFS algoritmasını kullanarak en az aktarmalı yolyı bulun
        3. yol bulunamazsa None, bulunursa istasyon listesi döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
        
        İpuçları:
        - collections.deque kullanarak bir kuyruk oluşturun, HINT: kuyruk = deque([(baslangic, [baslangic])])
        - Ziyaret edilen istasyonları takip edin
        - Her adımda komşu istasyonları keşfedin
        """

        # 1. başlangıç ve hedef istasyonunun kontrolü
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            # başlangıç veya hedef istasyonlarından en az birinin id'si kayıtlı değilse None döner.
            return None
        
        # 2. işlem yapabilmek için başlangıç ve hedef istasyonların ataması yapılır.
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # 3.başlangıç ve hedef aynıysa bfs'ye girmeden kontrol edilir.
        if baslangic == hedef:
            return [baslangic]

        # 4. ziyaret edilen istasyonların kaydı için set (veri tekrarlamaz) kullanılır.
        ziyaret_edildi = {baslangic}  
        ### başlangıç istasyonu ziyaret edildi.

        # 5. kuyruk oluşturma
        kuyruk = deque([(baslangic, [baslangic])])
        ## başlangıç istasyonunda ve yolda sadece başlangıç var.

        # 6. bfs
        while kuyruk:       # kuyruk boş olana kadar döner
                            # her döngüde bir istasyon ziyaret edilir, komşular kuyruğa eklenir

            # 7.en öndeki istasyon ve yol listesi.    ->  ilk giren ilk çıkar.
            istasyon, yol = kuyruk.popleft()

            # 8. hedef istasyona ulaşıldı mı?
            if istasyon == hedef:
                return yol
            
            # 9. istasyonun komşularının kontrolü
            for komsu, _ in istasyon.komsular:          # mevcut istasyonun komşuları kontrol edilir.
                if komsu not in ziyaret_edildi:         # ziyaret edilmediyse 
                    # 10. komsu istasyon ziyaret edilenlere eklendi
                    ziyaret_edildi.add(komsu)

                    # 11. yol listesi güncelenir. komşu ve yeni yol kuyruğa eklenir.
                    yeni_yol = yol + [komsu]
                    kuyruk.append((komsu, yeni_yol))

        # 12. hedefe ulaşamazsa
        return None


    def en_hizli_yol_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı yolyı bulur
        
        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. A* algoritmasını kullanarak en hızlı yolyı bulun
        3. yol bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
        
        İpuçları:
        - heapq modülünü kullanarak bir öncelik kuyruğu oluşturun, HINT: pq = [(0, id(baslangic), baslangic, [baslangic])]
        - Ziyaret edilen istasyonları takip edin
        - Her adımda toplam süreyi hesaplayın
        - En düşük süreye sahip yolyı seçin
        """
        
        # 1. başlangıç ve hedef istasyonların kontrolü yapılır.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            # en az birinin bile id'si eksikse None döner.
            return None

        # 2. başlangıç ve hedef istasyonlarının atamaları yapılır.
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # 3. başlangıç ve hedef istasyonun aynı olup olmadığı döngüye girmeden kontrol edilir.
        if baslangic == hedef:
            # aynıysa tek bir istasyon ve 0 dk döner.
            return [baslangic], 0

        # 4. ziyaret edilen istasyonlar kaydedilir.
        ziyaret_edildi = {}

        # 5. öncelik kuyruğu oluşturulur.
        heap = [(0, id(baslangic), baslangic, [baslangic])]

        # 6. A*
        while heap:
            toplam_sure, _, mevcut, yol = heapq.heappop(heap)
            # en hızlı rotayı çıkarır, değişkenlere böler.
            # _: bellekteki adresini tutar.
            # toplam_sure: öncelik kuyruğundan en düşük süreli yolu tutar.
            # mevcut: şu an ziyaret edilen istasyonu tutar.
            # yol: bu istasyona ulaşan en iyi yolu tutar.

            if mevcut == hedef:
                # 7. hedef istasyona ulaşıldıysa sonucu döndürür.
                return yol, toplam_sure
            
            if mevcut.idx in ziyaret_edildi and ziyaret_edildi[mevcut.idx] <= toplam_sure:
                # 8. mevcut istasyona daha kısa sürede ulaşan yol varsa:
                continue

            # 9. mevcut istasyon ziyaret edildiğinden kaydedilir.
            ziyaret_edildi[mevcut.idx] = toplam_sure

            # 10. mevcut istasyonun komşularının kontrolü
            for komsu, sure in mevcut.komsular:        # mevcut istasyonunun bütün komşularını alır.
                yeni_sure = toplam_sure + sure
                if komsu.idx not in ziyaret_edildi or yeni_sure < ziyaret_edildi[komsu.idx]:
                    # 11. ziyaret edilmediyse veya yeni rota eskisinden daha kısa süreliyse
                    heapq.heappush(heap, (yeni_sure, id(komsu), komsu, yol + [komsu]))
                    # 12. yeni rotanın toplam süresini ve tüm komşularını içeren yeni yolu hesaplar, heape ekler.

        # 13. hedefe ulaşamazsa None döner.
        return None




# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # # Senaryo 1: AŞTİ'den OSB'ye
    # print("\n1. AŞTİ'den OSB'ye:")
    # yol = metro.en_az_aktarma_bul("M1", "K4")
    # if yol:
    #     print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
    
    # sonuc = metro.en_hizli_yol_bul("M1", "K4")
    # if sonuc:
    #     yol, sure = sonuc
    #     print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol))
    
    # # Senaryo 2: Batıkent'ten Keçiören'e
    # print("\n2. Batıkent'ten Keçiören'e:")
    # yol = metro.en_az_aktarma_bul("T1", "T4")
    # if yol:
    #     print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
    
    # sonuc = metro.en_hizli_yol_bul("T1", "T4")
    # if sonuc:
    #     yol, sure = sonuc
    #     print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol))
    
    # # Senaryo 3: Keçiören'den AŞTİ'ye
    # print("\n3. Keçiören'den AŞTİ'ye:")
    # yol = metro.en_az_aktarma_bul("T4", "M1")
    # if yol:
    #     print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
    
    # sonuc = metro.en_hizli_yol_bul("T4", "M1")
    # if sonuc:
    #     yol, sure = sonuc
    #     print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol)) 

    # # Senaryo 4: Sıhhiye'den Batıkent'e
    # print("\n4. Sıhhiye'den Batıkent'e:")
    # yol = metro.en_az_aktarma_bul("M3", "T1")
    # if yol:
    #     print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
    
    # sonuc = metro.en_hizli_yol_bul("M3", "T1")
    # if sonuc:
    #     yol, sure = sonuc
    #     print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol)) 
    
    # # Senaryo 5: OSB'den Gar'a
    # print("\n5. OSB'den Gar'a:")
    # yol = metro.en_az_aktarma_bul("K4", "M4")
    # if yol:
    #     print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
    
    # sonuc = metro.en_hizli_yol_bul("K4", "M4")
    # if sonuc:
    #     yol, sure = sonuc
    #     print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol))

    
    senaryolar = [
        ["M1", "K4"],
        ["T1", "T4"],
        ["T4", "M1"],
        ["M3", "T1"],
        ["K4", "M4"],
    ]

    for n, [baslangic, hedef] in enumerate(senaryolar):
        print(f"\nSenaryo {n+1}: {metro.istasyonlar[baslangic].ad} - {metro.istasyonlar[hedef].ad}")
        yol = metro.en_az_aktarma_bul(baslangic, hedef)
        if yol:
            print("En az aktarmalı yol:", " -> ".join(i.ad for i in yol))
        
        sonuc = metro.en_hizli_yol_bul(baslangic, hedef)
        if sonuc:
            yol, sure = sonuc
            print(f"En hızlı yol ({sure} dakika):", " -> ".join(i.ad for i in yol))
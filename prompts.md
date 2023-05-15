# Setup

## "Give me the oracle DDL code to create the tables based on this json:"
input the json created in the main.py

## "Did you fully understand the table structure? Y/N"

## "Please provide me the oracle sql code for the questions I provide you. Take your time to think, explain the steps and use as few joins as needed."

### Preise der Preisliste 1 (PLID), deren Betrag größer als 70 Euro ist. Der Produktidentifikator (PID) und der Betrag des Produkts in dieser Preisliste sollen ausgegeben werden. Sortiert nach Betrag.

SELECT pr.PID, pr.Betrag
FROM Preis pr
WHERE pr.PLID = 1
  AND pr.Betrag > 70
ORDER BY pr.Betrag;

KORREKT

### Alle Verkaufsgebiete, die keine Obergebiete haben.

SELECT VGID, Bez, Ebene
FROM Verkaufsgebiet
WHERE Obergebiet IS NULL;

KORREKT

### Verkaufsgebiete und Kennzeichnung, ob ein Gebiet Wurzel der Hierarchie ist, innerer Knoten oder Blatt.

SELECT VG.VGID, VG.Bez, VG.Ebene,
       CASE
           WHEN VG.Obergebiet IS NULL THEN 'Wurzel'
           WHEN EXISTS (SELECT 1 FROM Verkaufsgebiet WHERE Obergebiet = VG.VGID) THEN 'Innerer Knoten'
           ELSE 'Blatt'
       END AS Kennzeichnung
FROM Verkaufsgebiet VG;

KORREKT

### Produktkategoriehierarchie mit Einrückungen entsprechend der Ebene. Sortiert nach KID.

SELECT K1.KID, LPAD(' ', (LEVEL - 1) * 4, ' ') || K1.Bez AS Bez, K1.Ebene
FROM Kategorie K1
START WITH K1.Oberkategorie IS NULL
CONNECT BY PRIOR K1.KID = K1.Oberkategorie
ORDER SIBLINGS BY K1.KID;

Gab erst eine Antwort mit "Recursive CTE", sagte aber, dass das noch nicht unterstützt sein könnte. Auf nachfragen ohne ging es dann.

### Bestellungen, bei denen (fehlerhaft) das Versanddatum vor dem Bestelldatum liegt. Sortiert nach PIB und BID.

SELECT B.BID, P.Bez AS ProduktName, B.Versanddatum, V.Lieferdatum
FROM Bestellung B
JOIN Produkt P ON B.PID = P.PID
JOIN Versand V ON B.VID = V.VID
WHERE B.Versanddatum < B.Bestelldatum
ORDER BY B.BID;

Frage war nicht direkt klar, hat erst PID hinhalluziniert. Auf Nachfragen dann nur BID gegeben. Ignoriert die Sortierungsfaktoren. Eventuell Memory overload, müsste hier neustarten. FEHLERHAFT bei 3.5
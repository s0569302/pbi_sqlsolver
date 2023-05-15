SELECT pr.PID, pr.Betrag
FROM Preis pr
WHERE pr.PLID = 1
  AND pr.Betrag > 70
ORDER BY pr.Betrag;
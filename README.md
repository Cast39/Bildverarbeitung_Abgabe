# Bildverarbeitung_Abgabe
Datensatz Beispiele:
![PCBBilder](https://github.com/amazon-science/spot-diff/blob/main/figures/VisA_samples.png?raw=true)
## Erster Ansatz
Im ersten Ansatz (get_contours.py) wird das Eingangsbild in eine Bitmaske umgewandelt indem es zunächst in ein Graubild und darauf mit einem Schwellwert von **134** in 1 oder 0 umgewandelt wird.
`1 if img[x,y] > 134 else 0`
Hier ein Beispiel anhand des Bildes "Bildname" aus dem Datensatz.
(Beispielbild einfügen)

Das maskierte Bild wird darauf in die openCV Funktion `cv2.findContours()` übergeben, welche eine Bloberkennung umsetzt. Mit Hilfe dieser Bloberkennung ist die genaue Bestimmung der Position des PCBs möglich, indem nur Blobs mit einer Fläche größer als **Schwellwert (in Prozent?) und größter Blob)** akzeptiert wird.
(Beispielbild einfügen)

Um diesen Blob zur weiteren Verarbeitung verwenden zu können, müssen die Blobs wieder in Rechtecke umgewandelt werden (get_box.py). Hierfür wurde die Funktion `cv2.minAreaRect()` eingesetzt, welche ein Rechteck ausgibt, welches optimal gedreht ist, um alle Pixel eines Blobs mit der kleinsten Fläche zu umschließen (Boundingbox).
(Beispielbild einfügen)

In diesem Schritt wird das Rechteck auf 0° Drehung korregiert (align.py). Dazu wird mit dem Winkel aus dem vorigen Schritt eine Rotationsmatrix erstellt `(cv2.getRotationMatrix2D())` und auf das Bild angewendet.
(you know the drill)

Nun wird die Erkennung der Boundingbox wiederholt (get_contours.py und get_Box.py), um Anomalien aus der Drehung sicher zu stellen **(Ist das so?)**
(Gegenüberstellung BB Änderung)

Folgend kann das Bild zugeschnitten werden (crop.py)
**Achtung änderung vllt?**
Zunächst behalten die Bilder ihre Originalauflösung, wurde die Vorbearbeitung für alle Bilder durchgeführt, wird eine optimale Bildgröße bestimmt, auf welche darauf auf alle Bilder skaliert werden.
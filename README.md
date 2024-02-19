# Bildverarbeitung_Abgabe
Datensatz Beispiele:
![PCBBilder](https://github.com/amazon-science/spot-diff/blob/main/figures/VisA_samples.png?raw=true)
## Erster Ansatz
![Ursprungsbild](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/1-normal_0029_normal_0029.JPG.png?raw=true)

### 1. segment.py
Das Eingangsbild wird mit einer Bitmaske über mehrere Farbkanäle bearbeitet. Es werden alle Pixel - welche die folgenden Schwellwerte nicht überschreiten - schwarz, bzw. transpartent überschrieben.

|Rot  |  Grün | Blau |
|-----|-------|------|
|< 133| < 133 | < 150|

Hier ein Beispiel anhand des Bildes "Bildname" aus dem Datensatz.
![Bitmaskiert](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/2-normal_0029_segmented.JPG.png?raw=true)

### 2. get_contour.py & 3. boundary_box.py
**Wieso hier Graubildumwandlung?**

Das maskierte Bild wird darauf in die openCV Funktion `cv2.findContours()` übergeben, welche eine Bloberkennung umsetzt. Mit Hilfe dieser Bloberkennung ist die genaue Bestimmung der Position des PCBs möglich, indem nur der Blob mit einer größten Fläche akzeptiert wird. 
<!--![Konturerkannt](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/3-normal_0029_contour.png?raw=true)-->
![Boundary Box](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/4-normal_0029_boundary.png?raw=true)

Um diesen Blob zur weiteren Verarbeitung verwenden zu können, muss der Blob wieder in ein Rechteck umgewandelt werden (boundary_box.py). Hierfür wurde die Funktion `cv2.minAreaRect()` eingesetzt, welche ein Rechteck ausgibt, welches optimal gedreht ist, um alle Pixel eines Blobs mit der kleinsten Fläche zu umschließen (Boundingbox). Es stellt sich nur das Problem, dass Ausreißer in dem Bild zu einem verdrehten Rechteck führen können.
(Beispielbild schief einfügen)

### 4. align.py
In diesem Schritt wird das Rechteck auf 0° Drehung korregiert. Dazu wird mit dem Winkel aus dem vorigen Schritt eine Rotationsmatrix erstellt `(cv2.getRotationMatrix2D())` und auf das Bild angewendet. Es wurde bloß ein extra eingefügt **(>45° -> -90°)**.
![Aligned](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/5-normal_0029_aligned.png?raw=true)

### 5. get_contour.py & 6. boundary_box.py
Nun wird die Erkennung der Boundingbox auf das gedrehte Bild angewand.


### 7. align.py
Nun wird align wieder ausgeführt, dieses mal jedoch auf das Originalbild, um den Hintergrund und die originalen Farben des Bildes bei zu behalten.

### 8. crop.py
Folgend kann das Bild zugeschnitten werden. Hierfür wird ein optimales Seitenverhältnis von **w / h = 980 / 580 = 1,69** vorgegeben. Stimmt dieses nicht mit der Bounding Box überein, wird diese auf das entsprechende Verhältnis nach oben erweitert.
Darauf wird das Bild auf diese Bounding Box ausgeschnitten.
![Cropped](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/6-normal_0029_cropped.png?raw=true)


### 9. orient.py
Nach dem align wird das PCB zwar horizontal orientiert, die Pins können aber noch oben oder unten liegen.
Es wird der Schwerpunkt des Blobs auf dem Zugeschnittenen Bild berechnet und liegt dieser oberhalb der Bildmitte, wird das Bild um 180° gedreht.
![Orientiert](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/7-normal_0029_oriented.png?raw=true)

### 10. scale.py
Folgend werden alle bilder mit `cv2.resize()` auf **980 x 580** skaliert.
![Scaled](https://github.com/Cast39/Bildverarbeitung_Abgabe/blob/main/figures/8-normal_0029_scaled.png?raw=true)


## Zweiter Ansatz: SVM
Es wurde in dem **feature/SVM** Branch versucht, eine Klassifizierung mit einem SVM zu realisieren.
Dafür war der Ansatz, die SVM auf jedes Bild einzeln zu trainieren, sodass sich die Grenzen der SVM an die Grenzen des PCBs anschmiegen.
Dies hat jedoch nicht funktioniert, da die Punkte alle auf der Grenze des PCBs liegen und nicht im PCB.
Stattdessen hätte der Ansatz mit einer direkten Analyse des Blobs auf die Binärmaske ausprobiert werden können.

## Dritter Ansatz: Blobanalyse
Mit diesem Ansatz soll die Erkennung der Eckpunkte gesteigert werden. Hierfür werden die Winkel der Konturpunkte (vom Schwerpunkt aus) berechnet und in 1° Schritten abgetastet.
Darauf werden vom original Schwerpunkt im Bereich von +-10° nach dem Wert mit dem weitesten Abstand gesucht und als neuer Eckpunkt definiert.
Der Ansatz konnte jedoch nicht zu Ende geführt werden, da sich die Ermittelten Werte nicht von den zuvor ermittelten Eckpunkten unterschieden.

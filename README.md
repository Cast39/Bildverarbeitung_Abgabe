# Bildverarbeitung_Abgabe
Datensatz Beispiele:
![PCBBilder](https://github.com/amazon-science/spot-diff/blob/main/figures/VisA_samples.png?raw=true)
## Erster Ansatz

### 1. segment.py
Das Eingangsbild wird mit einer Bitmaske über mehrere Farbkanäle bearbeitet. Es werden alle Pixel - welche die folgenden Schwellwerte nicht überschreiten - schwarz, bzw. transpartent überschrieben.

|Rot  |  Grün | Blau |
|-----|-------|------|
|< 133| < 133 | < 150|

Hier ein Beispiel anhand des Bildes "Bildname" aus dem Datensatz.
(Beispielbild einfügen)

### 2. get_contour.py & 3. boundary_box.py
**Wieso hier Graubildumwandlung?**

Das maskierte Bild wird darauf in die openCV Funktion `cv2.findContours()` übergeben, welche eine Bloberkennung umsetzt. Mit Hilfe dieser Bloberkennung ist die genaue Bestimmung der Position des PCBs möglich, indem nur der Blob mit einer größten Fläche akzeptiert wird. 
(Beispielbild einfügen)

Um diesen Blob zur weiteren Verarbeitung verwenden zu können, muss der Blob wieder in ein Rechteck umgewandelt werden (boundary_box.py). Hierfür wurde die Funktion `cv2.minAreaRect()` eingesetzt, welche ein Rechteck ausgibt, welches optimal gedreht ist, um alle Pixel eines Blobs mit der kleinsten Fläche zu umschließen (Boundingbox). Es stellt sich nur das Problem, dass Ausreißer in dem Bild zu einem verdrehten Rechteck führen können.
(Beispielbild schief einfügen)

### 4. align.py
In diesem Schritt wird das Rechteck auf 0° Drehung korregiert. Dazu wird mit dem Winkel aus dem vorigen Schritt eine Rotationsmatrix erstellt `(cv2.getRotationMatrix2D())` und auf das Bild angewendet. Es wurde bloß ein extra eingefügt **(>45° -> -90°)**.
(you know the drill)

### 5. get_contour.py & 6. boundary_box.py
Nun wird die Erkennung der Boundingbox auf das gedrehte Bild angewand.

### 7. align.py
Nun wird align wieder ausgeführt, dieses mal jedoch auf das Originalbild, um den Hintergrund und die originalen Farben des Bildes bei zu behalten.

### 8. crop.py
Folgend kann das Bild zugeschnitten werden. Hierfür wird ein optimales Seitenverhältnis von **w / h = 980 / 580 = 1,69** vorgegeben. Stimmt dieses nicht mit der Bounding Box überein, wird diese auf das entsprechende Verhältnis nach oben erweitert.
Darauf wird das Bild auf diese Bounding Box ausgeschnitten.


### 9. orient.py
Durch das Cropes Bildes ist es so, dass der Spunkt der PCB in einer Seite des Bildes sein wird. Daher wird das Bild dann an diesem dann ausgerichtet. 

### 10. scale.py
Folgend werden alle bilder mit `cv2.resize()` auf **980 x 580** skaliert.


## Zweiter Ansatz: SVM



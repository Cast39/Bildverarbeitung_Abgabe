import numpy as np
from cv2 import minAreaRect, boxPoints, moments


def get_kontur_graph(contour):
    momente = moments(contour)
    x_sw = int(momente["m10"] / momente["m00"])
    y_sw = int(momente["m01"] / momente["m00"])

    # Konturfunktion erstellen
    konturverlauf = []
    for punkt_abs in contour: # alle Punkte eines Blobs
        x, y = punkt_abs[0][0] - x_sw, punkt_abs[0][1] - y_sw

        radius = np.linalg.norm((x, y),ord=2)
        winkel = np.arctan2(x, y)+np.pi

        konturverlauf.append((winkel, radius))
    
    # Abtastung
    res = 1 # Grad
    winkels = np.arange(0, 360, res)*np.pi/180
    quant_lauf = [] # quantisierte Konturverläufe
    found = False
    
    # Fließender Mittelwert
    maxima = []
    is_rising = True

    for i, winkel in enumerate(winkels):
        for j in np.arange(len(konturverlauf)):
            found = False
            #print(winkel)
            if konturverlauf[j][0] >= winkel:
                quant_lauf.append([konturverlauf[j][0], konturverlauf[j][1], 0]) # winkel, radius, (mittel)
                found = True
                break

        if not found: # wenn kein Wert gefunden (z.b. bei 89°) abbrechen
            break
        
        if i >= 3:
            print(f"curr at {i}")
            #quant_lauf[i][2] = (quant_lauf[i-3][2] + quant_lauf[i-2][2] + quant_lauf[i-1][2] + quant_lauf[i][1])/4
            quant_lauf[i][2] = (quant_lauf[i-2][2] + quant_lauf[i-1][2] + quant_lauf[i][1])/3
            quant_lauf[i][2] = (quant_lauf[i-1][2] + quant_lauf[i][1])/2
            
            if is_rising and quant_lauf[i][2] < quant_lauf[i-1][2]:
                print(f"MAXIMUM at {i} ({quant_lauf[i]})")
                maxima.append(quant_lauf[i])
                is_rising = False

            elif not is_rising and quant_lauf[i][2] > quant_lauf[i-1][2]:
                is_rising = True

        else:
            print(f"prev {i}")
            quant_lauf[i][2] = quant_lauf[i][1]
    #print(quant_lauf)
    return quant_lauf

"""    rect = minAreaRect(contour)
    box = boxPoints(rect)
    box = int32(box)
    center, size, angle = rect

    return (box, center, size, angle)
"""
import numpy as np
from cv2 import minAreaRect, boxPoints, moments

def boundary_from_contour(contour):
    rect = minAreaRect(contour)
    box = boxPoints(rect)
    box = np.int32(box)
    center, size, angle = rect

    return (box, center, size, angle)


def contour_graph(contour, abtastung=1): # abtastung in Grad
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
    winkels = np.arange(0, 360, abtastung)*np.pi/180
    quant_lauf = [] # quantisierte Konturverläufe
    found = False
    
    # Fließender Mittelwert
    

    for i, winkel in enumerate(winkels):
        for j in np.arange(len(konturverlauf)):
            found = False

            if konturverlauf[j][0] >= winkel:
                quant_lauf.append([konturverlauf[j][0], konturverlauf[j][1], 0]) # winkel, radius, (mittel)
                found = True
                break

        if not found: # wenn kein Wert gefunden (z.b. bei 89°) abbrechen
            break
        
        if i >= 3:
            #quant_lauf[i][2] = (quant_lauf[i-3][2] + quant_lauf[i-2][2] + quant_lauf[i-1][2] + quant_lauf[i][1])/4     # 4 Mittelwerte
            #quant_lauf[i][2] = (quant_lauf[i-2][2] + quant_lauf[i-1][2] + quant_lauf[i][1])/3   # 3 Mittelwerte
            quant_lauf[i][2] = (quant_lauf[i-1][2] + quant_lauf[i][1])/2    # 2 Mittelwerte

        else:
            quant_lauf[i][2] = quant_lauf[i][1]
    #print(quant_lauf)
    return quant_lauf


def boundary_from_graph(contour_graph, rough_box, rough_center, resolution=1, searchwiggle=10): # [resolution] = Grad; [searchwiggle] = +-Grad
    angles = contour_graph[:, 0]
    radia = contour_graph[:, 1]
    mean_radia = contour_graph[:, 2]
    #print(angles)

    rough_angles = []
    precise_boxpoints = []
    
    for i, rough_boxpoint in enumerate(rough_box):
        rough_angles.append(np.arctan2(rough_boxpoint[0], rough_boxpoint[1])*180/np.pi)
        startwiggle = rough_angles[-1] - searchwiggle % len(angles)
        endwiggle = rough_angles[-1] + searchwiggle % len(angles)

        # umliegende maxima finden
        #print(f"searching for point ({rough_boxpoint[0]}, {rough_boxpoint[1]}) ({i})")
        i = int(startwiggle//resolution)
        maximum = {"angle": angles[i] , "radius": radia[i], "point": rough_boxpoint}
        for i in np.arange(startwiggle//resolution, endwiggle//resolution, resolution):
            i = int(i) % len(angles)
            if radia[i] > maximum["radius"]:
                maximum = {"angle": angles[i] , "radius": radia[i], "point": rough_boxpoint}

        precise_boxpoints.append(maximum)
    
    print("alles:")
    print(precise_boxpoints)
    """box = boxPoints(precise_boxpoints)
    box = np.int32(box)

    return (box)"""
    return precise_boxpoints
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

    is_rising = True
    rough_angles = []
    precise_boxpoints = []
    
    for i, rough_boxpoint in enumerate(rough_box):
        rough_angles.append(np.arctan2(rough_boxpoint[0], rough_boxpoint[1])*180/np.pi)
        startwiggle = rough_angles[-1] - searchwiggle
        endwiggle = rough_angles[-1] + searchwiggle

        # umliegende maxima finden
        print(f"searching for point ({rough_boxpoint[0]}, {rough_boxpoint[1]}) ({i})")
        maxima = []
        for i in np.arange(startwiggle//resolution, endwiggle//resolution, resolution):
            # print(f"i {i} | i%{len(angles)}={i % len(angles)}")
            i = int(i % len(angles))
            if is_rising and radia[i] < radia[i-1]:
                print(f"MAXIMUM at {angles[i]}, {radia[i]}")
                maxima.append({"angle": angles[i] , "radius": radia[i], "point": rough_boxpoint})
                is_rising = False

            elif not is_rising and radia[i] > radia[i-1]:
                is_rising = True

        # Punkte Filtern für nähsten
        if len(maxima) == 0:
            precise_boxpoints.append(rough_boxpoint)
            print("minimum(filled):")
            print(rough_boxpoint)
        
        elif len(maxima) == 1:
            precise_boxpoints.append(maxima[0]["point"])
            print("minimum(spotted):")
            print(maxima[0]["point"])
        
        elif len(maxima) > 1:
            min_maximum_point = maxima[0]
            min_diff = abs(rough_angles[-1] - min_maximum_point["angle"])
            
            for maximum in maxima:
                diff = abs(rough_angles[-1] - maximum["angle"])
                if diff < min_diff:
                    min_diff = diff
                    min_maximum_point = maximum["point"] # TODO -> Genauen Punkt berechnen
            print("minimum(eval):")
            print(min_maximum_point)
            precise_boxpoints.append(min_maximum_point)
        print()
    
    print("alles:")
    print(precise_boxpoints)
    return precise_boxpoints


    box = boxPoints(rect)
    box = np.int32(box)
    center, size, angle = rect

    return (box, center, size, angle)
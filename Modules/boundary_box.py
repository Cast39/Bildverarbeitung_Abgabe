import numpy as np
import cv2

param = 0.05 # Zwischen 0..1 ?

#def boundary_box(contour):
def boundary_box(contours, width, height):
    svm = cv2.ml.SVM_create()
    svm.setKernel(cv2.ml.SVM_LINEAR)
    #svm.setKernel(cv2.ml.SVM_RBF)
    svm.setType(cv2.ml.SVM_C_SVC)

    svm.setC(param) # Größer -> weniger Klassen
    svm.setGamma(param) # Hohes Gamma -> Punkte nahe an Grenze haben höhere Priorität im Training
    
    train = []
    response = []
    counter = 0
    for contour in contours:
        print(counter)
        newtrain = contour[:,0,:].astype(np.float32)

        train.extend(newtrain) # remove weird format artefact
        response.extend([counter]*(len(newtrain)))

        counter += 1

    train = np.array(train).astype(np.float32)
    response = np.array(response).astype(int)
    print(train)
    print(response)
    svm.train(train, cv2.ml.ROW_SAMPLE, response)

    mat=np.zeros((width*height,2)).astype(np.float32)
    #print(mat.shape)
    for i in range(height):
        for j in range(width):
            mat[i*width+j,:]=[i,j]
    
    #print(mat)
    erg = svm.predict(mat.astype(np.float32))
    erg = erg[1].reshape(height,width)

    #erg = mat.reshape(height, width, 2)
    #erg = erg[:,:,1].astype(np.float32)
    #print(erg.shape)
    cv2.normalize(erg,erg,0, 1, cv2.NORM_MINMAX)
    #erg=cv2.resize(erg,None,None,10,10,cv2.INTER_NEAREST)

    return svm, erg
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    center, size, angle = rect

    return (box, center, size, angle)

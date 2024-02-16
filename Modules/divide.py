import os
import random
import shutil

def divide(source_path,train_folder,test_folder):

    # Liste aller Dateien im Ordner
    file_list = os.listdir(source_path)

    # Bestimme die Anzahl der Trainings- und Testbilder
    num_total_images = len(file_list)
    num_train_images = int(num_total_images * 0.9)
    #num_test_images = num_total_images - num_train_images #falls benötigt

    # Zufällige Auswahl der Trainingsbilder
    train_images = random.sample(file_list, num_train_images)

    # Iteriere über alle Dateien im Ordner
    for file_name in file_list:
        # Bildpfad erstellen
        image_path = os.path.join(source_path, file_name)
        
        # Bestimme das Zielverzeichnis basierend auf der Zugehörigkeit zum Trainings- oder Testdatensatz
        if file_name in train_images:
            destination_folder = train_folder
        else:
            destination_folder = test_folder
        
        # Ziel-Pfad erstellen
        destination_path = os.path.join(destination_folder, file_name)
        
        # Verschiebe das Bild in das entsprechende Verzeichnis
        shutil.move(image_path, destination_path)
    
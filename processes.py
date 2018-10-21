import os
import time
import face_recognition
import cv2
import pickle
import pandas as pd

Faces = {
    '1_AiVanh':{'job':'teacher STEM','gender':'female','age':[18, 24]},
    'BaoVan':{'job':'teacher STEM','gender':'female','age':[18, 24]},
    'DangHuy':{'job':'Engineer','gender':'male','age':[18, 24]},
    'HongLinh':{'job':'Sale Marketer','gender':'female','age':[18, 24]},
    'HongThi':{'job':'teacher STEM','gender':'female','age':[25, 32]},
    'KimNgan':{'job':'teacher STEM','gender':'female','age':[25, 32]},
    'MongHuyen':{'job':'teacher STEM','gender':'female','age':[25, 32]},
    'ThanhGiang':{'job':'Manager','gender':'female','age':[25, 32]},
    'ThuThuy':{'job':'teacher STEM','gender':'female','age':[25, 32]},
    'TrangQuynh':{'job':'Consultant Lead','gender':'female','age':[18, 24]},
    'VanNhan':{'job':'Engineer','gender':'male','age':[18, 24]},
    'XuanSon':{'job':'teacher STEM','gender':'male','age':[25, 32]},
    'YenNhi':{'job':'teacher STEM','gender':'female','age':[25, 32]}
}
def load_face_db(path='FaceDb'):
    known_face_encodings = []
    label_names = []
    names = os.listdir(path)
    for name in names:
        name_path = os.path.join(path, name)
        im_names = os.listdir(name_path)
        for im_name in im_names:
            if '.txt' in im_name:
                continue
            im_path = os.path.join(name_path, im_name)
            # im = face_recognition.load_image_file(im_path)
            im = cv2.imread(im_path)
            face_encodings = face_recognition.face_encodings(im)
            if len(face_encodings) < 1:
                print (im_name, ' loading fail')
                continue
            known_face_encodings.append(face_encodings[0])
            label_names.append(name)
            print (im_name, im.shape, 'num faces:', len(face_encodings), ' success')
    known_face_encodings_f = open('known_face_encodings.pkl', 'wb')
    label_names_f = open('label_names.pkl', 'wb')
    pickle.dump(known_face_encodings, known_face_encodings_f)
    pickle.dump(label_names, label_names_f)
    known_face_encodings_f.close()
    label_names_f.close()
    return known_face_encodings, label_names

# known_face_encodings, known_face_names = load_face_db()
info = pd.read_csv('FaceDb/FaceDB')
known_face_encodings_f = open('known_face_encodings.pkl', 'rb')
label_names_f = open('label_names.pkl', 'rb')
known_face_encodings = pickle.load(known_face_encodings_f)
known_face_names = pickle.load(label_names_f)
known_face_encodings_f.close()
label_names_f.close()


def recognize(im_array):
    face_locations = face_recognition.face_locations(im_array)
    face_encodings = face_recognition.face_encodings(im_array, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            face_names.append(name)
        else:
            face_names = None
    return face_names

if __name__ == "__main__":
    start_time = time.time()
    im = cv2.imread('FaceDb/KimNgan/KimNgan (3).jpeg')
    name = recognize(im)
    print (name)
    print("--- %s seconds ---" % (time.time() - start_time))

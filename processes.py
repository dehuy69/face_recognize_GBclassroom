import os
import face_recognition
import cv2
import pickle
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
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            face_names.append(name)
    return face_names

if __name__ == "__main__":
    im = cv2.imread('FaceDb/AiVanh/AiVanh (1).png')
    name = recognize(im)
    print (name)

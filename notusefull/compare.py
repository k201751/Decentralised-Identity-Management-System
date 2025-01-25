from deepface import DeepFace
import cv2
img1=cv2.imread("D:\Dev projects\IDmanage\img1.png")
img2=cv2.imread("D:\Dev projects\IDmanage\img2.png")

result = DeepFace.verify(img1, img2)
print(result['verified'])
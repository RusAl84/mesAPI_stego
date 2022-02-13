from LSBSteg import LSBSteg
import cv2
#encoding
steg = LSBSteg(cv2.imread("new.png"))
img_encoded = steg.encode_text("my message RUSAL84")
cv2.imwrite("stego.png", img_encoded)

#decoding
im = cv2.imread("stego.png")
steg = LSBSteg(im)
print("Text value:",steg.decode_text())
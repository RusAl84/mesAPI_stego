#encoding
steg = LSBSteg(cv2.imread("my_image.png"))
img_encoded = steg.encode_text("my message")
cv2.imwrite("my_new_image.png", img_encoded)

#decoding
im = cv2.imread("my_new_image.png")
steg = LSBSteg(im)
print("Text value:",steg.decode_text())
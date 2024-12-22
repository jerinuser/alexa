import matplotlib.pyplot as plt
import cv2

image = cv2.imread("james.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
inverted = 255 - gray_image
blur = cv2.GaussianBlur(inverted, (15, 15), 0)
invertedblur = 255 - blur
sketch = cv2.divide(gray_image, invertedblur, scale=220.0)

adaptive_sketch = cv2.adaptiveThreshold(
    sketch, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
)


cv2.imwrite("sketch_image.png", sketch)

# Display using matplotlib
plt.imshow(sketch, cmap="gray")
plt.axis("off")
plt.show()

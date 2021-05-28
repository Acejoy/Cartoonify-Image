import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd


class Cartoonify:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('RGB-to-Gray-iser')
        # self.root.geometry("640x480")
        self.panelImg = None
        self.panelCartoon = None
        
        self.selectBtn = tk.Button(self.root, text="Select an image", command=self.select_image)
        self.selectBtn.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

        self.saveBtn = tk.Button(self.root, text="Save image", command=self.save_image)
        self.saveBtn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
        self.saveBtn.configure(state=tk.DISABLED)

    def color_quantisation(self, img, num_centers=10):
        # Transform the image
        data = np.float32(img).reshape((-1, 3))

        # Determine criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        # Implementing K-Means
        ret, label, center = cv2.kmeans(data, num_centers, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result
        

    def cartoonify(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        quantised_img = self.color_quantisation(img, 10)

        color = cv2.bilateralFilter(quantised_img, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    def select_image(self):
        path = fd.askopenfilename()

        if len(path)>0:
            image = cv2.imread(path)
            cartoon = self.cartoonify(image)

            im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

            imTk = Image.fromarray(im)
            cartoonTk = Image.fromarray(cartoon)

            imTk=ImageTk.PhotoImage(imTk)
            cartoonTk=ImageTk.PhotoImage(cartoonTk) 


            if self.panelImg is None or self.panelCartoon is None:

                self.panelImg = tk.Label(image=imTk)
                self.panelImg.image = imTk
                self.panelImg.pack(side="left", padx=10, pady=10)

                self.panelCartoon = tk.Label(image=cartoonTk)
                self.panelCartoon.image = cartoonTk
                self.panelCartoon.pack(side="right", padx=10, pady=10)

                self.saveBtn.configure(state=tk.ACTIVE)

            else:
                self.panelImg.configure(image=imTk)
                self.panelCartoon.configure(image=cartoonTk)
                self.panelImg.image = imTk
                self.panelCartoon.image = cartoonTk

        pass

    def save_image(self):
        fileTypes = [('JPG','*.jpg'), ('PNG', '*.png')]
        f = fd.asksaveasfile(mode='wb', filetypes=fileTypes,defaultextension=".jpg")
        
        if f is None:
            return
        
        img = ImageTk.getimage(self.panelCartoon.image)
        rgb_img = img.convert('RGB')
        rgb_img.save(f)
        

if __name__ == "__main__":
    c = Cartoonify()
    c.root.mainloop()
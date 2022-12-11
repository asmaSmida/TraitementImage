import random
import numpy as np
from tkinter import *

class myimage:
    def __init__(self, type, width, height, data, max_pixel_value) -> None:
        self.type = type
        self.width = width
        self.height = height
        self.data = data.astype(int)
        self.max_pixel_value = max_pixel_value

    SUPPORTED_TYPES = ["P2", "P3", "P5", "P6"]
    def read(filename):
        file = open(filename)#"C:\Users\octanet\OneDrive\Bureau\traitement myimage\chat.pgm"
        lines = [x.strip() for x in file.readlines() if not x.startswith("#")] 
        type = lines[0].upper()
        width, height = [ int(x) for x in lines[1].split(" ") ]
        max_pixel_value = int(lines[2])
        

        if type not in myimage.SUPPORTED_TYPES:
            print("Type is not supported.")
            return

        data = None
        if type == "P2":
            pixels = lines[3:]
            data = myimage._read_p2(pixels)
        elif type == "P3":
            pixels = lines[4:]
            data = myimage._read_p3(pixels)

        return myimage(type, width, height, data, max_pixel_value)

    def show(self):
        print(self.data)
    
    def write(self, filename):
        file = open(filename, "w")
        file.write(self.type + "\n")
        file.write("# Created by myimage_reader_lib @LLC\n")
        file.write(str(self.width) + " " + str(self.height) + "\n")
        file.write(str(self.max_pixel_value) + "\n")
        for row in self.data:
            for pixel in row:
                file.write(str(pixel) + " ")
            file.write("\n")

    def _read_p2(pixels):
        #print(pixels)
        data = []
        for row in pixels:
            row = np.array([int(x) for x in row.split(' ')])
            data.append(row)
        data = np.array(data)
        print(data)
        return data.astype(int)
    
    def _read_p3(pixels):
        data = []
        for row in pixels:
            row = np.array([int(x) for x in row.split(' ')])
            row = row.reshape((row.shape[0] // 3, 3))
            data.append(row)
        data = np.array(data)
        return data.astype(int)

    def convert_to_gray(self):
        if self.type == "P2":
            return self.data
        data = []
        for row in self.data:
            row = row.reshape((row.shape[0] * row.shape[1]))
            data.append(row)
        return np.array(data)

    def mean(self):
        data = self.convert_to_gray()
        sum = 0
        for row in data:
            for pixel in row:
                sum += pixel
        return sum / (self.width * self.height)
    
    def ecart_type(self):
        mean = self.mean()
        data = self.convert_to_gray()
        sum = 0
        for row in data:
            for pixel in row:
                sum += (pixel - mean) ** 2
        return (sum / (self.width * self.height)) ** (1/2)
    
    def gray_histogram(self):
        data = self.convert_to_gray()
        histogram = np.zeros(self.max_pixel_value + 1)
        for row in data:
            for pixel in row:
                histogram[pixel] += 1
        return histogram.astype(int)
    

    def cumulated_histogram(self):
        histogram = self.gray_histogram()
        cumulated_histogram = np.zeros((self.max_pixel_value + 1))
        cumulated_histogram[0] = histogram[0]
        for i in range(1, self.max_pixel_value + 1):
            cumulated_histogram[i] = cumulated_histogram[i - 1] + histogram[i]
        return cumulated_histogram
    
    def histogram_equalization(self):
        cumulated_histogram = self.cumulated_histogram()
        data = self.convert_to_gray()
        nbr=0
        for i in range(self.height):
            for j in range(self.width):
                nbr+=1
                pc_n = cumulated_histogram[data[i][j]] / (self.width * self.height)
                data[i][j] = round(pc_n * self.max_pixel_value)
        self.data = data
        #print(nbr)
        return data.astype(int)

    def show_with_matplotlib(self, data = None, show = True):
        import matplotlib.pyplot as plt
        # Show gray myimage
        if data is None:
            data = self.convert_to_gray()
        plt.imshow(data, cmap="gray")
        if show:
            plt.show()
    
    def modify_contrast(self, x, y, x2, y2):
        data = self.convert_to_gray()
        for i in range(self.height):
            for j in range(self.width):
                if data[i][j] < x:
                    data[i][j] = (y / x) * data[i][j]
                elif data[i][j] < x2:
                    data[i][j] = (y2 - y) / (x2 - x) * (data[i][j] - x) + y
                else:
                    data[i][j] = (self.max_pixel_value - y2) / (self.max_pixel_value - x2) * (data[i][j] - x2) + y2
        self.data = data
        return data

    def info(self):
        print("Taille: " + self.type)
        print("Largeur: " + str(self.width))
        print("Longueur: " + str(self.height))
        print("resolution: " + str(self.max_pixel_value))
        print("Moyenne: " + str(self.mean()))
        print("Ecart type: " + str(self.ecart_type()))
        print("Histogramme: " + str(self.gray_histogram()))
        print(" histogramme Cumulé: " + str(self.cumulated_histogram()))

    def bruiteLmyimage(self):
        for i in range(self.height):
            for j in range(self.width):
                n=random.randrange(0,20)
                match n : 
                    case 0:
                        self.data[i][j]=0
                    case 20:
                        self.data[i][j]=255
        return self.data

    def moyenneFilre(self,n):
        filtre = [[1/(n*n) for i in range(n)]for i in range(n)]
        for ligne in range(1,self.height-n):
            for col in range(1,self.width-n):
            # On calcule la somme 
                somme = 0
                for l in range(n):
                    for c in range(n):
                        somme = filtre[l][c]*self.data[ligne-1+l][col-1+c]+somme
                self.data[ligne][col] = somme

        return self.data

    def median_filter(data,filter_size):
        temp = []
        indexer = filter_size // 2
        data_final = []
        data_final = np.zeros((len(data),len(data[0])))
        for i in range(len(data)):

            for j in range(len(data[0])):

                for z in range(filter_size):
                    if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                        for c in range(filter_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(filter_size):
                                temp.append(data[i + z - indexer][j + k - indexer])

                temp.sort()
                data_final[i][j] = temp[len(temp) // 2]
                temp = []
        return data_final

    def passHautFiltre(self):
        filtre = np.array([[0, -0.5, 0],
                  [-0.5, 3, -0.5],
                  [0, -0.5, 0 ]])
        for ligne in range(1,self.height-1):
            for col in range(1,self.width-1):
                # On calcule la somme 
                somme = 0
                for l in range(3):
                    for c in range(3):
                        somme = filtre[l,c]*self.data[ligne-1+l,col-1+c]+somme
                self.data[ligne,col] = somme
        return self.data

    def signaltonoise(Arr, axis=0, ddof=0):
        Arr = np.asanyarray(Arr)
        me = Arr.mean(axis=None)
        sd = Arr.std(axis=None, ddof=ddof)
        return np.where(sd == 0, 0, me/sd)


    def seuillage(self,S1,S2,S3):
        #data= np.copy(self.data)
        data=self.data
        i=0
        for ligne in range(0,self.height,1):
            for col in range(0,self.width,1):
                i+=1
                if(data[ligne][col][0]<S1):
                    data[ligne][col][0]=0
                else:
                    data[ligne][col][0]=255
                if(data[ligne][col][1]<S2):
                    data[ligne][col][1]=0
                else:
                    data[ligne][col][1]=255
                if(data[ligne][col][2]<S3):
                    data[ligne][col][2]=0
                else:
                    data[ligne][col][2]=255
        print(i)
        return data

    def seuillageETOU(self,S1,S2,S3,type):
        #data= np.copy(self.data)
        data=self.data
        i=0
        if(type=='OU'):
            for ligne in range(0,self.height,1):
                for col in range(0,self.width,1):
                    i+=1
                    if(data[ligne][col][0]<S1 and data[ligne][col][1]<S2 and data[ligne][col][2]<S3):
                        data[ligne][col][0]=0
                        data[ligne][col][1]=0
                        data[ligne][col][2]=0
                    else:
                        data[ligne][col][0]=255
                        data[ligne][col][1]=255
                        data[ligne][col][2]=255
            print(i)
            return data
        else:
            for ligne in range(0,self.height,1):
                for col in range(0,self.width,1):
                    if(data[ligne][col][0]<S1 or data[ligne][col][1]<S2 or data[ligne][col][2]<S3):
                        data[ligne][col][0]=0
                        data[ligne][col][1]=0
                        data[ligne][col][2]=0
                    else:
                        data[ligne][col][0]=255
                        data[ligne][col][1]=255
                        data[ligne][col][2]=255
            return data






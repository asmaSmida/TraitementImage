from seuillage import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from Imagedefinition import *

imagePath = r"C:\Users\hp\Desktop\gl4\sem1\chat.pgm"
arr = None

self= myimage.read(imagePath)
type=self.type
height=self.height
width=self.width
arr=self.data
maxGreyLevel=self.max_pixel_value
print(self.data)
# print(arr)
# writePGM("images/bonjour", arr, width, height, maxGreyLevel)

(hist, cumulativeHist) = histogram(arr, maxGreyLevel)
(mean,std) = meanSTD(arr)
mean=format(mean,'.2f')
std=format(std,'.2f')
meanSTR = str(mean)
stdSTR = str(std)
def updateImageInfos():
    strings=imagePath.split('/')
    imageName= strings[len(strings)-1]
    btn_path.configure(text=imageName)
    heightBtn.configure(text=str(height))
    widthBtn.configure(text=str(width))
    maxGrayBtn.configure(text=str(maxGreyLevel))
    global mean
    global std
    global meanSTR
    global stdSTR
    global hist
    global cumulativeHist
    #hist=myimage.gray_histogram(self)
   # cumulativeHist=myimage.cumulated_histogram(self)
    (hist, cumulativeHist) = histogram(arr, maxGreyLevel)

    (mean,std) = meanSTD(arr)

    mean=format(mean,'.2f')
    std=format(std,'.2f')
    meanSTR = str(mean)
    stdSTR = str(std)  
    meanValue.configure(text=meanSTR)
    stdValue.configure(text=stdSTR)    

def updateImg(newPath):
    global imagePath 
    imagePath= newPath
    global width
    global height
    global maxGreyLevel
    global arr
    global self
    self= myimage.read(imagePath)
    type=self.type
    height=self.height
    width=self.width
    arr=self.data
    maxGreyLevel=self.max_pixel_value
   # updateImageInfos()
    plotImage(arr)

def equalize():
    # global arr
    # global maxGr
    global arr
    arr=myimage.histogram_equalization(self)
   # arr=egalisation(arr,maxGreyLevel,cumulativeHist,height,width)
    plotImage(arr)
    updateImageInfos()

def linearContrast():
    if xA.get(1.0, "end-1c") =="" :
        messagebox.showerror(title='xa not specified', message="please enter xa value ")
    elif yA.get(1.0, "end-1c") =="" :
        messagebox.showerror(title='ya not specified', message="please enter ya value ")
    elif xB.get(1.0, "end-1c") =="":
        messagebox.showerror(title='xb not specified', message="please enter xb value ")
    elif yB.get(1.0, "end-1c")=="":
         messagebox.showerror(title='yb not specified', message="please enter yb value ")
    else:
        y1 = int(yA.get(1.0, "end-1c"))
        x2 = int(xB.get(1.0, "end-1c"))
        y2 = int(yB.get(1.0, "end-1c"))
        print((x1,y1),(x2,y2))
        global arr
        arr=myimage.modify_contrast(self, x1, y1, x2, y2)
    #arr = linearContrastTransform(arr, height, width, x1, y1, x2, y2, maxGreyLevel)   
        updateImageInfos()
        plotImage(arr)
    #myimage.show_with_matplotlib(self)
def addNoiseAndShow():
    global arr
    arr=myimage.bruiteLmyimage(self)
   # arr= addingNoise(arr,height,width)
    plotImage(arr)
    updateImageInfos()

def  applyAverageFilter():
   
    if filterSizeValue.get(1.0, "end-1c")=="" :
        print("inside if")
        messagebox.showerror(title='no dimention specified', message="please enter the filter dimention ")
    else :
        n=int(filterSizeValue.get(1.0, "end-1c"))
        print("n= ",n)
        global arr
        arr=myimage.moyenneFilre(self,n)
        plotImage(arr)
        updateImageInfos()

def  applyMedianFilter():
    if filterSizeValue.get(1.0, "end-1c")=="" :
        print("inside if")
        messagebox.showerror(title='no dimention specified', message="please enter the filter dimention ")
    else :
        n=int(filterSizeValue.get(1.0, "end-1c"))
        global arr
        arr=myimage.median_filter(self.data,n)
    #arr = medianFilter(arr,height,width,n)
        plotImage(arr)

        updateImageInfos()

def  seuillage():
    s1=int(p1.get(1.0, "end-1c"))
    s2=int(p2.get(1.0, "end-1c"))
    s3=int(p3.get(1.0, "end-1c"))

    global arr
    arr=myimage.seuillage(self,s1,s2,s3)
    #arr = medianFilter(arr,height,width,n)
    plotImage(arr)

    updateImageInfos()

def  seuillageEtOu(type):
    s1=int(p1.get(1.0, "end-1c"))
    s2=int(p2.get(1.0, "end-1c"))
    s3=int(p3.get(1.0, "end-1c"))

    global arr

    arr=myimage.seuillageETOU(self,s1,s2,s3,type)
    #arr = medianFilter(arr,height,width,n)
    plotImage(arr)

    updateImageInfos()

def applyHighPassFilter():
    global arr
    arr = myimage.passHautFiltre(self)
    plotImage(arr)
    updateImageInfos()
def applyOTSU():
    global arr
    arr= otsu(width, height, maxGreyLevel, arr)
    plotImage(arr)
    updateImageInfos()

def printHist():
    print(hist)


def test():
    pass


def openImage():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("pgm files", "*.pgm"), ("ppm Files", "*.ppm")]
    )
    if not filepath:
        return
    updateImg(filepath)

plotImage(arr)
window = tk.Tk()

window.geometry("1500x800+0+0")

window.title("Image Editor")



# --------------Image infos ---------------------------

basicOperation = tk.Frame(window)

btn_original = tk.Button(basicOperation, text="Original image", width=18,
                        font=("Arial", 12), command=lambda: updateImg(imagePath))
btn_Img = tk.Button(basicOperation, text="Show current image", width=18,
                        font=("Arial", 12), command=lambda: plotImage(arr))
btn_openPGM = tk.Button(basicOperation, text="Open new image", width=18,
                        font=("Arial", 12), command= openImage)
btn_savePGM = tk.Button(basicOperation, text="Save current PGM", width=18,
                        font=("Arial", 12), command=test)

btn_original.grid(row=0, column=0)
btn_Img.grid(row=0, column=1)
btn_openPGM.grid(row=0, column=2)
btn_savePGM.grid(row=0, column=3)

# --------------Image infos ---------------------------

imageInfos = tk.Frame(window, relief=tk.RAISED, bd=2, pady=10)

firstSection2 = tk.Label(imageInfos, text="", font=("Arial", 14))
pathLabel = tk.Label(imageInfos,text="Path:", font=("Arial", 12))
heightLabel = tk.Label(imageInfos,text="Height:", font=("Arial", 12))
widthLabel = tk.Label(imageInfos,  text="Width", font=("Arial", 12))
maxGrayLabel = tk.Label(imageInfos, text="Max gray level:", font=("Arial", 12))
mean = tk.Label(imageInfos, text="Mean:", font=("Arial", 12))
std = tk.Label(imageInfos, text="Standard deviation:", font=("Arial", 12))

btn_path = tk.Button(imageInfos, text='image', width=10,
                     font=("Arial", 12),relief=tk.SUNKEN, command=test)

heightBtn = tk.Button(imageInfos, text=str(height),relief=tk.SUNKEN,  width=10,
                      font=("Arial", 12), command=test)

widthBtn = tk.Button(imageInfos, text=str(width), relief=tk.SUNKEN, width=10,
                     font=("Arial", 12), command=test)
maxGrayBtn = tk.Button(imageInfos, text="255", relief=tk.SUNKEN, width=10,
                       font=("Arial", 12), command=test)

meanValue = tk.Button(imageInfos, text=meanSTR,
                      font=("Arial", 12), width=10, relief=tk.SUNKEN, command=test)
stdValue = tk.Button(imageInfos, text=stdSTR,
                     font=("Arial", 12), width=10, relief=tk.SUNKEN, command=test)

cumulHistogButton = tk.Button(imageInfos, text="Cumulative Histogram",
                              font=("Arial", 12), width=18,  command=lambda: plotCumulativeHist(cumulativeHist, maxGreyLevel))
histoButton = tk.Button(imageInfos, text="Histogram",
                        font=("Arial", 12), width=18,  command=lambda: plotHistogram(hist))
equalizationBtn = tk.Button(imageInfos, text="Equalize",
                            font=("Arial", 12), width=20, command=equalize)

OTSUBtn = tk.Button(imageInfos, text="Apply OTSU Algorithm",
                            font=("Arial", 12), width=20, command=applyOTSU)

firstSection2.grid(row=0, column=0,sticky="w" )
pathLabel.grid(row=1, column=0, sticky="w")
btn_path.grid(row=1, column=1 , sticky="ew", padx=5, pady=10)
heightLabel.grid(row=2, column=0,sticky="w")
heightBtn.grid(row=2, column=1,sticky="ew", padx=5, pady=10)
maxGrayLabel.grid(row=3, column=0,sticky="w")
maxGrayBtn.grid(row=3, column=1,sticky="ew", padx=5, pady=10)
widthLabel.grid(row=4, column=0,sticky="w")
widthBtn.grid(row=4, column=1,sticky="ew", padx=5, pady=10)
mean.grid(row=5, column=0, sticky="w")
meanValue.grid(row=5, column=1,sticky="ew", padx=5, pady=10)
std.grid(row=6, column=0, sticky="w")

stdValue.grid(row=6, column=1,sticky="ew", padx=5, pady=10)
cumulHistogButton.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
histoButton.grid(row=0, column=4, sticky="ew", padx=5, pady=5)
equalizationBtn.grid(row=0, column=5, sticky="ew", padx=5, pady=5)
OTSUBtn.grid(row=0, column=6, sticky="ew", padx=5, pady=5)


linearTransformLabel = tk.Label(
    imageInfos, text="Linear contrast", font=("Arial", 12))
contrastButton = tk.Button(imageInfos, text="Apply linear contrast",
                           font=("Arial", 12), width=17, command=linearContrast)
linearTransformLabel.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
contrastButton.grid(row=4, column=3, sticky="ew", padx=50, pady=5)


lab1=tk.Frame(imageInfos)
lab1.grid(row=3, column=3,sticky="ew", padx=50)

labelX1 = tk.Label(lab1, text="X1", font=("Arial", 12))
labelY1 = tk.Label(lab1, text="Y1", font=("Arial", 12))
xA = tk.Text(lab1, height=1,width=3)
yA = tk.Text(lab1, height=1,width=3)
labelX2 = tk.Label(lab1, text="X2", font=("Arial", 12))
labelY2 = tk.Label(lab1, text="Y2", font=("Arial", 12))
xB = tk.Text(lab1, height=1,  width=3)
yB = tk.Text(lab1, height=1, width=3)

labelX1.grid(row=0, column=0,sticky="ew",padx=5, pady=5)
xA.grid(row=0, column=2,sticky="ew" ,padx=5, pady=5)
labelY1.grid(row=0, column=3, sticky="ew",padx=5, pady=5)
yA.grid(row=0, column=4,sticky="ew",padx=5, pady=5)

labelX2.grid(row=1, column=0,sticky="ew" ,padx=5, pady=5)
xB.grid(row=1, column=2,sticky="ew" ,padx=5, pady=5)
labelY2.grid(row=1, column=3, sticky="ew",padx=5, pady=5 )
yB.grid(row=1, column=4,sticky="ew",padx=5, pady=5 )

filtrsizeframe=tk.Frame(imageInfos,bg='grey')
filtrsizeframe.grid(row=2, column=4,)
filterSizeLabel = tk.Label(imageInfos, text="Filter size", font=("Arial", 12))
filterSizeValue = tk.Text(imageInfos, height=1, width=3)
filterSizeLabel.grid(row=2, column=4, )
filterSizeValue.grid(row=2, column=5, )

noiseBtn = tk.Button(imageInfos, text="Pepper and salt noise",
                            font=("Arial", 12), width=20, command=addNoiseAndShow)


averageFilterBtn=tk.Button(imageInfos, text="Average filter",
                            font=("Arial", 12), width=20, command=applyAverageFilter)
medianFilterBtn=tk.Button(imageInfos, text="Median filter",
                            font=("Arial", 12), width=20, command=applyMedianFilter)
highPassFilterBtn=tk.Button(imageInfos, text="High boost",
                            font=("Arial", 12), width=20, command=applyHighPassFilter)
noiseBtn.grid(row=3, column=4, sticky="ew", padx=5, pady=5)
averageFilterBtn.grid(row=3, column=5, sticky="ew", padx=5, pady=5)
medianFilterBtn.grid(row=4, column=4, sticky="ew", padx=5, pady=5)
highPassFilterBtn.grid(row=4, column=5, sticky="ew", padx=5, pady=5)


frmeRGB=tk.Frame(imageInfos)
frmeRGB.grid(row=2, column=6, sticky="ew", padx=50, pady=5)
P1label = tk.Label(frmeRGB, text="Rouge", font=("Arial", 12) ,bg='red')
p1 = tk.Text(frmeRGB, height=1, width=3)
P2label = tk.Label(frmeRGB, text="Vert", font=("Arial", 12),bg="green")
p2 = tk.Text(frmeRGB, height=1, width=3)
P3label = tk.Label(frmeRGB, text="Bleu", font=("Arial", 12),bg="blue")
p3 = tk.Text(frmeRGB, height=1, width=3)

P1label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
p1.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
P2label .grid(row=0, column=2, sticky="ew", padx=5, pady=5)
p2.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
p3.grid(row=0, column=5, sticky="ew", padx=5, pady=5)
P3label.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

SeuilBtn = tk.Button(imageInfos, text="Apply manuel seillage",
          font=("Arial", 12), width=20, command=seuillage)

SeuilBtn.grid(row=3, column=6, sticky="ew", padx=50, pady=5)

buttoseuillgframe=tk.Frame(imageInfos)
buttoseuillgframe.grid(row=4, column=6, sticky="ew", padx=50, pady=5)
SeuilBtnET = tk.Button(buttoseuillgframe, text="seillage ET",
          font=("Arial", 12), width=10, command=lambda:seuillageEtOu("ET"))

euilBtnOU = tk.Button(buttoseuillgframe, text="seillage OU",
          font=("Arial", 12), width=10, command=lambda:seuillageEtOu("OU"))

SeuilBtnET.grid(row=0, column=1, sticky="ew", padx=20, pady=5)
euilBtnOU.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

Section1 = tk.Label(
    imageInfos, text="Contrast", font=("Arial", 17,"bold",'underline'))
Section1.grid(row=1, column=3, sticky="ew", padx=10, pady=10)
Section2 = tk.Label(
    imageInfos, text="Filter", font=("Arial", 17,"bold",'underline'))
Section2.grid(row=1, column=5, sticky="w", padx=10, pady=10)
Section3 = tk.Label(
    imageInfos, text="Seuillage", font=("Arial", 17,"bold",'underline'))
Section3.grid(row=1, column=6, sticky="ew", padx=10, pady=10)

basicOperation.grid(row=0, column=0, sticky="ew")
imageInfos.grid(row=1, column=0, sticky="ew")

window.update()
window.mainloop()
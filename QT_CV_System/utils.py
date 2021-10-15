import matplotlib.pyplot as plt

def show(bgr):
    rgb = bgr[...,::-1]
    plt.imshow(rgb)
    plt.show()

def save(img,filename):
    img = img[...,::-1]
    plt.axis('off')
    plt.margins(0,0)
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
    plt.imshow(img,"gray")
    plt.savefig(filename + ".jpg",dpi=300)


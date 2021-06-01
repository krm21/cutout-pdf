import os
from PIL import Image
from imageio import imwrite
from concurrent import futures


class Cutout:
    def __init__(self):
        self.extension_set = {".jpg", ".jpeg", ".png"}
        self.image_list = [] # to chyba jednak nie
        self.pic_names = []

    def is_done(self):
        return len(self.pic_names) == 0

    def pop_image_name(self):
        return self.pic_names.pop(0)

    def push_image(self, img):
        self.image_list.append(img)
        
    def get_list_of_image_names(self, path):
        # pic_names = []
        _, _, filenames = next(os.walk(path))
        for file in filenames:
            if os.path.splitext(file)[1].lower() in self.extension_set:
                self.pic_names.append(file)
        # return pic_names

    def cut(self, img_name, corners):
        im = Image.open(img_name)
        im = im.crop(
            (corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        )
        im = im.convert('RGB')
        return im

    def convert_to_image_list(self):
        for image_name in self.pic_names:
            self.image_list.append(img)

    def convert_to_image_list_and_cut(self, corners):
        for img in self.pic_names:
            self.image_list.append(cut(img, corners))

    def gen_pdf(self, foldername):   
        pdfname = "out"
        # pdfname = foldername.split(os.path.sep)[-1]
        # if pdfname == ".":
        #     pdfname = "out"
        # self.image_list[0].save(f'{foldername}/{pdfname}.pdf', save_all=True, append_images=self.image_list[1:])
        if len(self.image_list)>1:
            self.image_list[0].save(f'{foldername}/{pdfname}.pdf', save_all=True, append_images=self.image_list[1:])
        else:
            self.image_list[0].save(f'{foldername}/{pdfname}.pdf', save_all=True)

    def cut_img(self, img, corners):
        rv = img.crop(
            (corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        )
        rv = rv.convert('RGB')
        return rv


def cut(img_name, corners):
    im = Image.open(img_name)
    im = im.crop(
        (corners["x1"], corners["y1"], corners["x2"], corners["y2"])
    )
    im = im.convert('RGB')
    return im

def cut_img(img, corners):
    return img.crop(corners["x1"], corners["y1"], corners["x2"], corners["y2"])

def gen_pdf(foldername, corners):
    pic_names = []
    imagelist = []

    extension_set = {".jpg", ".jpeg", ".png"}
    
    _, _, filenames = next(os.walk(foldername))
    for file in filenames:
        if os.path.splitext(file)[1].lower() in extension_set:
            pic_names.append(file)

    for img in pic_names:
        imagelist.append(cut(img, corners))

    pdfname = foldername.split(os.path.sep)[-1]
    if pdfname == ".":
        pdfname = "out"
    if len(imagelist)>1:
        imagelist[0].save(f'{foldername}/{pdfname}.pdf', save_all=True, append_images=imagelist[1:])
    else:
        imagelist[0].save(f'{foldername}/{pdfname}.pdf', save_all=True)

def main(corners):
    gen_pdf(".", corners)

if __name__ == '__main__':
    pass

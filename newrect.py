from cutout import Cutout
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from PIL import ImageTk, Image as PilImage
import os


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.cutout = Cutout()
        self.loaded_image = None
        self.item = None
        self.corners = {}

        self.set_up_frames()
        self.set_up_buttons()

        self.start = None

        # self.label = Label(self.body, text='Open a folder containing images to be converted to PDF...').pack(side=BOTTOM, expand=YES, fill=BOTH)

    def set_up_frames(self):
        self.topbar = Frame(self)
        self.topbar.pack(side=TOP, expand=NO, fill=BOTH)

        self.body = Frame(self, width=1056, height=594)
        self.body.pack(side=BOTTOM, expand=YES, fill=BOTH)

    def set_up_buttons(self):
        self.opendirbutton = Button(self.topbar, text="Open directory...", command=self.opendialog)
        self.opendirbutton.pack(side=LEFT, expand=FALSE, anchor=NW, padx=4, pady=4)
        
        self.savebutton = Button(self.topbar, text="Save page", command=self.save_page)
        self.savebutton.pack(side=LEFT, expand=FALSE, anchor=NW, pady=4)
        self.savebutton["state"] = DISABLED

        self.skipbutton = Button(self.topbar, text="Skip image", command=self.skip_image)
        self.skipbutton.pack(side=LEFT, expand=FALSE, anchor=NW, pady=4, padx=4)
        self.skipbutton["state"] = DISABLED

        self.saveallbutton = Button(self.topbar, text="Save all pictures with selected frame", command=self.save_all_pages)
        self.saveallbutton.pack(side=LEFT, expand=FALSE, anchor=NW, pady=4)
        self.saveallbutton["state"] = DISABLED

    def set_up_canvas(self):
        self.canvas = Canvas(self.body, cursor="tcross")
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind("<Button-1>", self.update, '+')
        self.canvas.bind("<B1-Motion>", self.update, '+')
        self.canvas.bind("<ButtonRelease-1>", self.stop, '+')

    def draw(self, start, end):
        """Draw the rectangle"""
        return self.canvas.create_rectangle(*(list(start)+list(end)),
        fill= "", width= 2, dash= (1, 2), outline= "black")
		
    def update(self, event):
        if not self.start:
            self.start = [event.x, event.y]
            return
		
        if self.item is not None:
            self.canvas.delete(self.item)
        self.item = self.draw(self.start, (event.x, event.y))
		
    def stop(self, event):
        print(self.start, [event.x, event.y])
        if (self.start[0] - event.x)**2 + (self.start[1] - event.y)**2 > 100: # selection must be big enough
            self.corners = {"x1": self.start[0], "y1": self.start[1], "x2": event.x, "y2": event.y}
            self.start = None

            self.saveallbutton["state"] = ACTIVE
            self.savebutton["state"] = ACTIVE

    def load_pic(self, pic_name):
        self.img = PilImage.open(os.path.join(self.path, pic_name))
        self.img.thumbnail((1056, 594), PilImage.ANTIALIAS)
        self.loaded_image = self.img
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.imgtk, anchor=NW)

    def load_first_pic(self, path):
        self.path = path
        self.set_up_canvas()
        self.cutout.get_list_of_image_names(path)
        self.load_pic(self.cutout.pop_image_name())
        self.skipbutton["state"] = ACTIVE

    def opendialog(self):
        self.path = filedialog.askdirectory(initialdir = "/",title = "Select directory")
        self.load_first_pic(self.path)

    def save_page(self):
        self.cutout.push_image(self.cutout.cut_img(self.loaded_image, self.corners))
        if not self.cutout.is_done():
            self.load_pic(self.cutout.pop_image_name())
            self.item = self.draw([self.corners["x1"], self.corners["y1"]], [self.corners["x2"], self.corners["y2"]])
        else:
            self.save_and_close()

    def save_all_pages(self):
        pass

    def skip_image(self):
        self.load_pic(self.cutout.pop_image_name())

    def save_and_close(self):
        self.cutout.gen_pdf()



app = Application()
# app.overrideredirect(True) # removes title bar
# topbar = Frame()
# topbar.pack(side=TOP, expand=YES, fill=BOTH)
# body = Frame()
# opendirbutton = Button(topbar, text="Open directory").pack(side=LEFT, fill=Y)
# body.pack(side=BOTTOM, expand=YES, fill=BOTH)
app.geometry("1056x594")
# app.maxsize(600, 400)
# app.resizable(0, 0)
app.mainloop()

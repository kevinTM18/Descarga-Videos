from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import requests
from io import BytesIO
from PIL import ImageTk, Image
from pytube import YouTube
import os
from threading import Thread

class Window_w :    

    def __init__(self,master):

        self.master = master

        self.master.title("Descarga de video YTB")

        self.master.resizable(width=0, height=0)

        self.master.attributes('-alpha',0.93)

        self.master['bg']="#6E4DB2"

        #variables para obtener o mostrar en el Entry

        self.video_Link = StringVar()

        self.download_Path = StringVar()

        self.img_mini = StringVar()

        def resolucion():         
            
            self.itery = 0

            self.iterx = 4

            self.var = StringVar()
    
            for stream in self.mostrar.streams.filter(progressive=True, type='video', subtype='mp4'):
                
                self.resultado_res = str(stream.resolution) + str(stream.fps)
                
                self.proper = str(stream.resolution)
                                    
                self.radio = Radiobutton(self.master, text = self.resultado_res, bg = "#6B4DB2", fg = "#000000", font = "Helvetica 10 bold", variable = self.var, value = self.proper, command= mos_text_actualizado)
                
                if self.itery <= 2 :
                
                    self.radio.grid(row = self.iterx, column = self.itery, pady = 5, padx = 7, sticky ='nsew')
                                    
                    self.itery += 1

                else:
                    
                    self.itery = 0    

                    self.iterx += 1    

        #buscar video y mostrar en label y text
        def mos_text_actualizado():

            self.showvideo.delete("1.0","end")

            self.url_link = self.video_Link.get()

            self.mostrar = YouTube("\'"+self.url_link+"\'")

            self.titulo = "Titulo : " + str(self.mostrar.title) + "\n"
                
            self.duracion = "Duracion: " + str("{:.2f}".format(self.mostrar.length / 60.00)) + " min" + "\n"

            self.tamaño_video = self.mostrar.streams.filter(resolution = self.var.get()).first()                            
                
            self.peso_video = 'FileSize : ' + str(round(self.tamaño_video.filesize/(1024*1024))) + 'MB' + "\n"

            self.showvideo.insert(END, self.titulo + self.duracion + self.peso_video)


        def search():  
    
            self.showvideo.delete("1.0","end")        

            try:

                self.url_link = self.video_Link.get()

                self.mostrar = YouTube("\'"+self.url_link+"\'")

                self.titulo = "Titulo : " + str(self.mostrar.title) + "\n"
                
                self.duracion = "Duracion: " + str("{:.2f}".format(self.mostrar.length / 60.00)) + " min" + "\n"

                self.showvideo.insert(END, self.titulo + self.duracion )
                
                self.imagen_des = str(self.mostrar.thumbnail_url)
        
                self.response = requests.get(self.imagen_des, stream=True)

                self.image_re = BytesIO(self.response.content)

                self.imagen_open = Image.open(self.image_re)

                self.imagen_open = self.imagen_open.resize((558, 200), Image.ANTIALIAS)
            
                self.imagen_ori = ImageTk.PhotoImage(self.imagen_open)

                self.showimagen = Label(self.master, bg="#6B4Dc2", image = self.imagen_ori)

                self.showimagen.grid(row=2, column=0,columnspan=3, pady=5, padx=7)
            
                resolucion()               

            except:
                
                messagebox.showinfo("Error","Link incorrecto ")

        #obtener direcion de guardado        
        def Browse():

            self.download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")

            #mostrar la direccion de donde se guardara
            self.download_Path.set(self.download_Directory) 
                
        def Download_Audio():

            if self.video_Link.get() == "":            

                messagebox.showinfo("ERROR", "LINK INVALIDED\n" )  

            else:

                #crear variable para almacenar la direcion url de youtube

                self.Youtube_link_audio = self.video_Link.get()

                #crear variable y almacenar la direccion de guardado

                if self.download_Path.get() == "":

                    messagebox.showinfo("ERROR", "DIRECCION DE CARPETA INVALIDED\n" )  

                else:
                    
                    self.download_Folder = self.download_Path.get()

                    #crear variable para almacenar video

                    self.get_Audio = YouTube(self.Youtube_link_audio)            

                    self.Audio_Stream = self.get_Audio.streams.filter(only_audio=True).first()

                    #llamando funcion de descarga de video 

                    self.Audio_Stream.download(self.download_Folder)

                    #llamando cuadrobox de informacion para cuando termine de descargar mas direccion de donde se guardo

                    messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + self.download_Folder)
    
    
        def show_progress_bar(stream=None, chunk=None, bytes_remaining=None):            

            self.progress_bar['value'] = 0

            self.percent_count = float("%.2f" %(100 - ( 100 * (bytes_remaining /self.MaxfileSize))))
        
            if self.percent_count <= 100:
                
                self.progress_bar['value'] = self.percent_count            

        def DownloadFile():
            
            self.getVideo.streams.filter(resolution = self.var.get()).first().download(self.Path_dow)


        def Download():
        
            if self.video_Link.get() == "" or self.download_Path.get() == "" or self.var.get() == "" :

                messagebox.showinfo("ERROR", "LINK INVALIDED \nOPTION RESOLUTION \nDIRECTION OF PATH INVALIDED \n" )

            else:    
                self.Path_dow = self.download_Path.get()
            
                self.getVideo = YouTube(self.video_Link.get()) 
            
                self.video_type = self.getVideo.streams.filter(resolution = self.var.get()).first() 
            
                self.MaxfileSize = self.video_type.filesize
            
                Thread(target = self.getVideo.register_on_progress_callback(show_progress_bar)).start()

                Thread(target = DownloadFile).start() 
            
        #Titulo

        self.encabezado= Label(self.master, text="Descargas de videos de Youtube", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 20 bold" )

        self.encabezado.grid(row=0,column=0, columnspan=3 , pady=5, padx=7, sticky='nsew')

        # creacion de buttons , label, Entry y mostrar

        self.link_label = Label(self.master, text="YouTube link  :", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold")
        
        self.linkText = Entry(self.master, width=50,bg="#E4D6D5", textvariable=self.video_Link,)

        self.search= Button(self.master, text="Search", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold", command = search )


        self.link_label.grid(row=1, column=0, pady=5, padx=7, sticky='nsew')

        self.linkText.grid(row=1, column=1, pady=5, padx=7, sticky='nsew' )   

        self.search.grid(row=1, column=2, pady=5, padx=7, sticky='nsew')


        self.showvideo = Text(self.master, wrap=CHAR,bd=0, bg="#6B4DB2",fg="#000000",font = "Helvetica 10 bold", height=5)     
    
        self.showvideo.grid(row=3, column=0,columnspan=3, pady=5, padx=7, sticky='nsew')
    
    
        self.destination_label = Label(self.master, text="Destination    :", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold")

        self.destinationText = Entry(self.master, width=50,bg="#E4D6D5", textvariable=self.download_Path)

        self.browse_B = Button(self.master,text="Browse", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold", command=Browse)

        self.elige = Label(self.master, text="Elige que descargar: ",bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold")

        self.Download_B = Button(self.master, text="Download Video", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold",command=Download)
        
        self.Download_A = Button(self.master, text="Audio mp4 ", bg="#91B24D",fg="#FFFFFF", font = "Helvetica 10 bold",command=Download_Audio)

        self.progress_bar = Progressbar(self.master, orient = HORIZONTAL, mode  = "determinate", length= 560 )


        self.destination_label.grid(row=10, column=0, pady=5, padx=7, sticky='nsew')
        
        self.destinationText.grid(row=10, column=1, pady=5, padx=7, sticky='nsew')

        self.browse_B.grid(row=10, column=2, pady=5, padx=7, sticky='nsew' )

        self.elige.grid(row=11, column=0, pady=5, padx=7, sticky='nsew')
    
        self.Download_B.grid(row=11, column=1, pady=5, padx=7, sticky='ne')
        
        self.Download_A.grid(row=11, column=2, pady=5, padx=7, sticky='nsew')
        
        self.progress_bar.grid(row=12, column=0, columnspan=3, pady=5, padx=7)

def main():

    root = Tk()

    app = Window_w(root)

    root.mainloop()

if __name__ == '__main__':
    main()
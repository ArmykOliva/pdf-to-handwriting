import os,pdfkit
from random import choice,randrange
from bs4 import BeautifulSoup
from unidecode import unidecode
from pypandoc import convert_file

def pdf_to_html(fonts,skakavost,rotace_pismen,width_shift,height_shift,rotace):
    #change all the html files
    for filee in os.listdir("data\\converted\\pdf"):
        filee_converted = "data\\converted\\pdf\\" + filee
        filee_dest = "data\\done\\" + filee
        #find text and change it
        with open(filee_converted,"r",encoding="utf-8") as f:
            result = f.read()
            whole_file = BeautifulSoup(result,"html.parser")
            schulubung = whole_file.find("div",attrs={"id" : "page-container"})
            #najit pages
            for data in schulubung.children:
                #page cislo
                if (data.name == "div"):
                    #najit jenom page
                    this_page = False
                    for page in data.children:
                        if (page.name == "div"): #jenom ten spravnej text
                            #for loop mezi divs
                            for bad_div in page.children:
                                for divs in bad_div.children:
                                    if (divs.name == "div"):
                                        divs["style"] = "margin:0px 0px {1}px {0}px;transform:rotate({2}deg);".format(randrange(width_shift[0],width_shift[1]),randrange(height_shift[0],height_shift[1]),randrange(rotace[0],rotace[1]))
                                        #loop v divu a randomize fontu
                                        line = divs.decode_contents()
                                        res = ""
                                        i = 0
                                        while i < len(line):
                                            if (line[i:i + 1] == " "):
                                                res += line[i:i + 1]
                                            elif (unidecode(line[i:i + 1]) == unidecode("")):
                                                res += " "
                                            elif (line[i:i + 5] == "<span" or line[i:i + 6] == "</span"):
                                                while line[i:i + 1] != ">":
                                                    res += line[i:i + 1]
                                                    i += 1
                                                res += ">"
                                            else:
                                                word = ["<span style='margin-top:10px;font-family:{0};color:#000F55;position:relative;top:{1}px;font-size:40%;transform:skewY({2}deg)'>".format(choice(fonts),randrange(skakavost[0],skakavost[1]),randrange(rotace_pismen[0],rotace_pismen[1])),"</span>"]
                                                res += word[0] + line[i:i + 1] + word[1]
                                            i += 1
                                        divs.string = res
                        this_page = not this_page
            

        #write new file
        with open(filee_dest,"w",encoding="utf-8") as f:
            whole_file = str(whole_file).replace("&lt;","<")
            whole_file = whole_file.replace("&gt;",">")
            f.write(str(whole_file))
            print("done")

def docx_to_html(fonts,skakavost,rotace_pismen,width_shift,height_shift,rotace):
    #change all the html files
    for filee in os.listdir("data\\converted\\docx"):
        filee_converted = "data\\converted\\docx\\" + filee
        filee_dest = "data\\done\\" + filee
        #find text and change it
        with open(filee_converted,"r",encoding="utf-8") as f:
            result = f.read()
            result = result.replace("<em>","")
            result = result.replace("</em>","")
            result = result.replace("<strong>","")
            result = result.replace("</strong>","")
            result = result.replace("<li>","<p>")
            result = result.replace("</li>","</p>")
            soup = BeautifulSoup(result,"html.parser")

            #align on line paper
            soup.append(soup.new_tag('style', type='text/css'))
            soup.style.append('body{margin-left:3cm; line-height:6.83mm; color:red;} p{margin:0px;}') #1.25inch nahore offset v chrome

            #style pismenka
            for p in soup.find_all("p"):
                p["style"] = "margin:0px 0px {1}px {0}px;transform:rotate({2}deg);".format(randrange(width_shift[0],width_shift[1]),0,randrange(rotace[0],rotace[1]))
                #randomize pismenka
                line = p.decode_contents()
                res = ""
                i = 0
                while i < len(line):
                    if (line[i:i + 1] == " "):
                        res += line[i:i + 1]
                    elif (unidecode(line[i:i + 1]) == unidecode("")):
                        res += " "
                    elif (line[i:i + 5] == "<span" or line[i:i + 6] == "</span"):
                        while line[i:i + 1] != ">":
                            res += line[i:i + 1]
                            i += 1
                        res += ">"
                    else:
                        word = ["<span style='font-family:{0};color:#000F55;top:{1}px;font-size:200%;transform:skewY({2}deg)'>".format(choice(fonts),randrange(skakavost[0],skakavost[1]),randrange(rotace_pismen[0],rotace_pismen[1])),"</span>"]
                        res += word[0] + line[i:i + 1] + word[1]
                    i += 1
                p.string = res

            
            

        #write new file
        with open(filee_dest,"w",encoding="utf-8") as f:
            soup = str(soup).replace("&lt;","<")
            soup = soup.replace("&gt;",">")
            f.write(str(soup))
            print("done")

        
if __name__ == "__main__":
    #pypandoc
    #from pypandoc.pandoc_download import download_pandoc
    #download_pandoc()

    #init
    #fonts = ["Krystof1","Krystof2","Krystof3"]
    #fonts = ["Anci2"]
    fonts = ["Hauz1","Hauz2"]
    sesit = [""]
    sesitID = 0
    skakavost = [0,1]
    rotace_pismen = [-2,2]
    width_shift = [0,10]
    height_shift = [0,1]
    rotace = [0,1]


    #converter
    slozka = "data"
    for filee in os.listdir(slozka):
        filename, file_extension = os.path.splitext(filee)
        file_extension = file_extension[1:]

        #sebrat jen files
        if (file_extension != ""):
            filee_converted = "{}\\converted\\{}\\{}.html".format(slozka,file_extension,filename)
            if (not os.path.exists(filee_converted)):
                if (file_extension == "pdf"):
                    config = "--zoom 1.3 --dest-dir data\\converted\\pdf data\\%s" % filee
                    os.system("pdf2htmlEX-win32-0.14.6-with-poppler-data\\pdf2htmlEX.exe "+str(config))
                elif (file_extension == "docx"):
                    print("data\\converted\\docx\\%s" % filee)
                    convert_file("data\\%s" % filee,"html",outputfile=filee_converted)
    
    #convert do naseho pisma
    pdf_to_html(fonts,skakavost,rotace_pismen,width_shift,height_shift,rotace)
    docx_to_html(fonts,skakavost,rotace_pismen,width_shift,height_shift,rotace)
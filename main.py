import urllib
from urllib.request import Request, urlopen
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from urllib.parse import unquote
from bs4 import BeautifulSoup
import os
from bs4.dammit import EntitySubstitution
import html
def fixBeuty(str):
    fix =""
    fix=str.replace("&amp;apos","\'")
    fix=str.replace("&#x27;&#x27;","\"")
    fix=str.replace('\xa0', ' ')
    return fix
def custom_formatter(string):
    """add &quot; and &apos; to entity substitution"""
    return EntitySubstitution.substitute_html(string).replace('"','&quot;').replace("'",'&apos;')

url = "https://www.wattpad.com/story/150327676-d-chistes-d"
url = unquote(url)

url = url+"/parts"
nombreAutora = ""
nombreHistoria =""


def leerHtml(archivo,root=""):
    f = open(root+archivo,'r')
    mensaje = f.read()
    f.close()

    return mensaje


def encontrarEtiqueta(etiqueta,str):
    newStr= str

def deleteN (str):
    strNew="a"
    for i in range(str.length):
        if(true):
            print("xd")

    return strNew

def crearArchivo(archivo,str,root=""):
    f = open(root+archivo,'w')
    f.write(str)
    f.close()

def descargarPagina(urlto,output="reciensalidodelhornopapu.html",root=""):
    try:
        url = urlto

        # now, with the below headers, we defined ourselves as a simpleton who is
        # still using internet explorer.
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read().decode('utf-8')

        saveFile = open(root+output,'w')
        saveFile.write(str(respData))

        saveFile.close()
    except Exception as e:
        print(str(e))





def capturarDatosIniciales(url):
    nautora = "autora"
    nhistoria = "historia"
    ndescription = "descripcion"
    ##Buscar el nombre de la historia
    comienzo = url.find("-")

    nhistoria = url[(comienzo):(len(url))]
    nhistoria = nhistoria.replace("/parts","")
    nhistoria = nhistoria.split("-")
    aux = nhistoria
    for item in range(len(nhistoria)):
        if(item == 0):
            nhistoria = ""

        nhistoria = nhistoria +aux[item].capitalize() +" "

    nhistoria = nhistoria[1:len(nhistoria)]

    #buscar autora
    descargarPagina(url,"nautora.html")
    nautora = leerHtml("nautora.html")
    comienzo = nautora.find("<a class=\"send-author-event on-navigate\"")
    nautora = nautora[comienzo:(comienzo+111)]
    comienzo = nautora.find(">")
    nautora = nautora[comienzo+1:(comienzo+111)]
    final = nautora.find("<")
    nautora = nautora[0:final]
    #
    nautora=BeautifulSoup(nautora,features="html.parser").__str__()
    #Fixes
    nautora=fixBeuty(nautora)
    #
    #buscar historia
    #buscar autora
    descargarPagina(url,"nautora.html")
    ndescription = leerHtml("nautora.html")
    comienzo = ndescription.find("<pre>")+5
    final = ndescription.find("</pre>")
    ndescription = ndescription[comienzo:final]

    ndescription = ndescription[0:final]
    #
    ndescription=BeautifulSoup(nautora,features="html.parser").__str__()
    #Fixes
    ndescription=fixBeuty(ndescription)
    #
    #os.remove("nautora.html")


    return [nautora,nhistoria,ndescription]



def extrarInfoEtiqueta(str):

    strContainer = str
    listContains = []
    tagContain = ""
    i = 0
    #Do loops to finish the listContains
    while(True):
        try:
            if(strContainer[0] == " "):
                strContainer = strContainer[1:len(strContainer)]

        except:
            print("lol")


        tagFinal = strContainer.find(">")


        tagInitial = strContainer.find("<")

        tagSpaceNearly = strContainer.find(" ")

        #print(tagFinal.__str__())
        #print(tagSpaceNearly.__str__())
        if(tagFinal < tagSpaceNearly and tagSpaceNearly != -1):
            #print("ROjo")
            tagName = strContainer[(tagInitial+1):tagFinal]

        if(tagFinal > tagSpaceNearly and tagSpaceNearly != -1):
            #print("VERDE")
            tagName = strContainer[(tagInitial+1):tagSpaceNearly]

        else:
            #print("aanar")
            tagName = strContainer[(tagInitial+1):tagFinal]
        #print("el tag is:" +tagName)
        #Set pos of tagName
        tagNameOpen = "<"+tagName+">"
        tagNameInit = tagInitial

        #Search the pos final

        tagNameClose = "</"+tagName+">"
        tagNameFinal = strContainer.find(tagNameClose)
        #print("the tag close is "+tagNameClose)

        #Then, show the result

        tagContain = strContainer[(tagFinal+1):(tagNameFinal)]
        #
        listContains.append(tagContain)
        #print("the tag CONTAIN is "+listContains[i])
        strContainer = strContainer[(tagNameFinal+len(tagNameClose)):len(strContainer)]
        #print("str cont"+strContainer)
        if( strContainer == "" ):
            break
        i = i+1

    return listContains

def extraerLink(str):
    strContainer = str
    listContains = []
    tagContain = ""
    i = 0
    #Do loops to finish the listContains
    while(True):
        if(strContainer[0] == " "):
            strContainer = strContainer[1:len(strContainer)]


        hrefInitial = strContainer.find("href=\"")

        hrefFinal = strContainer.find("\"",hrefInitial+len("href=\""))

        hrefContain = strContainer[(hrefInitial+len("href=\"")):(hrefFinal)]
        #contain of hrefFinal
        #print("The href actuallity is \""+hrefContain+"\"")
        listContains.append(hrefContain)
        #print("the href  CONTAIN is "+listContains[i])
        strContainer = strContainer[hrefFinal+1:len(strContainer)]
        #print("str cont"+strContainer)
        if( strContainer.find("href=\"") == -1 ):
            break
        i = i+1

    return listContains

def detectarVacio(str):
    if(str.find("<pre></pre>") == -1):
        return True#No existe esa etiqueta, por lo tanto hay texto
    else:
        return False #No hay texto
def descargarTodasLasPaginasYCapturarInfo(hrefList):
    #First Bucle The Capitule
    bookFinal =[]
    for item in range(len(hrefList)):
        capFinal=[]
        i = 1
        while True:

            if(i == 1):
                url=hrefList[item]
                name=item.__str__()+"-"+ i.__str__()
                descargarPagina(url,name,"paginasHtml/")
            else:
                url=hrefList[item]+"/page/"+i.__str__()
                name=item.__str__()+"-"+ i.__str__()
                descargarPagina(url,name,"paginasHtml/")

            if(detectarVacio(leerHtml("paginasHtml/"+name)) == False):
                os.remove("paginasHtml/"+name)
                break
            auxPage = leerHtml("paginasHtml/"+name)
            #Select the <pre>
            begin = auxPage.find("<pre>")+5
            final =  auxPage.find("</pre>")

            auxPage = auxPage[begin:final]

            auxPage=BeautifulSoup(auxPage,features="html.parser").__str__()
            #Fixes
            auxPage= html.unescape(auxPage)
            auxPage= auxPage.replace('\n','')
            auxPage= auxPage.replace('</br>','')
            auxPage= auxPage.replace('<b>','')
            auxPage= auxPage.replace('</b>','')
            auxPage=fixBeuty(auxPage)

            auxListContain = extrarInfoEtiqueta(auxPage)

            i = i+1
            capFinal.append(auxListContain)
        bookFinal = bookFinal.replace('&apos','\'')
        bookFinal.append(capFinal)

    return bookFinal



def buscarTabla(url):
    #Downloading first
    descargarPagina(url,"tabla_de_contenido.txt")

    #Capture Downleaded
    mensaje = leerHtml("tabla_de_contenido.txt")

    #Localizar la tabla <ul>
    comienza=mensaje.find("<ul class=\"table-of-contents\">")

    final = mensaje.find("</ul>",comienza)

    mensaje2 = mensaje[(comienza+30):final]
    #Borrar "\n"
    mensaje2= mensaje2.replace('\n','')
    mensaje2= html.unescape(mensaje2).__str__()
    #Fixes
    mensaje2=fixBeuty(mensaje2)
    crearArchivo("tabla_de_contenido.txt",mensaje2)


    #Is extracting in list
    l = extrarInfoEtiqueta(mensaje2)
    listOfContent = []
    for item in range(len(l)):
        listOfContent.append(extrarInfoEtiqueta(l[item])[0])

        #print("EUUUUU"+listOfContent[item])
    listOfContent=listOfContent[0:(len(listOfContent)-1)]
    return listOfContent



def buscarHref(url):
        #Downloading first
        descargarPagina(url,"tabla_de_contenido.txt")

        #Capture Downleaded
        mensaje = leerHtml("tabla_de_contenido.txt")

        #Localizar la tabla <ul>
        comienza=mensaje.find("<ul class=\"table-of-contents\">")

        final = mensaje.find("</ul>",comienza)

        mensaje2 = mensaje[(comienza+30):final]
        #Borrar "\n"
        mensaje2= mensaje2.replace('\n','')
        mensaje2=BeautifulSoup(mensaje2,features="html.parser").__str__()
        #Fixes
        mensaje2=fixBeuty(mensaje2)

        hrefList = extraerLink(mensaje2)

        for item in range(len(hrefList)):
            hrefList[item] = "https://www.wattpad.com"+hrefList[item]
            #print("EUUUUU"+hrefList[item])
        #print(hrefList)
        #print(listOfContent)
        os.remove("tabla_de_contenido.txt")
        return hrefList
#Recoleccion de datos
nombreAutora = capturarDatosIniciales(url)[0]
nombreHistoria =capturarDatosIniciales(url)[1]
nombredescription =capturarDatosIniciales(url)[2]
hrefList =buscarHref(url)
listOfContent = buscarTabla(url)
#Crear PDF
doc = SimpleDocTemplate(nombreHistoria+".pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
Story=[] #Texto Final

photo = "1.jpg"

title = "titulo"

book = descargarTodasLasPaginasYCapturarInfo(hrefList)

#photo
im = Image(photo, width=456.0, height=690.0 )
Story.append(im)


styles=getSampleStyleSheet()

styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY)) #Definir la orientacion


Story.append(PageBreak())
for i in range(len(book)):
    for a in range(len(book[i])):
        capitulo = book[i]
        ptext = '<font size=22>'+listOfContent[a]+'</font>'    #Para definir el tamaño
        Story.append(Paragraph(ptext, styles["Normal"])) #Para colocar el texto
        Story.append(Spacer(1, 25)) #Espacio entre texto
        for b in range(len(capitulo[a])):
            parrafo = capitulo[a]
            ptext = '<font size=12>'+parrafo[b].__str__()+'</font>'
            Story.append(Paragraph(ptext, styles["Normal"]))

        Story.append(Spacer(1, 25)) #Espacio entre texto
ptext = '<font size=12>'+"str"+'</font>'
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))


ptext = '<font size=12>Gracias a Ramiro Alex Flores Santa Cruz.</font>'
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
doc.build(Story)#Con la historia se hace el pdf

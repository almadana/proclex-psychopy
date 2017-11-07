# -*- coding: utf-8 -*-

#EXPERIMENTO N1 SEMANTIC


#"trial"=cond

from __future__  import division
from psychopy import visual, core, event, gui, data
import numpy as ny
import os

#from ctypes import windll

#Puerto paralelo para trigger
#trig= windll.inpout32


#            FUNCIÓN PARA CREAR 4 bloques         

# parte estimulos en bloques, manteniendo balanceado la proporción entre conImagen y sinImagen
# randomiza el orden de items
def getTrialList(itemImagen,itemNoImagen,nBloques):
    nItemsImagen=len(itemImagen)
    nItemsNoImagen=len(itemNoImagen)
    tamMinImagenBloque=int(ny.floor(nItemsImagen/float(nBloques)))
    tamMinNoImagenBloque=int(ny.floor(nItemsNoImagen/float(nBloques)))
    
    
    #randomizo
    itemImagen=list(ny.random.permutation(itemImagen))
    itemNoImagen=list(ny.random.permutation(itemNoImagen))
    
    #reparto items en bloques
    bloques=[]
    for nBloque in range(nBloques):
        #agrego 
        print "NBLOQ"
        print nBloque
        print tamMinImagenBloque
        esteBloque= itemImagen[nBloque*tamMinImagenBloque:(nBloque+1)*tamMinImagenBloque]  
        esteBloque.extend( itemNoImagen[nBloque*tamMinNoImagenBloque:(nBloque+1)*tamMinNoImagenBloque] )
        esteBloque=list(ny.random.permutation(esteBloque))
        bloques.append(esteBloque)
        print "BLOQUEEE::" + str(esteBloque[0])
    print bloques[0]
    return(bloques)


def presentarEstimulo(words,mywin):
    for nFrames in range(60): #tiempo de presentacion de cada palabra, a 60 Hz es 300 ms. Cada frame dura 0.01666 seg, si presento cada palabra por60 frames, cada palabra se presenta durante 1000 ms aprox
        words.draw()
        recuadro.draw()
        mywin.flip()


def presentarImagen(estimuloImagen,mwin):
        #        GENERAR ISI
    ISI= ny.random.randint(20,30)
#    for nFrames in range(ISI): #tendria que se random entre 1250 y 1500 x ej
#        mywin.flip()

    mywin.flip()
    for nFrames in range(90): #(60):
        estimuloImagen.draw()
        mywin.flip()
    #        GENERAR ISI
    ISI= ny.random.randint(60,80)
    for nFrames in range(ISI): #tendria que se random entre 1250 y 1500 x ej
        mywin.flip()

def getResp(esTarget,contesta):
    teclaSi="l"
    teclaNo="s"
    if contesta:
        contesta=contesta[0] # tomo el primer keypress
        #Tomo la respuesta
        if contesta[0]==teclaSi:
            if esTarget:
                resp,tResp=('1',contesta[1])     #no contesta y no es targetº
            else:
                resp,tResp=('0',contesta[1])     #no contesta y no es targetº
            
        elif contesta[0]==teclaNo:
            if not esTarget:
                resp,tResp=('1',contesta[1])     #no contesta y no es t
            else:
                resp,tResp=('0',contesta[1])     #no contesta y no es targetº
    else:
        resp,tResp=('NA','NA')
    print resp
    print tResp
    return(resp,tResp)

        
#    if not contesta and esTarget:
#        resp,tResp=('0','NA')    #no contesta y es target
#        print tResp
#        
#    if contesta and esTarget:
#        resp,tResp=('1',contesta[1])    #contesta y es target
#        print resp
#        print tResp
#         
#    if contesta and not esTarget:
#        resp,tResp=('0',contesta[1])    #conesta y no es target
#        print resp
#        print tResp
#    return(resp,tResp)




def loopEstimulo(mywin,block,trialClock,fixation,estimuloTexto,salida,ensayo,estimuloImagen):
    extension=".png"
    for item in block:
        print "ESTE ES EL ITEM COMPLETO"
        print item
        ensayo=ensayo+1
        # ESTE ES EL NUMERO DE ENSAYO
        print ensayo
        
        # function sendTrigger()
        ##código de trigger (
    #    trigCode=0
    #    if item[3]=='1.1': trigCode=10 #palabra
    #    elif item[3]=='1.2': trigCode=11 #palabra target
    #    elif item[3]=='1.3': trigCode=20 #pseudopalabra
    #    elif item[3]=='1.4': trigCode=21 #pseudopalabra target
    #    elif item[3]=='2.1': trigCode=30 #false font
    #    elif item[3]=='2.2': trigCode=31 #false font target

    #
    #    print 'trigCode'
    #    print trigCode
        
        
        #cruz de fijaciòn, 1 segundo
#        fixation.draw()
#        mywin.flip()
#        core.wait(1)
        
        #preparo estímulo
        estimulo = item[ncolItem]
        # Print EL ESTIMULO
        print estimulo
        tt = estimulo.decode('utf-8')  #tiene que transformarse de utf-8
        estimuloTexto.setText(tt)
        #imagen estimuloImagen
        # presento estimulo
        presentarEstimulo(estimuloTexto,mywin)
        # si hay imagen
        if item[ncolImagen]=="1":
            estimuloImagen.setImage(pathImagen+item[ncolArchivoImagen]+extension)
            trialClock.reset()
            event.clearEvents()
            presentarImagen(estimuloImagen,mywin)
            b=event.getKeys(keyList=['s','l'] , timeStamped=trialClock) #buscar opcion xa q se quede con el primer tr
            print 'va b'
            resp,tResp = getResp(int(item[ncolCongruencia]),b) # ojo que item[2]  està como string, lo convierto a entero para que el if quede más lindo
        else:
            resp="NA"
            tResp="NA"
#                 SALIDA                                             
        salida.write(item[0]+','+item[1]+','+item[2]+','+item[3]+','+item[4]+','+item[5]+','+item[6]+','+item[7]+','+resp+','+ str(tResp)+"\n")
        #        GENERAR ISI
        ISI= ny.random.randint(60,90)
        for nFrames in range(ISI): #tendria que se random entre 1250 y 1500 x ej
            recuadro.draw()
            mywin.flip()


def meterPausa(mywin,pausaTexto1,pausaTexto2):
    mywin.flip()
    pausaTexto1.draw()
    mywin.flip()
    core.wait(3) # pausa obligatoria
    event.waitKeys()
    mywin.flip()
    pausaTexto2.draw()
    mywin.flip()
    core.wait(1)
    event.waitKeys()
    mywin.flip()
    core.wait(1)
    
    
    
# ----------------- PRESETS --------------

#           Info del experimento
expInfo={'condicion':['practica','expe'],'experimentador':'LF', 'sujeto':'000000'}
expInfo['fecha']=data.getDateStr()
dial = gui.DlgFromDict(expInfo,title='N1_semantic',fixed=['fecha','LF'])

#           VENTANA
x=1024; y=768#defino tamano del monitor  

mywin = visual.Window(fullscr=False,size=[x,y],allowGUI=True, monitor="testMonitor", units="deg",color=[-0.2,-0.2,-0.2], screen=0)
mywin.setMouseVisible(False)

#trig.Out32(0x378,0)    

fps=mywin.getActualFrameRate()
print "-------------\nFrame Rate: "+str(fps)+"\n------------"
if fps!=None:
    frameDur = 1.0/round(fps)
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess


#archivos = 
archivos={"expe":"estimulos_task2_posta.csv","practica":"practica_task2.csv"}
pathImagenes={"expe":"imagenes task2/","practica":"imagenes practica/"}
pathImagen=pathImagenes[expInfo['condicion']]  # levanto directorio de imagenes
#abro archivo de estimulos
archivoEstimulos=open(archivos[expInfo['condicion']])

########DEFINIR NUMERO DE COLUMNA QUE TIENE INFO #####
ncolItem=2
ncolCongruencia=6
ncolArchivoImagen=7
ncolImagen=5

# la idea es separar los items entre los que llevan imagen y los que no, para balancearlo dentro de cada bloque
itemNoImagen=[]
itemImagen=[]

for l in archivoEstimulos:
    l=l.strip()
    f=l.split(',')
    #num_item,item,tipo_estim,cod_tipo_estim,tipo_pal,frec,frec_ac,num_caract,estr,imagen,congruencia = f
    imagen=f[5]
    print "ES IMAGeN?"
    print imagen
    if imagen=="1":
        print "Es imagen!"
        itemImagen.append(tuple(f))
    elif imagen=="0": #el header "imagen" no es ni 1 ni 0 entonces no lo pesco :)
        print "NO Es imagen!"
        itemNoImagen.append(tuple(f))


if expInfo['condicion']=='practica':
    nBloques=1
else:
    nBloques=4
bloques=getTrialList(itemImagen,itemNoImagen,nBloques)

print 'EMPIEZA EL EXPERIMENTO'

#OUTPUT
path=os.getcwd()
if not os.path.exists('salida N1_semantic'):
    os.makedirs('salida N1_semantic')
nombreArch=expInfo['experimentador']+'_N1_semantic_prueba'+expInfo['sujeto']+'_'+expInfo['fecha']
archivoOut=path+'\\salida N1_semantic\\'+nombreArch+'.csv' 
salida = open(archivoOut,'w')


 # test, itemOri,condExp,condCtx,subCondExp,prime,target,resp,tResp,lista
salida.write('num_item,item, tipoEstimulo, cod_tipoEstimulo, tipo_pal, frec, frec_ac, num_caract, estr, acierto,TR\n') #agregar tr y resp

# Estimulos graficos
#########################3
#Punto de fijacion
fixation = visual.ShapeStim(mywin, 
                lineColor='black', 
                lineWidth=1.0, 
                vertices=((-0.4, 0), (0.4, 0), (0,0), (0,0.4), (0,-0.4)), 
                closeShape=False, 
                pos= [0,0])  
# Recuadro----
recuadro=visual.Rect(mywin,lineWidth=1.0,lineColor='black',pos=(0,0), height=2,width=5)
#Palabras
estimuloTexto=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])
#imagen
estimuloImagen=visual.ImageStim(win=mywin,pos=[0,0])
# Texto intermedio
pausaTexto1=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])
pausaTexto1.setText("BIen! es hora de hacer un descansoo...!!!")
pausaTexto2=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])
pausaTexto2.setText("Seguimos..!!!... Presiona cualquier tecla para continuar")


# --------------COMIENZA RUTINA-----------



globalClock = core.Clock()
trialClock = core.Clock()

ensayo=0

#deberìan haber dos bloques, eso es lo que devuelve getTrialList()...
for nBloque,bloque in enumerate(bloques):
    if nBloque>0:
        meterPausa(mywin,pausaTexto1,pausaTexto2)
    loopEstimulo(mywin,bloque,trialClock,fixation,estimuloTexto,salida,ensayo,estimuloImagen)
 

mywin.close()
salida.close()
core.quit()
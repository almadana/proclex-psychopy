# -*- coding: utf-8 -*-

#EXPERIMENTO ONE-BACK REPETTION (Réplica Maurer 2015)


#"trial"=cond

from __future__  import division
from psychopy import visual, core, event, gui, data
import numpy as ny
import os

#from ctypes import windll

#Puerto paralelo para trigger
#trig= windll.inpout32


#            FUNCIÓN PARA CREAR LISTAS CON REPETICIONES ALEATORIAS         


# esta función toma de entrada una lista de items (como en "palabras_provisorio.csv")  y crea:
# A- 1 trial por item
# B_ nReps trials extra, repitiendo los items
# C_ randomiza orden, dejando margen al principio y al final sin repetidos
# D_ los repetidos van juntos :) (ej: cara cara nariz payaso boca mia mia)
# E_ Dos bloques 
nReps=20
def getTrialList(itemList,nReps):
    #flankers al principio y al final, que no se van a repetir
    flankers=3
    # condicion de stop
    if nReps+4*flankers+2>len(itemList):
        return(None)
    #for nItem,item,cond_target,bloque,e,f,g,h,i,j in itemList:
    #creo lista permutada
    trialList=list(  ny.random.permutation(itemList)   )
    # partir a la mitad itemList
    #cuanto es la mitad?
    mitaditemList=int(round(len(itemList)/2.0)) #la mitad    
   
    # partir a la mitad nReps
    #cuanto es la mitad?
    mitad1nReps=int(round(nReps/2.0)) #la mitad
    mitad2nReps=nReps-mitad1nReps # la otra mitad


    #vamos a generar dos bloques
    block1 = trialList[:mitaditemList]
    block2 = trialList[mitaditemList:]
           
    #vamos a elegir los indices de los repetidos, dejando flankers
    permItemList1=ny.random.permutation(range(flankers,len(block1)-flankers))
    permItemList2=ny.random.permutation(range(flankers,len(block2)-flankers))
    # son los primeros "12" de la permutaciòn, en orden de menor amayor
    itemsARepetir1=ny.array(sorted(permItemList1[range(mitad1nReps)]))
    itemsARepetir2=ny.array(sorted(permItemList2[range(mitad2nReps)]))
    #donde van a ir al final, antes de aleatorizar
    print block1
    itemsARepetir1a=itemsARepetir1 +  ny.arange(len(itemsARepetir1))
    itemsARepetir2a=itemsARepetir2 +  ny.arange(len(itemsARepetir2))
    posAInsertar1=itemsARepetir1a + 1
    posAInsertar2=itemsARepetir2a + 1
    
    
    print itemsARepetir1, block1[itemsARepetir1[0]+flankers] , block1[itemsARepetir1[1]+flankers]
    for indice,posicion in enumerate(posAInsertar1):
        nuevoTrial = tuple(block1[itemsARepetir1a[indice]+flankers])
        nItem,base,item,cond_target,bloque,e = nuevoTrial
        nuevoTrial = (nItem,base,item,'1',bloque,e)
        # en la posicion posAInsertar, inserto el item numero itemsARepetir[indice] de la lista
        print "insertandoooo"
        block1.insert(flankers+posicion,nuevoTrial)
    for indice,posicion in enumerate(posAInsertar2):
    # en la posicion posAInsertar, inserto el item numero itemsARepetir[indice] de la lista
        nuevoTrial = tuple(block2[itemsARepetir2a[indice]+flankers])
        nItem,base,item,cond_target,bloque,e  = nuevoTrial
        nuevoTrial = (nItem,base,item,'1',bloque,e)
        block2.insert(flankers+posicion,nuevoTrial)
    print str(len(block1)) + " ---- " + str(len(block2))
    return([block1,block2])

def presentarEstimulo(words,recuadro,mywin):
    for nFrames in range(60): #Cada frame dura 0.01666 seg, si presento cada palabra por60 frames, cada palabra se presenta durante 1000 ms aprox
        words.draw()
        recuadro.draw()
        mywin.flip()
                
    #        GENERAR ISI
    ISI= ny.random.randint(60,80) #SERIA ENTREE 1000 ms a 1330 ms aprx
    print ISI
    for nFrames in range(ISI): #tendria que se random entre 1250 y 1500 x ej
        recuadro.draw()
        mywin.flip()

def getResp(esTarget,contesta):
    
    #Tomo la respuesta
    if not contesta and not esTarget:
        resp,tResp=('1','NA')     #no contesta y no es targetº
        print resp
        print tResp
        
    if not contesta and esTarget:
        resp,tResp=('0','NA')    #no contesta y es target
        print tResp
        
    if contesta and esTarget:
        resp,tResp=('1',contesta[1])    #contesta y es target
        print resp
        print tResp
         
    if contesta and not esTarget:
        resp,tResp=('0',contesta[1])    #conesta y no es target
        print resp
        print tResp
    return(resp,tResp)


def loopEstimulo(mywin,block,trialClock,fixation,estimuloTexto,salida,ensayo):
    #antes de empezar, dibujo el recuadro un par de segundos....
    mywin.flip()
    recuadro.draw()
    mywin.flip()
    core.wait(1)
    for item in block:
        
        print item
        ensayo=ensayo+1
        print ensayo
        
        
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
        
        
        #preparo estímulo
        estimulo = item[2]
        print estimulo
        tt = estimulo.decode('utf-8')  #tiene que transformarse de utf-8
        estimuloTexto.setText(tt)
        trialClock.reset()
        event.clearEvents()
        # presento estimulo
        presentarEstimulo(estimuloTexto,recuadro,mywin)
        # LEVANTAR KEYPRESSES
        b=event.getKeys(keyList=['space'] , timeStamped=trialClock) #buscar opcion xa q se quede con el primer tr
        print 'va b'
        if b: 
            b=b[0]
            print 'nuevo b'
            print b
             
    #		if co=2:          
    #		    trig.Out32(0x378,trigCode)    
    #		    event.clearEvents()
    #		if c=2:
    # 		trig.Out32(0x378,0) 
        #transformo item[2] en un número
        print "B... "+ str(b)
        print "item 2 " +  item[2]
        
        resp,tResp = getResp(int(item[3]),b) # ojo que item[2]  està como string, lo convierto a entero para que el if quede más lindo
        
       
        salida.write(item[0]+','+item[1]+','+item[2]+','+item[3]+','+item[4]+','+item[5]+','+resp+','+ str(tResp)+"\n")

def meterPausa(mywin,pausaTexto1,pausaTexto2):
    mywin.flip()
    pausaTexto1.draw()
    mywin.flip()
    core.wait(5) # pausa obligatoria
    event.waitKeys()
    mywin.flip()
    pausaTexto2.draw()
    mywin.flip()
    core.wait(2)
    event.waitKeys()
    mywin.flip()
    core.wait(2)
# ----------------- PRESETS --------------

#           Info del experimento
expInfo={'experimentador':'LF', 'sujeto':'000000','cond':['palabra','pseudopalabra','falsefont' ]}
expInfo['fecha']=data.getDateStr()
dial = gui.DlgFromDict(expInfo,title='one_back',fixed=['fecha','LF'])

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

# archivos de estímulos para cada condición
archivos = {'palabra':'palabras.csv','pseudopalabra':'pseudopalabras.csv','falsefont':'falsefont.csv'}
nombreArchivoEstimulos=archivos[expInfo['cond']]

#fuente para palabra y pseudo= arial, falsefont=BACS2sans
fuentes = {'palabra':'arial','pseudopalabra':'arial','falsefont':'BACS2sans'}
fuente=fuentes[expInfo['cond']]

#lista=open('palabras_provisorio.csv')      
#if expInfo['cond']=='pseudopalabra':
#lista=open('pseudopalabras_provisorio.csv'     y false (lo pongo las 3 veces y fue?)

#abro archivo de estimulos
archivoEstimulos=open(nombreArchivoEstimulos)
#lista vacia de items/estimulos

itemlist=[]

for l in archivoEstimulos:
    l=l.strip()
    f=l.split(',')
    itemlist.append(tuple(f))

#remueve header del archivo!!!
itemlist.pop(0)

#genero bloques
bloques=getTrialList(itemlist,nReps)


#---------------OUTPUT
path=os.getcwd()
if not os.path.exists('salida'):
    os.makedirs('salida')
nombreArch=expInfo['experimentador']+'_one_back_prueba_'+expInfo['sujeto']+'_'+expInfo['fecha']
archivoOut=path+'\\salida\\'+nombreArch+'.csv'
salida = open(archivoOut,'w')


salida.write('num_item,base,item,cond_target,bloque,cond_bloque,acierto,TR\n') 




################## Estimulos graficos
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
estimuloTexto=visual.TextStim(win=mywin, font=fuente, pos=[0,0],color=[-1,-1,-1])
if expInfo["cond"]=="falsefont":
    estimuloTexto.setHeight(1.8)
# Texto intermedio

textoIntermedio1=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])
textoIntermedio1.setText("BIen! es hora de hacer un descansoo...!!!")
textoIntermedio2=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])
textoIntermedio2.setText("Seguimos..!!!... Presiona cualquier tecla para continuar")






# --------------COMIENZA RUTINA-----------



globalClock = core.Clock()
trialClock = core.Clock()

ensayo=0

print 'EMPIEZA EL EXPERIMENTO'
#deberìan haber dos bloques, eso es lo que devuelve getTrialList()...
for bloque in bloques:
    loopEstimulo(mywin,bloque,trialClock,fixation,estimuloTexto,salida,ensayo)
    meterPausa(mywin,textoIntermedio1,textoIntermedio2)



mywin.close()
salida.close()
core.quit()

    

    # 'Palabra1,Palabra2,Pregunta,Nombre_condicion,Two_words,orden,Congruencia,Resp,tResp,Tecla,\n'
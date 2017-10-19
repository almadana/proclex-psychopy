# -*- coding: utf-8 -*-

#EXPERIMENTO ONE-BACK REPETTION (Réplica Maurer 2015)


#"trial"=cond

from __future__  import division
from psychopy import visual, core, event, gui, data, sound
import numpy as ny
import re
import os

from ctypes import windll

#Puerto paralelo para trigger
#trig= windll.inpout32


# esta función toma de entrada una lista de items (como en "palabras_provisorio.csv")  y crea:
# A- 1 trial por item
# B_ nReps trials extra, repitiendo los items
# C_ randomiza orden, dejando margen al principio y al final sin repetidos
# D_ los repetidos van juntos :) (ej: cara cara nariz payaso boca mia mia)
def getTrialList(itemList,nReps):
    #flankers al principio y al final, que no se van a repetir
    flankers=4
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
        # en la posicion posAInsertar, inserto el item numero itemsARepetir[indice] de la lista
        print "insertandoooo"
        block1.insert(flankers+posicion,block1[itemsARepetir1a[indice]+flankers])
    for indice,posicion in enumerate(posAInsertar2):
    # en la posicion posAInsertar, inserto el item numero itemsARepetir[indice] de la lista
        block2.insert(posicion+flankers,block2[itemsARepetir2a[indice]+flankers])
    print str(len(block1)) + " ---- " + str(len(block2))
    return((block1,block2))

# ----------------- PRESETS --------------

#Info del experimento
expInfo={'experimentador':'LF', 'sujeto':'000000','cond':['palabra','pseudopalabra','falsefont' ]}
expInfo['fecha']=data.getDateStr()
dial = gui.DlgFromDict(expInfo,title='one_back',fixed=['fecha','LF'])

#VENTANA
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
#INPUT. Ejecuto el script que me genera estimulos para cada sujeto de acuerdo al experimento a correr
# hacer esto

#if expInfo['cond']=='palabra':
#    execfile('Lista_palabras.py')#hay q hacerlo


lista=open('palabras_provisorio.csv')
itemlist=[]
expe=[]

globalClock = core.Clock()
trialClock = core.Clock()
allnightClock = core.Clock()


for l in lista:   
    l=l.strip()
    f=l.split(',')
    itemlist.append(tuple(f))
    #print expe
    


exp=getTrialList(itemlist)

fin=len(expe)  
print fin

print 'EMPIEZA EL EXPERIMENTO'

#OUTPUT
path=os.getcwd()
if not os.path.exists('salida'):
    os.makedirs('salida')
nombreArch=expInfo['experimentador']+'_one_back_prueba_'+expInfo['sujeto']+'_'+expInfo['fecha']
archivoOut=path+'\\salida\\'+nombreArch+'.csv'
salida = open(archivoOut,'w')


 # test, itemOri,condExp,condCtx,subCondExp,prime,target,resp,tResp,lista
salida.write('num_item,item,cond_target, bloque, tr,respuesta,acierto\n') #agregar tr y resp







#Punto de fijacion
fixation = visual.ShapeStim(mywin, 
                lineColor='black', 
                lineWidth=1.0, 
                vertices=((-0.4, 0), (0.4, 0), (0,0), (0,0.4), (0,-0.4)), 
                closeShape=False, 
                pos= [0,0])  
#Palabras
words=visual.TextStim(win=mywin, pos=[0,0],color=[-1,-1,-1])


# --------------COMIENZA RUTINA-----------



#Aparece punto de fijación
fixation.draw()
mywin.flip()
core.wait(1)



ensayo=0

for item in expe:
    
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
    
    
    fixation.draw()
    mywin.flip()
    core.wait(1)
    
    contador=0
    
    # Presentamos oracion palabra a palabra
    for word in item[1:2]:
        
	c=contador+1
    
        print word
        
        for nFrames in range(60): #tiempo de presentacion de cada palabra, a 60 Hz es 300 ms. Cada frame dura 0.01666 seg, si presento cada palabra por60 frames, cada palabra se presenta durante 1000 ms aprox
                if word:
                    tt=word.decode('utf-8')  #tiene que transformarse de utf-8
                    words.setText(tt)
                    words.draw()
                    mywin.flip()
                    
        b=event.getKeys(keyList=['space'] , timeStamped=trialClock) #buscar opcion xa q se quede con el primer tr
        print 'va b'
        if b: 
            b=b[0]
            print 'nuevo b'
            print b
             
#		if co=2:          
#		    trig.Out32(0x378,trigCode)    
#		    event.clearEvents()
        ISI= ny.random.randint(60,90)
        for nFrames in range(ISI): #tendria que se random entre 1250 y 1500 x ej
            mywin.flip()
#		if c=2:
# 		trig.Out32(0x378,0) 


    #Tomo la respuesta

        if not b and item[2]=='1':
            (resp,tResp)=['1','0']     #no contesta y no es targetº
            print resp
            print tResp
            
        if not b and item[2]=='1':
            (resp,tResp)=['0','0']    #no contesta y es target
            print tResp
            
        if b and item [2] =='1':
            (resp,tResp)=['1',b[1]]     #contesta y es target
            print resp
            print tResp
            
        if b and item [2] =='0':
            (resp,tResp)=['0',b[1]]    #conesta y no es target
            print resp
            print tResp
            

        
        
        salida.write(item[0]+','+item[1]+','+item[2]+','+item[3]+','+item[4]+','+item[5]+','+item[6]+','+item[7]+','+item[8]+','+item[9]+','+resp','+ "tResp"+"\n")
#    print 'Respuesta'
#    print laResp
#    print 'TR'
#    print tResp

mywin.close()
salida.close()
lista.close()
core.quit()

    

    # 'Palabra1,Palabra2,Pregunta,Nombre_condicion,Two_words,orden,Congruencia,Resp,tResp,Tecla,\n'


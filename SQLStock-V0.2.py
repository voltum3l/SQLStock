import sqlite3
import os
from os import remove
from os import path
from tkinter import *
from tkinter import messagebox



#------------------------------>>> FUNCIONES

def CreateBDD():
	if os.path.exists('StockSQL') == False:
		global stock
		stock=sqlite3.connect("StockSQL")
		cursor=stock.cursor()
		cursor.execute("CREATE TABLE Stock ('id' integer primary key autoincrement,marca varchar(50),precio integer,talle varchar(3),cantidad integer)")
		messagebox.showinfo("Informacion","Base de datos CREADA con exito")
	else:
		messagebox.showinfo("ERROR","La Base de datos YA EXISTE")
	CheckBars()

def ConnectToDatabase():
	if os.path.exists('StockSQL') == False:
		messagebox.showinfo("ERROR","La BDD no está creada")
	else:
		global connected
		connected = True
		global stock
		stock=sqlite3.connect("StockSQL")
		messagebox.showinfo("EXITO","Base de datos CONECTADA")
		CheckBars()

def IsBDDConnected():
	global connected
	if connected == True:
		return True
	else:
		messagebox.showinfo("ERROR","La BDD NO está conectada")
		return False

def LoadFromTxt():
	#la idea de ésta funcion, es leer un archivo llamado productos.txt y devolver lo leído en un lista de tuplas
	#las tuplas se harán leyendo el volcado en forma de lista del archivo, agrupando de 3 en 3 los valores y metiendolos en una lista.

	archivo=open("productos.txt","r")
	listaArchivo=archivo.readlines()
	listaNueva=[]
	longitudLinea=0
	caracter=""
	variable=""
	index=0
	listaDepurada=[]
	for linea in listaArchivo:
		linea=linea.strip()
		listaDepurada.append(linea)
	variableFill=True
	#variableFill sirve para solcionar el error en el que var0 se completaba luego de cada salto de linea
	#el for/while crea tuplas de 3 argumentos y las pasa como variable a una lista que las agrupa.
	#esa lista va a ser la que devuelva la funcion con return
	for linea in listaDepurada:
		longitudLinea=0
		while longitudLinea < len(linea):
			caracter=linea[longitudLinea]
			if caracter !=",":
				variable+=caracter
				variableFill=True
			else:	
				if index==3:
					var3=variable
					tupla=(var0,var1,var2,var3)
					listaNueva.append(tupla)
					tupla=()
					index=0
					variableFill=False
				if index==2:
					var2=variable
					index=index+1
				if index==1:
					var1=variable
					index=index+1
				if index==0 and variableFill==True:
					var0=variable
					index=index+1	
					variableFill=True
				variable=""
			longitudLinea = longitudLinea +1	
	archivo.close()
	return listaNueva

def AboutWindowMenu():
	messagebox.showinfo("Informacion del Autor",
		"Nombre: E. Gastón Rayes\nGithub: github.com/voltum3l/")	

def EraseWidget():
	global frame1
	for widget in frame1.winfo_children():
		widget.destroy()	
	#global frame2
	#for widget in frame2.winfo_children():
	#	widget.destroy()

	global marcaADDstring
	marcaADDstring.set("")
	global marcaSEARCHstring
	marcaSEARCHstring.set("")
	global precioADDstring
	precioADDstring.set("")
	global precioSEARCHstring
	precioSEARCHstring.set("")
	global talleADDstring
	talleADDstring.set("")
	global talleSEARCHstring
	talleSEARCHstring.set("")
	global cantidadADDstring
	cantidadADDstring.set("")
	global cantidadSEARCHstring
	cantidadSEARCHstring.set("")

def AddFromWindow():
	EraseWidget()
	auxLabel=Label(frame1,text="Completar los datos: ",bg="#d0dbd3",fg="black",font=('bold',16))
	auxLabel.grid(row=0,column=0,columnspan=8,sticky="nsew")
	labelADDMarca=Label(frame1,text="MARCA",fg="black",bg="#d0dbd3",width=15)
	labelADDMarca.grid(row=1,column=1,sticky="nsew")
	labelADDPrecio=Label(frame1,text="PRECIO",fg="black",bg="#d0dbd3",width=15)
	labelADDPrecio.grid(row=2,column=1,sticky="nsew")
	labelADDTalle=Label(frame1,text="TALLE",fg="black",bg="#d0dbd3",width=15)
	labelADDTalle.grid(row=3,column=1,sticky="nsew")
	labelADDCantidad=Label(frame1,text="CANTIDAD",fg="black",bg="#d0dbd3",width=15)
	labelADDCantidad.grid(row=4,column=1,sticky="nsew")

	entryADDMarca=Entry(frame1,textvariable=marcaADDstring,bg="#8695b0",fg="yellow",width=20,justify="left")
	entryADDMarca.grid(row=1,column=2,sticky="nsew")
	entryAddPrecio=Entry(frame1,textvariable=precioADDstring,bg="#8695b0",fg="yellow",width=20,justify="left")
	entryAddPrecio.grid(row=2,column=2,sticky="nsew")
	entryAddTalle=Entry(frame1,textvariable=talleADDstring,bg="#8695b0",fg="yellow",width=20,justify="left")
	entryAddTalle.grid(row=3,column=2,sticky="nsew")
	entryAddCantidad=Entry(frame1,textvariable=cantidadADDstring,bg="#8695b0",fg="yellow",width=20,justify="left")
	entryAddCantidad.grid(row=4,column=2,sticky="nsew")

	labelAux=Label(frame1,text="",bg="#d0dbd3",fg="black")
	labelAux.grid(row=5,column=0,columnspan=5)
	buttonRegistry=Button(frame1,text="Cargar ITEM",command=lambda:RegisterItemInDatabase(),font=('bold',12),bg="#d0dbd3",fg="black")
	buttonRegistry.grid(row=6,column=3)

def RegisterItemInDatabase():
	#al final del registry, eraseWidget()
	if CheckAllFieldsAllFilled():
		if CheckIfDigitFieldAreOk():
			FillBDD(0)
			#cuando logre cargar, mando el success al frame2
			#podria hacer un EraseWidget()
			pass
	else:
		messagebox.showinfo("ERROR","Uno de los campos está vacío.")

def AddFromArchieve():
	EraseWidget()
	if IsBDDConnected():
		if os.path.exists('productos.txt') == True:
			auxLabel1=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel1.grid(row=0,column=0,columnspan=4,sticky="n")
			auxLabel2=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel2.grid(row=1,column=0,columnspan=4,sticky="n")
			auxLabel3=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel3.grid(row=2,column=0,columnspan=4,sticky="n")
			auxLabel4=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel4.grid(row=4,column=0,columnspan=4,sticky="n")
			auxLabel5=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel5.grid(row=5,column=0,columnspan=4,sticky="n")		
			auxLabel6=Label(frame1,text="                                                     ",bg="#d0dbd3",fg="black",font=('bold',13))
			auxLabel6.grid(row=6,column=0,columnspan=4,sticky="n")
			buttonRegistry=Button(frame1,text="Cargar Productos.txt",command=lambda:FillBDD(1),font=('bold',12),bg="#d0dbd3",fg="black")
			buttonRegistry.grid(row=3,column=3)
		else:
			messagebox.showinfo("ERROR","El archivo productos.txt no existe en el directorio raiz")

def CheckIfDigitFieldAreOk():
	if precioADDstring.get().isdigit() and cantidadADDstring.get().isdigit():
		if talleADDstring.get().isdigit() == False:
			return True
		else:
			messagebox.showinfo("ERROR TALLE","El campo talle solo acepta caracteres.")
			return False
	else:			
		messagebox.showinfo("ERROR PRECIO/CANTIDAD","Los campos Precio/Cantidad solo aceptan números.")
		return False

def CheckAllFieldsAllFilled():
	if marcaADDstring.get() != "" and precioADDstring.get() != "" and talleADDstring.get() != "" and cantidadADDstring.get() != "":
		return True
	else:
		return False

def ItemExist(mmarca,pprecio,ttalle,ccantidad):
	global stock

	tuplaToShow=(mmarca,pprecio,ttalle,ccantidad)
	if IsBDDConnected():
		cursor=stock.cursor()
		cursor.execute("SELECT * FROM Stock WHERE marca=? and talle=?",(mmarca,ttalle))
		item=cursor.fetchall()
		if len(item) == 0:
			cursor.execute("INSERT INTO Stock VALUES(NULL,?,?,?,?)",(mmarca,pprecio,ttalle,ccantidad))
			ShowInFrame2(0,tuplaToShow)
		else:
			cantidad=item[0][4]
			ccantidad = int(ccantidad) + cantidad		
			cursor.execute("UPDATE Stock SET cantidad=? WHERE marca=? and talle=?",(int(ccantidad),mmarca,ttalle))
			ShowInFrame2(1,tuplaToShow)				
		stock.commit()

def FillBDD(option):

	global marcaADDstring
	global precioADDstring
	global talleADDstring
	global cantidadADDstring

	if option==0:
		ItemExist(marcaADDstring.get().capitalize(),precioADDstring.get(),talleADDstring.get().capitalize(),cantidadADDstring.get())

	if option==1:
		toStoreList=LoadFromTxt()

		if IsBDDConnected():
			for line in toStoreList:
				ItemExist(line[0].capitalize(),line[1],line[2].capitalize(),line[3])

def ShowInFrame2(option,tupla):
	global logGeneral

	if option==0:
		mensaje="Añadido a Stock ||| Marca> " + tupla[0] + " Precio> " + str(tupla[1]) + " Talle> " + tupla[2] + " Cantidad> " + str(tupla[3])		
	if option==1:
		mensaje="Modificado en Stock por .txt ||| Marca> " + tupla[0] + " Precio> " + str(tupla[1]) + " Talle> " + tupla[2] + " Cantidad> " + str(tupla[3])
	if option==2:
		mensaje="Borrado de Stock ||| Marca> " + tupla[1] + " Precio> " + str(tupla[2]) + " Talle> " + tupla[3] + " Cantidad> " + str(tupla[4])
	if option==3:
		mensaje="Modificacion Precio ||| Marca> " + tupla[1] + " Precio> " + str(tupla[2]) + " Talle> " + tupla[3] + " Cantidad> " + str(tupla[4])
	if option==4:
		mensaje="Modificacion Cantidad ||| Marca> " + tupla[1] + " Precio> " + str(tupla[2]) + " Talle> " + tupla[3] + " Cantidad> " + str(tupla[4])

	logGeneral.insert(0,mensaje)

	Frame2StockLogView(logGeneral)

def Frame2StockLogView(message):
	global rowALLVar
	global logGeneral

	if len(logGeneral)<10:
		for i in range(len(logGeneral)):
			rowALLVar[i].set(logGeneral[i])
	else:
		for i in range(10):
			rowALLVar[i].set(logGeneral[i])


	auxLabel0=Label(frame2,text="Log de eventos: ",bg="#8695b0",fg="black",font=(10))
	auxLabel0.grid(row=0,column=0)
	auxLabel1=Label(frame2,textvariable=rowALLVar[0],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel1.grid(row=1,column=0,padx=5)
	auxLabel2=Label(frame2,textvariable=rowALLVar[1],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel2.grid(row=2,column=0,padx=5)
	auxLabel3=Label(frame2,textvariable=rowALLVar[2],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel3.grid(row=3,column=0,padx=5)
	auxLabel4=Label(frame2,textvariable=rowALLVar[3],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel4.grid(row=4,column=0,padx=5)
	auxLabel5=Label(frame2,textvariable=rowALLVar[4],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel5.grid(row=5,column=0,padx=5)
	auxLabel6=Label(frame2,textvariable=rowALLVar[5],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel6.grid(row=6,column=0,padx=5)
	auxLabel7=Label(frame2,textvariable=rowALLVar[6],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel7.grid(row=7,column=0,padx=5)
	auxLabel8=Label(frame2,textvariable=rowALLVar[7],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel8.grid(row=8,column=0,padx=5)
	auxLabel9=Label(frame2,textvariable=rowALLVar[8],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel9.grid(row=9,column=0,padx=5)
	auxLabel10=Label(frame2,textvariable=rowALLVar[9],bg="#8695b0",fg="black",font=('bold',9),anchor="w",width=80)
	auxLabel10.grid(row=10,column=0,padx=5)

def ShowLogGeneral():
	global logGeneral
	for line in logGeneral:
		print(line)

def ModifyItem():
	EraseWidget()

	if IsBDDConnected():

		modifyMarcaStringVar=StringVar()
		modifyTalleStringVar=StringVar()

		aux1Label=Label(frame1,text="Ingrese la MARCA y el TALLE del articulo a modificar",width=40,anchor="w")
		aux1Label.grid(row=0,column=1,rowspan=2)

		labelModifyMarca=Label(frame1,text="MARCA",fg="black",bg="#d0dbd3",width=10,justify="left")
		labelModifyMarca.grid(row=3,column=0,padx=5)
		entryADDMarca=Entry(frame1,textvariable=modifyMarcaStringVar,bg="#8695b0",fg="white",width=20,justify="left")
		entryADDMarca.grid(row=4,column=0,padx=5)


		labelModifyTalle=Label(frame1,text="Talle",fg="black",bg="#d0dbd3",width=10,justify="left")
		labelModifyTalle.grid(row=3,column=1,padx=5)
		entryADDTalle=Entry(frame1,textvariable=modifyTalleStringVar,bg="#8695b0",fg="white",width=20,justify="left")
		entryADDTalle.grid(row=4,column=1,padx=5)

		buttonRegistry=Button(frame1,text="Buscar Item para Modificar",command=lambda:subSearchByNameAndSize(modifyMarcaStringVar.get().capitalize(),modifyTalleStringVar.get().capitalize()),font=('bold',12),bg="#d0dbd3",fg="black")
		buttonRegistry.grid(row=6,column=3,padx=5)

def subSearchByNameAndSize(nname,ssize):
	global stock

	modifyPrecioActualStringVar=StringVar()
	modifyPrecioNuevoStringVar=StringVar()
	modifyCantidadActualStringVar=StringVar()
	modifyCantidadNuevaStringVar=StringVar()
	keyFromDatabaseStringVar=StringVar()

	auxTupla=(nname,ssize)
	cursor=stock.cursor()

	cursor.execute("SELECT * FROM Stock WHERE marca=? and talle=?",auxTupla)
	tuplaBuscar=cursor.fetchall()
	print(tuplaBuscar)
	if len(tuplaBuscar) == 0:
		messagebox.showinfo("ERROR","El elemento buscado no existe")
	else:

		aux1Label=Label(frame1,text="Ingrese el valor que quiere establecer ",width=40,anchor="w")
		aux1Label.grid(row=7,column=1,rowspan=2)

		modifyPrecioActualStringVar.set(tuplaBuscar[0][2])
		modifyCantidadActualStringVar.set(tuplaBuscar[0][4])
		keyFromDatabaseStringVar.set(tuplaBuscar[0][0])
		keyAux=int(keyFromDatabaseStringVar.get())

		labelModifyPrecioActual=Label(frame1,text="PRECIO ACTUAL",fg="black",bg="#d0dbd3",width=15,justify="left")
		labelModifyPrecioActual.grid(row=9,column=0,padx=5)
		labelModifyPrecioActual1=Label(frame1,textvariable=modifyPrecioActualStringVar,bg="#8695b0",fg="red",width=20,justify="left")
		labelModifyPrecioActual1.grid(row=10,column=0,padx=5)
		labelModifyPrecioNuevo=Label(frame1,text="PRECIO NUEVO",fg="black",bg="#d0dbd3",width=15,justify="left")
		labelModifyPrecioNuevo.grid(row=9,column=1,padx=5)
		entryModifyPrecioNuevo=Entry(frame1,textvariable=modifyPrecioNuevoStringVar,bg="#8695b0",fg="white",width=20,justify="left")
		entryModifyPrecioNuevo.grid(row=10,column=1,padx=5)
		buttonModifyPrecio=Button(frame1,text="Modificar Precio",command=lambda:SetModifyValues(0,keyAux,modifyPrecioNuevoStringVar.get()),font=('bold',12),bg="#d0dbd3",fg="black")
		buttonModifyPrecio.grid(row=11,column=1,padx=5)

		labelModifyCantidadActual=Label(frame1,text="CANTIDAD ACTUAL",fg="black",bg="#d0dbd3",width=15,justify="left")
		labelModifyCantidadActual.grid(row=9,column=2,padx=5)
		labelModifyCantidadActual1=Label(frame1,text="CANTIDAD NUEVA",fg="black",bg="#d0dbd3",width=15,justify="left")
		labelModifyCantidadActual1.grid(row=9,column=3,padx=5)
		labelModifyCantidadActual2=Label(frame1,textvariable=modifyCantidadActualStringVar,bg="#8695b0",fg="red",width=20,justify="left")
		labelModifyCantidadActual2.grid(row=10,column=2,padx=5)
		labelModifyCantidadActual2=Entry(frame1,textvariable=modifyCantidadNuevaStringVar,bg="#8695b0",fg="red",width=20,justify="left")
		labelModifyCantidadActual2.grid(row=10,column=3,padx=5)
		buttonModifyCantidad=Button(frame1,text="Modificar Cantidad",command=lambda:SetModifyValues(1,keyAux,modifyCantidadNuevaStringVar.get()),font=('bold',12),bg="#d0dbd3",fg="black")
		buttonModifyCantidad.grid(row=11,column=3,padx=5)

def SetModifyValues(option,stringKey,value):
	newValue=int(value)
	global stock
	cursor=stock.cursor()
	auxTupla=(newValue,stringKey)

	if option==0:
		print("entrando en modificar precio")
		cursor.execute("UPDATE Stock SET precio=? WHERE id=?",auxTupla)
	else:
		print("entrando en modificar cantidad")
		cursor.execute("UPDATE Stock SET cantidad=? WHERE id=?",auxTupla)

	#tengo que imprimir el mensaje
	#showinframe2 (option,tupla)
	#option 3 es para modificar precio    option 4 modificar cantidad
	tupla2=(stringKey,)
	cursor.execute("SELECT * FROM Stock WHERE id=?",tupla2)
	tuplaAPasarAFrame2=cursor.fetchall()
	option=option+3
	ShowInFrame2(option,tuplaAPasarAFrame2[0])
	stock.commit()
	EraseWidget()

def EraseStockItem():
	EraseWidget()
	if IsBDDConnected():

		eraseMarcaStringVar=StringVar()
		eraseTalleStringVar=StringVar()

		aux1Label=Label(frame1,text="Ingrese la MARCA y el TALLE del articulo a BORRAR",width=40,anchor="w")
		aux1Label.grid(row=0,column=1,rowspan=2)

		labelEraseMarca=Label(frame1,text="MARCA",fg="black",bg="#d0dbd3",width=10,justify="left")
		labelEraseMarca.grid(row=3,column=0,padx=5)
		entryEraseMarca=Entry(frame1,textvariable=eraseMarcaStringVar,bg="#8695b0",fg="white",width=20,justify="left")
		entryEraseMarca.grid(row=4,column=0,padx=5)


		labelEraseTalle=Label(frame1,text="Talle",fg="black",bg="#d0dbd3",width=10,justify="left")
		labelEraseTalle.grid(row=3,column=1,padx=5)
		entryEraseTalle=Entry(frame1,textvariable=eraseTalleStringVar,bg="#8695b0",fg="white",width=20,justify="left")
		entryEraseTalle.grid(row=4,column=1,padx=5)

		buttonRegistry=Button(frame1,text="Buscar Item para BORRAR",command=lambda:SearchAndErase(eraseMarcaStringVar.get().capitalize(),eraseTalleStringVar.get().capitalize()),font=('bold',12),bg="#d0dbd3",fg="black")
		buttonRegistry.grid(row=6,column=3,padx=5)

def SearchAndErase(eraseMarca,eraseTalle):
	global stock
	auxTupla=(eraseMarca,eraseTalle)
	cursor=stock.cursor()
	cursor.execute("SELECT * FROM Stock WHERE marca=? and talle=?",auxTupla)
	tuplaBuscar=cursor.fetchall()

	if len(tuplaBuscar) == 0:
		messagebox.showinfo("ERROR","El elemento buscado no existe")
	else:
		#borrar
		auxTupla=((tuplaBuscar[0][0]),)
		cursor.execute("DELETE FROM Stock WHERE ID=?",auxTupla)
		ShowInFrame2(2,tuplaBuscar[0])
		EraseWidget()

	stock.commit()

def LogToTXT():
	global logGeneral
	global indexLogGeneral

	if len(logGeneral) == 0:
		messagebox.showinfo("Error","El LOG está vacío.")
	else:
		if indexLogGeneral != len(logGeneral): 
			archivo=open("log.txt","a")
			for i in range(len(logGeneral)):
				archivo.writelines(logGeneral[i] + "\n")

			archivo.write("------------------------------")
			archivo.close()
			messagebox.showinfo("Exito","Log volcado en log.txt")
			indexLogGeneral = len(logGeneral)
		else:
			messagebox.showinfo("Error","El LOG ya está actualizado.")

def StockToTXT():
	if os.path.exists('StockSQL') == True:
		if IsBDDConnected():
			global stock
			global listaStockString
			stock=sqlite3.connect("StockSQL")
			cursor=stock.cursor()
			cursor.execute("SELECT * FROM Stock")
			allStock=cursor.fetchall()

			#ya tengo la lista rellena con tuplas de 5 (id,marca,precio,talle,cantidad)
			if len(allStock) == 0:
				print("no tiene nada cargado, cara de pija")
			else:
				for i in range(len(allStock)):
					print("a ver esto--> ",allStock[0])
					constructStringForTxt(allStock[i])

				makeStockTxtFromList(listaStockString)	
				messagebox.showinfo("Informacion","Creado el archivo stock.txt")
	else:
		print("que hace aca")
		messagebox.showinfo("ERROR","La base de datos NO EXISTE")

def constructStringForTxt(tupla):
	global listaStockString
	mensaje="Marca -> " + tupla[1] + " Precio -> " + str(tupla[2]) + " Talle -> " + tupla[3] + " Cantidad -> " + str(tupla[4]) + "\n"
	listaStockString.append(mensaje)
	
def makeStockTxtFromList(lista):
	archivo = open("stock.txt","w")
	for i in range(len(lista)):
		archivo.writelines(lista[i])
	archivo.close()

def DeleteBDD():
	if os.path.exists('StockSQL') == False:
		messagebox.showinfo("ERROR","La BDD no está creada")
	else:
		global stock
		global connected
		stock=sqlite3.connect("StockSQL")
		option = messagebox.askquestion("Borrar archivo","Estas seguro de querer borrar el archivo?")
		if option == "yes":
			stock.close()
			remove('StockSQL')
			messagebox.showinfo("Exito","La BDD ha sido borrada exitosamente")
			connected=False
			CheckBars()
			EraseWidget()

def ExitProgram():
	global root
	global stock
	option=messagebox.askquestion("Salir","¿Cerrar el programa?")
	if option=="yes":
		stock=sqlite3.connect("StockSQL")
		stock.close()
		root.destroy()

def CheckBars():
	global bddCreateStringVar
	global bddConnectedStringVar
	global connected

	if os.path.exists('StockSQL') == True:
		bddCreateStringVar.set("BASE DE DATOS CREADA")
		barraCreate=Label(frame0,bg="green",fg="white",textvariable=bddCreateStringVar,width=35)
		barraCreate.grid(row=0,column=0,padx=5,rowspan=3)
	else:
		bddCreateStringVar.set("BASE DE DATOS NO CREADA")
		barraCreate=Label(frame0,bg="red",fg="white",textvariable=bddCreateStringVar,width=35)
		barraCreate.grid(row=0,column=0,padx=5,rowspan=3)

	if connected == True:
		bddConnectedStringVar.set("BASE DE DATOS CONECTADA")
		barraCreate=Label(frame0,bg="green",fg="white",textvariable=bddConnectedStringVar,width=35)
		barraCreate.grid(row=0,column=1,padx=5,rowspan=3)
	else:
		bddConnectedStringVar.set("BASE DE DATOS NO CONECTADA")
		barraCreate=Label(frame0,bg="red",fg="white",textvariable=bddConnectedStringVar,width=35)
		barraCreate.grid(row=0,column=1,padx=5,rowspan=3)

def AllResults():
	EraseWidget()

	if IsBDDConnected():
	
		totalMarcas=""
		totalCantidades=0

		marcasVar=StringVar()
		totalVar=StringVar()

		totalMarcas=GiveMeMarcas()
		marcasVar.set(totalMarcas)

		totalCantidades=GiveMeCantidades()
		totalVar.set(str(totalCantidades))

		auxLabel=Label(frame1,text="TOTALES: ",bg="#d0dbd3",fg="black",font=('bold',16))
		auxLabel.grid(row=0,column=0,columnspan=8,sticky="nsew",pady=15)

		aux1=Label(frame1,text="                                                                        ",fg="black",bg="#d0dbd3",width=15)
		aux1.grid(row=1,rowspan=3,column=0)
		labelTotalMarcas=Label(frame1,text="MARCAS",fg="black",bg="white",width=15)
		labelTotalMarcas.grid(row=6,column=0,columnspan=2,sticky="nsew",padx=10)
		labelTotalMarcas1=Label(frame1,textvariable=marcasVar,fg="black",bg="yellow")
		labelTotalMarcas1.grid(row=6,column=2,columnspan=15,sticky="nsew",padx=10)
		aux2=Label(frame1,text="                                                                        ",fg="black",bg="#d0dbd3",width=15)
		aux2.grid(row=7,rowspan=2,column=0)

		labelTotalCantidades=Label(frame1,text="STOCK TOTAL",fg="white",bg="black",width=15)
		labelTotalCantidades.grid(row=9,column=0,columnspan=2,sticky="nsew",padx=10)
		labelTotalCantidades1=Label(frame1,textvariable=totalVar,fg="black",bg="yellow")
		labelTotalCantidades1.grid(row=9,column=2,sticky="nsew",padx=10)

		aux3=Label(frame1,text="                                                                        ",fg="black",bg="#d0dbd3",width=15)
		aux3.grid(row=12,rowspan=3,column=0)

def GiveMeMarcas():
	mensaje=""
	listaMarcas=[]

	global stock
	stock=sqlite3.connect("StockSQL")
	cursor=stock.cursor()
	cursor.execute("SELECT * FROM Stock")
	listaTotal=cursor.fetchall()

	for elemento in listaTotal:
		listaMarcas.append(elemento[1])

	listaMarcas.sort()
	listaABorrar=[]
	contador=0

	for item in range(len(listaMarcas)):
		if (item < len(listaMarcas)-1):
			contador=contador+1
			if listaMarcas[item] == listaMarcas[contador]:
				listaABorrar.append(item+1)

		contador=item+1


	for vuelta in range(len(listaABorrar)):
		indicador=listaABorrar.pop()
		listaMarcas.pop(indicador)

	
	for elemento in listaMarcas:
		mensaje = mensaje + elemento + " | "

	return mensaje

def GiveMeCantidades():

	cantidad=0
	global stock
	stock=sqlite3.connect("StockSQL")
	cursor=stock.cursor()
	cursor.execute("SELECT * FROM Stock")
	listaTotal=cursor.fetchall()

	for elemento in listaTotal:
		cantidad = cantidad + elemento[4]
		print(cantidad)


	return cantidad

#------------------------------>>> VARIABLES GLOBALES

#----var connected -> cuando la bdd está conectada
connected=False

#----var stock que maneja la BDD
stock=[]

#----var log general
logGeneral=[]
indexLogGeneral=0

#----var listaStockString para luego enviar a txt.
listaStockString=[]
#---------------->>> GUI ROOT and FRAMES
root=Tk()
root.title("STOCK HANDLER")
menuBar=Menu(root)
root.config(bg="white",menu=menuBar)
frame0=Frame(root,bg="#d0dbd3",width=500,height=20)
frame0.pack(fill=X,expand=True)
frame1=Frame(root,bg="#d0dbd3",width=500,height=300)
frame1.pack(fill=X, expand=True)
frame2=Frame(root,bg="#8695b0",width=500,height=200)
frame2.pack(fill=X, expand=True)

#--------------->>>> Live Bars (Create and Connected BDD)
bddCreateStringVar=StringVar()
bddConnectedStringVar=StringVar()
CheckBars()

#---------------->>> GUI string vars
marcaADDstring=StringVar()
marcaSEARCHstring=StringVar()
precioADDstring=StringVar()
precioSEARCHstring=StringVar()
talleADDstring=StringVar()
talleSEARCHstring=StringVar()
cantidadADDstring=StringVar()
cantidadSEARCHstring=StringVar()

#----var Frame2 Stock
row0Var=StringVar()
row1Var=StringVar()
row2Var=StringVar()
row3Var=StringVar()
row4Var=StringVar()
row5Var=StringVar()
row6Var=StringVar()
row7Var=StringVar()
row8Var=StringVar()
row9Var=StringVar()
rowALLVar=[row0Var,row1Var,row2Var,row3Var,row4Var,row5Var,row6Var,row7Var,row8Var,row9Var]
for i in range(len(rowALLVar)):
	rowALLVar[i].set("------------------------------------------------------")
#---------------->>> GUI MENU
databaseMenu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="Conectar",menu=databaseMenu)
databaseMenu.add_separator()
databaseMenu.add_command(label="Conectar con BDD",command=ConnectToDatabase)
databaseMenu.add_separator()
databaseMenu.add_command(label="Crear BDD",command=CreateBDD)
databaseMenu.add_separator()
databaseMenu.add_command(label="Volcar LOG en .txt",command=LogToTXT)
databaseMenu.add_separator()
databaseMenu.add_command(label="Borrar BDD",command=DeleteBDD)
databaseMenu.add_separator()
databaseMenu.add_command(label="Salir",command=ExitProgram)


inventoryMenu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="Cargar Inventario",menu=inventoryMenu)
inventoryMenu.add_command(label="Cargar Manualmente",command=AddFromWindow)
inventoryMenu.add_command(label="Cargar por archivo",command=AddFromArchieve)

modifyMenu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="Modificar/Borrar",menu=modifyMenu)
modifyMenu.add_command(label="Modificar Precio/Cantidad",command=ModifyItem)
modifyMenu.add_command(label="Borrar Elemento",command=EraseStockItem)

infoMenu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="Consultas",menu=infoMenu)
infoMenu.add_command(label="Consulta de totales",command=AllResults)
infoMenu.add_command(label="Descargar STOCK en archivo .TXT",command=StockToTXT)

aboutMenu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="About",menu=aboutMenu)
aboutMenu.add_command(label="Acerca del autor",command=AboutWindowMenu)
aboutMenu.add_command(label="aux",command=GiveMeCantidades)

root.mainloop()
#--------------->>> END

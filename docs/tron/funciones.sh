#!/bin/bash
#PROGRAMA TRON
# POR ELIAS HUNG
#elprofesorverdad@gmail.com
#YO DEFIENDO AL USUARIO..!
usuario=${SUDO_USER:-${USER}}
# __                  _                       
# / _|_   _ _ __   ___(_) ___  _ __   ___  ___    
#| |_| | | | '_ \ / __| |/ _ \| '_ \ / _ \/ __|
#|  _| |_| | | | | (__| | (_) | | | |  __/\__ \
#|_|  \__,_|_| |_|\___|_|\___/|_| |_|\___||___/
#
#NOTA: LAS FUNCIONES VACIAS RESULTAN EN ERROR
#-------------------------------------------------------------------------------

#UBICAR coloca el path de la consola en el area de trabajo
#UBICAR recibe la varible $nombre de la funcion diálogo
# _   _ _     _                
#| | | | |__ (_) ___ __ _ _ __ 
#| | | | '_ \| |/ __/ _` | '__|
#| |_| | |_) | | (_| (_| | |   
# \___/|_.__/|_|\___\__,_|_|   

function ubicar ()
{
    cd $carpeta_de_trabajo
    export CDPATH="$carpeta_de_trabajo"
    cd $carpeta_de_trabajo

}

#***********************************************
#    _    _          _        ____            _             
#   / \  | |__  _ __(_)_ __  / ___|  ___  ___(_) ___  _ __  
#  / _ \ | '_ \| '__| | '__| \___ \ / _ \/ __| |/ _ \| '_ \ 
# / ___ \| |_) | |  | | |     ___) |  __/\__ \ | (_) | | | |
#/_/   \_\_.__/|_|  |_|_|    |____/ \___||___/_|\___/|_| |_|

#ABRIR SESIÓN: abre el primer documento contenido en una carpeta con el programa dado y luego abre los demás con el mismo programa, pero en un ciclo for.

abrirsesion ()
{

	lista=$(ls "$3")
	#abre el primer documento del arreglo lista
	$1 ${lista[0]}
	#el ciclo for abre desde el segundo elemento (documento) hasta el ultimo contenido en "lista"
	for((i=1; i<${#lista[*]}; i++))
	do
		$2 ${lista[$i]}
	done

}

#  ____                           ____            _             
# / ___|___ _ __ _ __ __ _ _ __  / ___|  ___  ___(_) ___  _ __  
#| |   / _ \ '__| '__/ _` | '__| \___ \ / _ \/ __| |/ _ \| '_ \ 
#| |__|  __/ |  | | | (_| | |     ___) |  __/\__ \ | (_) | | | |
# \____\___|_|  |_|  \__,_|_|    |____/ \___||___/_|\___/|_| |_|
#                                                               


crearsesion ()

{
		#CREAR SESIÓN: 
		mkdir $2
		ubicar
		$1
		sleep 3
}

# ____                       _     _            
#|  _ \ ___  ___ _ __   __ _| | __| | __ _ _ __ 
#| |_) / _ \/ __| '_ \ / _` | |/ _` |/ _` | '__|
#|  _ <  __/\__ \ |_) | (_| | | (_| | (_| | |   
#|_| \_\___||___/ .__/ \__,_|_|\__,_|\__,_|_|   
#               |_|                             



# _____       _                
#| ____|_ __ | | __ _  ___ ___ 
#|  _| | '_ \| |/ _` |/ __/ _ \
#| |___| | | | | (_| | (_|  __/
#|_____|_| |_|_|\__,_|\___\___|
#                              

enlace ()
{

#TODO: investigar la naturaleza de los enlaces para enlazar o sincronizar documentos en otro disco 
# despues sincronizar a traves de fetp y de ssh

	#documentos=$(echo "$GEDIT_DOCUMENTS_URI" | grep -Eo '\S*')
	#la parte de arriba lee la dirección de las pestañas abiertas y
	#los convierte en valores separados por break line o retorno de carro.
	#grep convierte los valores separados por espacios de 
#	la variable de gedit $GEDIT_DOCUMENTS_URI en valores
#	separados por retorno de carro.para que pueda ser leída por
#	el ciclo for.


declare -a array=( $GEDIT_DOCUMENTS_URI ) #convertimos una variable en un arreglo 
cd "$carpeta_de_trabajo"
for (( i=0; i<${#array[*]}; i++ ))
do
	var=${array[i]} #almacenamos el valor del arreglo en la posición i en la variable
	printf -v var "%b" "${var//\%/\ }" #decodificamos la URI quitando los %, los sustituímos por espacios escapandolos en la ultima parte \ }"
	#se utiliza el operador <<< para alimentar la entrada estandar del comando sed, y funciona para cualquier otro comando
	file=$(sed 's/^.\{7\}//' <<<"$var") #cortamos los 7 primeros caracteres de la cadena var y asignamos a file://
	aux=\'"$file"\' #agregamos comillas a cada una de las direcciones o rutas, para encubrir los espacios

#	echo $carpeta_de_trabajo
	#asignamos el comando a ejecutar como un string dentro de una variable para que las variables internas se expandan antes de enlazar
	aux2=$(echo 'ln --backup --suffix="_respaldo" -f -v' $aux)  	# ln crea un respaldo del archivo
	#ejecutamos el código dentro de la variable con eval
	eval $aux2
	#echo $aux2
	
done

#	for file in "$documentos"
#	do
#		
#		echo creando enlace $file...
#		var=$(echo-e /"$(echo $file)/")
#		echo vamos en $var
#		ln -s --backup --suffix="_respaldo_$(date)" -f -v $var "$carpeta_de_trabajo/"
#		# ln crea un respaldo del archivo que es movido a la carpeta respaldo
#		# de cada carpeta de sesion
#	done

}
linkearUnArchivo ()
{
	cd "$GEDIT_CWD"
	ln --backup --suffix="_respaldo" -f -v $GEDIT_CURRENT_DOCUMENT_PATH $GEDIT_CWD
	cp -v *respaldo* /home/$usuario/tron/zzRespaldosDeLn/
    rm -v *respaldo*
    echo
    echo recuerde que si el enlace se sobreescribió puede 
    echo recuperar el documento en /home/usuario/tron/zzRespaldosDeLn/
    echo
}


#-----------------------------------------------------------------------------------------------------------------------
#***********************************************************************************************************************











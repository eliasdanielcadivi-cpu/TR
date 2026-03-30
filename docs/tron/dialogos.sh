#!/bin/bash

#!/bin/bash
#PROGRAMA TRON
# POR ELIAS HUNG
#elprofesorverdad@gmail.com
#YO DEFIENDO AL USUARIO..!



# ____  _       _                         ___       _      _       
#|  _ \(_) __ _| | ___   __ _  ___  ___  |_ _|_ __ (_) ___(_) ___  
#| | | | |/ _` | |/ _ \ / _` |/ _ \/ __|  | || '_ \| |/ __| |/ _ \ 
#| |_| | | (_| | | (_) | (_| | (_) \__ \  | || | | | | (__| | (_) |
#|____/|_|\__,_|_|\___/ \__, |\___/|___/ |___|_| |_|_|\___|_|\___/ 
#                       |___/                                      


#DIÁLOGO: permite la reutilización de las interfaces de dialogo
#en el sistema TRON
dialogo ()
{
case $1 in
	1) 
		#FUNCIONALIDAD:
		#retorna 1 si el usuario introdujo texto y presionó aceptar
		#retorna 2 si el usuario precionó cancelar o cerró el cuadro de diálogo o no introdujo un texto.
#		nombre=$(gjs "$ruta/dialogos.js" "1" "$2" "$3" "$4" "$5")
#		echo $nombre
#		echo salida dentro es $?
		
		:
		
	;;
	2)
		#diálogo 2 de ERROR un botón
		zenity --error \
       --title="$2" \
       --width=250 \
       --text="$3"
	;;
	3)
		#diálogo 3 MENÚ
		kdialog --title "$2" --menu "Seleccione su Opción" "op1" "$3" "op2" "$4" "op3" "$5" "op4" "$6" "op5" "$7" "op6" "$8"
	;;
	4)
		#diálogo 4 PREGUNTA Y DOS BOTONES DE RESPUESTAS
		texto="¿<span weight=\"bold\" foreground=\"green\">Qué quieres</span> Hacer?"
		zenity --question \
		       --title="$2" \
		       --width=250 \
		       --ok-label="$3" \
		       --cancel-label="$4" \
		       --text="${texto}"
		nombre=$?
	;;
	5)
		#DIÁLOGO 5 de SELECCION DE CARPETAS
		nombre=`zenity --file-selection --directory --title="$2" --filename =$3`
		salida=$?
		case $salida in
			0)
				echo "TRON:" "\"$nombre\" seleccionado."
			;;
			1)
				echo "TRON :No ha seleccionado ningún archivo."
				
			;;
			-1)
				echo "TRON: Ha ocurrido un error inesperado."
				
			;;
		esac
	;;
	esac

}


# ____  _       _                          __ _       
#|  _ \(_) __ _| | ___   __ _  ___  ___   / _(_)_ __  
#| | | | |/ _` | |/ _ \ / _` |/ _ \/ __| | |_| | '_ \ 
#| |_| | | (_| | | (_) | (_| | (_) \__ \ |  _| | | | |
#|____/|_|\__,_|_|\___/ \__, |\___/|___/ |_| |_|_| |_|
#                       |___/                         
#-----------------------------------------------------------------------------------------------------------------------
#***********************************************************************************************************************











#!/bin/bash
usuario=${SUDO_USER:-${USER}}
if [[ ! -f /home/$usuario/tron/plugins/bash/bashVariables.sh || ! -f /home/$usuario/tron/plugins/bash/alias.sh ]]; then
    source /home/tron/plugins/bash/bashVariables.sh
    source /home/tron/plugins/bash/alias.sh
    source /home/tron/Scripts/prog-predet.sh
else
    source /home/$usuario/tron/plugins/bash/bashVariables.sh
    source /home/$usuario/tron/plugins/bash/alias.sh
    source /home/$usuario/tron/Scripts/prog-predet.sh
fi
# FUNCIONES DEBAJO DE ESTO POR FAVOR

# $1 debe pasarse la ruta absoluta la db
# $2 en adelante comandos sqlite


# FUNCIONES LANZADORAS DE PROGRAMAS DE TRON////////////////////////////////////////


editarComando() {
    micro "$(command -v "$1")"
}

#kaban-on () {
 #  source  /home/$usuario/tron/programas/GesProgramas/instalar-restaurando-instantanea.sh
#}

#kaban-off () {
#    source /home/$usuario/tron/programas/GesProgramas/desintalar-guardando-instantanea.sh
#}



adminkaban () {
   source "$programas/GesProgramas/wekan-gantt.sh"
}



# utiliza broot para devolver una ruta
# $1  y ruta_carpeta es la carpeta donde se abrirá inicialmente broot
# USO: micro $(ruta ruta_carpeta) ; mpv $(ruta ruta_carpeta)....

# Devuelve la ruta a un directorio navegando con broot a él
# $1 es la carpeta donde se abrirá inicialmente broot

# Devuelve la ruta relativa de una documento referencia a
# uno relativo abriendo el navegador para que selecciones los documentos
# a analizar $1 abre broot en  la carpeta referencia, y $2 abre broot en la carpeta relativa
# si no se pasa $1 o $2 se abre broot en /

relativa () {
    realpath --relative-to="$(br --conf ~/.config/broot/select.toml $1)" "$(br --conf ~/.config/broot/select.toml $2)"   
}



grepcolor () {
    grep --color=always -R $1
}

lesscolor () {
    less -r $1
}

insensiblemayusculas () {
    shopt -s nocaseglob
}

sensiblemayusculas () {
    shopt -u nocaseglob
}


copiar() {
    if [ -z "$1" ]; then
        echo "❌ Dime qué quieres copiar. Ejemplo: copiar ini"
        return 1
    fi

    # Buscamos la ruta del comando
    RUTA=$(which "$1")

    if [ -n "$RUTA" ]; then
        cat "$RUTA" | xclip -sel clip
        echo "✅ El código de '$1' ($RUTA) ya está en tu portapapeles."
    else
        echo "❌ No encontré el comando '$1'. ¿Está instalado?"
    fi
}

verdependencias () {
echo "Presione 1 si el paquete es un deb descargado"
echo "Presiona 2 si introducirá el nombre de un paquete"
read num

if [[ $num == 1 ]]; then
	echo introduzca la dirección al paquete
	read direccion
	dpkg-deb -I $direccion
elif [[ $num == 2 ]]; then
	echo "¿Cuál es el nombre del paquete?"
	read paquete
	echo
	echo "las dependencias son:"
	echo
	apt-cache depends $paquete
	echo
fi
}
cp-igualito () {

cp -a -p -f -v $1 $2
    
}
function br {
    local cmd cmd_file code
    cmd_file=$(mktemp)
    if broot --outcmd "$cmd_file" "$@"; then
        cmd=$(<"$cmd_file")
        command rm -f "$cmd_file"
        eval "$cmd"
    else
        code=$?
        command rm -f "$cmd_file"
        return "$code"
    fi
}


dondelovi () {
if [[ -z $1 || -z $2 ]]; then
    echo "Uso: dondelovi texto ruta"
    return 1
else
    ag $1 $2
fi
}

chismoso () {
echo "uso: chismoso texto_a_buscar ruta"
echo
if [[ -z $1 || -z $2 ]]; then
    echo "uso: chismoso texto_a_buscar ruta"
    return 1
else

    echo "Busca con ag en $2"
    echo
    dondelovi "$1" "$2"

    echo
    echo '***********************************************'
    echo 'which:'
    which $1
    echo
    echo '***********************************************'

    echo
    echo 'command -V'
    command -V $1
    echo
    echo '***********************************************'
    echo

    #echo 'whereis -b (binarios)'
    #whereis -b $1
    #echo
    #echo '***********************************************'
    #echo
    #echo 'whereis -m (manuales)'
    #whereis -m $1
    #echo
    #echo '***********************************************'
    #echo
    #echo 'whereis -s (sources)'
    #whereis -s $1
    #echo
    echo '***********************************************'
fi
}

funAliased ()
 {

microOvisual $tronalias
ordenarfichero $tronalias

}


FunVared ()

{
microOvisual "$variables"

	  
}



FunVariables ()

{

#while IFS= read -r line
#do
#  echo "$line"
#done < $tron/plugins/bash/bashVariables.sh
var=$(cat $tron/plugins/bash/bashVariables.sh)

echo "$var" | sort
 

}
# $1=texto existente $2=texto nuevo $3 ruta al documento $4 comando systemctl 
# puede ser start o restart, nada para escribir "texto modificado" luego de la sustitución

leerencolores () {

cat $1 | ccze -A | less -R

}




grubi () {
ejecutarcomoroot
update-grub
lsblk
echo "En qué dispositivo INSTALAR Grub?"
read dispositivo
grub-install /dev/$dispositivo


}

#muestra que se ha instalado por terminal o linea de comando
queinstale () {
echo
echo "Con apt..."
echo
( zcat $( ls -tr /var/log/apt/history.log*.gz ) ; cat /var/log/apt/history.log ) | egrep '^(Start-Date:|Commandline:)' | grep -v aptdaemon | egrep '^Commandline:'

echo
echo
echo "Con brew..."
brew list

}

#alimenta comandos desde una lista en un documento creo que de horizontal a vertical
#$1 ruta a la lista #2 comando
alimentardesdelista (){

xargs -a <(awk '/^\s*[^#]/' "$1") -r -- $2
if [[ $? != 0 ]]; then echo "No se pudo ejecutar el comando"; fi

}


#hayinternet () {
#if ! [ "`ping -c 1 google.com 2>/dev/null`" ]; then echo "TRON: $usuario No tenemos Internet"; notify-send "TRON: $usuario No tenemos Internet"; else echo "TRON: $usuario Si hay Internet"; notify-send "TRON: $usuario Si hay Internet" ; fi
#}
hayinternet () {
  

  echo "TRON: $usuario Verificando tu conexión..."

  # Verificamos si hay internet
  if ! [ "`ping -c 1 google.com 2>/dev/null`" ]; then
    echo "TRON: $usuario No tenemos Internet"
    notify-send "TRON: $usuario No tenemos Internet"
  else
    echo "TRON: $usuario Si hay Internet"
    notify-send "TRON: $usuario Si hay Internet"

    # Verificamos si Speedtest-cli está instalado
    if ! [ -x "$(command -v speedtest-cli)" ]; then
      echo "TRON: $usuario Instalando Speedtest-cli..."
      sudo apt install speedtest-cli
      echo "TRON: $usuario Speedtest-cli instalado correctamente"
    fi

    # Si Speedtest-cli está instalado, ejecutamos el test
    if [ -x "$(command -v speedtest-cli)" ]; then
      echo "TRON: $usuario Ejecutando Speedtest..."
      speedtest-cli
    fi
  fi

  echo "TRON: $usuario fin del la comunicación felíz día..!"
}


#elimina las lineas repetidas de un documento
# $1 fichero origen $2 Fichero destino
unicos () {
uniq $1 > $2
}

pausa () {
echo "$1"
echo "Presiona cualquier tecla para continuar..."
read zoncomezon

}



ejecutarcomoroot (){
if (( $EUID != 0 )); then
    echo TRON:
    echo "Mi usuario $usuario por favor ejecute como root"
    echo "y así, venceremos a control maestro"
    sudo su

fi
}



#recibe el documento fuente y el sitio a copiar destino
cpigualito ()
{
cp -a -p -f -v $1 $2
}



preguntasalir () {
echo "TRON:"
echo $1...?
echo "Nota: $2"
echo "Presiona 1 Para salir"
echo  "Presiona Cualquier otra tecla para continuar"
#para que no de el error se esperaba un operador unario
read frase; if [ -z $frase ];then frase=0; fi
case $frase in
	1)
		
		return 1
	;;
	2)
		return 0
		
    ;;
esac


}

preguntasino () {
echo "TRON:"
echo $1...?
echo "Nota: $2"
echo "Presiona 1 para NO"
echo  "Presiona Cualquier otra tecla para SI"
read frase
case $frase in
	1)
		salir=1
	;;
	2)
		salir=0
		
    ;;
esac

if [ $salir -eq 1 ]
then
    exit
fi
}


cuentafinal () {
setterm -term linux -back red -fore white
echo "--------------------- $2 --------" 
setterm -term linux -default
echo
echo
sleep 1 # seconds
cont=0
DURATION=$(( $1  )) # convert minutes to seconds
START=$(date +%s)
x=-1
print0=1
while [ $x == -1 ]; do
	NOW=$(date +%s)				# get time now in seconds
	DIF=$(( $NOW-$START ))			# compute diff in seconds
	ELAPSE=$(( $DURATION-$DIF ))		# compute elapsed time in seconds
	MINS=$(( $ELAPSE/60 ))			# convert to minutes... (dumps remainder from division)
	SECS=$(( $ELAPSE - ($MINS*60) )) 	# ... and seconds
	if [ $MINS == 0 ] && [ $SECS == 0 ]	# if mins = 0 and secs = 0 (i.e. if time expired)
	then 					# blink screen
		for i in `seq 1 180`;    		# for i = 1:180 (i.e. 180 seconds)
		do
			if [ $print0==1 ]
            then
                echo 
            fi
			sleep 0.5
			sleep 0.5	
            let cont=cont+1
            print0=0
            if [ $cont == 1 ]
            then
                setterm -term linux -back red -fore white
                echo "*********** $2 **********************" 
                x=0
                setterm -term linux -default    
                echo
                break
            fi
		done  					# end for loop 
		break					# end script

	else 					# else, time is not expired
		echo "00:00:0$SECS"			# display time
		sleep 1  				# sleep 1 second
	fi					# end if
done	# end while loop	
echo
}

#$1 dispositivo $2 ruta de montaje
montapar () {
    if [[ ! -d $2 ]]; then
        mkdir $2
    fi
    cuentafinal 2 "Montando la Partición en la ruta de montaje..."
    echo la ruta de montaje es $2
    mount /dev/$1 $2
    if [ $? -eq 0 ]; then
        echo "Montaje exitoso"
    else 
        umount -lf $2
        mount /dev/$1 $2
#        exit
    fi

}



montarDiscos ()
{
cd /dev
for dsp in sd*
do
    particion=/dev/$dsp
    destino=/media/$usuario/$dsp
    mkdir $destino
    echo montando $particion en $destino
    mount $particion $destino
done

}
desmontarDiscos () {
cd /media/$usuario
for dsp in *
do
    umount -lf /media/$usuario/$dsp
    rm -d /media/$usuario/$dsp
done


}


infodiscos () {
clear
ejecutarcomoroot
montarDiscos pausa; echo;
lsblk -fml  -o NAME,FSTYPE,LABEL,SIZE,UUID,MOUNTPOINT;
echo; echo después se muestra el espacio ocupado; pausa; echo; echo "Mostrando Espacio"; echo;  df -h; echo; echo seguido se desmontarán las particiones; pausa;
desmontarDiscos; echo; echo Control Maestro: End of Line
}
#Descisión si bifurcarse a una función-rutina o nó
#Recibe la pregunta que describe la bifurcación
#Despues de la bifurcación continua el programa principal
desea () {
    echo "Desea $1 ...?"
    echo "Presione 1 para si"
    echo "Presione cualquier otra tecla para continuar"

    read des; if [ -z $des ];then des=0; fi
    if [ $des == 1 ]; then
        return 1
    else
        return 0
    fi

}
# LA opción menos comón es $1 y la mas común $2
dosopciones () {
    echo "Desea $1 ...?"
    echo "Presione 1 para si"
    echo "Presione cualquier otra tecla para $2"
    read des; if [ -z $des ];then des=0; fi
    if [ $des == 1 ]; then
        return 1
    else
        return 0
    fi

}





# $1 nombre de archivos y directorios a borrar. 
# se borrará todo lo que aparezca en la búsqueda de locate $1 
borrartodos () {
echo
echo "Los documentos y directorios a borrar son:"
echo
locate $1
echo
echo "Si presiona cualquier tecla para continuar se borrarán"
preguntasalir "Seguro desea borrarlos:"
rm -r -v -d `locate $1`
}

# Pausa el programa y dice: "Presiona cualquier tecla para continuar..."



# $1 Texto que se agregará al final de un documento $2 Ruta al documento
AgregarFinal () {

if [[ -z $1 ]];
then
  echo TRON: uso : AgregarFinal [Texto_A_Agregar] [Ruta_Documento]
  exit
else

echo $1 >> $2
echo TRON: mostrando $2...
echo
echo
cat $2
fi


}

ordenarfichero () {
inicio=$PWD
cd /home/$usuario
archivo=$1
echo $archivo > resp_alias.sh
cat $1 | sort --ignore-case > aux.txt
if [ -f aux.txt ]; then
    cat aux.txt > $archivo
    cat $archivo
    echo Tron:
    echo Mi usuario $usuario
    echo fichero ordenado
    rm -v aux.txt
else
    echo Mi usuario $usuario
    echo Ha ocurrido un error al ordenar el fichero
fi
cd $inicio
}



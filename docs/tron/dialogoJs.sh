#!/bin/bash
#FUNCIONALIDAD:
#retorna 1 si el usuario introdujo texto y presionó aceptar
#retorna 2 si el usuario precionó cancelar o cerró el cuadro de 
#diálogo o no introdujo un texto.
nombre=$(gjs dialogos.js 1 "Programa TRON" "Elegir de un listado" "Nueva Sesión" "¿Nombre Sesión? ")
ans=$?
echo $nombre
echo $ans




if [ $nombre eq 1 ] #si no eligio el boton alternativo...(si eligio la primera opción)
then #comandos si eligio el boton principal abrir sesion dando un nombre

elif [ $nombre eq 2 ] #comandos si ha elegido abrir la sesión por medio de un listado

fi


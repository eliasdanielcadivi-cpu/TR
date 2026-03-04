"""
Init Module - Gestión de Inicialización de Kitty
=================================================

Módulo independiente para gestionar la configuración centralizada de Kitty.
Sigue la regla de modularidad TRON: máximo 3 funciones públicas.

Funciones:
1. create_symlink(tr_config, user_config) - Crea enlace simbólico
2. reload_config(socket_path, config_path) - Recarga configuración en Kitty
3. get_status(tr_config, user_config, socket_path) - Retorna estado

CLI: tr init --status, --link, --reload, --unlink
"""

import os
import subprocess
from typing import Dict, Any, Optional


def create_symlink(tr_config: str, user_config: str) -> Dict[str, Any]:
    """
    Crea enlace simbólico de configuración TRON en ~/.config/kitty/

    Args:
        tr_config: Ruta a configuración TRON (TR/config/kitty.conf)
        user_config: Ruta de usuario (~/.config/kitty/kitty.conf)

    Returns:
        Dict con 'success' (bool), 'message' (str), 'target' (str)
    """
    result = {
        'success': False,
        'message': '',
        'target': ''
    }

    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(user_config), exist_ok=True)

        # Eliminar enlace o archivo existente
        if os.path.islink(user_config) or os.path.isfile(user_config):
            os.remove(user_config)
            result['message'] = 'Configuración anterior eliminada'

        # Crear enlace simbólico
        os.symlink(tr_config, user_config)

        if os.path.islink(user_config):
            result['success'] = True
            result['message'] = 'Enlace creado exitosamente'
            result['target'] = os.readlink(user_config)
        else:
            result['message'] = 'Error al crear enlace'

    except Exception as e:
        result['success'] = False
        result['message'] = f'Error: {str(e)}'

    return result


def reload_config(socket_path: str, config_path: str) -> Dict[str, Any]:
    """
    Recarga configuración en instancia de Kitty en ejecución.

    Args:
        socket_path: Ruta al socket de Kitty (unix:/tmp/mykitty)
        config_path: Ruta a configuración a cargar

    Returns:
        Dict con 'success' (bool), 'message' (str), 'output' (str)
    """
    result = {
        'success': False,
        'message': '',
        'output': ''
    }

    # Verificar si Kitty está corriendo
    if not os.path.exists(socket_path.replace('unix:', '')):
        result['success'] = False
        result['message'] = 'Kitty no está corriendo con socket'
        return result

    try:
        # Extraer ruta del socket (quitar 'unix:' prefix)
        socket = socket_path.replace('unix:', '')

        # Ejecutar comando de recarga
        cmd = ['kitty', '@', '--to', f'unix:{socket}', 'load-config', config_path]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if proc.returncode == 0:
            result['success'] = True
            result['message'] = 'Configuración recargada exitosamente'
            result['output'] = proc.stdout
        else:
            result['success'] = False
            result['message'] = f'Error: {proc.stderr}'
            result['output'] = proc.stderr

    except subprocess.TimeoutExpired:
        result['success'] = False
        result['message'] = 'Timeout al recargar configuración'
    except Exception as e:
        result['success'] = False
        result['message'] = f'Error: {str(e)}'

    return result


def get_status(tr_config: str, user_config: str, socket_path: str) -> Dict[str, Any]:
    """
    Obtiene estado completo de la configuración de Kitty.

    Args:
        tr_config: Ruta a configuración TRON
        user_config: Ruta de usuario (~/.config/kitty/kitty.conf)
        socket_path: Ruta al socket de Kitty

    Returns:
        Dict con estado de config, enlace, y Kitty
    """
    status = {
        'tr_config': {
            'exists': os.path.isfile(tr_config),
            'path': tr_config
        },
        'symlink': {
            'exists': False,
            'valid': False,
            'path': user_config,
            'target': ''
        },
        'kitty': {
            'running': False,
            'socket': socket_path,
            'tabs': 0
        }
    }

    # Verificar enlace simbólico
    if os.path.islink(user_config):
        status['symlink']['exists'] = True
        status['symlink']['target'] = os.readlink(user_config)
        status['symlink']['valid'] = (status['symlink']['target'] == tr_config)
    elif os.path.isfile(user_config):
        status['symlink']['exists'] = True
        status['symlink']['valid'] = False

    # Verificar Kitty
    socket_file = socket_path.replace('unix:', '')
    if os.path.exists(socket_file):
        try:
            cmd = ['kitty', '@', '--to', socket_path, 'ls']
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            if proc.returncode == 0:
                status['kitty']['running'] = True
                # Contar pestañas
                import json
                data = json.loads(proc.stdout)
                status['kitty']['tabs'] = sum(
                    len(w.get('tabs', [])) for w in data
                )
        except Exception:
            pass

    return status


def unlink_config(user_config: str) -> Dict[str, Any]:
    """
    Elimina enlace simbólico de configuración.

    Args:
        user_config: Ruta de usuario (~/.config/kitty/kitty.conf)

    Returns:
        Dict con 'success' (bool), 'message' (str)
    """
    result = {
        'success': False,
        'message': ''
    }

    try:
        if os.path.islink(user_config):
            os.remove(user_config)
            result['success'] = True
            result['message'] = 'Enlace eliminado'
        else:
            result['success'] = True
            result['message'] = 'No existe enlace simbólico'
    except Exception as e:
        result['success'] = False
        result['message'] = f'Error: {str(e)}'

    return result

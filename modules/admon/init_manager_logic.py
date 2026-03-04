import os
import subprocess

def create_symlink(src, dst):
    try:
        if os.path.lexists(dst):
            os.remove(dst)
        os.symlink(src, dst)
        return {'success': True, 'message': 'Enlace creado exitosamente', 'target': src}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def reload_config(socket, config_path):
    try:
        cmd = ["kitty", "@", "--to", socket, "load-config", config_path]
        subprocess.run(cmd, check=True, capture_output=True)
        return {'success': True, 'message': 'Configuración recargada en Kitty'}
    except Exception as e:
        return {'success': False, 'message': f'Error recargando: {str(e)}'}

def unlink_config(dst):
    try:
        if os.path.lexists(dst):
            os.remove(dst)
            return {'success': True, 'message': 'Enlace eliminado'}
        return {'success': True, 'message': 'No existía enlace'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_status(tr_conf, user_conf, socket):
    # Lógica simplificada de estado
    return {
        'tr_config': {'exists': os.path.exists(tr_conf)},
        'symlink': {'exists': os.path.lexists(user_conf)},
        'socket': socket
    }

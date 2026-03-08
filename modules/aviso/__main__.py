#!/usr/bin/env python3
"""
AVISO - Sistema de Recordatorios y Alarmas
===========================================

Wrapper independiente para globalización.
"""

import os
import sys

# Añadir TR al PATH
TRON_PATH = os.path.expanduser("~/tron/programas/TR")
sys.path.insert(0, TRON_PATH)

# Importar y ejecutar CLI
from modules.aviso.aviso import main

if __name__ == "__main__":
    main()

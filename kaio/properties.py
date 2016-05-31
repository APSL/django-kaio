#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# bcabezas@apsl.net

"""
Importa todas las opciones para esta aplicacion como variables del modulo.
Pensado como parche para compatiblidad con properties actuales.
Todas las properties de app.ini quedaran como variables de properties

Ejemplo de uso desde properties.py:

from kaio.properties import *

"""

import sys
from kaio.options import Options

opts = Options()

thismodule = sys.modules[__name__]

for name, value in opts:
    setattr(thismodule, name, value)

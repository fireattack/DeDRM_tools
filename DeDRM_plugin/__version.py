#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#@@CALIBRE_COMPAT_CODE_START@@
import sys, os

# Explicitly allow importing everything ...
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Bugfix for Calibre < 5:
if "calibre" in sys.modules and sys.version_info[0] == 2:
    from calibre.utils.config import config_dir
    if os.path.join(config_dir, "plugins", "DeDRM.zip") not in sys.path:
        sys.path.insert(0, os.path.join(config_dir, "plugins", "DeDRM.zip"))

if "calibre" in sys.modules:
    # Explicitly set the package identifier so we are allowed to import stuff ...
    __package__ = "calibre_plugins.dedrm"

#@@CALIBRE_COMPAT_CODE_END@@

PLUGIN_NAME = "DeDRM"
__version__ = '10.0.9'

PLUGIN_VERSION_TUPLE = tuple([int(x) for x in __version__.split(".")])
PLUGIN_VERSION = ".".join([str(x)for x in PLUGIN_VERSION_TUPLE])
# Include an html helpfile in the plugin's zipfile with the following name.
RESOURCE_NAME = PLUGIN_NAME + '_Help.htm'
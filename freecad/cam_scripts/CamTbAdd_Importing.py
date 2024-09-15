# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.0.4  2024/09/13
__version__ = "V0.0.4  2024/09/13"


import importlib
class LazyLoader () :
    'thin shell class to wrap modules.  load real module on first access and pass thru'

    def __init__ (me, modname) :
        me._modname  = modname
        me._mod      = None
   
    def __getattr__ (me, attr) :
        'import module on first attribute access'

        if me._mod is None :
            me._mod = importlib.import_module (me._modname)
        
        return getattr (me._mod, attr)
    


def tba_import():
    CamTbAddLib = LazyLoader('freecad.cam_scripts.CamTbAddLib')

    import freecad.cam_scripts.naming_rules.ex_naming_rules as ex_rules


    # Two different naming rules schemes
    # BoboxxRulesShape is set as default for all imports.
    boboxx_rulesShape = ex_rules.BoboxxRulesShape(shape_name='endmill')
    exagerated_rules_example = ex_rules.ExageratedRulesExample(shape_name='endmill')

    # Large test import file:
    #    Attempts to imports 90 Tools & adds to current CAM Tool Library
    #       Imports 70/57 depending on whether example user shapes installed.
    # Other test files are in cutting_tool_data directory
    file1 = "cutting_tool_data/cuttingtools1.csv"

    print()
    print("Importing : ", file1)

    loaded, ignored = CamTbAddLib.importToolCsv(file1, boboxx_rulesShape, dbg_print=False)

    print()
    print("Imported {} Tool details & added to current library.".format(loaded))
    print("Skipped or failed to import {} rows in csv file.".format(ignored))


print(f"CamTbAdd_Importing - CAM ToolBit Import Library {__version__} module imported")


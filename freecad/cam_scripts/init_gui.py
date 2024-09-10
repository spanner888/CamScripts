# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.3  2024/09/10
__version__ = "2024-09-10"

import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from freecad.cam_scripts.translate_utils import translate
from functools import partial
import webbrowser


ICONPATH = os.path.join(os.path.dirname(__file__), "resources")
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources/translations")

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join( __dir__, 'Icons' )

import importlib

# FC has lazy_loader /FC_wkly-38622/squashfs-root/usr/lazy_loader.py
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
    

cfp = LazyLoader('freecad.cam_scripts.CamFullProcessExample')
ctba = LazyLoader('freecad.cam_scripts.CamTbAddExample')
ctba_import = LazyLoader('freecad.cam_scripts.CamTbAdd_Importing')


import os, platform, subprocess
from pathlib import Path as osPath




class GenericCmd(object):
    def __init__(self, cmd):
        self.cmdfunction = cmd['action']
        self.MenuTxt = cmd["name"]
        self.ToolTip = cmd["tool_tip"]
        # self.icon = cmd["icon"]   there is no ico k/val ATM!!


    def IsActive(self):
        """
        availability of the command (eg.: check for existence of a document,...)
        if this function returns False, the menu/ buttons are ßdisabled (gray)
        """
        # if App.ActiveDocument is None:
        #     return False
        # else:
        #     return True

        # no conditions for Camscripts - if any doc required script creates it!
        return True

    def GetResources(self):
        """
        resources which are used by buttons and menu-items
        """
        return {'Pixmap': getIcon(os.path.join(ICONPATH, "camscripts")), 'MenuText': self.MenuTxt, 'ToolTip': self.ToolTip}

    def Activated(self):
        """
        the function to be handled, when a user starts the command
        """
        # FIXME - os distinction not required or just not here???
        if self.MenuTxt.startswith("README"):
            if running_under_windows:
                self.cmdfunction(self.MenuTxt)
            elif running_under_macos:
                # Fingers crossed works on Mac
                self.cmdfunction(self.MenuTxt)
            else:
                # assume Linux
                self.cmdfunction(self.MenuTxt)
        else:
            self.cmdfunction()


def running_under_windows() -> bool:
    return os.name in ['nt', 'ce']


def running_under_macos() -> bool:
    return "darwin" in platform.system().casefold()


def display_readme(readme_name=""):
    if readme_name == "":
        readme_name = "README.md"

    if not readme_name.endswith(".md"):
        readme_name += ".md"

    #git_repo_url = "https://github.com/spanner888/CamScripts/blob/main/"
    file_url = "https://github.com/spanner888/CamScripts/"
    
    try:
        webbrowser.open(file_url, new=0, autoraise=True)
    except Exception as e:
        print(e)


def get_user_config(printing=True):
    import Path.Preferences as p_pref
    workingdir = os.path.dirname(p_pref.lastPathToolLibrary())
    s_dir_name = os.path.sep + "Shape" + os.path.sep

    from freecad.cam_scripts.CamScriptingLib\
        import users_material_cfg_summary as users_mat_cfg_summary
    mat_cfg_summary = users_mat_cfg_summary(printing)


    cfg_info = {"Tools_wd": workingdir, "Tools_sd": s_dir_name,
            "cam_script_dir": os.path.dirname(os.path.realpath(__file__))}
    cfg_info.update(mat_cfg_summary)

    if printing:
        print()
        print("User Tool Shape folder location: ", workingdir + s_dir_name)
        print()

        print(mat_cfg_summary)

        print()
        script_dir = osPath(App.getUserAppDataDir() + '/Mod/CamScripts/freecad/cam_scripts/')
        print(script_dir)
        print("Script support data in folders: '/cutting_tool_data' and '/naming_rules'")

    return cfg_info


def copy_files():
    print("copy files = TODO")

    cfg_info = get_user_config(printing=False)
    print(cfg_info)
    print()
    print(cfg_info["mat_cfg_summary"]["pref_use_mat_from_custom_dir"])
    print()

    # NB Change of Materials pref requires restart FreeCAD,
    #   as does changing Macro directory.
    if not cfg_info["mat_cfg_summary"]["pref_use_mat_from_custom_dir"]:
        mat_prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
        mat_prefs.SetString("CustomMaterialsDir",
                            cfg_info["cam_script_dir"] + os.path.sep + "cutting_tool_data")
        mat_prefs.SetBool("UseMaterialsFromCustomDir", True)
        print("CamScripts configured Materials Custom Directory")
    else:
        print("CamScripts attempted to set Materials Custom Directory, but")
        print("found this directory flagged as already in use!")
        print("You should change preference to use Material custom directory to be False,")
        print("then rerun the CamScripts 'Once only setup', or manualy copy the example files.")
        print("Settings have NOT been changed.")

    # import shutil
    # # Copy only files of default Path/Tool folder to working directory (targeting the README.md help file)
    # example_user_tool_shape_dir = os.listdir(defaultdir)
    #
    # for file_name in src_toolfiles:
    #     if file_name in ["README.md"]:
    #         full_file_name = os.path.join(defaultdir, file_name)
    #         if os.path.isfile(full_file_name):
    #             shutil.copy(full_file_name, workingdir)


    # ex CAM-Path-Tool-Gui-BitLibrary

    # tb_files = ["roughing_HRangles.fcstd", "pcb corncutters.fcstd", "Pcb drill.fcstd",
    #             "roughing.fcstd", "slotdrill.fcstd"]
    print(cfg_info["cam_script_dir"] + os.path.sep + "cutting_tool_data" + os.path.sep + "Shape")

    # src = "{}{}{}".format(defaultdir, os.path.sep, dir)
    # src_files = os.listdir(src)
    # for file_name in src_files:
    #     full_file_name = os.path.join(src, file_name)
    #     if os.path.isfile(full_file_name):
    #         shutil.copy(full_file_name, subdir)


def getIcon(iconName):
     return os.path.join( iconPath , iconName)


def updateMenu(workbench):
    wb_name = ""
    # WB names not translated: https://forum.freecad.org/viewtopic.php?t=90237&sid=5e5774ab5aa5813fc764fc360061d7c5
    if workbench == 'PathWorkbench':
        wb_name = "Path"
    elif workbench == 'CAMWorkbench':
        wb_name = "CAM"
    else:
        return

    if len(wb_name) > 0:
        # TODO setup to translate below.
        addonMenu = None
        wb_tail = "Workbench"
        addon_tail = "Scripts"
        dressupMenuName = "Path Dressup"
        action_tool_tip =" automation scripts"
        loaded_text = ' WB-addon GUI menus loaded into :'

        # Note for READMEs, name must match file name, less '.md'.
        scripts = {1: {"name": "CSV Import", 
                       "tool_tip": "CSV bulk Import with naming rules", 
                       "action": ctba_import.tba_import},
                   2: {"name": "ToolBit Examples", 
                       "tool_tip": "Create ranges of ToolBits", 
                       "action": ctba.ctba_example},
                   3: {"name": "Full Process Example",
                       "tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation", 
                       "action": cfp.cfp_example},
                   4: {"name": "README files in github repo",
                       "tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation",
                       "action": display_readme},
                   #5: {"name": "README Import CSV Tool data",
                       #"tool_tip": "How to import Tool data from CSV, and add to current Library Tool Table",
                       #"action": display_readme},
                   #6: {"name": "README Tool Bits Add Example",
                       #"tool_tip": "Create ToolBits and add to current Library Tool Table",
                       #"action": display_readme},
                   #7: {"name": "README Cam Full Process Example",
                       #"tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation",
                       #"action": display_readme},
                   #8: {"name": "README Naming Rules",
                       #"tool_tip": "How to use the naming rules to create names for your ToolBits & Libraries",
                       #"action": display_readme},
                   9: {"name": "Show config and script file locations",
                       "tool_tip": "So you can tailor CSV importing and examples to your requirements",
                       "action": get_user_config},
                  10: {"name": "Once only setup",
                       "tool_tip": "Copy example ToolShapes, Material and Material Model", 
                       "action": copy_files}
                   }
        
        addon_menu_title = wb_name + " " + addon_tail
        # ================================================================
        # Add Menus to very TOP FreeCAD menu strip/bar.
        menu_actions = []
        for k, v in scripts.items():
            cmd_name = wb_name + '_Scripts_' + v["name"].replace(" ", "")
            # To register the command in FreeCAD:
            cmd = GenericCmd(v)
            Gui.addCommand(cmd_name, GenericCmd(v))
            menu_actions.append(cmd_name)

        c=Gui.activeWorkbench()
        c.appendMenu("&Scripts", menu_actions)
        c.reloadActive()
        # ================================================================
        print(addon_menu_title + loaded_text, workbench)


Gui.getMainWindow().workbenchActivated.connect(updateMenu)

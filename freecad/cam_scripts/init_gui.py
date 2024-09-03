import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from freecad.cam_scripts.translate_utils import translate

ICONPATH = os.path.join(os.path.dirname(__file__), "resources")
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources/translations")

# TODO think about menu links to open installed DIR so user can read files.... (Dir as 3x scripts & 3xlibs = lotta file links)
#   hmm DIR open = some file tool - rely on any-OS-default ...or just copy path to clipboard & tell user?

# TODO translations - at least test works ...at THINK if should at extend to script messages...& libs???
# credit ...BASED on FS addon for code
__dir__ = os.path.dirname(__file__)
iconPath = os.path.join( __dir__, 'Icons' )

#init_complete = False

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
    
#import freecad.cam_scripts.CamFullProcessExample as cfp
#import freecad.cam_scripts.CamTbAddExample as ctba
#import freecad.cam_scripts.CamTbAdd_Importing as ctba_import
cfp = LazyLoader('freecad.cam_scripts.CamFullProcessExample')
ctba = LazyLoader('freecad.cam_scripts.CamTbAddExample')
ctba_import = LazyLoader('freecad.cam_scripts.CamTbAdd_Importing')


import os, platform, subprocess
from pathlib import Path as osPath

def running_under_windows() -> bool:
    return os.name in ['nt', 'ce']


def running_under_macos() -> bool:
    return "darwin" in platform.system().casefold()

# FIXME??? not working or used ditto 3xplatform functions above???
def display_folder_in_fm(which_directory: osPath) -> None:
    #assert isinstance(which_directory, osPath), "ERROR: Passed a non-Path to display_folder_in_wm()!"
    #assert which_directory.is_dir(), "ERROR! Passed a non-directory to display_folder_in_wm()!"

    if running_under_windows():
        os.startfile(os.path.normpath(which_directory))
    elif running_under_macos():
        subprocess.run(['open', str(which_directory)])
    else:
        # assume Linux or other POSIX-like
        res = subprocess.run(['xdg-open', str(which_directory)])
        #res = subprocess.run(['open', str(which_directory)])
        print(res)

def display_readme(readme_name=""):
    if readme_name == "":
        readme_name = "REAMDME.md"

    git_repo_url = "https://github.com/spanner888/CamScripts/"
    
    mod_dir = osPath(App.getUserAppDataDir() + 'Mod/')
    print(mod_dir)
    
    #just list file names or txt file, or just display txt ...
    #open readmes????? <<<use weblink to github ...FF not understand markdown & nobody has MD viewer!!!
    #**works on z4: subprocess.run(['open', 'https://github.com/spanner888/CamScripts/blob/main/README.md'], check=True)
    #README 1 Import CSV Tool data.md
    #README 2 Tool Bits Add Example.md
    #README 3 Cam Full Process Example.md

    #++link to issues
    #wiki??? https://github.com/spanner888/CamScripts/wiki

    git_repo_url = "https://github.com/spanner888/CamScripts/tree/main/"
    subprocess.run(['open', git_repo_url + readme_name])
    #>>> subprocess.run(['open', git_repo_url + 'README2.md'], check=True)
    #for git branch: subprocess.run(['open', 'https://github.com/spanner888/CamScripts/tree/morph-into-addon/README.md'], check=True)

    #but G: ie sanity issue!!!

    #so next is FILE COPIES => look at CAM checkworking directory!!! should be crossplatform

        #at least till get confidence dump lotsa ENV info about CURENT CAM Lib & materials prefs & dirs

        #find CURRENT Lib - tool/shape dir
        #find user mat dir, or crete temp custom...
        #& still ??? is Model
    
    # This entire function + support funcs ...poss in a COMMADN mod instead of leaving in init_gui???
    # if can easliy get comamdns working
    
    # mmmmm works on gpc which won't open sanity & vice versa!!!
    # display_folder_in_fm(mod_dir)
    # os.startfile(mod_dir)
    #TO morph info the file copies or 2x sep functions
    ## below in menu/action creation &/or here??? test for file presence and either:
    # & if present CHANGE menu to RE-INSTALL, not install...
    # & here...give msg?
    # pass


def display_info():
    import Path.Preferences as p_pref
    workingdir = os.path.dirname(p_pref.lastPathToolLibrary())
    s_dir_name = os.path.sep + "Shape" + os.path.sep
    print()
    print("User Tool Shape folder location: ", workingdir + s_dir_name)
    print()

    from freecad.cam_scripts.CamScriptingLib\
        import users_material_cfg_summary as users_mat_cfg_summary
    users_mat_cfg_summary()

    print()
    script_dir = osPath(App.getUserAppDataDir() + '/Mod/CamScripts/freecad/cam_scripts/')
    print(script_dir)
    print("Script support data in folders: '/cutting_tool_data' and '/naming_rules'")


def copy_files():
    print("copy files = TODO")


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
                   4: {"name": "README",
                       "tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation",
                       "action": display_readme},
                   5: {"name": "README Import CSV Tool data",
                       "tool_tip": "How to import Tool data from CSV, and add to current Library Tool Table",
                       "action": display_readme},
                   6: {"name": "README Tool Bits Add Example",
                       "tool_tip": "Create ToolBits and add to current Library Tool Table",
                       "action": display_readme},
                   7: {"name": "README Cam Full Process Example",
                       "tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation",
                       "action": display_readme},
                   8: {"name": "Show config and script file locations",
                       "tool_tip": "So you can tailor CSV importing and examples to your requirements",
                       "action": display_info},
                   9: {"name": "Once only setup",
                       "tool_tip": "Copy example ToolShapes, Material and Material Model", 
                       "action": copy_files}
                   }
        
        mw = Gui.getMainWindow()
        
        # Find the main path menu
        pathMenu = mw.findChild(QtGui.QMenu, "&" + wb_name)
        
        for menu in pathMenu.actions():
            if menu.text() == wb_name + wb_tail:
                # create a new addon menu
                addonMenu = menu.menu()
                break

        if addonMenu is None:
            addonMenu = QtGui.QMenu(wb_name + " " + addon_tail)
            addonMenu.setObjectName(wb_name + "_" + addon_tail)

            # Find the dressup menu entry
            dressupMenu = mw.findChild(QtGui.QMenu, dressupMenuName)

            #addonMenu.setTitle("Path Addons")
            pathMenu.insertMenu(dressupMenu.menuAction(), addonMenu)

        def create_action_submenu(addonMenu, addon_dict):
            # create an action (becomes sub-menu) for this addon
            action = QtGui.QAction(addonMenu)
            action.setText(addon_dict["name"])
            action.setIcon(QtGui.QPixmap(getIcon('camscripts')))
            action.setStatusTip(addon_dict["tool_tip"])

            # TODO change to command
            #action.triggered.connect(cfp.cfp_example)
            #action.triggered.connect(ctba.ctba_example)
            from functools import partial
            if addon_dict["action"] == display_readme:
                action.triggered.connect(partial(addon_dict["action"], addon_dict["name"] + '.md'))
            else:
                action.triggered.connect(addon_dict["action"])

            # append this addon to addon menu
            addonMenu.addAction(action)
           
        for k, addon_dict in scripts.items():
            create_action_submenu(addonMenu, addon_dict)
        
        #global init_complete
        #init_complete = True
        print(wb_name + " " + addon_tail + loaded_text, workbench)
    
    
class Camscripts(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """
    MenuText = translate("cam_scripts", "CamScripts")
    ToolTip = translate("cam_scripts", "a simple CamScripts")
    Icon = os.path.join(ICONPATH, "camscripts")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        # Add translations path
        Gui.addLanguagePath(TRANSLATIONSPATH)
        Gui.updateLocale()

        App.Console.PrintMessage(translate(
            "cam_scripts",
            "Switching to cam_scripts") + "\n")
        App.Console.PrintMessage(translate(
            "cam_scripts",
            "Run a numpy function:") + "sqrt(100) = {}\n".format(my_numpy_function.my_foo(100)))

        self.appendToolbar(translate("Toolbar", "Tools"), self.toolbox)
        self.appendMenu(translate("Menu", "Tools"), self.toolbox)

    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        App.Console.PrintMessage(translate(
            "cam_scripts",
            "Workbench cam_scripts activated.") + "\n")

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        App.Console.PrintMessage(translate(
            "cam_scripts",
            "Workbench cam_scripts de-activated.") + "\n")


Gui.getMainWindow().workbenchActivated.connect(updateMenu)
# Class not used if WB = Menu added to EXISTING WB
# Gui.addWorkbench(Camscripts())

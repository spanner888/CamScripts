import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from freecad.cam_scripts.translate_utils import translate
import freecad.cam_scripts.CamFullProcessExample as cfp
import freecad.cam_scripts.CamTbAddExample as ctba
import freecad.cam_scripts.CamTbAdd_Importing as ctba_import

ICONPATH = os.path.join(os.path.dirname(__file__), "resources")
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources/translations")

# TODO tranlsations
# credit ...BASED on FS addon for code
__dir__ = os.path.dirname(__file__)
iconPath = os.path.join( __dir__, 'Icons' )

#init_complete = False

def dummyTODO():
    #TO morph info the file copies or 2x sep functions
    ## below in menu/action creatrion &/or here??? test for file presence and either:
    # & if present CHANGE menu to RE-INSTALL, not install...
    # & here...give msg?
    pass

def getIcon(iconName):
     return os.path.join( iconPath , iconName)


def updateMenu(workbench):
    if workbench == 'CAMWorkbench':
        # above & below translate ...includes WB name ie 'CAMWorkbench'???
        addonMenu = None
        wb_name = "CAM"
        wb_tail = "Workbench"
        addon_tail = "Scripts"
        dressupMenuName = "Path Dressup"
        action_tool_tip =" automation scripts"
        loaded_text = ' Addon loaded into :'
        scripts = {1: {"name": "CSV Import", 
                       "tool_tip": "CSV bulk Import with naming rules", 
                       "action": ctba_import.tba_import},
                   2: {"name": "ToolBit Examples", 
                       "tool_tip": "Create ranges of ToolBits", 
                       "action": ctba.ctba_example},
                   3: {"name": "Full Process Example", 
                       "tool_tip": "Create and recreate every step of the CAM process, from tool creation to G-code generation", 
                       "action": cfp.cfp_example},
                   4: {"name": "Once only setup", 
                       "tool_tip": "Copy example ToolShapes, Material and Material Model", 
                       "action": dummyTODO}
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

        def create_action_submenu(addonMenu, wb_name, addon_dict):
            # create an action (becomes sub-menu) for this addon
            action = QtGui.QAction(addonMenu)
            action.setText(addon_dict["name"])
            #action.setIcon(QtGui.QPixmap(getIcon('camscripts')))
            action.setStatusTip(addon_dict["tool_tip"])

            # TODO change to command
            #action.triggered.connect(cfp.cfp_example)
            #action.triggered.connect(ctba.ctba_example)
            action.triggered.connect(addon_dict["action"])
            

            # append this addon to addon menu
            addonMenu.addAction(action)
           
        for k, addon_dict in scripts.items():
            create_action_submenu(addonMenu, wb_name, addon_dict)
        
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

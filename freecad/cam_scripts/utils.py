# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.0.4  2024/09/13
__version__ = "V0.0.4  2024/09/13"

from freecad.cam_scripts.translate_utils import translate
import webbrowser
import os, platform, subprocess
from pathlib import Path as osPath

__dir__ = os.path.dirname(__file__)
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources/translations")


def running_under_windows() -> bool:
    return os.name in ['nt', 'ce']


def running_under_macos() -> bool:
    return "darwin" in platform.system().casefold()


def display_readme():
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


def one_time_setup():
    cfg_info = get_user_config(printing=True)


    # FIXME: nasty
    #     if User tools not setup...copies insode squashfs/usr/Mod/Cam/Tools ...INTO DEFUALT TOOLS DIR
    #     ??Appiamgae whne uncompressed = READONLY!!!!
    #
    # consider triggering check working dir????
    # OR just chk if valid (reasonable???) dest_dir = cfg_info["Tools_wd"] + cfg_info["Tools_sd"]
    #
    # ***check BOTH tool & mat conditions then msg/bail out or proceed BOTH!!!!
    # ???++message already done if - shpe files PRESNET...but have to check all AND date stamps...
    #                                 & mat boolen and dir set???

    preconditions_failed = True
    # CHECK all conditions, output all messages for user to act on, less FC srestarts...
    # so code assumes
    source_dir = cfg_info["cam_script_dir"] + os.path.sep + "cutting_tool_data" + os.path.sep + "Shape"
    dest_dir = cfg_info["Tools_wd"] + cfg_info["Tools_sd"]
    print(source_dir)
    print(dest_dir)
    # TODO does source dir exist (??whith files?), does dest exist AND IS WRITAABLE?????

    # CHECK EACH ITEM
    mat_prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
    cust_mat_dir = cfg_info["cam_script_dir"] + os.path.sep + "cutting_tool_data"
    current_val = mat_prefs.GetString("CustomMaterialsDir", cust_mat_dir)
    #
    #
    if preconditions_failed:
        print("Please fix above issue(s), then run the 'CAM Scripts Once only setup' again.")
        return
    else:
        import shutil

        src_files = os.listdir(source_dir)
        for file_name in src_files:
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_dir)
        print()
        print("Example Tool shape files copied to ", dest_dir)
        print()

        # Update Mat setting LAST, so last msg is restart FC.
        # NB Change of Materials pref requires restart FreeCAD,
        #   as does changing Macro directory.
        if not cfg_info["mat_cfg_summary"]["pref_use_mat_from_custom_dir"]:
            print("Updating Material preference to use a Usere defined custom directory "
                "for Full Process Example - Machining Materials "
                "and extended Speeds Feeds calculations.")
            if len(current_val) > 0:
                print("Current dir: ", current_val)

            mat_prefs.SetString("CustomMaterialsDir", cust_mat_dir)
            mat_prefs.SetBool("UseMaterialsFromCustomDir", True)
            #FIXME at least while testin gvalidate above actually sET!!!!


            print("New dir:     ", cust_mat_dir)
            print("CamScripts configured Materials User defined custom Directory")
            print("Note: Current and New dirs are 'different', "
                "Please restart FreeCAD to enable this change!")
        else:
            print("CamScripts attempted to set Materials Custom Directory, but")
            print("found this directory flagged as already in use!")
            print("Current dir: ", current_val)
            print("You should change preference to use Material custom directory to be False,")
            print("then rerun the CamScripts 'Once only setup'.")
            print("Custom Dir setting has NOT been changed.")

        print("Setup completed, remember to switch to a TEST Tool Library Table!.")


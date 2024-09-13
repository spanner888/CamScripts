# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.0.4  2024/09/13
__version__ = "V0.0.4  2024/09/13"

import FreeCAD as App
from freecad.cam_scripts.translate_utils import translate
import webbrowser
import os, platform, subprocess
from pathlib import Path as osPath

__dir__ = os.path.dirname(__file__)
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources/translations")


def display_readme():
    #git_repo_url = "https://github.com/spanner888/CamScripts/blob/main/"
    file_url = "https://github.com/spanner888/CamScripts/"
    
    try:
        webbrowser.open(file_url, new=0, autoraise=True)
    except Exception as e:
        print(e)


# FIXME DELETE modded from: FreeCAD - Mod/CAM/Path/Tool/Gui/BitLibrarycheckWorkingDir()
def checkDirWritableXXX(workingdir):
    # Does dir exist & is writable

    return os.access(workingdir, os.W_OK)

    # if dirOK():
    #     return True
    # else:
    #     return False

    # below for ref ATM
    qm = PySide.QtGui.QMessageBox
    ret = qm.question(
        None,
        "",
        translate("CAM_ToolBit", "Toolbit working directory not set up. Do that now?"),
        qm.Yes | qm.No,
    )

    if ret == qm.No:
        return False

    msg = translate("CAM_ToolBit", "Choose a writable location for your toolbits")
    while not dirOK():
        workingdir = PySide.QtGui.QFileDialog.getExistingDirectory(
            None, msg, Path.Preferences.filePath()
        )

    if workingdir[-8:] == os.path.sep + "Library":
        workingdir = workingdir[:-8]  # trim off trailing /Library if user chose it

    Path.Preferences.setLastPathToolLibrary("{}{}Library".format(workingdir, os.path.sep))
    Path.Preferences.setLastPathToolBit("{}{}Bit".format(workingdir, os.path.sep))
    Path.Log.debug("setting workingdir to: {}".format(workingdir))

    # Copy only files of default Path/Tool folder to working directory (targeting the README.md help file)
    src_toolfiles = os.listdir(defaultdir)
    for file_name in src_toolfiles:
        if file_name in ["README.md"]:
            full_file_name = os.path.join(defaultdir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, workingdir)

    # Determine which subdirectories are missing
    subdirlist = ["Bit", "Library", "Shape"]
    mode = 0o777
    for dir in subdirlist.copy():
        subdir = "{}{}{}".format(workingdir, os.path.sep, dir)
        if os.path.exists(subdir):
            subdirlist.remove(dir)

    # Query user for creation permission of any missing subdirectories
    if len(subdirlist) >= 1:
        needed = ", ".join([str(d) for d in subdirlist])
        qm = PySide.QtGui.QMessageBox
        ret = qm.question(
            None,
            "",
            translate(
                "CAM_ToolBit",
                "Toolbit Working directory {} needs these sudirectories:\n {} \n Create them?",
            ).format(workingdir, needed),
            qm.Yes | qm.No,
        )

        if ret == qm.No:
            return False
        else:
            # Create missing subdirectories if user agrees to creation
            for dir in subdirlist:
                subdir = "{}{}{}".format(workingdir, os.path.sep, dir)
                os.mkdir(subdir, mode)
                # Query user to copy example files into subdirectories created
                if dir != "Shape":
                    qm = PySide.QtGui.QMessageBox
                    ret = qm.question(
                        None,
                        "",
                        translate("CAM_ToolBit", "Copy example files to new {} directory?").format(
                            dir
                        ),
                        qm.Yes | qm.No,
                    )
                    if ret == qm.Yes:
                        src = "{}{}{}".format(defaultdir, os.path.sep, dir)
                        src_files = os.listdir(src)
                        for file_name in src_files:
                            full_file_name = os.path.join(src, file_name)
                            if os.path.isfile(full_file_name):
                                shutil.copy(full_file_name, subdir)

    # if no library is set, choose the first one in the Library directory
    if Path.Preferences.lastFileToolLibrary() is None:
        libFiles = [
            f for f in glob.glob(Path.Preferences.lastPathToolLibrary() + os.path.sep + "*.fctl")
        ]
        Path.Preferences.setLastFileToolLibrary(libFiles[0])

    return True


def setup_custom_material_cfg():
    from freecad.cam_scripts.CamScriptingLib\
        import users_material_cfg_summary as users_mat_cfg_summary
    mat_cfg_summary = users_mat_cfg_summary(printing)

    preconditions_OK = True
    cust_mat_source_dir = cfg_info["cam_script_dir"] + os.path.sep +\
        "cutting_tool_data" + os.path.sep + "Resources"
    if not os.access(cust_mat_source_dir, os.W_OK):
        preconditions_OK = False
        print("cust_mat_source_dir issue not exist or not writable: ", cust_mat_source_dir)
    else:
        print("cust_mat_source_dir is OK: ", cust_mat_source_dir)

    # Check Materials prefs-CustomUserDir Ok to change,
    # warn if going to change.
    mat_prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
    if not mat_prefs.GetBool("UseMaterialsFromCustomDir", True):
        preconditions_OK = False
        print("CamScripts attempted to set Materials Custom Directory, but")
        print("found this directory flagged as already in use!")
        if len(current_val) == 0:
            print("Current custom dir value is empty and will be set once enabled via above setting.")
        else:
            print("Current custom dir value is: ", current_val)
        print("You should change preference to use Material custom directory to be False,")
        print("then rerun the CamScripts 'Once only setup'.")
        print("Custom Dir setting has NOT been changed.")

    if preconditions_OK:
        # Update Mat setting LAST, so last msg is restart FC.
        # NB Change of Materials pref requires restart FreeCAD,
        #   as does changing Macro directory.
        current_val = ''
        # if not cfg_info["mat_cfg_summary"]["pref_use_mat_from_custom_dir"]:
        #     mat_prefs.SetBool("UseMaterialsFromCustomDir", True)
        #     print("Enabled Materials to use Custom Dir")
        #
        # current_val = mat_prefs.GetString("CustomMaterialsDir", cust_mat_source_dir)
        # mat_prefs.SetString("CustomMaterialsDir", cust_mat_source_dir)
        # print("Changed Materials CustomMaterialsDir:")
        # print("From : ", current_val)
        # print("  To :", cust_mat_source_dir)
        # print("Please note the above 'From' directory location if you wish to restore it later.")
        print("Updating Material preference to use User defined custom directory "
            "for Full Process Example - Machining Materials "
            "and extended Speeds Feeds calculations.")
        if len(current_val) > 0:
            print("Current dir: ", current_val)

        mat_prefs.SetString("CustomMaterialsDir", cust_mat_source_dir)
        mat_prefs.SetBool("UseMaterialsFromCustomDir", True)
        #FIXME at least while testing validate above actually SET!!!!

        print("New dir:     ", cust_mat_source_dir)
        print("CamScripts configured Materials User defined custom Directory")
        print("Note: Current and New custom dirs are 'different'.")
        print("Setup completed, remember switch to a TEST Tool Library Table and restart FreeCAD!")
    else:
        print("Please fix above issue(s), then run this setup again.")
        print()
        return


def setup_custom_tool_shapes():
    import Path.Preferences as p_pref
    # CamScripts uses Last Tool Lib, not last ToolBit etc
    # becasue NEW TB added to current Lib Tool Table
    # which equates/equals Last Tool Lib
    # AND because the other prefs can/often point to dif locations!
    destTooldir = os.path.dirname(p_pref.lastPathToolLibrary())
    s_dir_name = os.path.sep + "Shape" + os.path.sep

    # Check shape files source & dest directories
    preconditions_OK = True
    source_dir = cfg_info["cam_script_dir"] + os.path.sep + "cutting_tool_data" + os.path.sep + "Shape"
    if not os.access(source_dir, os.W_OK):
        preconditions_OK = False
        print("source_dir issue not exist or not writable: ", source_dir)
    else:
        print("source_dir is OK: ", source_dir)

    dest_dir = cfg_info["Tools_wd"] + cfg_info["Tools_sd"]
    if not os.access(dest_dir, os.W_OK):
        preconditions_OK = False
        print("dest_dir issue not exist or not writable: ", dest_dir)
    else:
        print("dest_dir is OK: ", dest_dir)

    if preconditions_OK:
        # copy all shape files in source_dir,
        # UNLESS file same name exists in dest.
        import shutil
        src_files = os.listdir(source_dir)
        for file_name in src_files:
            s_full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(s_full_file_name):

                FIXME no msg skipping!!!!!
                ++split mat/shapes as users may need only DO one but not other
                ++rename checkDir to checkDirWritable...or just do inline!!!
                    becasue of below !!! ie inconsistent/confusings

                full_file_dest = os.path.join(dest_dir, file_name)
                if os.access(full_file_dest, os.F_OK):
                    print(f"Shape {file_name} already exists in {dest_dir}, NOT copied")
                else:
                    shutil.copy(s_full_file_name, dest_dir)
        print()
        print("Example Tool shape files copied to ", dest_dir)
        print()
        print("Setup completed, remember switch to a TEST Tool Library Table.")

    else:
        print("Please fix above issue(s), then run this setup again.")
        print()
        return


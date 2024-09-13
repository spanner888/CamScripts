# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.4  2024/09/13
__version__ = "V0.4  2024/09/13"

import FreeCAD
import Materials

# edit/save library without close/reopen FC.
from importlib import reload
import freecad.cam_scripts.CamScriptingLib as csl
reload(csl)

# Scripting Path workbench  https://forum.freecad.org/viewtopic.php?t=33328
import freecad.cam_scripts.JobUtils as JobUtils

from PySide import QtGui

def cfp_example():
    print("ToolBits created using tcProps1 & tcProps2 rely on the Toolbits from")
    print("    CamTbAddExample, Examples 1 and 2.")

    # =====================================================
    # USER settings
    # =====================================================
    clear_report_pane = True
    clear_console_pane = False

    # Optional information to print, set True if you get can't find material issues
    # Note you need very recent Weekly FreeCAD to include the Machinability materials
    print_mat_cfg_summary = False

    # ---------------------------------------------------------
    # Create some JOB properties & default values to set
    j_props = csl.job_props()

    j_props.jobname = "Job_ju_created"
    j_props.postProcessor = "grbl"
    j_props.postProcessorArgs = '--no-show-editor --no-comments --bcnc --translate_drill --preamble "G17 G40 G49 G90 G92.1 G94 G54 G21 F200" --postamble "G17 G90 M5 M9 M2"'

    # "%D/%d_%j_%O_%T_%t_%S.ngc"
    # If document is NOT saved, %D does not know the directory and forces file chooser to open
    # So using %M to save to users Macro directory.
    j_props.postProcessorOutputFile = "%M/%d_%j_%O_%T_%t_%S.ngc"

    # ** CARE default INTERNAL units are per SECOND.
    #    This is ONLY for Rapids, not Feeds - again CARE!!
    # Not changing mm/s as reminder when working in FreeCAD CAM!!!!
    # ** using divide by 60 to make it easier to use common mm/s values.
    j_props.hRapid = '400/60 mm/s'
    j_props.vRapid = '150/60 mm/s'
    # ---------------------------------------------------------

    # will be saved in directory set by above j_props.postProcessorOutputFile = "%M/%d_%j_%O_%T_%t_%S.ngc"
    sanity_report = 'CAM_sanity_check.html'


    # ---------------------------------------------------------
    # Add specified ToolBits as ToolControllers to the Job, & set some TC properties.
    # These require existing/matching ToolBits in the Users *current* Library.
    #   tcProps1 is found by using: bitName = "28120.0_8.12D_3F_endmill"
    #   tcProps2 is found by using: lib_tool_nr = 26350
    # The above Toolbits can be created by running:
    #   Example 1, 2 in CamTbAddExample.FCMacro
    tcProps1 = csl.tc_props()
                        
    tcProps1.bitName = "28120.0_8.12D_3F_endmill"
    # tcProps1.lib_tool_nr =        # Not used as adding this TC by name, not number
    tcProps1.hfeed = '200 mm/min'
    tcProps1.vfeed = '100 mm/min'

    # May overwritten by SpindleSpeed CALCULATED from Stock-material-machinability date
    tcProps1.spindleSpeed = 5000.0
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    tcProps2 = csl.tc_props()

    tcProps2.bitName = ""       # Not used as adding this TC by number, not name
    tcProps2.lib_tool_nr = 26350
    tcProps2.hfeed = '213 mm/min'
    tcProps2.vfeed = '123 mm/min'

    # May overwritten by SpindleSpeed CALCULATED from Stock-material-machinability date
    tcProps2.spindleSpeed = 5678.9
    # ---------------------------------------------------------
    # --------------------------------------------------------------------------
    # USER settings END ========================================================
    # --------------------------------------------------------------------------


    # ----------------------------------------
    # Output/Documentation helpers
    exampleNr = 1
    prefix = "JobUtils:"

    def printExPrefix(exampleNr, prefix="", ExampleDesc="", topRow=False, bottomRow=False):
        if topRow:
            print("-"*80)
        print("Example", exampleNr, prefix, ExampleDesc, end = ' ')
        exampleNr += 1
        if bottomRow:
            print("-"*80)
        return exampleNr

    #--------------------------------------------------------
    # Examples follow, one per block.
    #---------------------------------------------------------
    ExampleDesc="New doc & Job, optionaly clear report/python panes.\n\t\t\t"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=True, bottomRow=False)
    doc, job = csl.initDocJob(j_props, clear_console_pane, clear_report_pane)

    ExampleDesc="Add profile operation to specified job.\n\t\t\t"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=False, bottomRow=False)
    profile_op = csl.add_profile_op(job)

    ExampleDesc="Add profile operation & Boundary Dressup to specified job.\n\t\t"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=False, bottomRow=False)
    # NOTE: Dia of TC MUST position tool INSIDE the limiting boundary, else no gcode nor message!!
    # SEE: JobUtil test_01(): xNeg": 4.0,  # Ensure 2.5mm radius of default 5mm bit ...ditto yNeg prop.
    # Can see boundary visualy in FC by making Stock under DressupPathBoundary op visible!!
    profile_op1, dressup1 = csl.add_profile_op_with_boundary_dressup(job)
    # ---------------------------------------------------------


    # ---------------------------------------------------------
    ExampleDesc="Add ToolControllers to Job-Tools & desired Operation.\n\t\t"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=True, bottomRow=False)
    toolNames = csl.printAvailableLibraryTools()

    # Add Tools into Job as ToolControllers AFTER ALL operations,
    #   to avoid script pausing for user input to select desired ToolController.
    # This also reduces chance of error, as above sets SAME TC for ALL operations.
    tc1 = csl.addTc(job, tcProps1, byNr=False)
    if tc1 is None:
        return
    print("Set profile_op.ToolController to above TC+user scripted settings")
    profile_op.ToolController = tc1

    tc2 = csl.addTc(job, tcProps2, byNr=True)
    print("\tSet profile_op1.ToolController to above TC+user scripted settings")
    profile_op1.ToolController = tc2

    # recompute document
    JobUtils._set_visibility_and_view(doc, job)
    JobUtils.FreeCAD.ActiveDocument.recompute()
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # set some example printing vars & print header for RPM calc example
    prefix = "csl:"
    ExampleDesc="Job-Operation & TC props + Machinability data to calculate:\n\t\t\
    RPM, Vf(hor feed), Power, cutting torque"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=True, bottomRow=False)

    # Get the stock object of desired CAM-Job
    stk = doc.getObject("Stock")
    # materialManager = Materials.MaterialManager()

    if print_mat_cfg_summary:
        csl.users_material_cfg_summary()

    print()
    # If you see errors or exceptions from below, check FreeCAD preferences - Materials - Directories,
    # as you may need to disable "Use Materials from external workbenches" & "user defined directory"
    # save prefs and then restart FreeCAD.

    # HardWood
    csl.detailed_calcs('ba2474ee-f62c-45f5-b388-823ea105847f')

    print()
    # AluminumWroughtAlloy
    csl.detailed_calcs('5528dd01-e009-4e88-8c71-d5e9bbe8f7f3')
    print()

    # Example material needs to be installed in your User or Custom Materials dir
    # and the extension of machinability materials model also needs installing.
    # AlCastAlloyINHERITED+fz
    csl.detailed_calcs('5043f450-2158-4aa7-ba22-59f0db62e391')
    # ---------------------------------------------------------


    # ---------------------------------------------------------
    # set some example printing vars & print header for
    #   Sanity report and postprocess/save gcode example
    ExampleDesc="Create & save: CAM Sanity check report & Postprocessed gcode.\n\t\t"
    exampleNr = printExPrefix(exampleNr, prefix, ExampleDesc, topRow=True, bottomRow=False)

    csl.saveSanityreport(job, sanity_report)

    csl.postProcSaveGcode(job.PostProcessorOutputFile)

    # print trailing "line" to complete block outline of this example.
    print("-"*80)
    print("CamFullProcessExample.FcMacro finished.")
    # ---------------------------------------------------------

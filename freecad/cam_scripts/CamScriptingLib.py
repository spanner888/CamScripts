# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.0.4  2024/09/13
__version__ = "V0.0.4  2024/09/13"

import FreeCAD
import Path
# import JobUtils
import freecad.cam_scripts.JobUtils as JobUtils
import Path.Post.Utils as postutils
from PySide import QtGui
import webbrowser
import os

import Materials;
from math import sin, cos, acos, tan, atan, sqrt, pi
from math import degrees, radians, pi

__version__ = "2024-09-01"

   
# ---------------------------------------------------------------------------
# remove this block if get JobUtils updated to find Shape dir
# ...and five marked functions further down...
import Path.Tool.Bit as Bit
import freecad.cam_scripts.CamTbAddLib as CamTbAddLib

if FreeCAD.GuiUp:
    import Path.Main.Gui.Job as JobGui

    Job = JobGui.PathJob
    GUI_UP = True
else:
    import Path.Main.Job as Job

    GUI_UP = False

ToolController = Job.PathToolController
ToolBit = ToolController.PathToolBit
# ---------------------------------------------------------------------------


# ###################################################################
# Functions using JobUtils Library
def add_profile_op(job):
    # Add profile operation to job
    print(f"adding profile operation using top face, Face6.")
    p2 = JobUtils.add_profile_operation(
        job,
        [
            (
                job.Model.Group[0],
                [
                    "Face6",
                ],
            )
        ],
    )
    return p2


# Create of profile operation and boundary dressup
# Add profile operation to SAME job. If need new job, extract code from JobUtils. _testPrep()
def add_profile_op_with_boundary_dressup(job):
    # Add profile operation to job
    print(f"adding profile operation")
    p1 = JobUtils.add_profile_operation(job)

    # Add boundary dressup on profile operation
    print(f"adding boundary dressup on profile operation")
    d1 = JobUtils.add_dressup_boundary(
        p1,
        extendValues={
            "xNeg": 4.0,  # Ensure 2.5mm radius of default 5mm bit
            "xPos": -50.0,  # Cut off roughly half of 100mm test cube profile paths
            "yNeg": 4.0,  # Ensure 2.5mm radius of default 5mm bit
            "yPos": -50.0,  # Cut off roughly half of 100mm test cube profile paths
            "zNeg": 1.0,
            "zPos": 1.0,
        },
    )
    return p1, d1
# ###################################################################


# -------------------------------------------------------------------
#Helper functions
def clearConsolePane(clear=False):
    mw = FreeCAD.Gui.getMainWindow()
    if clear == True:
        pc = mw.findChild(QtGui.QPlainTextEdit,"Python console")
        pc.onClearConsole()


def clearReportPane(clear=False):
    mw = FreeCAD.Gui.getMainWindow()
    if clear == True:
        report = mw.findChild(QtGui.QTextEdit, "Report view")
        report.clear()


def printAvailableLibraryTools():
    print("JobUtils...", end = ' ')
    toolNames = JobUtils.available_tool_filenames()
    if len(toolNames) == 0:
        print("No tool files found.")
    return toolNames


# helper classes to make it easier to pass related properties
class job_props:
    def __init__(self):
        self.jobname = "Job"
        self.postProcessor = ""
        self.postProcessorArgs = ""
        self.postProcessorOutputFile = ""

        # ** CARE default INTERNAL units are per SECOND.
        #   This is ONLY for Rapids, not Feeds - again CARE!!
        # Not changing mm/s as reminder when working in FreeCAD CAM!!!!
        # ** using divide by 60 to make it easier to use common mm/s values.
        self.hRapid = '0/60 mm/s'
        self.vRapid = '0/60 mm/s'


class tc_props:
    def __init__(self):
        self.bitName = "Please add YOUR tool Name!"    # Not a TC prop, but for TC.Tool.Name
        self.lib_tool_nr = 1            # Not a TC prop, number of Tool in current Library
        self.hfeed = '0 mm/min'
        self.vfeed = '0 mm/min'
        self.spindleSpeed = 0.0
# -------------------------------------------------------------------


def initDocJob(job_props, clear_console_pane, clear_report_pane):
    clearConsolePane(clear=clear_console_pane)
    clearReportPane(clear=clear_report_pane)

    doc, job = JobUtils._testPrep()

    # -----------------------------------------------------------------
    # now apply your JOB properties/defaults
    job.Label = job_props.jobname
    job.PostProcessor = job_props.postProcessor
    # job.PostProcessor = "refactored_grbl"
    job.PostProcessorArgs = job_props.postProcessorArgs
    job.PostProcessorOutputFile = job_props.postProcessorOutputFile
    job.SetupSheet.HorizRapid = job_props.hRapid
    job.SetupSheet.VertRapid = job_props.vRapid
    # -----------------------------------------------------------------
    
    return doc, job


# ---------------------------------------------------------------------------
# remove this block if get JobUtils updated to find Shape dir
#modding from JobUtils
def _get_tool_by_number(number):
    """
    _get_tool_by_number(number)
    Arguments:
        number:  number of toolbit stored in tool library
    Returns a tool number and toolbit object as a tuple if the number is found.
    Taken from Path.Tool.Gui.BitLibrary.ModelFactory.findLibraries()
    """

    s_dir = None
    libraries = JobUtils._get_available_tool_library_paths()

    for libLoc, libFN, libFile in libraries:
        for toolNum, toolDict, bitPath in JobUtils._read_library(libFile):
            #print(toolDict)
            if toolNum == number:
                s_name = toolDict['shape']
                s_location, s_dir = CamTbAddLib.find_shape_location(s_name)
                toolBit = Bit.Factory.CreateFromAttrs(toolDict, toolDict["name"], s_dir)
                if hasattr(toolBit, "ViewObject") and hasattr(
                   toolBit.ViewObject, "Visibility"
                ):
                    toolBit.ViewObject.Visibility = False
                return (toolNum, toolBit)

    print(f"No tool found with number '{number}'")

    return None, None


def _get_tool_by_filename(name):
    """
    _get_tool_by_filename(name)
    Arguments:
        name: name of toolbit file without extension
    Returns a tool number and toolbit object as a tuple if the name file is found.
    Taken from Path.Tool.Gui.BitLibrary.ModelFactory.findLibraries()
    """

    s_dir = None
    libraries = JobUtils._get_available_tool_library_paths()
    for libLoc, libFN, libFile in libraries:
        for toolNum, toolDict, bitPath in JobUtils._read_library(libFile):
            loc, fnlong = os.path.split(bitPath)
            fn, ext = os.path.splitext(fnlong)
            if fn == name:
                s_name = toolDict['shape']
                s_location, s_dir = CamTbAddLib.find_shape_location(s_name)
                toolBit = Bit.Factory.CreateFromAttrs(toolDict, name, s_dir)
                if hasattr(toolBit, "ViewObject") and hasattr(
                    toolBit.ViewObject, "Visibility"
                ):
                    toolBit.ViewObject.Visibility = False
                return (toolNum, toolBit)

    print(f"No tool found with name '{name}'")

    return None, None


#modding from JobUtils
def _add_tool_to_job(job, tool):
    """
    _add_tool_to_job(job, tool)
    Arguments:
        job:  target parent job object for tool controller
        tool:  toolbit object as base for tool controller
    Adds a new tool controller based on the tool argument to the target job object provided.
    Code based on Path.Main.Gui.Controller.CommandPathToolController.Activated()
    """

    # Identify correct tool number
    toolNr = None
    for tc in job.Tools.Group:
        if tc.Tool == tool:
            toolNr = tc.ToolNumber
            break
    if not toolNr:
        toolNr = max([tc.ToolNumber for tc in job.Tools.Group]) + 1

    # Create tool controller object
    if FreeCAD.GuiUp:
        tc = ToolController.Create("TC: {}".format(tool.Label), tool, toolNr)
    else:
        tc = ToolController.Create(
            "TC: {}".format(tool.Label), tool, toolNr, assignViewProvider=False
        )

    # Add tool controller to job
    job.Proxy.addToolController(tc)
    FreeCAD.ActiveDocument.recompute()

    return tc


#modding from JobUtils
def add_toolcontroller_by_filename(job, name):
    """
    add_toolcontroller_by_filename(job, name)
    Arguments:
        job:  target parent job object for tool controller
        name:  filename (without extension) of file to be used as base for tool controller
    Adds a new tool controller based on the name argument to the target job object provided.
    Returns tool controller object.
    """
    tn, tool = _get_tool_by_filename(name)
    tc = _add_tool_to_job(job, tool)
    return tc


#modding from JobUtils
def add_toolcontroller_by_number(job, number):
    """
    add_toolcontroller_by_number(job, number)
    Arguments:
        job:  target parent job object for tool controller
        number:  number of tool as returned from 'available_tool_filenames()' to be used as base for tool controller
    Adds a new tool controller referenced by the number argument to the target job object provided.
    """
    tn, tool = _get_tool_by_number(number)

    return _add_tool_to_job(job, tool)
# ---------------------------------------------------------------------------


# Add ToolController using either Name or Library Tool Number
# and also set user defined TC properties.
def addTc(job, tcProps, byNr=False):
    tc = None
    try:
        if byNr:
            print("Add TC using tool#: '{}' and set h/v feeds & spindle speed."
                .format(tcProps.lib_tool_nr))
            tc = add_toolcontroller_by_number(job, tcProps.lib_tool_nr)
        else:
            if len(tcProps.bitName) < 1:
                print("Please add a bitName to tcProps")
                return tc
            
            print("Add TC using toolname: '{}' and set h/v feeds & spindle speed."
                .format(tcProps.bitName))

            tc = add_toolcontroller_by_filename(job, tcProps.bitName)
            tc.HorizFeed = tcProps.hfeed
            tc.VertFeed = tcProps.vfeed
            tc.SpindleSpeed = tcProps.spindleSpeed
    except:
        print("\t***Could NOT find above tool. Please review above \
'Available tool files' list.")

    return tc


# Retreive "Machinability" cutting data from
# early WIP in the new Materials WorkBench.
def get_extended_machinability(doc, mat_obj, tool_mat, tool_dia, printing=False):
    # Only using MaterialManager ATM, others left for later...
    ModelManager = Materials.ModelManager()
    MaterialManager = Materials.MaterialManager()
    uuids = Materials.UUIDs()

    q = FreeCAD.Units.Quantity

    # props = mat_obj.ShapeMaterial.PhysicalProperties
    props = mat_obj.PhysicalProperties
    # print(props)

    print("mat inf: ", mat_obj.Directory,
                       "\n\t\t\t\t\t",
                       mat_obj.LibraryName,
                       mat_obj.LibraryRoot)


    fzp= MaterialManager.getMaterial(mat_obj.Parent)
    print("parent inf:", fzp.Directory,
                        fzp.LibraryName,
                        fzp.LibraryRoot)


    # Test if this material supports Machinability model.
    tool_mat_nr = None
    vc_t_mat = None
    fz_t_mat = None
    if mat_obj.hasPhysicalModel(uuids.Machinability):
        if "ToolMat" in props:
            toolMats = mat_obj.getPhysicalValue("ToolMat")
            tool_mat_nr = toolMats.index(tool_mat)
            # print(toolMats, tool_mat_nr)
            # print(toolMats, toolMats[tool_mat_nr])

            # TODO can prob also address array cols by name!!!!

            # if mat_obj.hasPhysicalProperty('Vc2Column'):
            if "Vc" in props:
                Vc = mat_obj.getPhysicalValue("Vc")
                #vc_t_mat = q(Vc.Array[tool_mat_nr][1]).getValueAs("mm/min")
                vc_t_mat = q(Vc.Array[tool_mat_nr][1])
                print("Vc array data", Vc.Array)
                print("Vc for Tool Mat:", tool_mat, " is: ", vc_t_mat, Vc.Array[tool_mat_nr][1])
                # Vc2Column.Columns
                # Vc2Column.Rows
                # Vc2Column.getRow(1)
                print()

            # if mat_obj.hasPhysicalProperty('Fz3Column'):
            if "Fz" in props:
                Fz = mat_obj.getPhysicalValue("Fz")
                print("Fz.Array data:")
                for row in Fz.Array:
                    print("\t", row)

                d = tool_dia.Value
                # FC Quantity rightly complains at tool_dia^2 + tool_dia
                # as this is trying to add units m^2 to mm.
                # For now just using value until sort out units below.
                fz_t_mat = Fz.Array[tool_mat_nr][1] * d * d +\
                           Fz.Array[tool_mat_nr][2] * d +\
                           Fz.Array[tool_mat_nr][3]
                
                fz_t_mat = fz_t_mat * q("1 mm")
                print("Calculated Fz for Tool Mat:", tool_mat, " is: ", fz_t_mat)
                print()

            # Test to allow comparing with source data used
            # dias = [6,8,10,12,16,20]
            # for dia in dias:
            #     fz = dia*dia*Fz.Array[tool_mat_nr][1] + dia*Fz.Array[tool_mat_nr][2] + Fz.Array[tool_mat_nr][3]
            #     print(f"Pretend fz for {dia} dia tool :", fz)

        return vc_t_mat, fz_t_mat

    else:
        print(f"Material {mat_obj.name} does not support *extended* Machinability materials model")

    return None, None


def users_material_cfg_summary(printing=True):
    # Examine Users Material settings & Directories.
    from materialtools.cardutils import get_material_preferred_directory, get_material_preferred_save_directory
    from materialtools.cardutils import get_material_libraries

    mat_prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
    pref_use_built_in_materials = mat_prefs.GetBool("UseBuiltInMaterials", True)
    pref_use_mat_from_config_dir = mat_prefs.GetBool("UseMaterialsFromConfigDir", True)
    pref_use_mat_from_custom_dir = mat_prefs.GetBool("UseMaterialsFromCustomDir", True)
    pref_use_mat_from_ext_wb_dir = mat_prefs.GetBool("UseMaterialsFromWorkbenches", True)

    mat_dir = get_material_preferred_directory()
    save_dir = get_material_preferred_save_directory()
    if mat_dir is None:
        mat_dir = FreeCAD.getResourceDir() + "Mod/Material"

    if printing:
        print("Material Library summary:")
    for k, v in get_material_libraries().items():
        if printing:
            print(k, v)
    print()

    if printing:
        print("pref_use_built_in_materials {}".format(pref_use_built_in_materials))
        print("pref_use_mat_from_config_dir {}".format(pref_use_mat_from_config_dir))
        print("pref_use_mat_from_custom_dir) {}".format(pref_use_mat_from_custom_dir))
        print("pref_use_mat_from_ext_wb_dir) {}".format(pref_use_mat_from_ext_wb_dir))
        print("material_preferred_directory :", mat_dir)
        print("material_preferred_save_directory :", save_dir)

    mat_cfg_summary = {"mat_cfg_summary": {"pref_use_built_in_materials": pref_use_built_in_materials,
                       "pref_use_mat_from_config_dir": pref_use_mat_from_config_dir,
                       "pref_use_mat_from_custom_dir": pref_use_mat_from_custom_dir,
                       "pref_use_mat_from_ext_wb_dir": pref_use_mat_from_ext_wb_dir,
                       "material_preferred_directory": mat_dir,
                       "material_preferred_save_directory": save_dir}
                      }
    return mat_cfg_summary


def detailed_calcs(mat_uuid, print_machinability=False):
    # Both of github user: baehr pr's below are VERY informative & worth the read!
    # https://github.com/FreeCAD/FreeCAD/pull/15910
    # https://github.com/FreeCAD/FreeCAD/pull/16021
    # code below is based examples from above PRs.

    modelManager = Materials.ModelManager()
    materialManager = Materials.MaterialManager()
    uuids = Materials.UUIDs()

    if mat_uuid not in materialManager.materialsWithModelComplete(uuids.Machinability):
        if mat_uuid in materialManager.materialsWithModel(uuids.Machinability):
            print(f"Material does not have SOME properties for Machinability model")
            print("\t will attempt to calculate Speeds and Feeds!")
        else:
            # TODO show material name & maybe path/location
            print(f"Material does not use Machinability model, skipping....")
            return
    try:
        mat = materialManager.getMaterial(mat_uuid)
    except LookupError:
        print("Material mat_uuid not found, ignoring")
        return
        


    # ---------------------------------------------------------
    # PROPERTIES RETRIEVED FROM specified Operation (see below) & related TC-TB
    # TODO instead pass in Op

    # TODO need trap exceptions - NO TB is gaurenteed to have any of these Propeties!!!!
    # esp ToolRakeAngle, ToolHelixAngle
    doc = FreeCAD.ActiveDocument
    op = doc.getObject("Profile")
    # ToolDiameter = FreeCAD.Units.Quantity('3 mm')
    ToolDiameter = op.ToolController.Tool.Diameter
    # ToolNumberOfFlutes = 2
    ToolNumberOfFlutes = op.ToolController.Tool.Flutes
    ToolMaterial = op.ToolController.Tool.Material

    # ap = FreeCAD.Units.Quantity('5 mm') # depth of cut (axial)
    ap = op.StepDown

    if "HelixAngle" in op.ToolController.Tool.PropertiesList:
        ToolHelixAngle = op.ToolController.Tool.HelixAngle
        print(f"ToolBit {op.ToolController.Tool.FullName} "
              f"has HelixAngle, using value: {ToolHelixAngle}")
    else:
        ToolHelixAngle = FreeCAD.Units.Quantity('15°')
        print(f"ToolBit {op.ToolController.Tool.FullName} "
              "has no HelixAngle property, defaulting to 15°")

    if "RakeAngle" in op.ToolController.Tool.PropertiesList:
        ToolRakeAngle = op.ToolController.Tool.RakeAngle
        print(f"ToolBit {op.ToolController.Tool.FullName} "
              f"has RakeAngle, using value: {ToolRakeAngle}")
    else:
        ToolRakeAngle = FreeCAD.Units.Quantity('30°')
        print(f"ToolBit {op.ToolController.Tool.FullName} "
              "has no RakeAngle property, defaulting 30°")
    # ---------------------------------------------------------


    # ---------------------------------------------------------
    # currently HARCODED properties ...future work

    # TODO: book has fz vs dia tables
    ToolMaxChipLoad = FreeCAD.Units.Quantity('0.030 mm') # not a tool setting; differs per material! (ToolMaxTorque would be nice but no vendor specifies this. And for soft materials large chips jam the bit before max torque is reached)

    # SOME operations have StepOver, eg Pocket.
    # Profile & other Ops do not, so Not easy to get from FC doc/op.
    # 1st approx = distance from Model to outside of stock
    #   ...but that will NOT be constant distance, & ONLY for Profile Op
    # ..but that dist can be wider than tool dia...
    # Then there are offsets...
    ae = FreeCAD.Units.Quantity('3 mm') # width of cut (radial)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # User/Machine Limit/Setting - also could include:
    #   Min RPM or even a Torque curve to set min RPM at Load
    #   Max Spindle Power
    #   max Hor & Vert Feed rates

    # Spindle max RPM
    n_max = FreeCAD.Units.Quantity("20000/min")

    # OTHER user settings:
    # +++ User will want adjust - eg tool wear...
    #   Might be a global default, but really should be a PER TOOL, or for convience, per op/TC??
    eff = 0.85 # machine efficiency:
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Now get data from Material - Machinability properties:

    print("material :", mat.Name)
    print()
    
    vc_set = None
    fz = None
    vc_set, fz = get_extended_machinability(doc, mat,
                                        ToolMaterial,
                                        ToolDiameter,
                                        printing=print_machinability)

    kc11 = FreeCAD.Units.Quantity(mat.PhysicalProperties['UnitCuttingForce'])
    h0 = FreeCAD.Units.Quantity('1 mm') # unit chip thickness, per definition 1mm for k_c1.1
    mc = float(mat.PhysicalProperties['ChipThicknessExponent'])

    if vc_set is None:
        #vc_set = FreeCAD.Units.Quantity(mat.PhysicalProperties['SurfaceSpeedCarbide'])
        vc_set = FreeCAD.Units.Quantity(mat.PhysicalProperties['SurfaceSpeedHSS'])
        # vc_set.getValueAs("m/min")
        print("Using SurfaceSpeedHSS:", vc_set)
    # ------------------------------------------------------------------

    # project angle: https://math.stackexchange.com/questions/2207665/projecting-an-angle-from-one-plane-to-another-plane
    # not really worth taking the helix into account here; below 40° the effect is neglectable
    gamma_eff = degrees(atan(tan(ToolRakeAngle.getValueAs("rad")/cos(ToolHelixAngle.getValueAs("rad")))))
    gamma = ToolRakeAngle.getValueAs("deg")
    Kg = 1 - 0.01 * gamma_eff # correction factor for rake angle

    kapr = radians(90) # straight milling cutter, i.e. chamfer=90° aka no chamfer

    D = ToolDiameter

    phie = acos(1 - (2 * ae / D)) # engagement angle

    # TODO: honor chip-thinning: calculate fz from h_max (not h_mean!) when phi_e < 90°
    if fz is None:
        fz = ToolMaxChipLoad # feed per tooth
        print("Using default fz:", fz)
    
    Sb = D * pi * (phie / (2*pi)) # chip arc length
    hm = fz * (ae/Sb) * sin(kapr) # mean undeformed chip thickness using Cavalieri's principle

        # Book is Kver
    Kw = 1.2 # correction factor for tool wear:
             # 1 for new sharp tools,
             # 1.2 for used tools,
             # 1.5 for dull tools that need to be replaced

        # 4 corrections in all:
            # book/heremachine efficiency:
            # Kver/Kw Tool wear 1 to 1.5
            # Kgamma symbol/Kg Correction factor rake angle
            #     Kg = 1 - (g - g0)/100
            #     g0 basic rake angle: + 6° for steel, + 2° for cast iron
            #     g actual rake angle
            # Kvc/NONE Cutting speed correction factor
            #     lookup table
            #                         Vc range    Kvc
            #                         m/min
            #     HSS                 30 to 60    1.2
            #     HM (hardened Mat?)  60 to 300   1
            #     Ceramic             180 to 500  0.85
            # Ksp/NONE Chip compression correction factor
            #                 ^^??Chip thinning?? ...cf other refs for formula & MY work on MC...
            #                                                 moved into adjustemnts at end of work??
            #     Manufacturing process               Ksp
            #     External turning                    1.0
            #     Broaching, planing, slotting        1.1
            #     Drilling, milling, internal turning 1.2
            #     Parting off turning, plunge turning 1.3


    # lots lookups, even *nested lookups**,
    #    depends on Tool D/Mat, Rake, Vc, Cutting/Manufact process....
    # CAN BE broken into simpler steps as done throughout here
    # 2 corrections ignored (ie NOT used/applied) ATM
    # +++ User will want adjust - eg tool wear...
    # ++ INSERT style calculations and adv machining????
    kc = kc11 * (hm/h0)**-mc * Kg * Kw # specific cutting force machine efficiency:e

    Fcz = ap * hm * kc # cutting force per flute

    z = ToolNumberOfFlutes
    if z == 0:
        print("Warning Tool Bit Flutes = 0, this occurs if property not set in tool, or for Probes, which have not flutes.")
        print("This means Power, force & Torque outputs will be zero.")

    ze = phie * z / (2*pi) # engaged flutes

    Fc = Fcz * ze # cutting force

    n_set = vc_set / (pi * D) # spindle speed
    n_set.getValueAs("1/min")

    if n_set > n_max:
        print("INFO: Limiting Calculated RPM of {} to max setting of {}."
              .format(n_set.getValueAs("1/min").toStr(0),
                      n_max.getValueAs("1/min").toStr(0)))

    n = min(n_set, n_max)
    n.getValueAs("1/min")

    vc = n * (pi * D)
    vc.getValueAs("m/min")

    Pc = Fc * vc # mechanical cutting power

    P = Pc / eff # electrical spindle power
    P.getValueAs("kW")
    print("electrical spindle power ", P.getValueAs("kW").toStr(3), "kW")

    Mc = Fc * D / 2 # cutting torque (maybe better base this on h_max instead of h_mean?)
    Mc.getValueAs("Nm")
    print("Mc cutting torque", Mc.getValueAs("Nm").toStr(5),"Nm")


    vf = n * z * fz # feed rate
    print("vf ", vf.getValueAs("mm/min").toStr(0), "mm/min")
    # vf.getValueAs("mm/min")

    mrr=vf*ap*ae
    print("mrr ", mrr.toStr(0))


    #TODO return vals...


def saveSanityreport(job, sanity_report_name):
    print("Processing file outputs: Sanity Job common errors report & PostProcess Gcode")

    fg = postutils.FilenameGenerator(job)
    filepath = fg.qualified_path
    sanity_report = filepath + os.path.sep + sanity_report_name

    # FreeCAD/src/Mod/CAM/Path/Main/Gui/SanityCmd.py
    sanity_checker = Path.Main.Sanity.Sanity.CAMSanity(job, sanity_report)
    html = sanity_checker.get_output_report()

    if html is None:
        print("Sanity check failed. No report generated.")
        return
        #exit()

    with open(sanity_report, "w") as fp:
            fp.write(html)
    print("Sanity check report written to: {}\n".format(sanity_report))

    # webbrowser.open_new_tab(sanity_report)
    webbrowser.open(sanity_report, new=0, autoraise=True)


def postProcSaveGcode(postProcessorOutputFile):
    users_current_policy = Path.Preferences.defaultOutputPolicy()
    restore_users_current_policy = False
    if users_current_policy != "Overwrite existing file":
        Path.Preferences.setOutputFileDefaults(postProcessorOutputFile, "Overwrite existing file")
        restore_users_current_policy = True

    # TODO pass doc & names ...use below
    FreeCAD.Gui.Selection.addSelection('Test_JobUtils','Job')
    FreeCAD.Gui.runCommand('CAM_Post',1)

    if restore_users_current_policy:
        Path.Preferences.setOutputFileDefaults(postProcessorOutputFile, users_current_policy)


print(f"CamScriptingLib (CAM Scripting Library) {__version__} module imported")

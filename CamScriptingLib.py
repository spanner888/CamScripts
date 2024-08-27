# -*- coding: utf-8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 spanner888 <spanner888@usabledevices.com>          *
# *                                                                         *
# *   This file is a supplement to the FreeCAD CAx development system.      *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD
import Path
import JobUtils
from PySide import QtGui
import webbrowser
import sys, os

import Materials;
from math import sin, cos, acos, tan, atan, sqrt, pi
from math import degrees, radians, pi

# ---------------------------------------------------------------------------
# remove this block if get JobUtils updated to find Shape dir
# ...and five marked functions further down...
import Path.Tool.Bit as Bit
import CamTbAddLib

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

    def wtf(self):
        print("Hello  " + self.jobname)


class tc_props:
    def __init__(self):
        self.bitName = "Please add YOUR tool Name!"    # Not a TC prop, but for TC.Tool.Name
        self.lib_tool_nr = 1         # Not a TC prop, number of Tool in current Library
        self.hfeed = '0 mm/min'
        self.vfeed = '0 mm/min'
        self.spindleSpeed = 0.0

    def wtf(self):
        print("Hello  " + self.bitName + " " + self.tool_nr)
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
        #print(f"CS#166 {libLoc}, {libFN}, {libFile}")
        for toolNum, toolDict, bitPath in JobUtils._read_library(libFile):
            #print("CS#169", toolNum, toolDict, bitPath)
            loc, fnlong = os.path.split(bitPath)
            #print("CS#170")
            fn, ext = os.path.splitext(fnlong)
            #print(f"CS#173 {fn}, {ext}, {name}<<name is 3rd val")
            if fn == name:
                print()
                s_name = toolDict['shape']
                s_location, s_dir = CamTbAddLib.find_shape_location(s_name)
                #print("CS#180 s_dir: ", s_dir)
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

    return _add_tool_to_job(job, tool)


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
    #print("Add TC....{}, {}, {}".format(tcProps.bitName, tcProps.lib_tool_nr, byNr))

    # try:
    if byNr:
        print("Add TC using tool#: '{}' and set h/v feeds & spindle speed."
            .format(tcProps.lib_tool_nr))
        # tc = JobUtils.add_toolcontroller_by_number(job, tcProps.lib_tool_nr)
        tc = add_toolcontroller_by_number(job, tcProps.lib_tool_nr)
    else:
        if len(tcProps.bitName) < 1:
            print("Please add a bitName to tcProps")
            return
        print("Add TC using toolname: '{}' and set h/v feeds & spindle speed."
            .format(tcProps.bitName))
        # Allowing for User shapes in User Tools/Shapes,
        # must pass path to add_toolcontroller_by_filename ...then to FC Bit.ToolBitFactory.CreateFromAttrs
        # ....so at least for testing need copy/mod JobUtils _get_tool_by_filename & add_toolcontroller_by_filename
        # ????but was OK before helix/rake???? ...assume for now did not see issue...still need fix above

        # tc = JobUtils.add_toolcontroller_by_filename(job, tcProps.bitName)
        tc = add_toolcontroller_by_filename(job, tcProps.bitName)

        tc.HorizFeed = tcProps.hfeed
        tc.VertFeed = tcProps.vfeed
        tc.SpindleSpeed = tcProps.spindleSpeed
    # except:
    #     print("\t*Could NOT find above tool. Please review above \
    #         'Available tool files' list.", tc)
    #     print("Exiting macro!")
    #     sys.exit(1)

    return tc


#   >>>KEEP<<<< ACTIVELY USED!!!
# Retreive "Machinability" cutting data from
# early WIP in the new Materials WorkBench.
def get_mat_machinability(doc, mat_obj, printing=False):
    # Worked out below from Materials test code AND CAM-Sanity:
    machinining_props = ["SurfaceSpeedCarbide", "SurfaceSpeedHSS"]

    # Only using MaterialManager ATM, others left for later...
    ModelManager = Materials.ModelManager()
    MaterialManager = Materials.MaterialManager()
    uuids = Materials.UUIDs()

    q = FreeCAD.Units.Quantity

    SurfaceSpeedCarbide = None
    SurfaceSpeedHSS = None
    # if hasattr(mat_obj, "ShapeMaterial"):
        # if mat_obj.ShapeMaterial is not None:
    # m_name = mat_obj.ShapeMaterial.Name
    # if printing:
    #     print("Material machining summary for object: {}, material: {}.".format(mat_obj.Name, m_name))

    found_machinining_prop = False
    # props = mat_obj.ShapeMaterial.PhysicalProperties
    props = mat_obj.PhysicalProperties

    print(props)

    print("mat inf: ", mat_obj.Directory,
                mat_obj.LibraryName,
                mat_obj.LibraryRoot)


    fzp= MaterialManager.getMaterial(mat_obj.Parent)
    print("parent inf:", fzp.Directory,
                        fzp.LibraryName,
                        fzp.LibraryRoot)


    # Test if this material supports Machinability model.
    tool_mat_nr = None
    if mat_obj.hasPhysicalModel(uuids.Machinability):
        # FIXME FIXME ++ BIG NOTE: I have bodgied current Machinability model just appened my tests
        #     ***BUT same UUID and ONLY one material has new model props!!!!
        # fz.hasPhysicalProperty('ToolMat')
        # True
        # fz.hasPhysicalProperty('ToolMats')
        # False
        # BELOW has *two* dif wasy check if prop actually exists in the material
        # if mat_obj.hasPhysicalProperty('ToolMat'):

        # so if returned LISTS cointains uuid of curent material...not need for all the ifs & buts
        # MaterialManager.materialsWithModelComplete("9d81fcb2-bf81-48e3-bb57-d45ecf380096")
        # {'72814d63-f200-469b-9d99-5b6d9c526daa': <Material at 0x55def0347930>}

        if "ToolMat" in props:
            toolMats = mat_obj.getPhysicalValue("ToolMat")
            tool_mat_nr = toolMats.index("HSS")
            print(toolMats, tool_mat_nr)
            print(toolMats, toolMats[tool_mat_nr])

            # if mat_obj.hasPhysicalProperty('Vc2Column'):
            if "Vc2Column" in props:
                Vc = mat_obj.getPhysicalValue("Vc2Column")
                print(Vc.Array, q(Vc.Array[tool_mat_nr][1]).getValueAs("mm/min"))
                # Vc2Column.Columns
                # Vc2Column.Rows
                # Vc2Column.getRow(1)

            # if mat_obj.hasPhysicalProperty('Fz3Column'):
            if "Fz3Column" in props:
                Fz = mat_obj.getPhysicalValue("Fz3Column")
                print(Fz.Array, Fz.Array[tool_mat_nr][1],
                                Fz.Array[tool_mat_nr][2])

        if "SurfaceSpeedHSS" in props:
            m_ss_hss = q(props["SurfaceSpeedHSS"]).UserString
            found_machinining_prop = True
            SurfaceSpeedHSS = q(props["SurfaceSpeedHSS"])
            if printing:
                print("\tSurfaceSpeedHSS:     ", m_ss_hss)

        if "SurfaceSpeedCarbide" in props:
            m_ss_cbd = q(props["SurfaceSpeedCarbide"]).UserString
            found_machinining_prop = True
            SurfaceSpeedCarbide = q(props["SurfaceSpeedCarbide"])
            if printing:
                print("\tSurfaceSpeedCarbide: ", m_ss_cbd)

        if not found_machinining_prop:
            print("Material '{}' has no machining properties in list:\n\t\t\t{}\n".format(mat_obj.ShapeMaterial.Name, machinining_props))

        # >>>...TODO 2nd GOAL = EXPLORING ATM CASUAL TO GET BETTER IDEA OF APPROACH!!!
        #           eg mod this funtion to return materila obj to aid getting data for the adv calcs....
        # ATM 2 more props:  ChipThicknessExponent, UnitCuttingForce
        # BUT me want extend to 2x Arrays
        #     1 VcToolMat & SurfaceSpeed
        #     2 FzToolMat(no dup vars!!), fzIntercept, fzSlope <<<maybe 3x for polynomial(??)
        #     & ToolMat LIST only
        #     ++ all the advice/adj/.....
        # ...so maybe just validate basics of mat here & return the obj for detailed checks, then grab data...
        #     +++ all the inital plotting & curating & tweaking & ESP COMPARING...cf nsw code support script
        return SurfaceSpeedCarbide, SurfaceSpeedHSS

    else:
        print(f"Material {mat_obj.name} does not support Machinability materials model")

    return None, None

def users_material_cfg_summary():
    # Examine Users Material settings & Directories.
    from materialtools.cardutils import get_material_preferred_directory, get_material_preferred_save_directory

    mat_prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Material/Resources")
    use_built_in_materials = mat_prefs.GetBool("UseBuiltInMaterials", True)
    use_mat_from_config_dir = mat_prefs.GetBool("UseMaterialsFromConfigDir", True)
    use_mat_from_custom_dir = mat_prefs.GetBool("UseMaterialsFromCustomDir", True)
    use_mat_from_ext_wb_dir = mat_prefs.GetBool("UseMaterialsFromWorkbenches", True)

    mat_dir = get_material_preferred_directory()
    save_dir = get_material_preferred_save_directory()
    if mat_dir is None:
        mat_dir = FreeCAD.getResourceDir() + "Mod/Material"

    print("use_built_in_materials {}".format(use_built_in_materials))
    print("use_mat_from_config_dir {}".format(use_mat_from_config_dir))
    print("use_mat_from_custom_dir) {}".format(use_mat_from_custom_dir))
    print("use_mat_from_ext_wb_dir) {}".format(use_mat_from_ext_wb_dir))
    print("mat_dir :", mat_dir)
    print("save_dir :", save_dir)


def detailed_calcs(mat):
    # Both of github user: baehr pr's below are VERY informative & worth the read!
    # https://github.com/FreeCAD/FreeCAD/pull/15910
    # https://github.com/FreeCAD/FreeCAD/pull/16021
    # code below is based examples from above PRs.
    # ------------------------------------------------------------------
    #Related files:
        #Appearance/Wood.FCMat

        #Machining/BalsaWood.FCMat
        #Machining/HardWood.FCMat
        #Machining/MDFWood.FCMat
        #Machining/ParticleBoard.FCMat
        #Machining/SoftWood.FCMat

        #FIXME or wait for weekly release>>>>>  Standard/Wood/StandardWood.FCMat

    # #??possible install these + model??? ...and the metal mat files???
    # >>>so TRY ...do NOT add to sys/squashfs .... but user dir/s!!!!!!

    # Working cfgs ie prefs as shown & files in dir shown ...always need reload FC:
    #     19:26:02  use_built_in_materials True
    #     19:26:02  use_mat_from_config_dir True
    #     19:26:02  use_mat_from_custom_dir) True
    #     19:26:02  use_mat_from_ext_wb_dir) True
    #     19:26:02  mat_dir : /home/spanner888/.local/share/FreeCAD/CamScripts/materials-temp/

    # 19:32:15  use_built_in_materials True
    # 19:32:15  use_mat_from_config_dir True
    # 19:32:15  use_mat_from_custom_dir) False
    # 19:32:15  use_mat_from_ext_wb_dir) True
    # 19:32:15  mat_dir : /home/spanner888/Documents/_APPS_lappy/FC_wkly-38495/squashfs-root/appd_mlappy_new/Material



    # Do this first, so can have info if getting material fails.
    # FIXME: works as sep macro, max recursion depth error here!!!
    # ....well on first run here, now fine!!!
    # users_material_cfg_summary()

    # ---------------------------------------------------------
    # PROPERTIES RETREIVED FROM specified Operation or TC-TB
    # TODO instead pass in Op

    # FIXME need trap exceptions - NO TB is gaurenteed to have any of these Propeties!!!!
    # esp ToolRakeAngle, ToolHelixAngle
    op = FreeCAD.ActiveDocument.getObject("Profile001")
    # ToolDiameter = FreeCAD.Units.Quantity('3 mm')
    ToolDiameter = op.ToolController.Tool.Diameter
    # ToolNumberOfFlutes = 2
    ToolNumberOfFlutes = op.ToolController.Tool.Flutes

    # ap = FreeCAD.Units.Quantity('5 mm') # depth of cut (axial)
    ap = op.StepDown

    ToolHelixAngle = op.ToolController.Tool.HelixAngle
    ToolRakeAngle = op.ToolController.Tool.RakeAngle
    # ToolHelixAngle = FreeCAD.Units.Quantity('15°')
    # ToolRakeAngle = FreeCAD.Units.Quantity('30°')
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

    # Spindle max RPM = User/Machine Limit/Setting
    n_max = FreeCAD.Units.Quantity("20000/min")
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Now get data from Material - Machinability proprerties:
    print("material :", mat.Name)
    # print("Desc :", mat.Description)
    print()
    doc = FreeCAD.ActiveDocument
    get_mat_machinability(doc, mat, printing=True)
    print()

    kc11 = FreeCAD.Units.Quantity(mat.PhysicalProperties['UnitCuttingForce'])
    h0 = FreeCAD.Units.Quantity('1 mm') # unit chip thickness, per definition 1mm for k_c1.1
    mc = float(mat.PhysicalProperties['ChipThicknessExponent'])

    # vc = FreeCAD.Units.Quantity(alu.PhysicalProperties['SurfaceSpeedCarbide'])
    vc_set = FreeCAD.Units.Quantity(mat.PhysicalProperties['SurfaceSpeedCarbide'])
    # vc_set.getValueAs("m/min")
    # ------------------------------------------------------------------

    # project angle: https://math.stackexchange.com/questions/2207665/projecting-an-angle-from-one-plane-to-another-plane
    # not really worth taking the helix into account here; below 40° the effect is neglectable
    gamma_eff = degrees(atan(tan(ToolRakeAngle.getValueAs("rad")/cos(ToolHelixAngle.getValueAs("rad")))))
    gamma = ToolRakeAngle.getValueAs("deg")
    Kg = 1 - 0.01 * gamma_eff # correction factor for rake angle

    kapr = radians(90) # straight milling cutter, i.e. chamfer=90° aka no chamfer

    D = ToolDiameter

    phie = acos(1 - (2 * ae / D)) # engangement angle

    # TODO: honor chip-thinning: calculate fz from h_max (not h_mean!) when phi_e < 90°
    fz = ToolMaxChipLoad # feed per tooth

    Sb = D * pi * (phie / (2*pi)) # chip arc length
    hm = fz * (ae/Sb) * sin(kapr) # mean undeformed chip thickness using Cavalieri's principle

        # Book is Kver
    Kw = 1.2 # correction factor for tool wear:
             # 1 for new sharp tools,
             # 1.2 for used tools,
             # 1.5 for dull tools that need to be replaced

        # 4 corrections in all:
            # book/here
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


    # Complex lookups, even *nested lookups**,
    #    depends on Tool D/Mat, Rake, Vc, Cutting/Manufact process....
    # CAN BE broken into simpler steps as down throughout here
    # 2 corrections ignored ATM
    # +++ User will want adjust - eg tool wear...
    # ++ INSERT style calculations and adv machining????
    kc = kc11 * (hm/h0)**-mc * Kg * Kw # specific cutting force

    # ??extended calc?? for this with tool rotation angle ....for the vibration/force min/max/diag!!!
    Fcz = ap * hm * kc # cutting force per flute

    z = ToolNumberOfFlutes

    ze = phie * z / (2*pi) # engaged flutes # <<<<< STUDY ...prob NOT in ref to vibration/force min/max/diag

    Fc = Fcz * ze # cutting force	 	#<< max?? & not vary with angle.


    n_set = vc_set / (pi * D) # spindle speed
    n_set.getValueAs("1/min")

    if n_set > n_max:
        print("INFO: Limiting Calculated RPM of {} to max setting of {}."
              .format(n_set.getValueAs("1/min").toStr(0),
                      n_max.getValueAs("1/min").toStr(0)))

    n = min(n_set, n_max)
    n.getValueAs("1/min")
    print("RPM ", n.getValueAs("1/min").toStr(0), 'RPM')

    vc = n * (pi * D)
    vc.getValueAs("m/min")

    Pc = Fc * vc # mechanical cutting power

    eff = 0.85 # machine efficiency:
    P = Pc / eff # electrical spindle power
    P.getValueAs("kW")
    print("electrical spindle power ", P.getValueAs("kW").toStr(3), "kW")

    Mc = Fc * D / 2 # cutting torque (maybe better base this on h_max instead of h_mean?)
    Mc.getValueAs("Nm")
    print("Mc cutting torque", Mc.getValueAs("Nm").toStr(5),"Nm")


    vf = n * z * fz # feed rate
    print("vf ", vf.getValueAs("mm/min").toStr(0), "mm/min")
    vf.getValueAs("mm/min")

    #TODO return vals...


def saveSanityreport(job, sanity_report):
    print("Processing file outputs: Sanity Job common errors report & PostProcess Gcode")

    # FreeCAD/src/Mod/CAM/Path/Main/Gui/SanityCmd.py
    sanity_checker = Path.Main.Sanity.Sanity.CAMSanity(job, sanity_report)
    html = sanity_checker.get_output_report()

    if html is None:
        print("Sanity check failed. No report generated.")
        exit()

    with open(sanity_report, "w") as fp:
            fp.write(html)
    print("Sanity check report written to: {}\n".format(sanity_report))

    webbrowser.open_new_tab(sanity_report)


def postProcSaveGcode(postProcessorOutputFile):
    users_current_policy = Path.Preferences.defaultOutputPolicy()
    restore_users_current_policy = False
    if users_current_policy != "Overwrite existing file":
        Path.Preferences.setOutputFileDefaults(postProcessorOutputFile, "Overwrite existing file")
        restore_users_current_policy = True

    # FIXME pass doc & names ...use below
    FreeCAD.Gui.Selection.addSelection('Test_JobUtils','Job')
    FreeCAD.Gui.runCommand('CAM_Post',1)

    if restore_users_current_policy:
        Path.Preferences.setOutputFileDefaults(postProcessorOutputFile, users_current_policy)

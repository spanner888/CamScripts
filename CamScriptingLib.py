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

import Materials;
from math import sin, cos, acos, tan, atan, sqrt, pi
from math import degrees, radians, pi

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
        self.bitName = "tool bit"    # Not a TC prop, but for TC.Tool.Name
        self.lib_tool_nr = 1         # Not a TC prop, number of Tool in current Library
        self.hfeed = '0 mm/min'
        self.vfeed = '0 mm/min'
        self.spindleSpeed = 0.0

    def wtf(self):
        print("Hello  " + self.bitName + " " + self.tool_nr)


# Add ToolController using either Name or Library Tool Number
# and also set user defined TC properties.
def addTc(job, tcProps, byNr=False):
    tc = None
    #print("Add TC....{}, {}, {}".format(tcProps.bitName, tcProps.lib_tool_nr, byNr))

    try:
        if byNr:
            print("Add TC using tool#: '{}' and set h/v feeds & spindle speed."
                .format(tcProps.lib_tool_nr))
            tc = JobUtils.add_toolcontroller_by_number(job, tcProps.lib_tool_nr)
        else:
            print("Add TC using toolname: '{}' and set h/v feeds & spindle speed."
                .format(tcProps.bitName))
            tc = JobUtils.add_toolcontroller_by_filename(job, tcProps.bitName)

        tc.HorizFeed = tcProps.hfeed
        tc.VertFeed = tcProps.vfeed
        tc.SpindleSpeed = tcProps.spindleSpeed
    except:
        print("\t*Could NOT find above tool. Please review above \
            'Available tool files' list.", tc)
        print("Exiting macro!")
        exit(0)

    return tc


# Retreive "Machinability" cutting data from
# early WIP in the new Materials WorkBench.
def get_mat_machinability(doc, mat_obj, printing=False):

    # Worked out below from Materials test code AND CAM-Sanity:

    machinining_props = ["SurfaceSpeedCarbide", "SurfaceSpeedHSS"]

    # Only using MaterialManager ATM, others left for later...
    ModelManager = Materials.ModelManager()
    MaterialManager = Materials.MaterialManager()
    uuids = Materials.UUIDs()

    # doc = App.ActiveDocument
    shp = doc.getObject("Box")
    mdl = doc.getObject("Model-Cube")
    stk = doc.getObject("Stock")

    # print default material machinability info.
    # get_mat_machining_summary(obj, print_machinability)
    # get_mat_machining_summary(stk, print_machinability)

    # get material by known UUID
    # steel = MaterialManager.getMaterial("92589471-a6cb-4bbc-b748-d425a17dea7d")
    # get same material by path & Name.
    #   NB 'System' are default materials. ONE of other options is 'User'
    # mat = MaterialManager.getMaterialByPath('Standard/Metal/Steel/CalculiX-Steel.FCMat', 'System')

    # Machining has very DRAFT materials with SurfaceSpeedCarbide/HSS
    
    # OLDER bulds:    # mat = MaterialManager.getMaterialByPath('Machining/Aluminum-Cast.FCMat', 'System')
    
    # LATEST builds
    mat = MaterialManager.getMaterialByPath('Machining/AluminumCastAlloy.FCMat', 'System')

    # print(mat.Name)
    # Ideal = add material to shape, before creating Job.
    # But would need split library code (easy, but trying for msotly KISS here ATM)
    # Hence applay Material to bot shape & Job-Stock(which is used by CAM - Sanity report)

    # FYI: Machining model and materials.... button in the job dialog to assign a material.
    # https://github.com/FreeCAD/FreeCAD/pull/14460
    # Job - Setup - Layout ...need make pane WIDE...to see the little round material button!!!

    shp.ShapeMaterial = mat
    stk.ShapeMaterial = mat
    # obj.ShapeMaterial.Name
    # obj.ShapeMaterial.UUID

    # get from the Cube
    # get_mat_machining_summary(obj, print_machinability)
    #get from the Job Stock - which is used by the CAM Sanity report.

    q = FreeCAD.Units.Quantity

    SurfaceSpeedCarbide = None
    SurfaceSpeedHSS = None
    if hasattr(mat_obj, "ShapeMaterial"):
        if mat_obj.ShapeMaterial is not None:
            m_name = mat_obj.ShapeMaterial.Name
            if printing:
                print("Material machining summary for object: {}, material: {}.".format(mat_obj.Name, m_name))

        found_machinining_prop = False
        props = mat_obj.ShapeMaterial.PhysicalProperties
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

    # 1st goal try get ALL "tool/user settings from exsting TC etc...."
    # >>>...TODO 2nd GOAL = EXPLORING ATM CASUAL TO GET BETTER IDEA OF APPROACH!!!
    #           eg mod this funtion to return materila obj to aid getting data for the adv calcs....
    # TODO 3rd - is calc fz=chipload if so, COMPARE/PLOT calc to the telenbach{??} data eg in ods just created/plotted!!!
    # ATM 2 more props:  ChipThicknessExponent, UnitCuttingForce
    # BUT me want extend to 2x Arrays
    #     1 VcToolMat & SurfaceSpeed
    #     2 FzToolMat(no dup vars!!), fzIntercept, fzSlope <<<maybe 3x for polynomial(??)
    #     & ToolMat LIST only
    #     ++ all the advice/adj/.....
    # ...so maybe just validate basics of mat here & return the obj for detailed checks, then grab data...
    #     +++ all the inital plotting & curating & tweaking & ESP COMPARING...cf nsw code support script
    return SurfaceSpeedCarbide, SurfaceSpeedHSS


def calcRpm(tc, SurfaceSpeedCarbide, SurfaceSpeedHSS):
    #   Default TC-Tool DOES have Material: 'Generic material with density of 1'
    #   ...so expect FUTURE will have material AND more detailed Tool Machinability(other name?) properties.
    #   For now, use tc.Tool.Material & ONLY calc accoriding to that ie HSS tool or Carbide Tool
    if tc.Tool.Material == "HSS":
        ss = SurfaceSpeedHSS
    elif tc.Tool.Material == "Carbide":
        ss = SurfaceSpeedCarbide
    else:
        print("TC.Tool {} has invalid Tool material type: {} \
    ie is not 'HSS' or 'Carbide', exiting macro."
    .format(tc.Tool.Label, tc.Tool.Material))
        exit(0)

    rpm = ss / (tc.Tool.Diameter * pi)

    q = FreeCAD.Units.Quantity
    print("\t**Calculated** RPM for {} tool is {} RPM"
        .format(tc.Tool.Material, round(q(rpm).getValueAs('1/min'), 1)))
    # print()
    print("\tformula: SurfaceSpeed / (Diameter * math.pi)")
    print("\tNB: FreeCAD Units are all normalised in metric, so SurfaceSpeed*1000 is not required.")

    # print()
    print("Calculated SpindleSpeed RPM has not been set in ToolController SpindleSpeed.")
    print("You can do this manualy, or uncomment code in line below this print statement in the macro.")
    #TODO read print above - code to set calc rpm in TC
    return rpm

# now old - replacing with modded code from Wood PR
def calcLots_TO_RETIRE():
    #  https://github.com/FreeCAD/FreeCAD/pull/15910
    from math import acos, sqrt, sin
    from math import degrees, radians, pi
    import Materials;

    materialManager = Materials.MaterialManager()
    alu = materialManager.getMaterial('5528dd01-e009-4e88-8c71-d5e9bbe8f7f3')
    alu.Name
    alu.Description

    kc11 = FreeCAD.Units.Quantity(alu.PhysicalProperties['UnitCuttingForce']) # why is the property a string, not a Quantity as defined by the model???
    h0 = FreeCAD.Units.Quantity('1 mm') # unit chip thickness, per definition 1mm for k_c1.1
    mc = float(alu.PhysicalProperties['ChipThicknessExponent']) # why is the property a string, not a float as defined by the model???

    ToolRakeAngle = FreeCAD.Units.Quantity('20°')
    Kg = 1 - 0.01 * ToolRakeAngle.getValueAs("deg") # correction factor for rake angle

    ToolDiameter = FreeCAD.Units.Quantity('6 mm')
    D = ToolDiameter

    ae = FreeCAD.Units.Quantity('2.5 mm') # width of cut (radial)
    ap = FreeCAD.Units.Quantity('5 mm') # depth of cut (axial)

    ToolNumberOfFlutes = 3
    z = ToolNumberOfFlutes

    ToolHelixAngle = FreeCAD.Units.Quantity('35°')

    #kapr = radians(90 - ToolHelixAngle.getValueAs("deg")) # this looks wired! to be investigated
    kapr = radians(90) # straight milling cutter, i.e. chamfer=90° aka no chamfer

    fz = FreeCAD.Units.Quantity('0.03 mm') # feed per tooth

    phie = acos(1 - (2 * ae / D)) # engangement angle

    #hm = sqrt(ae/D) * fz * sin(kapr) # mean undeformed chip thickness; good approximation for ae << D; 20%-30% too large for ae=D
    Sb = D * pi * (phie / (2*pi)) # chip arc length
    hm = fz * (ae/Sb) * sin(kapr) # mean undeformed chip thickness using Cavalieri's principle

             # Book Kver
    Kw = 1.2 # correction factor for tool wear: 1 for new sharp tools, 1.2 for used tools, 1.5 for dull tools that need to be replaced
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

    # Extremely complex lookups, even *nested lookups**,
    #    depends on Tool D/Mat, Rake, Vc, Cutting/Manufact process....
    # CAN BE broken into simpler steps as down throughout here
    # 2 corrections ignored ATM
    # +++ User will want adjust - eg tool wear...
    # ++ INSERT style calculations and adv machining????
    kc = kc11 * (hm/h0)**-mc * Kg * Kw # specific cutting force

    # ??extended calc?? for this with tool rotation angle ....for the vibration/force min/max/diag!!!
    Fcz = ap * hm * kc # cutting force per flute

    ze = phie * z / (2*pi) # engaged flutes # <<<<< STUDY ...prob NOT in ref to vibration/force min/max/diag

    Fc = Fcz * ze # cutting force           #<< max?? & not vary with angle.

    vc = FreeCAD.Units.Quantity(alu.PhysicalProperties['SurfaceSpeedCarbide'])

    Pc = Fc * vc # mechanical cutting power

    eff = 0.85 # machine efficiency:
    P = Pc / eff # electrical spindle power
    print("electrical spindle power ", P.getValueAs("kW").toStr(3), "kW")

    Mc = Fc * D / 2 # cutting torque
    print("Mc cutting torque", Mc.getValueAs("Nm").toStr(5),"Nm")

    n = vc / (pi * D) # spindle speed
    print("RPM ", n.getValueAs("1/min").toStr(0), 'RPM')

    vf = n * z * fz # feed rate
    print("vf ", vf.getValueAs("mm/min").toStr(0), "mm/min")

    print("Console Hint: P, Mc, n, vf = CamScriptingLib.calcLots()\n after you 'import CamScriptingLib'")
    return P, Mc, n, vf


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
    users_material_cfg_summary()

    # TODO instead pass in Op
    op = doc.getObject("Profile001")

    op.ToolController.Tool.Diameter
    op.StepDown
    op.ToolController.Tool.Flutes


    ToolDiameter = FreeCAD.Units.Quantity('3 mm')
    ToolNumberOfFlutes = 2
    ToolRakeAngle = FreeCAD.Units.Quantity('30°')
    ToolHelixAngle = FreeCAD.Units.Quantity('15°')

    ToolMaxChipLoad = FreeCAD.Units.Quantity('0.030 mm') # not a tool setting; differs per material! (ToolMaxTorque would be nice but no vendor specifies this. And for soft materials large chips jam the bit before max torque is reached)

    ae = FreeCAD.Units.Quantity('3 mm') # width of cut (radial)
    ap = FreeCAD.Units.Quantity('5 mm') # depth of cut (axial)
    # ------------------------------------------------------------------


    print("material :", mat.Name)
    # print("Desc :", mat.Description)

    kc11 = FreeCAD.Units.Quantity(mat.PhysicalProperties['UnitCuttingForce'])
    h0 = FreeCAD.Units.Quantity('1 mm') # unit chip thickness, per definition 1mm for k_c1.1
    mc = float(mat.PhysicalProperties['ChipThicknessExponent'])

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
    Kw = 1.2 # correction factor for tool wear: 1 for new sharp tools, 1.2 for used tools, 1.5 for dull tools that need to be replaced
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

    # vc = FreeCAD.Units.Quantity(alu.PhysicalProperties['SurfaceSpeedCarbide'])
    vc_set = FreeCAD.Units.Quantity(mat.PhysicalProperties['SurfaceSpeedCarbide'])
    vc_set.getValueAs("m/min")

    n_set = vc_set / (pi * D) # spindle speed
    n_set.getValueAs("1/min")

    n_max = FreeCAD.Units.Quantity("30000/min")
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

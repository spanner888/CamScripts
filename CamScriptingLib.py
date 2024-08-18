#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
import Materials
import JobUtils
from PySide import QtGui
import math
import webbrowser

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
    # mat = MaterialManager.getMaterialByPath('Machining/Aluminum-Cast.FCMat', 'System')
    mat = MaterialManager.getMaterialByPath('Machining/Aluminum-6061.FCMat', 'System')

    # print(mat.Name)
    # Ideal = add material to shape, before creating Job.
    # But would need split library code (easy, but trying for msotly KISS here ATM)
    # Hence applay Material to bot shape & Job-Stock(which is used by CAM - Sanity report)
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

    rpm = ss / (tc.Tool.Diameter * math.pi)

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


def calcLots():
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

    Kw = 1.2 # correction factor for tool wear: 1 for new sharp tools, 1.2 for used tools, 1.5 for dull tools that need to be replaced

    kc = kc11 * (hm/h0)**-mc * Kg * Kw # specific cutting force

    Fcz = ap * hm * kc # cutting force per flute

    ze = phie * z / (2*pi) # engaged flutes

    Fc = Fcz * ze # cutting force

    vc = FreeCAD.Units.Quantity(alu.PhysicalProperties['SurfaceSpeedCarbide'])

    Pc = Fc * vc # mechanical cutting power

    eff = 0.85 # machine efficiency:
    P = Pc / eff # electrical spindle power
    print("electrical spindle power ", P.getValueAs("kW"), "kW")

    Mc = Fc * D / 2 # cutting torque
    print("Mc cutting torque", Mc.getValueAs("Nm"),"Nm")

    n = vc / (pi * D) # spindle speed
    print("RPM ", n.getValueAs("1/min"), 'RPM')

    vf = n * z * fz # feed rate
    print("vf ", vf.getValueAs("mm/min"), "mm/min")

    print("Console Hint: P, Mc, n, vf = CamScriptingLib.calcLots()")
    return P, Mc, n, vf

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






# DUMPING STUFF HERE TEMP UNTIL RE-ORG MAIN CALLIGN SCRIPT/S

# output substitions/ordering - wiki MISSING some subs
#     ++ missing some can be used in path &name & others ONLY path or only name
#     ++ some ONLY active if Job Order by FOR THAT SUBS {& MAYBE also need split by???}
# CAM-Path-Post-Utils.py
#         validPathSubstitutions = ["D", "d", "M", "j"]
#         validFilenameSubstitutions = ["j", "d", "T", "t", "W", "O", "S"]
#
#             "%D": os.path.dirname(self.job.Document.FileName or "."),
#             "%d": self.job.Document.Label,
#             "%j": self.job.Label,
#             "%M": os.path.dirname(FreeCAD.getUserMacroDir()),
#
#             "%d": self.job.Document.Label,
#             "%j": self.job.Label,
#             "%T": self.subpartname,  # Tool     \ name/# or TC/tb names?????
#             "%t": self.subpartname,  # Tool     /   gives -1
#             "%W": self.subpartname,  # Fixture
#             "%O": self.subpartname,  # Operation
#
#             %S ??? had idea was Fixture(s) but already W.
#               Currently = "0" in filename, WITH Split Output False
#
#                 ____0-G54 <<< Fixture ...also can see Job-Fixtures [G54]
#
# T, t, W, O: need select Job-output-"split" for these to work!!!
# & only ONE works at a time as only one order by level: Order by: Fixture, Tool, Operation
# -----------------------------------------------------------------







# *** SLIPTONIC IN 2017 ABOUT "data model" & MATERIALS...
#     IN THREAD: "Towards a feeds & speeds tool"
#     https://forum.freecad.org/viewtopic.php?t=23325
#
# hmmm new FC materials - MIGHT HAVE property "SpecificCuttingForce"...not yet populated
#     https://github.com/FreeCAD/FreeCAD/issues/14867 <<<ISSUE IS STILL OPEN!!!!!!
# ...above GOOD ...just renaming of UnitCuttingForce??
# ...but is NOT when SurfaceSpeeds introduced

# Machining model and materials #14460 https://github.com/FreeCAD/FreeCAD/pull/14460




# print(tc1.SpindleSpeed, tc2.SpindleSpeed)
# RPM_HSS_value = q(round(q(RPM_HSS).getValueAs('1/min'), 1)).Value
# RPM_CBD_value = q(round(q(RPM_CBD).getValueAs('1/min'), 1)).Value
# print(RPM_HSS_value, RPM_CBD_value)
# tc1.SpindleSpeed = RPM_HSS_value
# tc2.SpindleSpeed = RPM_CBD_value
# print(tc1.SpindleSpeed, tc2.SpindleSpeed)

# A cross check caulation using SurfaceSpeeds from a 3rd party calculator
# other_ss_hss = 146300 # mm/min
# other_ss_cbd = 331300 # mm/min
# no * 60 as Vc/ss NOT using FC.Quantity below
# otherRPM_HSS=(other_ss_hss) / (tc1.Tool.Diameter * math.pi)
# otherRPM_CBD=(other_ss_cbd) / (tc1.Tool.Diameter * math.pi)
# print("other_ss RPM HSS: {}, CBD: {}\n".format(otherRPM_HSS, otherRPM_CBD))
# other_ss RPM HSS: 19403, CBD: 43940 ....witihn ~1% of other calc.
# obj.Tool.Chipload << is NOT from material, but tool


# Related info....
# StepDown, Stepover, OpToolDiameter
# Hmmm FC Profile Op only does single layerxlayer cut top to bot,
# ie it has NO consideration of Stepover & multiple passes to clear outside stock
# MillFace op has StepOver (default=50%)
#
# 4Equations.csv
# calculated_output	        	     adjustment_var
# RPM=(Vc*1000) / (Tool_Dia * PI)	      Vc
#
# hFeed = RPM*chipload*Tool_Z	          chipload
# vFeed = RPM*chipload*Tool_Z	          chipload
#
# mrr=hFeed*ap*ae/1000	                  ap
# Power = mrr * kx	                      kx
# PowerFactor=Power*C
# PowerWear = Power*W
# PowerCutter = Power/E
# Torque = (Power*60*1000)/(PI*RPM)

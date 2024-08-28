# -*- coding: utf-8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Russell Johnson (russ4262) <russ4262@gmail.com>    *
# *                                                                         *
# *   This file is a supplement to the FreeCAD CAx development system.      *
# *                                                                         *
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
import os
import Path
import glob
import json
import Path.Tool.Bit as Bit

if FreeCAD.GuiUp:
    import Path.Main.Gui.Job as JobGui

    Job = JobGui.PathJob
    GUI_UP = True
else:
    import Path.Main.Job as Job

    GUI_UP = False


__title__ = "Job Utilities"
__author__ = "russ4262 (Russell Johnson)"
__url__ = ""
__doc__ = (
    "Path workbench utility functions to aid in job and tool controller scripting."
)
__version__ = "2024-02-25"
__freecad_revision_base__ = "32821"
__contributors__ = ""
__note__ = "This macro is based on updated Path code structure."

ToolController = Job.PathToolController
ToolBit = ToolController.PathToolBit


# Support functions
def _get_available_tool_library_paths():
    """
    Finds all the fctl files in a location
    Code based on Path.Tool.Gui.BitLibrary.ModelFactory.findLibraries()
    """

    path = Path.Preferences.lastPathToolLibrary()

    libraries = []
    if os.path.isdir(path):  # opening all tables in a directory
        libFiles = [f for f in glob.glob(path + os.path.sep + "*.fctl")]
        libFiles.sort()
        for libFile in libFiles:
            loc, fnlong = os.path.split(libFile)
            fn, ext = os.path.splitext(fnlong)
            libraries.append((loc, fn, libFile))

    # print(f"{libraries}")

    return libraries


def _read_library(path):
    """
    _read_library(path)
    Arguments:
        path:  path to library file
    Returns list of tuples, each containing toolbit information for the tool referenced in path file
    Code based on Path.Tool.Gui.BitLibrary.ModelFactory.__libraryLoad()
    """

    with open(path) as fp:
        library = json.load(fp)

    data = []
    for toolBit in library["tools"]:
        try:
            nr = toolBit["nr"]
            bit = ToolBit.findToolBit(toolBit["path"], path)
            if bit:
                tool = ToolBit.Declaration(bit)
                data.append((nr, tool, bit))
            else:
                FreeCAD.Console.PrintError(
                    "Could not find tool #{}: {}\n".format(nr, toolBit["path"])
                )
        except Exception as e:
            msg = "Error loading tool: {} : {}\n".format(toolBit["path"], e)
            FreeCAD.Console.PrintError(msg)

    return data


def _get_tool_by_number(number):
    """
    _get_tool_by_number(number)
    Arguments:
        number:  number of toolbit stored in tool library
    Returns a tool number and toolbit object as a tuple if the number is found.
    Taken from Path.Tool.Gui.BitLibrary.ModelFactory.findLibraries()
    """

    libraries = _get_available_tool_library_paths()

    for libLoc, libFN, libFile in libraries:
        for toolNum, toolDict, bitPath in _read_library(libFile):
            if toolNum == number:
                toolBit = Bit.Factory.CreateFromAttrs(toolDict)
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

    libraries = _get_available_tool_library_paths()

    for libLoc, libFN, libFile in libraries:
        for toolNum, toolDict, bitPath in _read_library(libFile):
            loc, fnlong = os.path.split(bitPath)
            fn, ext = os.path.splitext(fnlong)
            if fn == name:
                toolBit = Bit.Factory.CreateFromAttrs(toolDict)
                if hasattr(toolBit, "ViewObject") and hasattr(
                    toolBit.ViewObject, "Visibility"
                ):
                    toolBit.ViewObject.Visibility = False
                return (toolNum, toolBit)

    print(f"No tool found with name '{name}'")

    return None, None


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
    if GUI_UP:
        tc = ToolController.Create("TC: {}".format(tool.Label), tool, toolNr)
    else:
        tc = ToolController.Create(
            "TC: {}".format(tool.Label), tool, toolNr, assignViewProvider=False
        )

    # Add tool controller to job
    job.Proxy.addToolController(tc)
    FreeCAD.ActiveDocument.recompute()

    return tc


def _testPrep():
    """
    _testPrep()
    Returns new document with a cube and Job object based on cube.
    """
    doc = FreeCAD.newDocument("Test_JobUtils")

    # Create simple cube as base model for Job object
    cube = doc.addObject("Part::Box", "Box")
    cube.Length.Value = 100.0
    cube.Width.Value = 100.0
    cube.Height.Value = 100.0
    cube.Label = "Cube"

    # Create new Job object
    job = add_job([cube])

    print(f"Active document is {doc.Name} with {job.Name} object")

    return doc, job


def _set_visibility_and_view(doc, job):
    """
    _set_visibility_and_view(doc, job)
    **Intended to be used with test_xx() functions in this macro.**
    Turns on axis cross
    Toggles visibility of job model and stock.
    Sets view to ViewFit and Isometric
    No return value.
    """
    # Show axis cross and toggle visibilty of cube and Job model & stock
    if GUI_UP:
        import FreeCADGui

        doc.Box.ViewObject.Visibility = False
        job.Model.ViewObject.Visibility = True
        job.Stock.ViewObject.Visibility = True
        FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
        FreeCADGui.activeDocument().activeView().viewIsometric()
        FreeCADGui.SendMsgToActiveView("ViewFit")


# Public functions
def add_job(models=[], templateFile=None, useGui=False):
    """
    add_job(models=[], templateFile=None, useGui=False)
    Arguments:
        models:  list of model objects, or names of model objects
        templateFile:  template file name to be used
        useGui:  set True to interact with GUI during Job creation
    Adds a new Job object to the active document.
    """

    if GUI_UP:
        job = JobGui.Create(models, templateFile, openTaskPanel=useGui)
    else:
        job = Job.Create("Job", models, templateFile)

    FreeCAD.ActiveDocument.recompute()

    return job


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


def available_tool_filenames():
    """
    available_tool_filenames()
    Finds all the '.fctl' (FC tool library) files in last tool library location saved to FreeCAD preferences.
    Code based on Path.Tool.Gui.BitLibrary.ModelFactory.findLibraries()
    """

    available = []
    print("Available tool files:")

    for libLoc, libFN, libFile in _get_available_tool_library_paths():
        for toolNum, toolDict, bitPath in _read_library(libFile):
            loc, fnlong = os.path.split(bitPath)
            fn, ext = os.path.splitext(fnlong)
            available.append(fn)
            print(f"     {toolNum} ::   {fn}")

    print(" ")

    return available


def add_profile_operation(job, baseGeom=[], useGui=False):
    """
    add_profile_operation(job, baseGeom=[], useGui=False)
    Add profile operation to indicated job using provided baseGeom list.
    Arguments:
        job is pointer to receiving job
        baseGeom is list of tuples of format: (baseObj, [list_of_feature_names])
        useGui is boolean to enable use of GUI task panel for profile operation creation
    """

    if FreeCAD.GuiUp:
        import Path.Op.Gui.Profile as ProfileGui

        Profile = ProfileGui.PathProfile
        res = ProfileGui.Command.res
    else:
        import Path.Op.Profile as Profile

    FreeCAD.ActiveDocument.openTransaction("Create Profile")
    obj = Profile.Create("Profile", obj=None, parentJob=job)
    try:
        if FreeCAD.GuiUp:
            obj.ViewObject.Proxy = ProfileGui.PathOpGui.ViewProvider(
                obj.ViewObject, res
            )
            obj.ViewObject.Visibility = True
            if useGui:
                obj.ViewObject.Document.setEdit(obj.ViewObject, 0)
            else:
                obj.ViewObject.Proxy.deleteOnReject = False
        if baseGeom:
            for base, subs in baseGeom:
                for s in subs:
                    obj.Proxy.addBase(obj, base, s)
        FreeCAD.ActiveDocument.commitTransaction()
    except Exception as ee:
        print(f"{ee}")
        FreeCAD.ActiveDocument.removeObject(obj.Name)
        FreeCAD.ActiveDocument.abortTransaction()
        return None

    return obj


def add_dressup_boundary(
    baseOp,
    extendValues={
        "xNeg": 1.0,
        "xPos": 1.0,
        "yNeg": 1.0,
        "yPos": 1.0,
        "zNeg": 1.0,
        "zPos": 1.0,
    },
    useGui=False,
):
    """
    add_dressup_boundary(baseOp,
    extendValues={
        "xNeg": 1.0,
        "xPos": 1.0,
        "yNeg": 1.0,
        "yPos": 1.0,
        "zNeg": 1.0,
        "zPos": 1.0,
    },
    useGui=False)
    Add profile operation to indicated job using provided baseGeom list.
    Arguments:
        baseOp is pointer to the base operation
        extendValues is dictionary of "xNeg", "xPos", "yNeg", "yPos", "zNeg", and "zPos" values.
            Postive numbers increase boundary size for that direction,
            and negative numbers decrease boundary size for that direction.
            The job's existing stock is the basis for these boundary modifications.
        useGui is boolean to enable use of GUI task panel for profile operation creation
    """

    if FreeCAD.GuiUp:
        import Path.Dressup.Gui.Boundary as BoundaryGui

        Boundary = BoundaryGui.PathDressupPathBoundary
    else:
        import Path.Dressup.Boundary as Boundary

    FreeCAD.ActiveDocument.openTransaction("Create Boundary Dressup")
    obj = Boundary.Create(baseOp)
    obj.Stock.ExtXneg = extendValues["xNeg"]
    obj.Stock.ExtXpos = extendValues["xPos"]
    obj.Stock.ExtYneg = extendValues["yNeg"]
    obj.Stock.ExtYpos = extendValues["yPos"]
    obj.Stock.ExtZneg = extendValues["zNeg"]
    obj.Stock.ExtZpos = extendValues["zPos"]

    try:
        if FreeCAD.GuiUp:
            obj.ViewObject.Proxy = BoundaryGui.DressupPathBoundaryViewProvider(
                obj.ViewObject
            )
            obj.Base.ViewObject.Visibility = False
            obj.Stock.ViewObject.Visibility = False
            if useGui:
                obj.ViewObject.Document.setEdit(obj.ViewObject, 0)
            else:
                obj.ViewObject.Proxy.deleteOnReject = False
        FreeCAD.ActiveDocument.commitTransaction()
    except Exception as ee:
        print(f"{ee}")
        FreeCAD.ActiveDocument.removeObject(obj.Name)
        FreeCAD.ActiveDocument.abortTransaction()
        return None

    return obj


def set_job_origin_to_point(job, pnt):
    """
    set_job_origin_to_point(job, pnt)
    Arguments:
        job:  Job object to be adjusted
        pnt:  reference point to become new origin of Job object
    Sets the origin of the job to the given pnt argument.
    No return value
    Code based on Path.Main.Gui.Job.TaskPanel.alignSetOrigin()
    """
    import Draft

    move = FreeCAD.Vector().sub(pnt)

    # Move each model in Job
    for mdl in job.Model.Group:
        Draft.move(mdl, move)

    # Move Job Stock
    if job.Stock:
        Draft.move(job.Stock, move)


# Test functions
def test_00():
    """
    test_00()
    Simple test function test job creation,
    and tool controller addition functions in this macro.
    """
    print(f"test_00 test job creation, and tool controller addition functions")

    doc, job = _testPrep()

    # Identify available tools
    toolNames = available_tool_filenames()
    if len(toolNames) == 0:
        print("No tool files found.")
        return

    # Add tool by file name
    print(f"test_00 tool by name: {toolNames[3]}")
    add_toolcontroller_by_filename(job, toolNames[3])

    # Add tool by number from available tools list, above
    print(f"test_00 tool by number: 5")
    add_toolcontroller_by_number(job, 5)

    # recompute document
    _set_visibility_and_view(doc, job)
    FreeCAD.ActiveDocument.recompute()

    return job


def test_01():
    """
    test_01()
    Simple test function to test test creation of profile operation
    and boundary dressup in this macro.
    """
    print(f"test_01 test creation of profile operation and boundary dressup")

    doc, job = _testPrep()

    # Add profile operation to job
    print(f"test_01 adding profile operation")
    p1 = add_profile_operation(job)

    # Add profile operation to job
    print(f"test_01 adding second profile operation using top face, Face6.")
    p2 = add_profile_operation(
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

    # Add boundary dressup on profile operation
    print(f"test_01 adding boundary dressup on profile operation")
    d1 = add_dressup_boundary(
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

    # recompute document
    _set_visibility_and_view(doc, job)
    FreeCAD.ActiveDocument.recompute()

    return job


def test_02():
    """
    test_02()
    Simple test function test setting of job origin function in this macro.
    """
    print(f"test_02 test set job origin function")

    doc, job = _testPrep()

    # Set job origin to top-right corner of stock, (101.0, 101.0, 101.0)
    print(f"test_02 set job origin to point (101, 101, 101)")
    set_job_origin_to_point(job, FreeCAD.Vector(101.0, 101.0, 101.0))

    # recompute document
    _set_visibility_and_view(doc, job)
    FreeCAD.ActiveDocument.recompute()

    return job


print(f"Job Utilities {__version__} module imported")

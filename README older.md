https://wiki.freecad.org/Package_Metadata
Tags: CAM, Library, ToolBits, Bulk, Create
Tags: CAM, All, Job, Operations, Library, ToolControllers, ToolBits, Materials, Calculate, Speeds, Feeds, Sanity, Report, Gcode
spanner888@usabledevices.com

addon mgr - gui seems "v incomplete"
    ...doing most data by hand
    BUT NOT ALL showing in addon mgr-dev mode
addon mgr - suggest read meta from "main" file ...gues style like JobUtils
but doesn't the XML override???

addon mgr CAN show readme & images......
so xml = search/sort & prob fallback if readme not found??

TODO - before/after...or just say empty before screen shot of Lib TB
TODO - screen shot of EXPANDED Job tree
TODO - MAYBE code snippet/full console output



# FreeCAD CAM process end to end scripting
scripting all features complete end to end process

The included libraries and FreeCAD macros provide examples of all CAM steps to create a Job, Operations, ToolControllers, Sanity report postprocessed gcode and calculate Spindle RPM from Tool and Stock material properties. Many key properties are set to provide realistic FreeCAD Job and gcode.


desc one liner or more?
>>>DECIDE - 1 or TWO releases...but refer each other!!!!!

Fully automated creation of:
One or many ToolBits and add to current Tool Library.

script 1: CamLibTbAddExample.FCMacro Provides {four/Five WIHT IMPORT??} examples of single and bulk creation of ToolBits and adding to the current tool Library.

There is also one support example to retrieve properties & attributes of all shape files in FC Tool- Shape directory. This enables a user to script any property of any existing shape.

This script uses the provided CamLibTbAdd.py library to streamline the example code.

script 2: CamFullProcessExample.FcMacro

Uses the JobUtils library by @Russ4262 to demonstrate a wide range of FreeCAD CAM features.
It also adds examples that:
a) complete fully scripted CAM Job creation from start to end, including setting many properties for Job, Operations, ToolControllers and running Sanity & Postprocessing the gcode
b) calculate Spindle RPM from material-machinabilty and tool data. This is a simple example of early design work by Material and CAM workbench developers.


Script appear long at first glance but well over half the content is support for setting properties, printing some Example header information and licence etc.
The actual code to go from creating a moderately complicated Job, set a lot of properties for Job, Operations, ToolControllers and to run Sanity & Postprocess is relatively short.

The script uses the provided CamScripting.py library and also JobUtils.py (written by Russ4262) library to streamline the example code.

This script also can be used to test the newly created ToolBits from the CamLibTbAddExample.FCMacro script.

Sanity report and the gcode.

Job, Ops, ToolBits and add to current Tool Library, gcode & sanity output...just not EVERY Op & Dressup ATM

++Key properties are set, including Job..., Op-TC
The ToolController for each Operation and key properties.....

Features of JobUtils that are not demonstrated here are:
set_job_origin_to_point



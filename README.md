https://wiki.freecad.org/Package_Metadata
Tags: CAM, Library, ToolBits, Bulk, Create
Tags: CAM, All, Job, Operations, Library, ToolControllers, ToolBits, Materials, Speeds, Feeds, Sanity, Report, Gcode
spanner888@usabledevices.com

# Title

desc one liner or more?
>>>DECIDE - 1 or TWO releases...but refer each other!!!!!

Fully automated creation of:
One or many ToolBits and add to current Tool Library.

script#2 fetaures

script#2 Can, and as released, does test the newly created ToolBits from the Library, {say all below AGAIN...or "through all the above steps."}
    by adding to a Job, updating Speeds and Feeds, assigning to Operations, creating and saving both a CAM Sanity report and the gcode.

Job, Ops, ToolBits and add to current Tool Library, gcode & sanity output...just not EVERY Op & Dressup ATM

++Key properties are set, including Job..., Op-TC
The ToolController for each Operation and key properties.....

## Speeds and Feeds Demo.
New Materials Machinability model is used to set Job-Stock material, then retreive Machinability SurfaceSpeeds.
Calculate the Spindle RPM for either HSS or Carbide, based on ToolController.Tool.Material property. Note this is an existing ToolBit property, not a new Material object.

This a demonstration of the very early work to design Speeds and Feeds for FreeCAD. SEE XXXXX
In future the ToolController material, might be set via a "new Material", depending on how we all decide to progress Speeds and Feeds.


# Installation &

Install via the Addon manager in the macros section.

??Manual Installation:
Get from either of these locations below and copy content the folder into your FreeCAD macro directory.
Location: [forum thread ++TITLE??](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
Location: [Development repo FIX URL](https://github.com/shaise/FreeCAD_SheetMetal)

???content/files:  <<GET FROM ADDON MGR package.xml ...or make sure both agree!!!
FEATURES depends again of 1 or 2 sep releases!!!
uiashfhsadn: 1x Library NAME supplied
uiashfhsadn: 1x Library NAME supplied and depends

# Example Use
One example file is provided for each library, each containing several examples.

Both example files provide full automation, ie once user has set desired properties and actions, running each script requires no further user interaction.

## CamLibTbAdd Library
Example code is simple and focussed entirely on creating ToolBits (a file in the Bit directory)
and adding each ToolBit to the current ToolLibrary.

All examples show how to set all standard EndMill properties.
??How to get for other shapes <<<HAVE CODE FOR THAT in the lib????
add example ...if so cahnge wording above.

# -----------------------------------------------------------------------
# Doco/instructions:
    # Set desired....ops, TC & which TC for which Job
    #
    # script does everything
    # comment out/remove...
    # No need to create document or load any workbench.
    # Script creates an empty document, if no document already open,
    #   no changes are made to the document.

    # ToolBits are added to the current Tool Library.
    # Existing Toolbit file of same name will be overwritten.
    # Existing Tools in Library will NOT be overwritten,
    #     a new Tool will be added with same or partially same properties.
    #

# -----------------------------------------------------------------------

Example 1. Adds one Toolbit to the current library.
Example 2.
Example 3.

At present, customising the ToolBit or Library Tool numbering schemes will require editing the CamLibTbAdd Libray.

??TODO Import example??

Examples of how to add a ToolBit to a CAM Job ToolController and set which Operation uses a ToolController are contained in the [CamScripting Library]

## CamScripting Library
This library uses the excelent ....,
++extends the example provided to set several Job and Operation parameters, including Operation ToolController.

In addition
demo of new materials machinability use to calcualte spindle RPM
Creates and saves a CAM Sanity Job check report.
Creates and saves gcode for the job.

Note: First execution time using CamLibTbAddExample.FCMacro and it's two libraries can be up to 10 times longer eg 40 seconds, vs 4 seconds on my 12 year old laptop.

# Terminology
## FreeCAD CAM Tools/Bits/Shapes/Library Job-TC ++ for ju - Ops/materials/SF...
so sev sections????

# related FreeCAD CAM Terminology:
    # ToolBitLibrary: provides way to manage many libraries each with many Tools
    #   all organised/grouped as desired. eg Same TooBit can be in many Library-Tool-Tables.
    #   Each Library contains Tool Tables with ROWS of: Tn/Tool/Shape.
    # Tool-Bit = a cutting tool, with defined Shape properties,
    #       including a property for the underlying Tool-Shape file
    #       & other Tool-bit Properties such as number of flutes.
    #       The Tool-Bit shape is used in Operations and Simulators to
    #       "cut" the stock material to desired shape & size.
    # Tool-Shape file contains a sketch profile of cutting tool,
    #   with default Paramatised shape dimensions,
    #   that are updated from Tool-Bit properties.
    # Job-ToolController has properties for Rapids, Feeds, Speed
    #   and contains copy of the Tool-Bit used with all the specific sizes/properties.

#### References
* FreeCAD Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
* JobUtils.py Library Russ's lib Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
...all the materials

#### Release notes:
* V0.001  11 Jun 2015:  Initial version

alt format watch #### /### indents!!!
### 1.97
* accept PR from mario52
* set fixed width for some elements to prevent them getting too wide at times
* change backup file name formatting

## License
LGPL-2.1-or-later (see [LICENSE](LICENSE))

## About CamScripts

CamScripts macros create and configure *every* step of [FreeCAD CAM process](https://wiki.freecad.org/CAM_Workbench).

Image below shows output created by CamScripts macros including:

  - Import csv tool data to create Library ToolBits using different automatic naming and numbering rules,
  - Operations, ToolControllers, with key properties values set,
  - Assigning ToolControllers to Operations,
  - Speed and Feed example calculations from new Materials Machinabilty work is shown in report view.

PostProcessed gcode and Sanity check report were also created and saved, but not shown.

![Import, Rules, Full process condensed example](./images/Import_RulesFull_process.png)

## Special mention:

1. An Extensive ToolBit rule based naming system which allows use of ANY ToolBit property and allows setting order of each component as well as leading/trailing seperators and abbreviations.

  - For example:
    - 2F-D6.35-L31
    - 1F_D3.0-L50.0_endmill
    - 3F_D4.0-L50.0_roughing
    - 28600.0_8.6D_0F_860_em
    - Last item above also shows one example of an auto-numbered name.

  - A ridulous example used for testing imported Tools with uncommon properties:
      - 30000.0_0.0D4F_0.0CL__HSS__60.0deg_0.0CL_54.2L_8.0ND_5.0NH_0.0DS_td5.0deg_dovetail__
      - 30000.0_0.0D0F_0.0CL__HSS__90.0deg_0.0CL_20.0L_0.0DS_td1.0deg_v-bit__v-bit
      - 40000.0_10.0D3F_0.0CL__HSS__60.0deg_0.0CL_30.0L_6.0DS_td5.0deg_chamfer__
        - Note double underscores included above show missing properties in a ToolBit do not cause errors.

2. Demonstration of possiblities of FreeCAD CAM Speeds and Feeds calculations using the new Materials workbench and Material Machining Model containing cutting data, all of which are functional, but the design work and data collection, curation, documentation and inclusion are all at very early stages.

So please consider reading and contributing to all aspects of this work. For example see the FreeCAD Materials forum [Material overhaul](https://forum.freecad.org/viewtopic.php?t=78242).

Example macro code is simplified by two supplied python libraries and one excelent JobUtils library from russ4262 and also includes sample code from imm and jbaehr and of course FreeCAD developers of CAM new Materials workbenches.

## Documentation

To get all features, requires very recent FC v.....some warnings or errors may occur if older version of FreeCAD is use.

Easy install via single install....

?? Materials with late FC, BUT IF MY example MODS Tell user where/how/???

## Background informatiion

### FreeCAD CAM Terminology:
ToolBitLibrary: provides way to manage many libraries each with many Tools
  all organised/grouped as desired. eg Same TooBit can be in many Library-Tool-Tables.
  Each Library contains Tool Tables with ROWS of: Tn/Tool/Shape.
Tool-Bit = a cutting tool, with defined Shape properties,
      including a property for the underlying Tool-Shape file
      & other Tool-bit Properties such as number of flutes.
      The Tool-Bit shape is used in Operations and Simulators to
      "cut" the stock material to desired shape & size.
Tool-Shape file contains a sketch profile of cutting tool,
  with default Paramatised shape dimensions,
  that are updated from Tool-Bit properties.
Job-ToolController has properties for Rapids, Feeds, Speed
  and contains copy of the Tool-Bit used with all the specific sizes/properties.

### Machinability & RPM

The early work using the new Materials Workbench to add a default group of "Machining" materials, 8 common metal and 5 wood, that have "Machinability" properties is also demonstrated in the second script 'CamFullProcessExample.FcMacro'.

Spindle RPM <<MORE UPDATE is calculated, by retreiving ToolController material type of HSS or Carbide and then retreiving the corresponding HSS or Carbide surfaceSpeed from the Material data of the Job-Stock, which would be inherited from the design object.

Note "ToolController material type" is an existing ToolController property and is not a "new Material", but maybe in future, [follow or join the design process]()

In future the ToolController material, might be set via a "new Material", depending on how we all decide to progress Speeds and Feeds.

Note: The cutting machinability data and calculated RPM are real, usable values, but are not yet matched with background information on the expected machine capability and limitations. For example is the cutting machine:
* a very rigid milling machine, with 20kW spindle @20,000 RPM (as seen in many tool catalogs)
* a commercial hobby machine, by comparison not as rigid & maybe 1kW spindle @10,000 RPM
* a DIY milling machine with even less capability & rigidity
* a commercial/DIY routing machine, great for timber, plastics, but stretched to cut metals
* one of the many types of 3040 Engraver have even less ability than above

Implied by above is the need to adapt the cutting parameters such as Spindle RPM to the situation.

This is also demonstrated in Tool catalogs by all of the footnotes and asterix and appendix that provide some guidance on how to change the cutting parameters for a wide variety of situations.

These catalogs usually state that the data is "starting values" or some "maximum values" and maybe other.....


## References and Credits

* FreeCAD Forum announcement/discussion [thread](https://forum.freecadweb.org/)
* Material forum in particular [Material overhaul](https://forum.freecad.org/viewtopic.php?t=78242)
* JobUtils.py Library Russ's lib Forum announcement/discussion [thread](https://forum.freecad.org/viewtopic.php?t=33328)

The third library provides many of the core Job features for `CamFullProcessExample.FcMacro` was created by Russ..
Excelent example code is provided in this library in the Test## functions.
Those examples have been extended here with many aded features to give the full scripted end to end CAM process.

??++ He also worked on CAM changes to make scripting have less user intervention to answer dialogs...???

Path and Material developers and forum users including Russ, onekk, imm...


## Limitations, Feedback and Contributions

SEVERAL ALREADY ABOVE ...just remove the section????
See the github repo issues for latest information.


# Release notes:

* V0.1  2024-08-08:  Initial release
    * Initial release, 2 scripts/macros with 3 libraries and support information.
    * Scripting all features of FreeCAD CAM for a complete end to end process

* V0.1  2024-08-16:
            - Initial release
            - creates start to finish FreeCAD CAM process
            - demo of FreeCAD WIP Machinability materials properties and sample Speeds and Feeds calculations.
            - csv Tool import
            - scripted tool bit creation

## License

JobUtils Copyright (c) 2023 Russell Johnson (russ4262) <russ4262@gmail.com>, see [JobUtils](JobUtils.py)

All other files in CamScripts are Copyright 2024 Spanner888 and is licensed under GNU GPL (v2+) license, see [LICENSE](LICENSE).

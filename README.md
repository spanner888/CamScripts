## CamScripts for FreeCAD CAM

CamScripts automates many tasks in FreeCAD's CAM (Computer-Aided Manufacturing) environment including:

- Bulk create ToolBits from:

    - Imported CSV tool data
    - Defined ranges of Diameter and Flute count, or list of Shape types
    - Using very flexible naming rules and autonumbering for easy organisation
    - ToolBits are added to current FreeCAD Library Tool table

- Process Automation:

    - Create and recreate every step of the CAM process, from tool creation to G-code generation
    - Ensure consistent settings for tools, feeds, operations and postprocessors
    - Run sanity check report to review

- Showcase FreeCAD's new Machinability Materials and Model:

    - Provides underlying data and structure for machining calculations, ie Speeds and Feeds
    - Includes dataset for common metal and wood and wood-like materials
    - Demonstrate speeds and feeds calculations using the newly released Machinability Materials.
    - Explore an extended Machinability model for improved data flexibility through less code dependencies/changes and highlight areas for further discussion.

CamScripts provides a valuable toolkit for FreeCAD users seeking to improve efficiency and consistency in their CAM workflows.

![Import, Rules, Full process condensed example](./images/Import_RulesFull_process3.png)

## Special mention:

1. An Extensive ToolBit rule based naming system which allows use of ANY ToolBit property and allows setting order of each component as well as leading/trailing separators and abbreviations.

- For example:
  - 2F-D6.35-L31
  - 1F_D3.0-L50.0_endmill
  - 3F_D4.0-L50.0_roughing
  - 28600.0_8.6D_0F_860_em
  - Last item above also shows one example of an auto-numbered name.

- A ridiculous example used for testing imported Tools with uncommon properties:
    - 30000.0_0.0D4F_0.0CL__HSS__60.0deg_0.0CL_54.2L_8.0ND_5.0NH_0.0DS_td5.0deg_dovetail__
    - 30000.0_0.0D0F_0.0CL__HSS__90.0deg_0.0CL_20.0L_0.0DS_td1.0deg_v-bit__v-bit
    - 40000.0_10.0D3F_0.0CL__HSS__60.0deg_0.0CL_30.0L_6.0DS_td5.0deg_chamfer__
      - Note double underscores included above show missing properties in a ToolBit do not cause errors.
- Note that rules must create a valid filename for the ToolBit. Also it is best if filename is valid on any of the three supported platforms, avoid using \/:*?"<>| and non-printable characters such as the ASCII control-characters. Also avoid spaces and graphic characters.

2. FreeCAD CAM Speeds and Feeds calculation prototype example using the new Materials workbench and Material Machining Model containing the cutting data.

The cutting data is impressive due to it's coherence (for example: data for different sections can be matched to related sections, which is a common failing in many data sets) and also because of the notes on adapting the parameters for many different cutting conditions.

This is intended to inspire you to contribute to the design work, further data collection, curation and documentation.

A proof of concept Machinability model that could allow users to add new Tool material and coating data and data, without requiring code changes is also included.

So please consider reading and contributing to all aspects of this work. For example see the FreeCAD Materials forum [Material overhaul](https://forum.freecad.org/viewtopic.php?t=78242).

Example macro code is simplified by use of supplied python libraries and one excellent JobUtils library from russ4262. The macros also include use code from imm, jbaehr, russ4262 and of course FreeCAD developers of CAM and new Materials workbenches.

## Installing and using

CamScripts can be installed using the FreeCAD Addon Manager.  You must restart FreeCAD after installing CamScripts.

> [!CAUTION]
> Please create a test Library Tool Table before you run any of the scripts, which are the first three macros items. This stops test Tool data being added into your main ToolTable.

Before running any of the macros, it is best to open the CAM WorkBench.

Then open the FreeCAD macro manager to find the scripts, for example:

![CamScripts Macros](./images/CamScriptsMacros.png)

The fourth macro opens the github repository to show the main README information. There are more READMEs describing the import process and naming rules etc.

If you have not used the CAM workbench before and setup the default Tool directory and files, then:

- Create and empty FreeCAD document
- Open the CAM workbench
- Open Tool Library menu to trigger first time setup & copy. If you are not sure, accept all of the defaults including creating directories and copying files.
- This is also a good time to use the top left side + button to create a "Test" Tool table, so the example scripts doo not clutter the default ToolBit entries provided.

This repo also contains the files for the extended Machinability demonstration (within the CamScripts_3Full Process Example) and the example custom user shapes, including one containing Helix and Rake angles.

These latter files can be configured (the Materials) and copied (the Tool shapes) by using the FreeCAD macro manager to run the macros:

- CamScripts_5Setup_CustomToolShapes
- CamScripts_6Setup_CustomMaterialCfg

Output of the scripts:

- ToolbitAdd and Import scripts output messages to indicate ToolBits created, or skipped and also the actual
- ToolBit files in tools/Tool folder and Tools in the active Tool Library ToolTable
- FullProcess also creates a FreeCAD document with a simple shape CAM Job, Operations, Toolbits and many specific settings/properties
- Messages in report or notifications, often a lot, in part because the macros do a lot. Some more information is below.

You may notice random shapes flashing briefly on screen while running the Import and ToolBitAdd macros. This is normal and due to the need to briefly open the all system default CAM Tool Shapes and any User shape files. The FullProcess macro does create a lot of FreeCAD document objects and temporary views, so it has very active screen 'flashes'.

You may also notice that the FreeCAD cursor flashes and nothing else seems to be happening when running any of the scripts.
This is because these scripts are providing extended features including:

- Extracting all available Tool Shape properties, involves opening every default and user shape file, which are actually FreeCAD documents. This allows creation of ToolBits and setting values of any custom properties, including custom properties.
- CSV Import example also opens CSV file and attempts to create over 90 ToolBit files and Tool Library entries
- Full Process Example, tends to have more visible activity on screen, but can take a few seconds
- First run adds compile time, later runs are much faster

Some apparent warnings and errors are shown in FreeCAD report view and an example is shown below. These arise while opening ToolShape documents to extract Tool properties. These files all open and close without error manually, so current theory is that files are being closed rapidly prior to sketcher completing checks after document opened. These warnings can be safely ignored.

```
10:32:29  	Adding ToolBit Shape: v-bit, Dia: 0.0 Name: 2F_D0.0-L20.0_v-bit
10:32:29  Updating geometry: Error build geometry(6): Both points are equal
10:32:29  Invalid solution from SQP(augmented system) solver.
10:32:29  Sketch: Solving the sketch failed
10:32:29  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 4F_D3.0-L50.0_endmill
10:32:29  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 2F_D5.0-L50.0_endmill
10:32:29  	Adding ToolBit Shape: endmill, Dia: 1.5 Name: 4F_D1.5-L50.0_endmill
10:32:29  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
```


A very recent development version of 22.0dev or the 1.0RC is currently required. Dates and features added on that date are listed below:
2024-08-24  wood cards with machining model   commit bb01ec7f7c7eb54cf72a8fd2583de94e5cd22981
2024-08-18  metal cards with machining model  commit 70bb45430d30cb61d08ac0e7291d1b9a0e931a48
2024-07-9   Machining model and materials     revision 38314
2024-02     CSV Import may work 2024-02 with  revision 32821, but this is untested.

This limitation is due to the extent lot of changes in FreeCAD migrating Path to CAM and many fixes and enhancements, in the since late 2023.

In addition the new Materials Workbench is undergoing extensive development and has been progressively enhanced during the second quarter 2024.

Also during creation of these macro scripts, the extended Machinability example for Vc and in particular Fz was created to test more advanced features. These require a new material model and sample material with appropriate properties and they need to be setup as described above.

The extended model and material are included in the CamsScripts install directory in ```/cutting_tool_data/Ressources```

Some details of using and adapting each macro/example are within each macro, some in this file and some in:

![README 1 Import CSV Tool data](README_1_ImportCSVToolData.md)


## Background information

### FreeCAD CAM Terminology:

ToolBitLibrary: provides way to manage many libraries each with many Tools

  - all organised/grouped as desired. eg Same TooBit can be in many Library-Tool-Tables.
  - each Library contains Tool Tables with ROWS of: Tn/Tool/Shape.

Tool-Bit = a cutting tool, with defined Shape properties:

  - including a property for the underlying Tool-Shape file
  - other Tool-bit Properties such as number of flutes.
  - The Tool-Bit shape is used in Operations and Simulators to "cut" the stock material to desired shape & size.
  - Tool-Shape file contains a sketch profile of cutting tool, with default Paramatised shape dimensions that are updated from Tool-Bit properties.

Job-ToolController has properties for Rapids, Feeds, Speed and contains copy of the Tool-Bit and shape used with all the specific sizes/properties.

### Machinability & CAM Speeds and Feeds

The early work using the new Materials Workbench to add a default group of "Machining" materials, includes 8 common metal and 5 wood(ish) materials, that have "Machinability" properties is demonstrated in the second script 'CamFullProcessExample.FcMacro' in "Example 5 CamScriptingLib: Job-Operation & TC props + Machinability data to calculate".

Cutting settings such as ToolController Diameter and ap or StepDown are retreived from the CAM-Job and other cutting data such as Vc or SurfaceSpeed etc is retrieved from the selected material.

One property not yet retrieved is ae or StepOver, as that is only available directly in some Operations, such as Pocket. In other Operations such as Profile this will require thought as to how this property should be managed.

If the ToolBit has Rake or Helix angle properties, then that data will be used instead of fixed defaults. This requires Tool shape files with those properties and the specific values. Some example files are included.

Another property with only a fixed example value in the default Example 5 is fz, commonly known as chipload.

Example output is shown below.
```
  ToolBit has no HelixAngle property, defaulting to 15°
  ToolBit has no RakeAngle to property, defaulting 30°
  material : AluminumWroughtAlloy
  RPM  13534 RPM
  electrical spindle power  0.942 kW
  Mc cutting torque 0.56494 Nm
  vf  1624 mm/min
  mrr  516 mm^3/s
```

Example 5 can also be extended with a different materials model, MachinabilityFz.yml, to store Vc and fz data. This model is more flexible , allowing users to simply add new Tools with different material and coatings and the detailed data, without require changes to the code.

To use the extension to example 5, requires installing the above model and sample material. Example 5 also needs to be changed to use the AlCastAlloyINHERITED+fz material. Then the new data will be used to retrieve Vc and Fz and the vf, the horizontal feed calculation will be improved with tool-material specific data, instead of a current example fixed value.

The proposed approach uses Materials arrays and a look up table to retieve the Tool Material name.

Also suggested is a way to simple store fz data as parameters from a linear or 2nd level polynomial regression of the data. This has benefit of not requiring interpolation later, and does allow for example using metric tools if you only have imperial sized tool data and vice versa, as well as any intermediate tool size not in the orignial data. Tool sizes outside the original data can also be used, but with more caution, especially for smaller tools approaching "micromilling"...which is a very loosely defined, but important concept.

The biggest advantage of plotting the fz data, is that it highlights errors, are more common than expected, even from very high end manufacturers, and also make it easier to compare data from other sources as well as more confidently tailor the data to your needs.

Further automation of this task to plot source data, aid analysis and linear (etc) regression has commenced but on long waiting list.

Note extended changes above change both the Machinability model and materials and provided example updates to CAM default shapes to hold the required Tool properties. This part of the work is entirely my own ideas and included purely to aid design thinking and feedback to FreeCAD.

Output using Extended Machinability Model and Material, includes detailed Vc and Fz raw data.

```
ToolBit: Test_JobUtils#_F_D6_4_L50_0_roughing_HRangles , has HelixAngle, using value: 17.2 deg
ToolBit: Test_JobUtils#_F_D6_4_L50_0_roughing_HRangles , has RakeAngle, using value: 29.9 deg
material : AlCastAlloyINHERITED+fz

mat inf:  Material/Machining/AlCastAlloyINHERITED+fz.FCMat
	 Custom /home/spanner888/.local/share/FreeCAD/Mod/CamScripts/freecad/cam_scripts/cutting_tool_data/Resources
parent inf: Machining/AluminumCastAlloy.FCMat System /tmp/.mount_FC_wkljiUjBg/usr/share/Mod/Material/Resources/Materials
Vc array data [[0.0, 1333.3333333333335 mm/s], [1.0, 2000.0000000000002 mm/s], [2.0, 516.6666666666667 mm/s]]
Vc for Tool Mat: HSS  is:  1333.3333333333335 mm/s 1333.3333333333335 mm/s

Fz.Array data:
	 HSS [0.0, -0.00020581, 0.00861056, -0.03485845]
	 Carbide [1.0, -0.00024088, 0.00965887, -0.037093]
	 HSS coated [2.0, 0.0, 0.0, 0.0]
Calculated Fz for Tool Mat: HSS  is:  0.011819156400000003 mm

Calculated RPM = 3979
electrical spindle power  0.153 kW
Mc cutting torque 0.31204 Nm
vf  141 mm/min
mrr  45 mm^3/s
```

Note: The cutting machinability data and calculated RPM are real, usable values, but are not yet matched with background information on the expected machine capability and limitations. For example is the cutting machine:

* a very rigid milling machine, with 20kW spindle @20,000 RPM (as seen in many tool catalogs)
* a commercial hobby machine, by comparison not as rigid & maybe 1kW spindle @10,000 RPM
* a DIY milling machine with even less capability & rigidity
* a commercial/DIY routing machine, great for timber, plastics, but stretched to cut metals
* one of the many types of 3040 Engraver have even less ability than above

Implied by above is the need to adapt the cutting parameters such as Spindle RPM to the situation.

This is also demonstrated in Tool catalogs by all of the footnotes and asterix and appendix that provide some guidance on how to change the cutting parameters for a wide variety of situations.

These catalogs usually state that the data is "starting values" or some "maximum values" and maybe other.....


## References

* FreeCAD Forum announcement/discussion [thread](https://forum.freecadweb.org/)
* Material forum in particular [Material overhaul](https://forum.freecad.org/viewtopic.php?t=78242)
* Material Machinability [ Material: Add metal cards with machining model #15910 ](https://github.com/FreeCAD/FreeCAD/pull/15910)
* JobUtils.py Library Russ's lib Forum announcement/discussion [thread](https://forum.freecad.org/viewtopic.php?t=33328)
* csv flexible import imm [post with csv import code ](https://forum.freecad.org/viewtopic.php?t=59856&start=50#p549782)

The jobutils library provides many of the core Job features for `CamFullProcessExample.FcMacro` was created by FreeCAD forum user russ4262. It demonstrates the work he did to further open the CAM workbench to scripting and provides excellent example code is provided in this library in the Test## functions. Those examples have been extended here with many aded features to give the full scripted end to end CAM process.


## Limitations, Feedback and Contributions

Minimum FreeCAD version required to demonstrate Wood and Metal machinability materials with Speeds and Feeds calculations is: Version: 0.22.0dev.38553 (Git)

See the [github repo issues](https://github.com/spanner888/CamScripts/issues) for latest information.

These scripts started out as an import and scripted Toolbit creation for personal use. Then I got excited about the new Materials Machinability capability and also remembered the existing JobUtils library by russ4262, hence so many features.

However, while a lot of testing and polishing has occurred and the import work very well, there are still rough edges that you might find. One example is below and more up to date list is in the [github repo issues](https://github.com/spanner888/CamScripts/issues) for latest information.

There are no checks when saving ToolBit files or while adding a ToolBit to the current Tool table to see item of same name already exists.

If a ToolBit file of the same name exists if will be overwritten.

Duplicates do occur with current test data and can cause warning like:

```Tool number 28120 already exists for Tool 3F_D8.12-L50.0_endmill.```


## Release notes:

* V0.0.5  2024/09/25

- Requested CamScripts be added to FreeCAD Addons, so fully integratred Addon Manager install
- minor print & bugs fixes related to FullProcess Example 5, only with Extended Material/Model
- documentation updates, removed additional readme's outlines

* V0.0.4 2024-09-16

- Setup split into Materials and Tool Shape, in case user needs to preserve files or settings
- Using FreeCAD macros for user to launch scripts, abandoning both menu attempts
- Removed duplicate ToolBit number warnings, really really slowed down for large ToolTables
- Bug fix where CamScriptingLib.addTc() did not update properties.
- More work on readme's and images

* V0.0.3  2024-09-10

- Bug fix related to FreeCAD AddonManager not loading
- Improving Example 4 to reduce duplicate tool messages (still WIP)
- Documented and tested how to get new Materials-Model inheritance working for user folder
- README's menu fixes, which need github release for test confirmation
- Still possible blocking issue related to FC toolbars being closed and more duplicate tool etc msgs to fix.

* V0.0.2  2024-09-02

- Install using FreeCAD Addon Manager, but only via FC Prefs - Addon Manager add repo at present
- Add menu "Scripts" to FreeCAD menu bar, to run scripts, show readme's, Tool Shape, Material and script file info
- Early draft README's for Import, ToolBit Add and Full Process

* V0..01  2024-08-31:

- Initial release, fully functional, but not yet fully polished
- CSV Tool import
- Scripted tool bit creation
- Creates start to finish FreeCAD CAM process
- Demo of FreeCAD WIP Machinability materials properties and sample Speeds and Feeds calculations
- Extended machinability with Fz in equation form


## License

JobUtils Copyright (c) 2023 Russell Johnson (russ4262) <russ4262@gmail.com>, see [JobUtils](./freecad/cam_scripts/JobUtils)

All other files in CamScripts are Copyright 2024 Spanner888 and licensed under GNU GPL (v2+) license, see [LICENSE](LICENSE).

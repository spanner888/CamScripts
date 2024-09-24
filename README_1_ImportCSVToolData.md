## CSV Import Overview

The import process reads a CSV file to create FreeCAD CAM ToolBit file for each valid row and sets matching shape properties. Each ToolBit is added to FreeCAD current Tool Table in the Tool Library.

As each CSV row is processed, the "shape" column values is checked to match an existing FreeCAD default system shape, or User's own shape name and if matched:

- Column name of each cell in the row is checked against all properties of the specified shape and if an exact property match is found then if a valid value exists, the property is set
- ToolBit file created
- ToolBit is added to the current ToolLibrary Tool Table.

Shape names in the csv file AND in the FreeCAD Tools-Shape directories, both system and user, are case sensitive and must match exactly.

Mandatory columns "shape" and "Diameter". Rows without a matching shape file (system or user) or a valid positive number for the Diameter will be ignored.

The CSV format used is very flexible. It does not enforce column order and ignores additional columns.

There are a few rules and the flexibility also means you must provide valid data. Import attempts to convert every cell in every row into a Float type number and if it fails, leaves that imported cell value as a string. Only exception is "Flutes" which is converted to positive Integer, otherwise a default of 3 is used as this seems better than 0.

ToolBit file and Tool Table entry naming:

- ![Naming rules](README_NamingRules.md) can used to create the ToolBit file name, Name of Tool in Library and the Tool Table Tool number.
- very simple default of Diameter-val_Shape-name
- specified text, which is fixed and must be set for each tool

At present, duplicate Tool Numbers and names are allowed and will be added. Messages may appear in FreeCAD Report or Notification areas related to duplicates. Note these can be for both a duplicate Tool in a Tool Table and also for a duplicate ToolBit file saved into the current library Bit directory.

### Steps to import your data

- Get familiar with running the example import, in particular the simple setup steps
- Place your data into a CSV file, where first row has column names and every other row your data
- Other data, such as stock levels or location etc etc can be left in the file.
- Note rules above for columns "shape" and "Diameter" and "Flutes"
- Simplest approach is to replace content of example file in your FreeCAD Mod dir/CamScripts/freecad/cam_scripts/cutting_tool_data/cuttingtools1.csv
- Custom Tool shapes may be required if you have a tool with a different shapeoutline, or different properties. These should be created and added to your User tools/shape directory. It is recommended that you do not edit any system shapes, instead you can copy, and rename and place in your User Shape directory as was done with the example user shapes provided and installed when macro CamScripts_5Setup_CustomToolShapes.FcMacro is run.
- Run macro: CamScripts_1CSV_Import.FCMacro

If you wish to import different tools into different FreeCAD tool Library Tables, then the most reliable way is to split your tool data into one CSV file for each dataset. Switch to that Library Tool Table and then import the desired CSV file.

### Important setup steps before doing an import

CamScripts_1CSV_Import.FCMacro
CamTbAdd_Importing.py

But first to prevent clutter in your Tool Table data and ensure FreeCAD CAM is fully configured follow the two simple steps in 1. Follow steps in above [Before importing any data](##before-importing-any-data). To run the import process see [Import example data](##import-example-data).


### Before importing any data

1. Ensure your FreeCAD tool Library is stored in writable location. See ![CAM Tools Organization](https://wiki.freecad.org/CAM_Tools#Organization)

2. Open FreeCAD CAM Workbench and use CAM menu, ToolBit Library Editor, to open the Tool Table that imported tools should be added to.

3. If you wish to import custom user shapes, then run macro CamScripts_5Setup_CustomToolShapes.FcMacro

> [!CAUTION]
> 4. It is recommended to test with an empty Tool Table, until you have fully tested your import data.

### Running the CSV Import example

1. Follow steps in above [Before importing any data](##before-importing-any-data)

2. Ensure you have valid, writable location for your FreeCAD tool Library.....

3. Open FreeCAD CAM Workbench and use CAM menu, ToolBit Library Editor, to open the Tool Table that imported tools should be added to. It is recommended to test with an empty Tool Table.

4. Select: CAM Menu - CamScripts - CSV Import to run the import process for the default example. Note OTHER EXAMPLE FILES.....
If you want to test missing mandatory columns: 'shape', 'Diameter' <<must match case!
<class 'KeyError'>: ('shape',)
 Mandatory property 'Diameter' not found, ignoring this tool bit

++ref the sketcher solver warnings & errors

Output:


13:19:24  CamTbAdd_Importing - CAM ToolBit Import Library V0.0.4  2024/09/16 module imported
13:19:24
13:19:24  Importing :  cutting_tool_data/cuttingtools1.csv
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 0.3 Name: 2F_D0.3-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.1 Name: 2F_D2.1-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: pcb corncutters, Dia: 2.0 Name: 4F_D2.0-L50.0_pcb corncutters
13:19:24  	Adding ToolBit Shape: pcb corncutters, Dia: 3.0 Name: 4F_D3.0-L50.0_pcb corncutters
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.05 Name: 0F_D2.05-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.15 Name: 2F_D2.15-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.25 Name: 2F_D2.25-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.85 Name: 2F_D2.85-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 2.95 Name: 2F_D2.95-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: Pcb drill, Dia: 0.3 Name: 2F_D0.3-L50.0_Pcb drill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 4F_D6.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 1.5 Name: 4F_D1.5-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 4F_D2.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.5 Name: 4F_D2.5-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 4F_D3.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.5 Name: 4F_D3.5-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 4F_D4.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 4F_D5.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.5 Name: 4F_D5.5-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 4F_D6.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 1.0 Name: 1F_D1.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 1F_D2.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: v-bit, Dia: 0.0 Name: 2F_D0.0-L20.0_v-bit
13:19:24  Updating geometry: Error build geometry(6): Both points are equal
13:19:24  Invalid solution from SQP(augmented system) solver.
13:19:24  Sketch: Solving the sketch failed
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 4F_D3.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 2F_D5.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 1.5 Name: 4F_D1.5-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 4F_D2.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.5 Name: 4F_D2.5-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 4F_D3.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.5 Name: 4F_D3.5-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 4F_D4.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.5 Name: 4F_D4.5-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 4F_D5.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.5 Name: 4F_D5.5-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 4F_D6.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 0.9 Name: 2F_D0.9-L50.0_endmill
13:19:24  	 ignoring shape : T slot. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : T slot. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	Adding ToolBit Shape: dovetail, Dia: 0.0 Name: 4F_D0.0-L54.2_dovetail
13:19:24  Sketch: Solving the sketch failed
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.175 Name: 1F_D3.175-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.175 Name: 2F_D3.175-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.175 Name: 2F_D3.175-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 1.0 Name: 2F_D1.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 2F_D2.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 2F_D3.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 2F_D4.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 2F_D5.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 2F_D6.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 2F_D5.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 4F_D6.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: chamfer, Dia: 6.0 Name: 4F_D6.0-L30.0_chamfer
13:19:24  Sketch: Solving the sketch failed
13:19:24  	Adding ToolBit Shape: chamfer, Dia: 4.0 Name: 4F_D4.0-L30.0_chamfer
13:19:24  Sketch: Solving the sketch failed
13:19:24  	Adding ToolBit Shape: roughing, Dia: 6.0 Name: 3F_D6.0-L50.0_roughing
13:19:24  	Adding ToolBit Shape: roughing, Dia: 4.0 Name: 3F_D4.0-L50.0_roughing
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 2F_D2.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.5 Name: 2F_D2.5-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 2F_D3.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 2F_D3.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 2F_D4.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 5.0 Name: 2F_D5.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 2F_D6.0-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 1F_D4.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.0 Name: 1F_D3.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: slotdrill, Dia: 3.0 Name: 2F_D3.0-L50.0_slotdrill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: slotdrill, Dia: 4.0 Name: 2F_D4.0-L50.0_slotdrill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: slotdrill, Dia: 6.0 Name: 2F_D6.0-L50.0_slotdrill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 4.0 Name: 1F_D4.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.0 Name: 1F_D6.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: endmill, Dia: 8.0 Name: 1F_D8.0-L50.0_endmill
13:19:24  <Sketch> SketchObject.cpp(344): Edge too small: Edge4
13:19:24  	Adding ToolBit Shape: ballend, Dia: 6.0 Name: 4F_D6.0-L50.0_ballend
13:19:24  	Adding ToolBit Shape: ballend, Dia: 16.0 Name: 2F_D16.0-L50.0_ballend
13:19:24  	Adding ToolBit Shape: chamfer, Dia: 10.0 Name: 3F_D10.0-L30.0_chamfer
13:19:24  Sketch: Solving the sketch failed
13:19:24  	 ignoring shape : Conical engrave point. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : Burr Cylindrical (Square). It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : Burr Cylindrical (Radius). It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : Burr Tree (Pointed). It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : Burr Flame. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : Burr Ball. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	Adding ToolBit Shape: endmill, Dia: 2.0 Name: 2F_D2.0-L50.0_endmill
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : v engrave. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	Adding ToolBit Shape: endmill, Dia: 3.175 Name: 2F_D3.175-L50.0_endmill
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	 ignoring shape : ??ballend??. It is not in user shapes folder /home/spanner888/.local/share/FreeCAD/Macro/Tools:
13:19:24  	Adding ToolBit Shape: endmill, Dia: 6.1 Name: 4F_D6.1-L50.0_endmill
13:19:24  	Adding ToolBit Shape: endmill, Dia: 1.6 Name: 4F_D1.6-L50.0_endmill
13:19:24  	Adding ToolBit Shape: chamfer, Dia: 4.1 Name: 4F_D4.1-L30.0_chamfer
13:19:24  Sketch: Solving the sketch failed
13:19:24  	Adding ToolBit Shape: roughing_HRangles, Dia: 6.4 Name: 3F_D6.4-L50.0_roughing_HRangles
13:19:24  	Adding ToolBit Shape: roughing_HRangles, Dia: 4.2 Name: 3F_D4.2-L50.0_roughing_HRangles
13:19:24
13:19:24  Imported 77 Tool details & added to current library.
13:19:24  Skipped or failed to import 19 rows in csv file.



Each valid CSV row....
Invalid CSV row....

Summary counts....

Notes:

- Sample data provided includes shapes with names roughing, PCB....
COPY menu item?????

console + warnings - dup names, dup tb files
```Tool number 28120 already exists for Tool 3F_D8.12-L50.0_endmill.```
If input data and naming rules create no duplicates, then these will not appear.

```Sketch: Solving the sketch failed```
Shape files and contained sketches are valid and have been in use for about two years. It is suspected that the rapid open close of these shapes files to read the property data, does not allow time for FreeCAD to finish refreshing the internals of the file.

Notes:

- The CAM ToolBit Library Editor can be used to delete Tools from the ToolTable. Bulk selection is allowed.
- Deleting after testing is also a good idea to clean up ToolBit files. At present this has to be done by manually deleting the files.
- Test ToolTables or Libraries also need to be deleted in the same way.

Note: Use the ```Show config and script file locations``` menu item to find the above file locations.
![Menu items](/images/Menu items.png)

## Simple steps to import your own tool data

1. Follow steps in above [Before importing any data](##before-importing-any-data)

2 .Create your CSV file with relevant data in the mandatory columns and any additional columns that you wish matching Tool Properties to be set.

3. Copy file to the ```CamScripts/freecad/cam_scripts/cutting_tool_data/``` directory. You can find this by selecting this addon in the Addon manager and lookign a Install location path near the top of the dialog.
Confirm and queries to ensure the new file overwrites the exsiting example file.
Note a copy of the example file named "cuttingtools1.csv" will remain in the cutting_tool_data directory.

4. Select: CAM Menu - CamScripts - CSV Import to run the import process.

## Additonal Import Features

- naming rules copy/create/change script
- change CSV file name
- sort each CSV file and save seperate files with only one shape type etc. This is especially useful to save the tools from each imported in a different Tool Table in FreeCAD.

## How and when to create custom Tool Bit shape files

- dif shape not provided by FC
- Sometimes there is a need to use the same shape, but the shape is used in different ways, which need to be highlighted in FreeCAD. For example a roughing cutter, is an endmill, but should use different settings for an Operations StepOver and StepDown (WOC/DOC) and also the Horiztonal Feed rate.
By copying the default endmil.fcstd shape to your user shapes directory and renaming to roughing.fcstd, then in combination with the import naming_rules, the name of the ToolBit and ToolController can automatically include "roughing", to alert you to the different settings required.
Example shapes provided demonstrate this by providing shape files ORIG + NEW-copies
It would also be possible to change the import code so that the detecting shapename of say "roughing" could automatically adjust the default endmill SurfaceSpeed by a fixed multiplier and also the DOC/WOC. These multipliers could be included in the CSV file and different for every tool.

- Additonal Machinability properties - in samples or by......

## CSV file format and rules

First row is a header that names every column.
Column header of cell matches EXACTLY (ie text case and no extra spaces)
Column headers can be in any order. You are free to add additonal columns with your own data, as shown in the provided   example file [cutting_tool_data/cuttingtools1.csv](cutting_tool_data/cuttingtools1.csv)
Every row will be read during import and every column process according to rules below.
All data is assumed to be in mm, or degrees.
With the few exceptions noted here and below, there are no restrictions on data content. This means there is very little or NO data validation. So float data or negative data or unrealistic values, say 100000 (mm) for a tool diameter will be added into your ToolBit with no checks.
Import process tries to convert every cell to a float value, otherwise value remains as text, with the exceptions noted in next section.

### CSV Special Columns:

- "shape" MANDATORY column. If text in matches exactly an available FreeCAD or User Tool shape filename, then rest of row data is processed. If no match, message is printed "TODO GET COPY IGNORING MSG"

- "Diameter"  MANDATORY column.??? No default??

- "Flutes"  MANDATORY column.??? If cell text can be converted to positive??? Only if imported value = 0, is the value changed to a default = 3??. This is so the Machinability calculations will produce realistic and safe defaults, which a 0 value woould not!


Script will add ToolBits to the CURRENT CAM Library Tool Table.
So make sure you have the desired Tool Table active BEFORE you run script.
It is probably best to create a test Table so to avoid cluttering your existing data!

How to see avail shapes files and shape properties that will be macthed to CSV columns.....

CamTbAdd_Importing provides bulk import very flexible csv data to create ToolBits and add to current library. Includes powerful naming rules as well as ability to auto-number both ToolBit name and number in the Tool Library. Note that the import macro is not considered an example, but is ready for use.

...
    The csv import is very flexible, thanks to @imm, but if you wish data to match default ToolBit properties,
    An auto numbering system is also an option.
        28120.0_8.12D_0F_endmill
    then the column names must match exactly.
    At present, empty cells are forced to number zero, and some data erros are handled, but not all.
    If Tool shapenames do not match any of those in your User tool Shape directory,
    a message will inform you of it being ignored.
    Also at present things like duplicate Library Tool Numbers, or duplicate Tool  names, or empty names (se example 7)
    are also ignored as they cause no error, and all these scripts were mainly written for my own use.






## File locations

doco once only
  FC Tool for users, Materials
  CamScripts files - CSV, rules, actual scripts


Shape files:

Copy to for USer CAM Library Shape directory.

For the import testXXX and also for the Full-materials XXXXX
CamScripts/cutting_tool_data/Shape/roughing_HRangles.fcstd



DOC: How to cope with other bits:
  ** SAME as default shapes, btu if want to highlight in TC-TB need for diff Op/cutting-settings
    **roughing
    **slot drill
    T slot = slitting saw???
    **PCB drills - v diff rpm/material ...just cutting props
    **PCB corn cutters ...like roughing endmill...need to know, but just dif cutting props

    One view is still endmills, but WHEN selecting for Op AND get/calc SF need know diff....
        Name - cannot use as get overridden by rules!!
        Family/Part not really
        ...or suggest SpecialUse col/data <<<NEEDS CODE then to carry info/show - eg via rule into name
            OR just new shape name....and just copy equiv shape in tool lib???


DOC: File CSV format. comma seperated, no commas WITHIN a cell.
Default number format is Float.
Import data scrubbing converts empty string to float=0.0,
  except if data "Flute", converted to int=0.
Other than above, any text in number cell = error like:
....<class 'ValueError'>: could not convert string to float: '6-10'
Where the last '6-10' shows the text where a float was expected.
So you may end up with Diameter=0.0 or Flutes=0.
Diameter=0.0 will usually show errors like one or both of:
  "Updating geometry: Error build geometry(11): Both points are equal"
  "Sketch001: Solving the sketch failed"
So 0 is better than incorrect value with no error/warning.
Every time script is run:
  ToolBit files will be created or overwrite existing files
  ToolBits will be added to the current Tool library.
so ...include my aldtready wrtten doc: re use empty test lib.
or even an entire test Tool dir with default tools/shapes.



# EXAMPLE OUTPUT ...started above???? search for summary

ignoring shape name: v engrave. It is not in user shapes folder /home/spanner888/Documents/_APPS_lappy/FC_wkly-38553/squashfs-root/appd_mlappy/Tools:

Adding ToolBit Shape: endmill, Dia: 3.175 Name: 2F_D3.175-L50.0_endmill

Imported 57 Tool details & added to current library.
Skipped or failed to import 34 rows in csv file.

Multiple messages like:
Sketcher::setUpSketch()-T:0.00035092
May appear for each ToolBit added. These are not errors and can be ignored.

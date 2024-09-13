
script = Menu name



Script will add ToolBits to the CURRENT CAM Library Tool Table.
So make sure you have the desired Tool Table active BEFORE you run script.
It is probably best to create a test Table so to avoid cluttering your existing data!



CamTbAddExample has seven examples of creating ToolBits in code and using the above naming rules.

DETAILS or explain code location.....


Example 1. Add single example default endmill to current Library.

Example 2. Add SINGLE Tool 6.35 mm dia to current library

Example 3. Create range of tools from dia to dia_max, incrementing dia by dia_inc
   But only If BOTH dia_max & dia_inc are greater than zero,
           Else: ONLY create ONE TB of this dia in current library.

Example 4. Retrieve properties & attributes of all shape files in FC Tool- Shape directory.
By default this example is disabled.
Change the value of the line:

    ```getDefaultShapeAttrs = False```

to

    ```getDefaultShapeAttrs = True```

and save the macro to run this example. Then the shape dictionaries output in report pane can be used to create different types of ToolBits above.

An example is shown below:

```
{'shape': 'v-bit.fcstd', 'name': 'v-bit', 'parameter': {'CuttingEdgeAngle': 90.0 deg, 'CuttingEdgeHeight': 1.0 mm, 'Diameter': 10.0 mm, 'Length': 20.0 mm, 'ShankDiameter': 5.0 mm, 'TipDiameter': 1.0 mm}, 'attribute': {'Chipload': 0.0 mm, 'Flutes': 0, 'Material': 'HSS'}}
```

The output above includes all properties in the default shapes, as a patch suggested to fix missing properties has been applied locally. Details of the issue and a suggested fix have been submitted in FreeCAD/FreeCAD#15637.

FreeCAD CAM Tools/Bits/Shapes/Library Job-TC ++ for ju - Ops/materials/SF...

CHANGE TO ABOVE KISS FORMAT/DETAILS!!!!
so sev sections WITH Example NUMBERING????

## Example output

![Example 2 Cam Full Process](./images/CamFullProcessExample.png)

```
19:43:01  Job Utilities 2024-02-25 module imported
19:43:01  --------------------------------------------------------------------------------
19:43:01  Example 1 JobUtils: New doc & Job, optionaly clear report/python panes.
			 Active document is Test_JobUtils with Job object
19:43:06  Example 2 JobUtils: Add profile operation to specified job.
			 adding profile operation using top face, Face6.
19:43:06  Example 3 JobUtils: Add profile operation & Boundary Dressup to specified job.
		 adding profile operation
19:43:06  adding boundary dressup on profile operation
19:43:06  --------------------------------------------------------------------------------
19:43:06  Example 4 JobUtils: Add ToolControllers to Job-Tools & desired Operation.
		 JobUtils... Available tool files:
19:43:06       1 ::   5mm_Endmill
19:43:06       2 ::   5mm_Drill
19:43:06       3 ::   6mm_Ball_End
19:43:06       4 ::   6mm_Bullnose
19:43:06       5 ::   60degree_Vbit
19:43:06       6 ::   45degree_chamfer
19:43:06       7 ::   slittingsaw
19:43:06       8 ::   probe
19:43:06       9 ::   5mm-thread-cutter
19:43:06       20820.0 ::   20820default_em
19:43:06       20635.0 ::   20635em
19:43:06       20820 ::   820_em
19:43:06       20840 ::   840_em
19:43:06       20860 ::   860_em
19:43:06       20880 ::   880_em
19:43:06       20900 ::   900_em
19:43:06
19:43:06  Add TC using toolname: 880_em and set h/v feeds & spindle speed.
19:43:11  	Set profile_op.ToolController to above TC+user scripted settings
19:43:11  Add TC using tool#: 20840 and set h/v feeds & spindle speed.
19:43:11  	Set profile_op1.ToolController to above TC+user scripted settings
19:43:15  --------------------------------------------------------------------------------
19:43:15  Example 5 CamScripting: Machinability & SpindleSpeed RPM calculation:
		 Retrieved Stock Material SurfaceSpeeds & tc1 Diameter
			in common base Units of mm/s & mm, to Calculate cutting RPM
19:43:15  		HSS: 2916.67 mm/s, CBD: 6483.33 mm/s, TC1 dia: 8.8 mm
19:43:15  	**Calculated** RPM for HSS tool is 6330.0 RPM
19:43:15  	formula: SurfaceSpeed / (Diameter * math.pi)
19:43:15  	NB: FreeCAD Units are all normalised in metric, so SurfaceSpeed*1000 is not required.
19:43:15  Calculated SpindleSpeed RPM has not been set in ToolController SpindleSpeed.
19:43:15  You can do this manualy, or uncomment code in line below this print statement in the macro.
19:43:15  --------------------------------------------------------------------------------
19:43:15  Example 6 CamScripting: Create & save: CAM Sanity check report & Postprocessed gcode.
		 Processing file outputs: Sanity Job common errors report & PostProcess Gcode
19:43:16  Sanity check report written to: /home/spanner888/Documents/cam_sanity/sanity_auto.html
19:43:16
19:43:17  Post Processor: script_module postprocessing...
19:43:17  Done postprocessing.
19:43:17  File written to /home/spanner888/Documents/_source/_APPS/FC_wkly_38334/squashfs-root/appd_mlappy/Test_JobUtils1_Job_ju_created____0.ngc
19:43:19  --------------------------------------------------------------------------------
```

Uses CamLibTbAdd Library....

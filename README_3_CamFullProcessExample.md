CAM Full Process blurb - Script 3.....

script Menu name


Script relies on two existing tool bits being in ??any or current?? of your Tool Library/s??
To create those....run menu ""
Script does not add any ToolBits to your Tool Library.



Materials Machinability data.
    FC now includes...

    Fz data from an older version of Tabellen.... is included in [mat file]() for Tool Materials HSS and Carbide, but only for the single Material Al.......
    This data has been limited due to differences through the data set to those in the above reference  2022 version.


Supported by 2 libraries of mine and Russ JobUtils
Details are provided in linked readmes and within the example scripts.
WARNING about using a Test lib!!!!

Scripts are very highly capable and tested, but there are limitations,
including your need to configure settings, naming rules and especially for #3 NAME, change the examples.
Limitations and minor bugs are documented ?????
Discussion can occur in forum thread [LINK]() and pull requests, bugs, issues, via this GITHUBREPO

Execution speed is reasonable, it can create & add several ToolBits per second, on old hardware.
Once I accidently created and 1600 Toolbits to a Library.
This took 20minutes????, but I think a lot of the slowness was debug prints at the time.

Example naming rules are in ...
Example csv file for import is in...
SHORT HERE!!!!!!


TWO sep release 1x end-end as EXAMPLE ...but note can use toolbits from....

vv-- OR becasue of the one dir focus, then one summary overview readme that links to 2x detaild ones...
sep MAJOR = bulk create/import...
    >>>ESP when "last" effort got 20K views...but sidetracked from the TB import/create!!!
...so split all the files apart....
    START WITH same repo...but dir for each
    BECASUE in GH/FC macros ONExdir .....???? try/maybe
BUT = MORE annoy to user as FC macro needs dir change........

study MD features+syntax - refine this!!

FIXME: numbering for "2. Set FreeCAD macro directory."
    ..& subsequent all = 1 !!!! <<<in ReText!!!

review 1st read me for missing stuff
    even if just some console output ...SNIPPETS???

# FreeCAD CAM scripting

Scripting all features of FreeCAD CAM for a complete end to end process:

* bulk import Tool Data to populate FreeCAD Tool Library

* create Job, Operations, ToolControllers

* set wide range properties

* assign ToolController to Operation

* use Tool & Material material-machinability cutting properties to calculate Spindle RPM

* create and save Sanity report to check for common errors

* postprocess Job to create and save gcode

All of the ToolBits were created and added to the Library shown in the left hand image below by `CamTbAddExample.FCMacro` and every item in the right hand image was created by `CamFullProcessExample.FcMacro`. An extensive number of properties were also set.

++anotyher file???
+++++++ the TB bulk creation is highly usefull in creating {??or importing??} TB and with a bit of community testing & refinement be ready for serious use. This tool only requires you to specify the tool or range of tool properties you need and any naming rules. There are a lot of settings, so this needs care and it would be safer to create and activate a test CAM Tool Table in your current Library before executing this script.

The other examples are fully functional, but require more customisation of the code to match your specific needs.

 ![CamFullProcessExample Tools&Tree](./images/CamFullProcessExample Tools&Tree scaled.png)

# Installation

??4th = +github repo in
Select Menu - Preferences - Addon Manager: Then to "Custom Repositories" add github repo
???will this dump all into current macro dir...if so recommend create dir & set FC Macro dir to that dir first.

3 methods - addon manager (not yet avail)
    https://wiki.freecad.org/Addon#Information_for_developers
     add macro to Macros recipes page...automatically be picked up by Addon manager
    https://wiki.freecad.org/Macros_recipes

file copy
zip <<<<<<<<attached to forum = zip...or never attach forum  only link??
![FreeCAD wiki Installing macros](https://wiki.freecad.org/How_to_install_macros#Installing_macros)

Before in addon repo
add my repo ...

after in addon repo - addon manager...

Manual - wiki link


`CamTbAddExample.FCMacro`

`CamFullProcessExample.FcMacro`.



# How to use

1. Required FreeCAD version:

A very recent development version of FreeCAD to run the Machionability RPM example for example FreeCAD revision 38314 or later.

If not, then Stable Version: 0.21.2.33771 (Git) works for the Creation of Job, Operations and TC, but not the Machinability RPM example.

2. Set FreeCAD macro directory.

Because the scripts and library files are supplied in a directory, the FreeCAD macro utility much be set to use that directory, as shown below:

![Select Macro directory](./images/Select Macro directory.png)

If after setting the Macro directory and running one of the macros, you get an error in the report pane, like that shown below:


>>>UPDATE BELOW DUE TO FILE RENAMES!!!!!!!!!!!!!!!
```
    .....
    shiboken2/files.dir/shibokensupport/feature.py", line 139, in _import
    return original_import(name, *args, **kwarg
At present not all ToolBit properties are return when using Example 4. s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    <class 'ModuleNotFoundError'>: No module named 'CamTbAddLib'
```

Then try restarting FreeCAD to fix the issue.

3. Select CAM workbench and create a test library

Open CAM wb.

Create and empty Tool Table in your library so that tests ToolBits do not interfere with your "good" ToolBits.

![CamLibTbAdd before - empty library tool table](./images/CamLibTbAdd before - empty library tool table.png)

If the CAM - ToolBit Library editor menu is greyed out, then you need to open or create any FreeCAD document. That document will not be changed.

4. Run default example scripts, or reconfigure and run.

The following sections briefly discuss each of the examples. Note by default all example except 4th in the first script will run.

One example script file is provided for each library, each containing several examples.

Both example files provide full automation, ie once user has set desired properties and actions, running each script requires no further user interaction.

TODO: remove what was last example 4 - no longer req - invisble mostly to user
        NB new last example needs doc - creates 1xTB for EVERY shape.

REDUCE to KISS/short generic - each example is on command call to the associated library, complete wtih example properties, either in the function call, or in variables prior.
>>>>>MAYBE EVEN THE **entire** SECTION MUCH SHORTER...keep the intro stuff, but shorten if poss, maybe skip some images??
You can run the examples as is, or modify the properties to suit your needs.
++Notes in the code.
In `CamFullProcessExample.FcMacro`, there is a fair bit of output printing that can be removed, if not required.
Also if you you remove features, be aware that later code might be dependant upon those outputs and fail. Sometimes you may be able to adjust the later code. For example removing one operation will cause related property value setting and assing a ToolController to fail.

????How to edit scripts and the libraries....
1. changing properties
2. add/remove calls to create TB, or add Operation to Job etc.
3. ...tailor libraries...

related FreeCAD CAM Terminology: ??just brief sentence& link?? [Machinability & RPM]()
.......

## Example output

![Example 1 new Library ToolBits](./images/Example 1 after running CamLibTbAdd.png)

![CamLibTbAdd before - after populated library tool table](./CamLibTbAdd before - after populated library tool table.png)


```
19:38:25  Adding ToolBit Shape: endmill Name: 20820default_em, #20820.0, Dia: 8.2 mm
19:38:25  ...finished.
19:38:25
19:38:25  Adding ToolBit Shape: endmill Name: 20635em, #20635.0, Dia: 6.35 mm
19:38:25  ...finished.
19:38:25
19:38:25  ToolBit diameters to be created:  [8.2 8.4 8.6 8.8 9. ]()
19:38:25  Adding ToolBit Shape: endmill Name: 820_em, #20820, Dia: 8.2 mm
19:38:25  Adding ToolBit Shape: endmill Name: 840_em, #20840, Dia: 8.4 mm
19:38:25  Adding ToolBit Shape: endmill Name: 860_em, #20860, Dia: 8.6 mm
19:38:25  Adding ToolBit Shape: endmill Name: 880_em, #20880, Dia: 8.8 mm
19:38:25  Adding ToolBit Shape: endmill Name: 900_em, #20900, Dia: 9.0 mm
19:38:25  ...finished.
```



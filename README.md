
Three FreeCAD macros demonstrating *every* step of CAM process:
    1. CamTbAdd_Importing provides bulk import very flexible csv data to create ToolBits and add to current library. Includes powerful naming rules as well as ability to auto-number both ToolBit name and number in the Tool Library. Note that the import macro is not considered an example, but is ready for use.
    2. CamTbAddExample has seven examples of creating ToolBits in code and using the above naming rules.
    3. CamFullProcessExample....

Two parts of the above are worth special mention:
    1. An Extensive rule system to provided to auto create Tolbit names.
    This can use ANY ToolBit property and allows setting order of each component as well as
    leading/trailing seperators and abbreviations.
    For example:
        2F-D6.35-L31
        1F_D3.0-L50.0_endmill
        3F_D4.0-L50.0_roughing
        28600.0_8.6D_0F_860_em
        Last item above also shows one example of an auto-numbered name.

    A ridulous example used for testing imported Tools with uncommon properties:
        30000.0_0.0D4F_0.0CL__HSS__60.0deg_0.0CL_54.2L_8.0ND_5.0NH_0.0DS_td5.0deg_dovetail__dovetail
        30000.0_0.0D0F_0.0CL__HSS__90.0deg_0.0CL_20.0L_0.0DS_td1.0deg_v-bit__v-bit
        40000.0_10.0D3F_0.0CL__HSS__60.0deg_0.0CL_30.0L_6.0DS_td5.0deg_chamfer__chamfer

    2. The demonstration of CAM Speeds and Feeds uses the new Materials workbench and a Material Machining Model as well as cutting data, all of which are functional, but incomplete. So this design work is highlighted to get more attention and contributions. For example see mat forum...that Mat Maching PR.

Above code is simplified by two supplied python libraries and one excelent lib from Russ
To get all features, requires very recent FC v.....

Easy install via single install....

LINKS to 3x readmes and other background???


## Limitations & Issues

SEVERAL ALREADY ABOVE ...just remove the section????
See the github repo issues for latest information.

# Credits????
The two scripts and

The third library which provides most of the core Job features for `CamFullProcessExample.FcMacro` was created by Russ..
Excelent example code is provided in this library in the Test## functions.

++ He worked on CAM changes to make scripting have less user intervention to answer dialogs...???

Path and Material developers and forum users including Russ, onekk, CSV guy...

# Background informatiion

## FreeCAD CAM Terminology:
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

## Machinability & RPM

The early work using the new Materials Workbench to add default group of "Machining" materials that have "Machinability" properties is also demonstrated in the second script 'CamFullProcessExample.FcMacro'.

Spindle RPM is calculated, by retreiving ToolController material type of HSS or Carbide and then retreiving the corresponding HSS or Carbide surfaceSpeed from the Material data of the Job-Stock, which would be inherited from the design object.

Note "ToolController material type" is an existing ToolController property and is not a "new Material", but maybe in future, [follow or join the design process]()

??This a demonstration of the very early work to design Speeds and Feeds for FreeCAD. SEE XXXXX
In future the ToolController material, might be set via a "new Material", depending on how we all decide to progress Speeds and Feeds.


Note: The cutting machinability data and calculated RPM are real, usable values, but are not yet matched with background information on the expected machine capability and limitations. For example is the cutting machine:
* a very rigid milling machine, with 20kW spindle @20,000 RPM (as seen in many tool catalogs)
* a commercial hobby machine, by comparison not as rigid & maybe 1kW spindle @10,000 RPM
* a DIY milling machine with even less capability & rigidity
* a commercial/DIY routing machine, great for timber, plastics, but stretched to cut metals
* one of the many types of 3040 Engraver have even less ability than above

Implied by above is the need to adapt the cutting parameters such as Spindle RPM to the situation.

This is also demonstrated in Tool catalogs by all of the footnotes and asterix and appendix that provide some guidance on how to change the cutting parameters for a wide variety of situations.

These catalogs usually state that the data is "starting values" or some "maximum values" and maybe other

## References
* FreeCAD Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
* JobUtils.py Library Russ's lib Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
...all the materials

## Credits????
The two scripts containing examples each kept simple by use of a related library.

The third library provides many of the core Job features for `CamFullProcessExample.FcMacro` was created by Russ..
Excelent example code is provided in this library in the Test## functions.
Those exapmles have been included here and extended with many other features to give the full scripted end to end CAM process.

??++ He also worked on CAM changes to make scripting have less user intervention to answer dialogs...???

Path and Material developers and forum users including Russ, onekk, CSV guy...

## References
* FreeCAD Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
* JobUtils.py Library Russ's lib Forum announcement/discussion [thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=60818)
...all the materials

# Release notes:

* V0.1  2024-08-08:  Initial release
    * Initial release, 2 scripts/macros with 3 libraries and support information.
    * Scripting all features of FreeCAD CAM for a complete end to end process

* V0.1  2024-08-16: Initial release
                    - creates start to finish FreeCAD CAM process
                    - 2 scripts/macros, 3 libraries & support information.

* V0.1  2024-08-16: Initial release
            - creates start to finish FreeCAD CAM process
            - 2 scripts/macros, 3 libraries & support information.

* V0.1  2024-08-16:
            - Initial release
            - creates start to finish FreeCAD CAM process
            - 2 scripts/macros, 3 libraries & support information.

* V0.1  2024-08-16:
            - Initial release
            - creates start to finish FreeCAD CAM process
            - 2 scripts/macros, 3 libraries & support information.

* V0.1  2024-08-16:
            - Initial release
            - creates start to finish FreeCAD CAM process
            - 2 scripts/macros, 3 libraries & support information.

* V0.1  2024-08-16:
            - Initial release
            - creates start to finish FreeCAD CAM process
            - 2 scripts/macros, 3 libraries & support information.

## License
LGPL-2.1-or-later (see [LICENSE](LICENSE))

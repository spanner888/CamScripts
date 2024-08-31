


script = Menu name

Script will add ToolBits to the CURRENT CAM Library Tool Table.
So make sure you have the desired Tool Table active BEFORE you run script.
It is probably best to create a test Table so to avoid cluttering your existing data!




CamTbAdd_Importing provides bulk import very flexible csv data to create ToolBits and add to current library. Includes powerful naming rules as well as ability to auto-number both ToolBit name and number in the Tool Library. Note that the import macro is not considered an example, but is ready for use.






If want to test missing mandatory columns: 'shape', 'Diameter' <<must match case!
<class 'KeyError'>: ('shape',)
 Mandatory property 'Diameter' not found, ignoring this tool bit



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
+ Unwanted TB files can be deleted
Shape names in the csv file AND in the FC Tools - Shape dir
  are case sensitive on Linux and must match exactly.


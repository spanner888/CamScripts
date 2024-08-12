# TODO licence/macro info

import os
import sys
# this is python module, not a FC module
from pathlib import Path as osPath

import FreeCAD
import Path
import Path.Tool.Gui.BitLibrary as PathToolBitLibraryGui
import Path.Base.PropertyBag as PathPropertyBag
import Path.Base.Util as PathUtil

from PySide.QtCore import Qt
import numpy as np

import collections



if False:
    Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
    Path.Log.trackModule(Path.Log.thisModule())
else:
    Path.Log.setLevel(Path.Log.Level.INFO, Path.Log.thisModule())


###################################################################
def getDefaultShapes():
    # FIXME will FAIL if user never created ToolBit from a shape!!
    # FIXME also fails if NO SHAPES ...ie FC has not copied to user dir
    shapeDir = Path.Preferences.lastPathToolShape()
    shapeDir = shapeDir.replace("/", os.path.sep)
    # Make sure the path ends with a separator
    if shapeDir[-1] != os.path.sep:
        shapeDir += os.path.sep

    # ATM only gets default FreeCAD Tools/Shape dir, not your User Tools/Shape dir.
    shape_names = [os.path.splitext(f)[0] for f in os.listdir(shapeDir)]

    return shapeDir, shape_names


def getToolShapeProps(shape_name_dir, shape_name):
        doc = FreeCAD.openDocument(shape_name_dir + shape_name + ".fcstd", False)
        parameters = dict()
        attributes = dict()
        for o in doc.Objects:
            if PathPropertyBag.IsPropertyBag(o):
                idx=0
                for p in (o.Proxy.getCustomProperties()):     # sorted()
                    grp = o.getGroupOfProperty(p)
                    typ = o.getTypeIdOfProperty(p)
                    ttp = PathPropertyBag.getPropertyTypeName(typ)
                    val = PathUtil.getProperty(o, p)
                    dsc = o.getDocumentationOfProperty(p)

                    idx+=1
                    if grp == "Shape":
                        parameter = {p: val}
                        parameters.update(parameter)
                    elif grp == "Attributes":
                        attribute = {p: val}
                        attributes.update(attribute)
                    else:
                        FreeCAD.Console.PrintWarning(
                            "Shape type {} for shape_name: {} is unknown, ignoring.\n"
                            .format(grp, shape_name))

                # Default TB file 'shape' prop ALL include ".fcstd"
                attrs = {'shape': shape_name + ".fcstd",     # match FC tool shape_name filename
                         "name": shape_name,                 # your choice
                         "parameter": parameters,
                         "attribute": attributes
                    }

                FreeCAD.closeDocument(doc.Name)
                return attrs


def getAllToolShapeProps(shape_name_dir, shape_names):
    props = dict()
    attrs = dict()
    idx=0
    for i, fname in enumerate(shape_names):
        # FreeCAD.Console.PrintMessage("fname: {}\tshape_name_dir:{}\n".format(fname, shape_name_dir))
        props = getToolShapeProps(shape_name_dir, fname)
        attrs.update({idx: props})
        idx += 1
    return attrs


def full_path(filename):
    # Parse out the name of the file and write the structure
    loc, file = os.path.split(filename)
    fname = os.path.splitext(file)[0]
    fullpath = "{}{}{}.fctb".format(loc, os.path.sep, fname)
    return fullpath, fname


# derived from FC BitLibrary.py
def toolBitNew(library, filename, shape_name, shape_full_path_fname, attrs):
    fullpath, fname = full_path(filename)
    Path.Log.debug("filename: {} shape_full_path_fname: {} fullpath: {}".format(filename, shape_full_path_fname, fullpath))

    library.temptool = Path.Tool.Bit.ToolBitFactory().CreateFromAttrs(attrs, name=attrs["name"], path=shape_full_path_fname)

    library.temptool.Label = fname
    library.temptool.Proxy.saveToFile(library.temptool, fullpath)


def addToolToCurrentLibrary(library, shape_name, tool_props, tb_nr, tb_name_rules):
    tp = tool_props["parameter"]

    ### >>>    NOW USE THE NE TB_NAME_TMPLATE TO CHANGE endmill_tool_props["name"]..using TB values
    tb_name = create_tb_name(tb_name_rules, tb_nr, tool_props)
    tool_props["name"] = tb_name

    if PathToolBitLibraryGui.checkWorkingDir():
        workingdir = os.path.dirname(Path.Preferences.lastPathToolLibrary())

        tb_full_path_nr_name = workingdir + "/Bit/" + tool_props["name"] + ".fctb"

        shape_full_path_fname = workingdir + "/Shape/" + shape_name + ".fcstd"
        shape_full_path_fname_as_path = osPath(shape_full_path_fname)
        if shape_full_path_fname_as_path.is_file():
            shape_full_path_fname_attrs = getToolShapeProps(workingdir + "/Shape/", shape_name)
            params = shape_full_path_fname_attrs["parameter"]

            new_tool_params = tool_props["parameter"]
            print("Adding ToolBit Shape: {} Name: {}, #{}, Dia: {}"
                  .format(shape_name, tool_props['name'],
                          tb_nr,
                          new_tool_params['Diameter']
                          )
                )
            toolBitNew(library, tb_full_path_nr_name, shape_name, shape_full_path_fname, tool_props)

            library.temptool = None
            artifacts = FreeCAD.ActiveDocument.findObjects(Label=tool_props['name'])
            for o in artifacts:
                FreeCAD.ActiveDocument.removeObject(o.Name)

            for row in range(library.toolModel.rowCount()):
                # print (row, tb_nr, library.toolModel.item(row,0).text(), int(library.toolModel.item(row,0).text()))
                if int(library.toolModel.item(row,0).text()) == tb_nr:
                    FreeCAD.Console.PrintWarning("Tool number {} already exists for Tool {}.\n"
                                                 .format(tb_nr, tool_props["name"]))

            # add tool to the model , ie current CAM Library & save Library
            try:
                fullpath, fname = full_path(tb_full_path_nr_name)
                tool = Path.Tool.Bit.Declaration(fullpath)
            except Exception as e:
                Path.Log.error(e)
                return

            library.toolModel.appendRow(library.factory._tool_add(tb_nr, tool, fullpath))
            library.librarySave()
        else:
            print("Shapefile does not exist: {}".format(shape_full_path_fname))
    else:
        FreeCAD.Console.PrintWarning(">>>PathToolBitLibraryGui.checkWorkingDir() could not find user writable CAM working directory, macro exiting!\n\n")


def addToolListToCurrentLibrary(library, shape_name, dia_list,
                                tb_base_name, tb_base_nr, tb_nr_inc,
                                tool_props,
                                tb_name_rules):
    params = tool_props["parameter"]
    for d in dia_list:
        tb_nr = int(tb_base_nr + tb_nr_inc * d)
        params["Diameter"] = str(round(d, 3)) + " mm"
        tool_props["parameter"].update(params)

        # Set my dia based numbering prefix. If not required, only set = tb_base_name
        tool_props["name"] = str(int(round(tb_nr_inc * d, 2))) + "_" + tb_base_name
        # print("\tCreating: {}".format(tool_props["name"]))
        addToolToCurrentLibrary(library, shape_name, tool_props, tb_nr, tb_name_rules)


#TODO IMPORT at least csv
def importToolCsv():
    # import expect need set EVERY tool data via
    addToolToCurrentLibrary(endmill_tool_props, tb_nr, tb_name_rules)
    # THEN set individ props, like #Flutes, shank dia, material........


def processUserToolInput(tb_name_rules,
                         shape_name="endmill",
                         tb_base_name="default_em",
                         tb_base_nr=20000,
                         tb_nr_inc=100,
                         dia=8.12,           # Odd size so less likely to clash with existing TB
                         dia_max=0,
                         dia_inc=0
                        ):
    # FIXME review @least location of this "rule" & other TB name rules
    tb_nr = tb_base_nr + dia * tb_nr_inc

    # FIXME move dict to be module/global var once in Lib!!!

    # need any document open, no changes are made.
    if FreeCAD.ActiveDocument == None:
        doc = FreeCAD.newDocument()

    # FIXME user should not be editing this here ...should be in euser example code!!
    # Need to create dict for EACH known prop names FOR EVERY SHAPE TYPE that will be created.
    # NB 'name' is set to my default naming scheme for a SINGLE tool of dia (see about a dozen lines up)
    # Also this dictionary matches that used by FreeCAD for ToolBit

                                                            # 'name': str(int(round(tb_nr))) + tb_base_name,
    endmill_tool_props = {'shape': shape_name + '.fcstd', 'name': tb_base_name,
                                'parameter': {'CuttingEdgeHeight': '30.5 mm',
                                                'Diameter': str(dia) + ' mm',
                                                'Length': '50.0 mm',
                                                'ShankDiameter': '6.0 mm'},
                                'attribute': {'Chipload': '0.01 mm',
                                                'Flutes': 4,
                                                'Material': 'HSS',
                                                'SpindleDirection': 'Forward'}
                                }

    library = PathToolBitLibraryGui.ToolBitLibrary()
    workingdir = None

    if dia > 0:
        if dia_max > 0 and dia_inc > 0:

            dia_list = np.arange(dia, dia_max, dia_inc)
            print("ToolBit diameters to be created: ", dia_list)

            # CHOOSE to create many ToolBits & add to current library.
            addToolListToCurrentLibrary(library, shape_name, dia_list,
                                        tb_base_name, tb_base_nr, tb_nr_inc,
                                        endmill_tool_props,
                                        tb_name_rules)
        else:
            # create ONE ToolBit with diameter = dia
            addToolToCurrentLibrary(library, shape_name, endmill_tool_props, tb_nr, tb_name_rules)
    else:
        print("Tool diameter must be number greater than zero.")

    # print("...finished.\n")


def create_tb_name(tb_name_rules, tb_nr, tool_props):
    q = FreeCAD.Units.Quantity

    # TODO cope/warn about duplicate order#s
    segs_nested = dict()
    for k, v in tb_name_rules.items():
        if v["order"] > 0:
            s2 = {v["order"]: {k:v}}
            segs_nested.update(s2)

    # sort, so can collate all the parts on TB name in Users desired order
    od_segs_nested = collections.OrderedDict(sorted(segs_nested.items()))

    # now iterate od_segs_nested dict
    tb_name_template = ""
    tb_prop_val = None
    for k, v in od_segs_nested.items():
        for k1, v1 in v.items():
            if v1["ptype"] == "TbShape":
                tp = tool_props["parameter"]
                # FIXME what if that prop not exist???
                # TEST for str props - eg Material, SpindleDirection
                # test units, or add another control in in tb_name_rules?? <<< do as # digits on RHS of dec point. 0=int, -1= str???
                #   ++ float for all EXCEPT int for Flutes ?others?
                try:
                    tb_prop_val = q(tp[k1]).Value
                except KeyError:
                    # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                    pass
            elif v1["ptype"] == "TbAttributes":
                # Chipload  & SpindlePower=Float, Flutes=Integer, Material & SpindleDirection=text
                ta = tool_props["attribute"]
                if k1 == "Chipload" or k1 == "SpindlePower":
                    try:
                        tb_prop_val = q(ta[k1]).Value
                    except KeyError:
                        # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                        pass
                elif k1 == "Flutes":
                    try:
                        tb_prop_val = round(q(ta[k1]).Value)
                    except KeyError:
                        # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                        pass
                else:
                    try:
                        tb_prop_val = ta[k1]
                    except KeyError:
                        # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                        pass
            elif v1["ptype"] == "added_macro_prop":
                if k == 'shapename':
                    tb_prop_val = tool_props['shape']
                if k == 'base_name':
                    tb_prop_val = tool_props['name']
            else:
                print("ToolBit property type is not 'TbShape' \
                    or 'TbAttributes' or 'added_macro_prop', but is: ", v1["ptype"])

            # TODO TODO really showcase TB sev Shape types & sev NAME RULES
                        ## maybe auto create with Range of Flutes....
                        ## ++bulk import

            # FIXME what is the _3 at then end OF EVERY TB NAME???? eg: _9.0 mmD_4F_3
            # FIXME cater for None?? ie have default rules dict
            # FIXME and the space between dia# & 'mm'
            # TODO add My numbering tb_nr <<is it already calc from dia etc here???
            #       or only use tb_nr for the Library T#??
            # TODO
            # if the order# =1 SKIP adding v1["sep_left"]
            #     unless prepending my tb_nr
            tb_name_template += v1["sep_left"] + str(tb_prop_val) + v1["abbrev"] + v1["sep_r"]
    # print("==>", tb_name_template)

    return tb_name_template

#####################################################################

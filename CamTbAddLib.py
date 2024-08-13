# -*- coding: utf-8 -*-

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
import csv


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
                return shape_name, attrs


def getAllToolShapeProps(shape_name_dir, shape_names):
    props = dict()
    all_shape_attrs = dict()
    for i, fname in enumerate(shape_names):
        # FreeCAD.Console.PrintMessage("fname: {}\tshape_name_dir:{}\n".format(fname, shape_name_dir))
        shape_name, props = getToolShapeProps(shape_name_dir, fname)
        all_shape_attrs.update({shape_name: props})
    return all_shape_attrs


# Get all users available shape_names & all properties of each shape.
def getAllAvailUserShapeDetails():
    shapeDir, shape_names = getDefaultShapes()

    # Get all the shape properties and other attributes for each shpe.
    all_shape_attrs = getAllToolShapeProps(shapeDir, shape_names)

    return shape_names, all_shape_attrs


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

    # USE THE NEW TB_NAME_TMPLATE TO CHANGE endmill_tool_props["name"]..using TB values
    tb_name = create_tb_name(tb_name_rules, tb_nr, tool_props)
    tool_props["name"] = tb_name

    if PathToolBitLibraryGui.checkWorkingDir():
        workingdir = os.path.dirname(Path.Preferences.lastPathToolLibrary())

        tb_full_path_nr_name = workingdir + "/Bit/" + tool_props["name"] + ".fctb"

        shape_full_path_fname = workingdir + "/Shape/" + shape_name + ".fcstd"
        shape_full_path_fname_as_path = osPath(shape_full_path_fname)

        #  TODO : get shapes ...then again????
        # for FC code...need use real/existing shape OK
        # is here supposed to merge users shape props with tempale/existing shape??
        # shoulD be ABLE TO MOVE THIS TO top THIS MODULES - NO NEED REREAD EVERY TIME
        if shape_full_path_fname_as_path.is_file():
            # KISS BEGINNING remove above file check as well???
            shape_name, shape_full_path_fname_attrs = getToolShapeProps(workingdir + "/Shape/", shape_name)
            shape_full_path_fname_attrs_NEW = all_shape_attrs[shape_name]

            print(shape_full_path_fname_attrs)
            print()
            print(shape_full_path_fname_attrs_NEW)
            print()
            # if shape_full_path_fname_attrs == shape_full_path_fname_attrs_NEW:
            #     print("yea the SAME")
            # else:
            #     print("o oh!!!!!")
            # print()
            #
            # for k, v in shape_full_path_fname_attrs:
            #     if k in shape_full_path_fname_attrs_NEW:
            #         if v == shape_full_path_fname_attrs_NEW[k]:
            #             print(k, "BOTH values = ", v)
            #         else:
            #             print(k, "values DIFFER ", v, shape_full_path_fname_attrs_NEW[k])
            #
            #     else:
            #         print("Key {} not present in new attrs")

            print("TODO swap order of vars to check presence in New  & Not in old")
            params = shape_full_path_fname_attrs["parameter"]

            new_tool_params = tool_props["parameter"]
            print("Adding ToolBit Shape: {}, Dia: {} Name: {}"
                  .format(shape_name,
                          new_tool_params['Diameter'],
                          tool_props['name']
                          )
                )
            toolBitNew(library, tb_full_path_nr_name, shape_name, shape_full_path_fname, tool_props)

            library.temptool = None
            artifacts = FreeCAD.ActiveDocument.findObjects(Label=tool_props['name'])
            for o in artifacts:
                FreeCAD.ActiveDocument.removeObject(o.Name)

            for row in range(library.toolModel.rowCount()):
                # print (row, tb_nr, library.toolModel.item(row,0).text(), int(library.toolModel.item(row,0).text()))
                # print (row, tb_nr, library.toolModel.item(row,0).text())
                if float(library.toolModel.item(row,0).text()) == tb_nr:
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
    addToolToCurrentLibrary(tool_props, tb_nr, tb_name_rules)
    # THEN set individ props, like #Flutes, shank dia, material........

# TODO replace ALL tb_base_name var from default rules
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

    # need any document open, no changes are made.
    if FreeCAD.ActiveDocument == None:
        doc = FreeCAD.newDocument()
   
    # update tool_props with dia, tb_base_name
    tool_props = all_shape_attrs[shape_name]
    tool_props["name"] = tb_base_name

    tp = tool_props["parameter"] 
    tp["Diameter"] = dia
    tool_props.update(tp)

    library = PathToolBitLibraryGui.ToolBitLibrary()
    workingdir = None

    if dia > 0:
        if dia_max > 0 and dia_inc > 0:

            dia_list = np.arange(dia, dia_max, dia_inc)
            print("ToolBit diameters to be created: ", dia_list)

            # CHOOSE to create many ToolBits & add to current library.
            addToolListToCurrentLibrary(library, shape_name, dia_list,
                                        tb_base_name, tb_base_nr, tb_nr_inc,
                                        tool_props,
                                        tb_name_rules)
        else:
            # create ONE ToolBit with diameter = dia
            addToolToCurrentLibrary(library, shape_name, tool_props, tb_nr, tb_name_rules)
    else:
        print("Tool diameter must be number greater than zero.")

    # print("...finished.\n")

# Use rules with "order" > 0 and some tool_props
# to join segment data & seperators to create each tb name.
# TODO tb_nr should be redundant now - REMOVE.
def create_tb_name(tb_name_rules, tb_nr, tool_props):
    q = FreeCAD.Units.Quantity
    tp = tool_props["parameter"]
    # Save TB dia to calc TB# later
    t_dia = q(tp["Diameter"]).Value
    
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
    for k, v in od_segs_nested.items():
        tb_prop_val = ""
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
                try:
                    keyname = k1
                except KeyError:
                    # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                    pass
                if keyname == 'shapename':
                    tb_prop_val = tool_props['shape']
                if keyname == 'base_name':
                    tb_prop_val = tool_props['name']
                if keyname == "t_auto_number":
                    base_nr = v1["tb_base_nr"]
                    dia_multiplier = v1["tb_dia_mult"]
                    tb_prop_val = base_nr + dia_multiplier * t_dia

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

            # only add l/r seperators of value exists
            if len(str(tb_prop_val)) > 0:
                tb_name_template += v1["sep_left"] + v1["abbrev_left"] + str(tb_prop_val) + v1["abbrev_r"] + v1["sep_r"]
            # print("\t\t==>", k1, tb_name_template)

    return tb_name_template



# --- csv -----------------------------
# From user imm https://forum.freecadweb.org/viewtopic.php?f=15&t=59856&start=50
# -- any numeric value that can be converted to float is converted to float.

def fitem(item):
    item.strip()
    try:
        item = float(item)
    except ValueError:
        pass
    return item


# -- takes a header list and row list converts it into a dict.
# Numeric values converted to float in the row list wherever possible.
def row_convert(h, a):
    b = []
    for x in a:
        b.append(fitem(x))
    k = iter(h)
    it = iter(b)
    res_dct = dict(zip(k, it))
    return res_dct


# Uses header row as dictionary keys & each same row-column cell as values.
# Ignores empty(ish) rows at top of file
# Returns list of dictionaries for each row with "col-name: cell-value" pairs
def load_data(dataFile, print_csv_file_names=False):
    import os
    p = os.path.dirname(__file__)
    filename = p + '/' + dataFile

    if print_csv_file_names:
        print('load_data csv file: ', filename)

    data_dict = []

    # https://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c
    # To fix error on windows 7, UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 3701:
    # character maps to <undefined>
    import codecs
    with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as csvin:
        # with open(filename, 'r') as csvin:
        alist = list(csv.reader(csvin))
        firstLine = True
        for a in alist:
            if firstLine:
                # a  ['# -- null line below --'] 1
                # a =  [] 0
                # a =  ['# -- whitespace line below --'] 1
                # a =  ['   '] 1
                # a =  ['# -- comments here --'] 1
                # a =  ['# Diameters across top'] 1
                # counts are of # items in this row
                if len(a) == 0: continue  # noqa: E701
                if len(a) == 1:
                    continue  # noqa: E701
                else:
                    h = a  # becomes header LIST

                    firstLine = False
            else:
                data_dict.append(row_convert(h, a))

    return data_dict
# -------------------------------------
#####################################################################


# Init these when this Library imported, so only need to do slow-ish open/close files once
# BEWare IF SHAPE FILES CHANGE without another re/import!!!!
shape_names, all_shape_attrs = getAllAvailUserShapeDetails()
print("imported 'CamTbAddLib' and loaded all users Tool shape properties")

....SO below is debug trying work out how all_shape_attrs has DIFF content way above @ LINE: # KISS.......
    seems like user setting s for tb to create

print(all_shape_attrs)
print()
for k, v in all_shape_attrs.items():
    print(k, v["name"], "\t\t", end="")
    tp = v["parameter"]
    print(tp)
    for k1, v1 in tp.items():
        print(k1,v1)
    ta = v["attribute"]
    for k1, v1 in ta.items():
        print(k1,v1)

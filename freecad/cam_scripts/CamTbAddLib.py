# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.0.4  2024/09/16
__version__ = "V0.0.4  2024/09/16"


import os
import sys
# this is python module, not a FC module
from pathlib import Path as osPath

import FreeCAD
import FreeCADGui as Gui
import Path
import Path.Tool.Gui.BitLibrary as PathToolBitLibraryGui
import Path.Base.PropertyBag as PathPropertyBag
import Path.Base.Util as PathUtil

from PySide.QtCore import Qt
import numpy as np

from enum import Enum
import collections
import ast
import csv

from freecad.cam_scripts import NamingRulesLib


if False:
    Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
    Path.Log.trackModule(Path.Log.thisModule())
else:
    Path.Log.setLevel(Path.Log.Level.INFO, Path.Log.thisModule())


###################################################################
def getShapeNamesFromDir(shapeDir):
        s_names = []
        for f in os.listdir(shapeDir):
            if f.endswith('.fcstd'):
                s_names.append(os.path.splitext(f)[0])

        return s_names


def getAllShapeNamesFromDir(user=False):
    # get shapes User or system dir.
    if user:
        workingdir = os.path.dirname(Path.Preferences.lastPathToolLibrary())
        s_dir_name = os.path.sep + "Shape" + os.path.sep
        shapeDir = workingdir + s_dir_name
        dir_msg = "User Tool shapeDir: "
    else:
        if "PathWorkbench" in Gui.listWorkbenches():
            homep_to_shapes = "Mod/Path/Tools/Shape/"
        else:
            # assuming must be CAMWorkbench, becuse no other option!!!
            homep_to_shapes = "Mod/CAM/Tools/Shape/"

        shapeDir = FreeCAD.getHomePath() + homep_to_shapes
        shapeDir = shapeDir.replace("/", os.path.sep)
        dir_msg = "System Tool shapeDir: "

    s_names = getShapeNamesFromDir(shapeDir)
    print(f"{   dir_msg} has {len(s_names)} shapes in: {shapeDir}")

    return shapeDir, s_names


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
                        if isinstance(val, FreeCAD.Units.Quantity):
                            parameter = {p: val.toStr()}
                        else:
                            parameter = {p: val}
                        parameters.update(parameter)
                    elif grp == "Attributes":
                        if isinstance(val, FreeCAD.Units.Quantity):
                            attribute = {p: val.toStr()}
                        else:
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


def getShapePropsFromDir(shape_name_dir, s_names):
    props = dict()
    all_shp_at = dict()
    for i, fname in enumerate(s_names):
        shape_name, props = getToolShapeProps(shape_name_dir, fname)
        all_shp_at.update({shape_name: props})
    return all_shp_at


def getAllShapeDetails():
    # Only do this ONCE as slow-ish open/close ALL shape files IN FreeCAD!
    # Get all users available shape_names & all properties of each shape.
    is_global = "avail_shape_details" in globals()
    # Only every edit this global here, so other uses do not need global
    if is_global:
        return
    else:
        global avail_shape_details
    
        # *Opens* every FC shape DOCUMENT to retreive properties!
        shapeDirUser, s_namesUser = getAllShapeNamesFromDir(user=True)
        all_shp_attrUser = getShapePropsFromDir(shapeDirUser, s_namesUser)

        shapeDirSys, s_namesSys = getAllShapeNamesFromDir(user=False)
        all_shp_attrSys = getShapePropsFromDir(shapeDirSys, s_namesSys)

        # NB User shapes might OFTEN be empty!!!
        avail_shape_details = dict({"user": {"dir": shapeDirUser,
                                            "shape_names": s_namesUser,
                                            "attr": all_shp_attrUser}})
        avail_shape_details.update({"system": {"dir": shapeDirSys,
                                            "shape_names": s_namesSys,
                                            "attr": all_shp_attrSys}})


def get_list_all_shape_names():
    # Shape names can be in System and User directories
    # In this example, BOTH lists are retreived & joined
    # so that ToolBits for EVERY AVAILABLE shape will be created.
    getAllShapeDetails()
    shape_names = avail_shape_details["user"]['shape_names'] +\
                    avail_shape_details["system"]['shape_names']
    return shape_names


def find_shape_location(shape_name):
    if shape_name.endswith(".fcstd"):
        shape_name = shape_name[:-len(".fcstd")]

    #print("find_shape_location ", shape_name)
    
    s_location = None
    s_dir = None
    
    getAllShapeDetails()
        
    if shape_name in avail_shape_details["system"]['shape_names']:
        s_location = "system"
    elif shape_name in avail_shape_details["user"]['shape_names']:
        s_location = "user"

    s_dir = avail_shape_details[s_location]["dir"]

    #print("find_shape_location ", s_location, s_dir)
    return s_location, s_dir


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


def addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules=None, dbg_print=False):
    # if dbg_print:
    #     print("dbg_print addToolToCurrentLibrary")
    import freecad.cam_scripts.NamingRulesLib as nrl
    # nrl.Rules
    # <class 'freecad.cam_scripts.NamingRulesLib.Rules'>

    tb_name = ""
    tb_nr = 1
    if tb_name_rules is None:
        tb_name = str(tool_props["parameter"]['Diameter']) +\
                    "_" +  shape_name
    elif isinstance(tb_name_rules, str):
        tb_name = tb_name_rules
    elif isinstance(tb_name_rules, nrl.Rules):
        tb_name = tb_name_rules.create_tb_name(tool_props, dbg_print)
        tb_nr = tb_name_rules.create_tb_nr(tool_props, dbg_print)
    else:
        print("Warning skipping Tool: naming_rules type must be Empty(None), "
              "String or Rules, not: ", type(tb_name_rules))
        return
    tool_props["name"] = tb_name

    # As lastPathBitLibrary etc can be empty or point to entirely different library,
    # ...now deriving Bit dir from Lib dir, as ALL the example macros
    # work with CURRENT library, so Bit dir must also be in same Lib.
    lib_dir = Path.Preferences.lastPathToolLibrary()
    head, tail = os.path.split(lib_dir)
    if not (tail == "Library"):
        print("Cannot find Tools Library directory!")
        return

    if len(head) > 0:
        tb_full_path_nr_name =  head + os.sep + "Bit" + os.sep +\
                                tool_props["name"] + ".fctb"
    else:
        print("Cannot find Tools Library parent directory!")
        return



    s_location, s_dir = find_shape_location(shape_name)
    shape_full_path_fname = s_dir + shape_name + ".fcstd"
    shape_full_path_fname_as_path = osPath(shape_full_path_fname)

    if shape_full_path_fname_as_path.is_file():
        shape_full_path_fname_attrs = avail_shape_details[s_location]['attr'][shape_name]
            
        params = shape_full_path_fname_attrs["parameter"]

        new_tool_params = tool_props["parameter"]
        print("\tAdding ToolBit Shape: {}, Dia: {} Name: {}"
                .format(shape_name,
                        new_tool_params['Diameter'],
                        tool_props['name']
                        )
            )
        if dbg_print:
            print(library, tb_full_path_nr_name, shape_name, shape_full_path_fname, tool_props)

        toolBitNew(library, tb_full_path_nr_name, shape_name, shape_full_path_fname, tool_props)

        library.temptool = None
        artifacts = FreeCAD.ActiveDocument.findObjects(Label=tool_props['name'])
        for o in artifacts:
            FreeCAD.ActiveDocument.removeObject(o.Name)

        # Disabling as repetitive searches of Library as slow, esp as table grows larger!
        # Ultimately it is user cheoice to add duplicates or not.
        # Also library tables can be sorted to aid management
        # for row in range(library.toolModel.rowCount()):
        #     if float(library.toolModel.item(row,0).text()) == tb_nr:
        #         FreeCAD.Console.PrintWarning("Tool number {} already exists for Tool {}.\n"
        #                                         .format(tb_nr, tool_props["name"]))

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


def addToolListToCurrentLibrary(library, shape_name, dia_list,
                                tb_base_name, tb_base_nr, tb_nr_inc,
                                tool_props,
                                tb_name_rules=None, dbg_print=False):
    if dbg_print:
        print("dbg_print addToolListToCurrentLibrary")
    for d in dia_list:
        tb_nr = int(tb_base_nr + tb_nr_inc * d)
        tool_props["parameter"]["Diameter"] = str(round(d, 3)) + " mm"

        # Set my dia based numbering prefix. If not required, only set = tb_base_name
        tool_props["name"] = str(int(round(tb_nr_inc * d, 2))) + "_" + tb_base_name
        addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print)



def importToolCsv(csvfile, rules, dbg_print=False):
    # import expect need set EVERY tool data via

    # NOPE see example file: addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print=False))
    # THEN set individ props, like #Flutes, shank dia, material........

    getAllShapeDetails()
    # Imports csv as LIST of dicts of each row, ie header row cells are dict Keys
    data_list = load_data(csvfile)

    count_success = 0
    count_fail = 0
    for row_dict in data_list:
        if createToolFromProps(rules, row_dict, dbg_print=False):
            count_success += 1
        else:
            count_fail += 1

    return count_success, count_fail


def deepcopy_toolprops(tp):
    # Cannot copy/deepcopy all_shape_attrs[] due to the FC Quantities
    # Not removing Quantities as really want those to help validate
    # lots Speed&Feeds calc with diff units & vary dif data sources...
    tool_props_str = "{"
    for k, v in tp.items():
        if k == "parameter":
            tool_props_str += "'parameter': {"
            for k1, v1 in v.items():
                tool_props_str += "'" + k1 + "': '" + str(v1) + "', "
            tool_props_str += "}, "
        elif k == "attribute":
            tool_props_str += "'attribute' : {"
            for k1, v1 in v.items():
                tool_props_str += "'" + k1 + "': '" + str(v1) + "', "
        else:
            tool_props_str += "'" + k + "': '" + v + "', "
    tool_props_str += "}}"
    
    tool_props = ast.literal_eval(tool_props_str)

    return tool_props


def convert_imported_val(col, ip_val):
    # TODO extend with DATA type ie str, int, float and convert incoming data, else warning

    if isinstance(ip_val, str) and len(ip_val) < 1:
        ip_val = 0
    try:
        ip_val = float(ip_val)
    except ValueError:
        print("\t\tWARNING: In column {}, cannot convert {} to Float"\
            .format(col, ip_val))

    return ip_val


def createToolFromProps(tb_name_rules, imported_t_props, dbg_print=False):
    # imported_t_props is dict of imported data(typically), so need match keys to known tool properties...
    #NB tool_props CHANGE with diff shape!!!
    mandatory_imported_t_props_found = {'shape': False, 'parameter': {'Diameter': False}}
    tool_props = dict()
    shape_name = imported_t_props['shape']
    shape_names = get_list_all_shape_names()

    s_location = ""
    s_dir = ""
    if shape_name in shape_names:
        s_location, s_dir = find_shape_location(shape_name)
        if s_location is None:
            print("Shape '{}' is not in User or System shape directory.".format(shape_name))
            print("\tUser shapes found are: {}."
                    .format(avail_shape_details["user"]['shape_names']))
            print("\tSystem shapes found are: {}."
                    .format(avail_shape_details["system"]['shape_names']))
            print()

            return False
        tool_props = deepcopy_toolprops(avail_shape_details[s_location]['attr'][shape_name])
        mandatory_imported_t_props_found['shape'] = True
        # force Diameter = 0, in case error traps below fail...
        tool_props['parameter']['Diameter'] = 0.0
        dia = 0
        tp = tool_props['parameter']
        for tpk, v in tp.items():
            if tpk in imported_t_props.keys():
                if tpk in mandatory_imported_t_props_found['parameter'].keys():
                    mandatory_imported_t_props_found['parameter'][tpk] = True
                tp[tpk] = float(convert_imported_val(tpk, imported_t_props[tpk]))

        ta= tool_props['attribute']
        for tak, v in ta.items():
            if tak in imported_t_props.keys():
                ta[tak] = float(convert_imported_val(tak, imported_t_props[tak]))

        # TODO +++PROB need for other props like len & deg... - so make method!!!
        dia = float(convert_imported_val('Diameter', tool_props['parameter']['Diameter']))
        try:
            # Keep FC:Quantity if possible for future unit management in Speeds & Feeds calculations
            dia = q(tool_props["parameter"]["Diameter"]).Value
        except:
            print("\t\tWARNING: Warning 'Diameter' is NOT a valid number: ",
                tool_props['parameter']['Diameter'])
    else:
        print("\t ignoring shape : {}. It is not in user shapes folder {}:"
              .format(shape_name, os.path.dirname(Path.Preferences.lastPathToolLibrary())))
        return False

    if mandatory_imported_t_props_found['parameter']['Diameter'] == False:
        print("Mandatory property 'Diameter' not found, ignoring this tool bit" )
        return False
    else:
        pass
        # TODO review @least location of this "rule" & other TB name rules

    if 'Flutes' in tool_props['attribute'].keys():
        tool_props['attribute']['Flutes'] =\
            int(convert_imported_val('Flutes', tool_props['attribute']['Flutes']))

    tool_props['parameter']['Diameter'] = dia

    # need any document open, no changes are made.
    if FreeCAD.ActiveDocument == None:
        doc = FreeCAD.newDocument()

    # FYI: below is sort of code that code be moved/run ONCE for performance!
    library = PathToolBitLibraryGui.ToolBitLibrary()

    addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print)

    return True


# TODO replace ALL tb_base_name var from default rules
def processUserToolInput(tb_name_rules=None,
                         shape_name="endmill",
                         tb_base_name="default_em",
                         tb_base_nr=20000,
                         tb_nr_inc=100,
                         dia=8.12,           # Odd size so less likely to clash with existing TB
                         dia_max=0,
                         dia_inc=0,
                         flutes=3,
                         dbg_print=False
                        ):
    #dbg_print=True
    if dbg_print:
        # print("dbg_print processUserToolInput")
        print("---> processUserToolInput tb_base_nr: ", tb_base_nr)

    getAllShapeDetails()

    s_location, s_dir = find_shape_location(shape_name)
    if s_location is None:
        print("Shape '{}' is not in User or System shape directory.".format(shape_name))
        print("\tUser shapes found are: {}."
                .format(avail_shape_details["user"]['shape_names']))
        print("\tSystem shapes found are: {}."
                .format(avail_shape_details["system"]['shape_names']))
        print()

        return


    try:
        dia=float(dia)
    except ValueError:
        print("Warning dia is NOT a valid number!")
        return

    tb_nr = tb_base_nr + dia * tb_nr_inc

    # need any document open, no changes are made.
    if FreeCAD.ActiveDocument == None:
        doc = FreeCAD.newDocument()

    # FYI: below is sort of code that code be moved/run ONCE for performance!
    # global avail_shape_details
    getAllShapeDetails()
        
    # an oops paste?? shapeDirUser, s_namesUser = getAllShapeNamesFromDir(user=True)
    
    tool_props = deepcopy_toolprops(avail_shape_details[s_location]['attr'][shape_name])
    
    tool_props['parameter']['Diameter'] = dia
    tool_props['attribute']['Flutes'] = flutes
    
    # FYI: below is sort of code that code be moved/run ONCE for performance!
    library = PathToolBitLibraryGui.ToolBitLibrary()
    #workingdir = None

    if dia > 0:
        if dia_max > 0 and dia_inc > 0:
            dia_list = np.arange(dia, dia_max, dia_inc)
            print("\tToolBit diameters to be created: ", dia_list)

            # CHOOSE to create many ToolBits & add to current library.
            addToolListToCurrentLibrary(library, shape_name, dia_list,
                                        tb_base_name, tb_base_nr, tb_nr_inc,
                                        tool_props, tb_name_rules,
                                        dbg_print
                                        )
        else:
            # create ONE ToolBit with diameter = dia
            addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print)
    else:
        print("Tool diameter must be number greater than zero.")

    # print("processUserToolInput...finished.\n")




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




q = FreeCAD.Units.Quantity

print(f"CamTbAddLib (CAM ToolBit Add Library) {__version__} module imported")

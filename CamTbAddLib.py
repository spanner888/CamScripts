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
import ast
import csv

if False:
    Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
    Path.Log.trackModule(Path.Log.thisModule())
else:
    Path.Log.setLevel(Path.Log.Level.INFO, Path.Log.thisModule())


# FIXME FIXME 0: DO not get SYSTEM shapes from user dir!!!
#                 DO still *also* get user shapes....
#     IDEA - MOST likely best NOT to use....but just note idea fyi
#     could copy sys shapes to a DIFF dir under user tools
# +++ macro to open/recalc/save *all* SYSTEM macros
#
# FreeCAD.getHomePath()
# '/home/spanner888/Documents/_source/_APPS/FC_wkly-38459/squashfs-root/usr/'
# /Mod/CAM/Tools/Shape/endmill.fcstd
#
# If NO user Tool dir or any type esp shape...ignore

# SO NOW: next steps from rename of: shape_names, all_shape_attrs
#     ...to below.
#     For every use of EITHER *old* var:
#         rename *and* dup code or ADD module to process second set/both sets if module


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
        dir_msg = "User shapeDir: "
    else:
        homep_to_shapes = "Mod/CAM/Tools/Shape/"
        shapeDir = FreeCAD.getHomePath() + homep_to_shapes
        shapeDir = shapeDir.replace("/", os.path.sep)
        dir_msg = "System shapeDir: "

    s_names = getShapeNamesFromDir(shapeDir)
    # print(dir_msg, shapeDir, s_names)

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


# Get all users available shape_names & all properties of each shape.
def getAllShapeDetails():
    # *Opens* every FC shape DOCUMENT to retreive properties!

    shapeDirUser, s_namesUser = getAllShapeNamesFromDir(user=True)
    all_shp_attrUser = getShapePropsFromDir(shapeDirUser, s_namesUser)

    shapeDirSys, s_namesSys = getAllShapeNamesFromDir(user=False)
    all_shp_attrSys = getShapePropsFromDir(shapeDirSys, s_namesSys)

    avail_shape_details = dict({"user": {"dir": shapeDirUser,
                                         "shape_names": s_namesUser,
                                         "attr": all_shp_attrUser}})
    avail_shape_details.update({"system": {"dir": shapeDirSys,
                                           "shape_names": s_namesSys,
                                           "attr": all_shp_attrSys}})

    # return s_namesUser, all_shp_attrUser, s_namesSys, all_shp_attrSys
    return avail_shape_details


def get_list_all_shape_names():
    # Shape names can be in System and User directories
    # In this example, BOTH lists are retreived & joined
    # so that ToolBits for EVERY AAVILABLE shape will be created.
    avail_shape_details = getAllShapeDetails()
    shape_names = avail_shape_details["user"]['shape_names'] +\
                    avail_shape_details["system"]['shape_names']
    return shape_names


def find_shape_location(shape_name):
    s_location = None
    if shape_name in avail_shape_details["user"]['shape_names']:
        s_location = "user"
    elif shape_name in avail_shape_details["system"]['shape_names']:
        s_location = "system"

    s_dir = avail_shape_details[s_location]["dir"]

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


def addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print=False):
    # if dbg_print:
    #     print("dbg_print addToolToCurrentLibrary")
    # FIXME INTERIM usign BOTH old/new-class tb_name_rules
    # print("tool_props:", tool_props)
    tb_name = tb_name_rules.create_tb_name(tool_props, dbg_print)
    tool_props["name"] = tb_name

    s_dir_type, s_dir = find_shape_location(shape_name)

    bit_dir = Path.Preferences.lastPathToolBit()
    bit_dir = os.path.dirname(bit_dir)
    if len(bit_dir) > 0:
        tb_full_path_nr_name =  bit_dir + "/Bit/" + tool_props["name"] + ".fctb"
    else:
        print("Preference LastPathToolBit is empty, cannot proceed.")
        return

    tb_nr = tb_name_rules.create_tb_nr(tool_props, dbg_print)

    shape_full_path_fname = s_dir + shape_name + ".fcstd"
    shape_full_path_fname_as_path = osPath(shape_full_path_fname)

    if shape_full_path_fname_as_path.is_file():
        shape_full_path_fname_attrs = avail_shape_details[s_dir_type]['attr'][shape_name]
            
        params = shape_full_path_fname_attrs["parameter"]

        new_tool_params = tool_props["parameter"]
        print("\tAdding ToolBit Shape: {}, Dia: {} Name: {}"
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


def addToolListToCurrentLibrary(library, shape_name, dia_list,
                                tb_base_name, tb_base_nr, tb_nr_inc,
                                tool_props,
                                tb_name_rules, dbg_print=False):
    if dbg_print:
        print("dbg_print addToolListToCurrentLibrary")
    for d in dia_list:
        tb_nr = int(tb_base_nr + tb_nr_inc * d)
        tool_props["parameter"]["Diameter"] = str(round(d, 3)) + " mm"

        # Set my dia based numbering prefix. If not required, only set = tb_base_name
        tool_props["name"] = str(int(round(tb_nr_inc * d, 2))) + "_" + tb_base_name
        addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print)


#TODO IMPORT at least csv
def importToolCsv():
    # import expect need set EVERY tool data via
    # NOPE see eampole file: addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print=False))
    # THEN set individ props, like #Flutes, shank dia, material........
    pass


def deepcopy_toolprops(tp):
    # Cannot copy/deepcopy all_shape_attrs[] due to the FC Quantities
    # Not removing Quantities as really want those to help validate
    # lots Speed&Feeds calc with diff units & vary dif data sources...
    tool_props_str = "{"
    for k, v in tp.items():
        if k == "parameter":
            tool_props_str += "'parameter': {"
            for k1, v1 in v.items():
                #print(k1, v1 )
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

    if shape_name in shape_names:
        s_location, s_dir = find_shape_location(shape_name)
        if s_location is None:
            print("Shape '{}' is not in User or System shape directory.".format(shape_name))
            print("\tUser shapes found are: {}."
                    .format(avail_shape_details["user"]['shape_names']))
            print("\tSystem shapes found are: {}."
                    .format(avail_shape_details["system"]['shape_names']))
            print()

            return
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

        # FIXME +++PROB need for othr props like len & deg... - so make method!!!
        dia = float(convert_imported_val('Diameter', tool_props['parameter']['Diameter']))
        try:
            # Keep FC:Quantity if possible for future unit management in Speeds & Feeds calculations
            dia = q(tool_props["parameter"]["Diameter"]).Value
        except:
            print("\t\tWARNING: Warning 'Diameter' is NOT a valid number: ",
                tool_props['parameter']['Diameter'])
    else:
        print("\t ignoring shape name: {}. It is not in user shapes folder:".format(shape_name))
        return

    if mandatory_imported_t_props_found['parameter']['Diameter'] == False:
        print("Mandatory property 'Diameter' not found, ignoring this tool bit" )
        return
    else:
        pass
        # FIXME review @least location of this "rule" & other TB name rules

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


# TODO replace ALL tb_base_name var from default rules
def processUserToolInput(tb_name_rules,
                         shape_name="endmill",
                         tb_base_name="default_em",
                         tb_base_nr=20000,
                         tb_nr_inc=100,
                         dia=8.12,           # Odd size so less likely to clash with existing TB
                         dia_max=0,
                         dia_inc=0,
                         dbg_print=False
                        ):
    # if dbg_print:
    #     print("dbg_print processUserToolInput")

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
    tool_props = deepcopy_toolprops(avail_shape_details[s_location]['attr'][shape_name])
    tool_props['parameter']['Diameter'] = dia

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
                                        dbg_print=False
                                        )
        else:
            # create ONE ToolBit with diameter = dia
            addToolToCurrentLibrary(library, shape_name, tool_props, tb_name_rules, dbg_print)
    else:
        print("Tool diameter must be number greater than zero.")

    # print("processUserToolInput...finished.\n")

    # FIXME review @least location of this "rule" & other TB name rules

# --- Rules using Classes -----------------------------

# TODO add helpers eg:
#       show props in order & example of the rule based name
#       alert if dup order#s
#       alert if order >0, but no other props set
#       dump all props that have val
# TODO #1-ish Let user define alt Tool-prop names &/or just select default alternatives, from ISO, Imperial....
#       & let user edit/add more templates/sets....

from enum import Enum
import collections
# Each rule item, must be one of these types.
class PropType(Enum):
    rule_prop = 'rule_prop',
    user_prop = 'user_prop',
    tb_attrib = 'TbAttributes',
    tb_shape = 'tb_shape'


class RuleItem:
    def __init__(self, name,
                       ptype: PropType,
                       order=0) -> None:
        self.pref_name = name
        self.ptype = ptype
        self.abbrev_left = ''
        self.abbrev_r = ''
        self.sep_left = ''
        self.sep_r = ''
        self.order = order

    def __str__(self) -> str:
        return f'ptype: {self.ptype.name}'
        # yield f'{ptype <<get str(class.prop)}: {self.ptype.name}'


class Rules:
    def __init__(self, shape_name):
        self.activeSortedRules = self.getActiveSortedRules()

    def getActiveSortedRules(self, dbg_print=False):
        # TODO cope/warn about duplicate order#s
        segs_nested = dict()
        for k, v in vars(self).items():
            # print("k, v", k, v)
            if v.order > 0:
                s2 = {v.order: {k:v}}
                segs_nested.update(s2)
        # sort, so can collate all the parts on TB name in Users desired order
        od_segs_nested = collections.OrderedDict(sorted(segs_nested.items()))
        if dbg_print:
            print("dbg_print: Active, ordered rules:", od_segs_nested)

        return od_segs_nested


    def create_tb_name(self, tool_props, dbg_print=False):
        # if dbg_print:
        #     print("create_tb_name CLASS create_tb_name")
        # Save TB dia to calc TB# later
        t_dia = q(tool_props["parameter"]["Diameter"]).Value


        # now iterate activeSortedRules dict
        tb_name_template = ""
        for k, v in self.activeSortedRules.items():
            tb_prop_val = ""
            for k1, v1 in v.items():
                #print("\t", v1.ptype)
                if v1.ptype == PropType.tb_shape:
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
                elif v1.ptype == PropType.tb_attrib:
                    # Chipload  & SpindlePower=*BOOLEAN*, Flutes=Integer, Material & SpindleDirection=text
                    ta = tool_props["attribute"]
                    if k1 == "Chipload" or k1 == "SpindlePower":
                        try:
                            tb_prop_val = q(ta[k1]).Value
                        except (ValueError, KeyError) as e:
                            # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                            # or is text or boolean & cannot be evaluated as a FC Quantity
                            pass
                    elif k1 == "Flutes":
                        try:
                            tb_prop_val = round(q(ta[k1]).Value)
                        except (ValueError, KeyError) as e:
                            # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                            # or is text or boolean & cannot be evaluated as a FC Quantity
                            pass
                    else:
                        try:
                            tb_prop_val = ta[k1]
                        except (ValueError, KeyError) as e:
                            # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                            # or is text or boolean & cannot be evaluated as a FC Quantity
                            pass
                elif v1.ptype == PropType.rule_prop:
                    try:
                        keyname = k1
                    except KeyError:
                        # Specified name rule Property does NOT exist in this ToolBit, IGNORE
                        pass
                    if keyname == 'shapename':
                        # tb_prop_val = tool_props['shape']
                        tb_prop_val = os.path.splitext(tool_props['shape'])[0]
                    if keyname == 'base_name':
                        tb_prop_val = tool_props['name']
                    if keyname == "t_auto_number":
                        base_nr = v1.tb_base_nr
                        dia_multiplier = v1.tb_dia_mult
                        tb_prop_val = base_nr + dia_multiplier * t_dia
                elif v1.ptype == PropType.user_prop:
                    print("TODO add code for PropType.user_prop....hmm mainly for IMPORT, eg tool-Family, Brand/Model, uid, ...")
                    print("...so get rule as above, but save the specific data to temp var to use @ end - like dia @top??")
                    print("     or build partial string here???")
                    print("IS >>>>>PropType.user_prop<<<< actually req or is simialr idea for toolprop ...imported what req??")
                else:
                    print("ToolBit property type is not 'TbShape' \
or 'TbAttributes' or 'added_macro_prop', but is: ", v1.ptype)

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
                    tb_name_template += v1.sep_left + v1.abbrev_left + str(tb_prop_val) + v1.abbrev_r + v1.sep_r
                # print("\t\t==>", k1, tb_name_template)

        return tb_name_template


    def create_tb_nr(self, tool_props, dbg_print):
        # ???if NO self.t_auto_number.tb_base_n/tb_dia_mult
        # or no self.t_auto_number
        # DO NOT create via this rule!!!!
        # some dflt#...or get next avail in lib
        #     >>>could get save every time add TB??

        # Force to be a number, else create attrib/s=0/1
        if hasattr(self, 't_auto_number'):
            if hasattr(self.t_auto_number, 'tb_base_nr'):
                if not type(self.t_auto_number.tb_base_nr) in (int, float):
                    self.t_auto_number.tb_base_nr = 0
            else:
                self.t_auto_number.tb_base_nr = 0

            if hasattr(self.t_auto_number, 'tb_dia_mult'):
                if not type(self.t_auto_number.tb_dia_mult) in (int, float):
                    self.t_auto_number.tb_dia_mult = 1
            else:
                self.t_auto_number.tb_dia_mult = 1
        else:
            self.t_auto_number = RuleItem(name='', ptype=PropType.rule_prop)
            self.t_auto_number.tb_base_nr = 0
            self.t_auto_number.tb_dia_mult = 1

        # Get dia as FC Quantity...then Value
        # ATM for the create, not import code
        dq = q(tool_props["parameter"]["Diameter"]).Value

        tb_nr = round(self.t_auto_number.tb_base_nr +\
                    self.t_auto_number.tb_dia_mult *\
                        dq)
        return tb_nr
# -------------------------------------


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



# Init these when this Library imported,
#   so only need to do slow-ish open/close shape files IN FreeCAD once!


# s_names_User, all_shp_attr_User, s_names_Sys, all_shp_attr_Sys = getAllShapeDetails()
avail_shape_details = getAllShapeDetails()
# print(avail_shape_details)
# print("imported 'CamTbAddLib' and loaded all user & systems Tool shape_names & properties")
# print("at import found User shapes: ", avail_shape_details["user"])
# print("at import found System shapes: ", avail_shape_details["system"])
# print()

q = FreeCAD.Units.Quantity

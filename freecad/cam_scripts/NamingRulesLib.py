# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.3  2024/09/10
__version__ = "V0.3  2024/09/10"

from enum import Enum
import collections
import os

import FreeCAD
q = FreeCAD.Units.Quantity

# --- Rules using Classes -----------------------------
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


#New shapes... just assing some BASE & log so user can update
#user can update >>> easy way to do this ...eg in the rules!!!
#so create enum in rules & user can update
#thaen use OPTIONALLY BACK HERE???
#???FOR SHAPE MAYBE/OPTION EXACT MATCH OR CONTAINS
# >>>PROB ONLY WAY to stop dups (both TB file & Lib-ToolTable NUMBER) is check first then 
#       ...then have to CHANGE numbering scheme!!! ...say base_nr*100....
# totally change scheme so dia part is FIRST...then leave say 2/3 trailing digits to avoid dupes
# or even SKIP ToolTable #s...let FC handle....so if need #, get from TB NAME...if is 1st item in name...can sort...
# or for TB...ONLY use the bsae #, eg 2# = endmill, & ignore the 99.99 dia...ALREADY HAVE DIA as option!!!
# NB Tool table can sort by #, name or shape!!!...as well as many tables/libs
# MAYBE one part of all this is use from csv or create & write back to csv some unitque TolID
#    ...then if reimport ....can at at skip SAME tool in CURRENT lib....or maybe dif function to find from LIST of Libs/tables....and DO SOMEHTING
# STILL *also* POSS DUP NAME ISSUE ....which is suspect of casuing some Tool Not found errors?????

# OOOOOOPS nto part of class hsould it be????
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


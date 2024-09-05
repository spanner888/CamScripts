# -*- coding: utf-8 -*-

# Copyright 2024 Spanner888 Licensed under GNU GPL (v2+)
# V0.1  2024/08/31

# allow edited library updates, without close/reopen FC.
from importlib import reload
import freecad.cam_scripts.CamTbAddLib as CamTbAddLib
reload(CamTbAddLib)

# Code derived from or inspired by:
# FC sliptonic: toolbit-attributes.py & several more CAM-Path modules
# russ JobUtils and related FC changes
# FreeCAD forum users & developers:
#   russ/sliptonic/imm/onekk

# DESC Create ToolBits from definitions or import csv. Add to CAM Tool Library
# Details and how to use in README.MD
# Flexible rule based TB names auto derived from selected TB properties
#   Any Tool property in specified order, with pre/post seperators and Abbreviations/Units
# LIMITATION: If you duplicate and order# in a second item, it will NOT show in TB name.
# Rules "debug mode" pass in dbg_print=True and prnted to console are:
#   toolprops and ordered list of rules WITH order >0.

from importlib import reload
import freecad.cam_scripts.naming_rules.ex_naming_rules as ex_rules
reload(ex_rules)

def ctba_example():
    # create a naming rules object with DESIRED rules
    tb_class_naming_rules = ex_rules.Ex1Rules(shape_name='any')
    boboxx_rulesShape = ex_rules.BoboxxRulesShape(shape_name='endmill')
    exagerated_rules_example = ex_rules.ExageratedRulesExample(shape_name='endmill')

    # Six examples on adding a Default, One or a list of Tools to current Library,
    # with differing naming rule examples.
    print("Examples 1 and 2 use a sample set of ToolBit naming rules.")
    print("Example 3 matches naming rules suggested by github user boboxx")
    print("Example 4 uses exagerated_rules_example, to show how dif properties only appear when present.")
    print("Example 5 add Shape name to RHS of boboxx rules.")
    print("Example 6 Shows what happens with an empty naming rule set.")
    print()
    # -----------------------------------------------------------------------
    print("Example 1. Add single example default endmill to current Library.")
    CamTbAddLib.processUserToolInput(tb_class_naming_rules, dbg_print=False)
    print("\t...Example 1 finished.\n")
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    print("Example 2. Add SINGLE Tool 6.35 mm dia to current library, shows all settings")
    CamTbAddLib.processUserToolInput(tb_class_naming_rules,
                                    shape_name = "endmill",
                                    tb_base_name = "em",
                                    tb_base_nr = 20000,
                                    tb_nr_inc = 100,
                                    dia = 6.35,
                                    dia_max = 0,
                                    dia_inc = 0,
                                    flutes=4)
    print("\t...Example 2 finished.\n")
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    print("Example 3. Create many tools: dia to dia_max, increment dia_inc")
    #   But only If BOTH dia_max & dia_inc are greater than zero,
    #            Else: ONLY create ONE TB of this dia in current library.
    CamTbAddLib.processUserToolInput(boboxx_rulesShape,
                                    shape_name = "endmill",
                                    tb_base_name = "em",
                                    tb_base_nr = 20000,
                                    tb_nr_inc = 100,
                                    dia = 8.2,
                                    dia_max = 9.0,
                                    dia_inc = 0.2,
                                    flutes=4)
    print("\t...Example 3 finished.\n")
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    print("Example 4. For EVERY Tool Shape SINGLE Tool 3.125 mm dia to current library")
    # Shape names can be in System and User directories
    # In this example, BOTH lists are retreived & joined
    # so that ToolBits for EVERY AVILABLE shape will be created.
    # avail_shape_details = CamTbAddLib.getAllShapeDetails()
    # shape_names = avail_shape_details["user"]['shape_names'] +\
    #                 avail_shape_details["system"]['shape_names']
    shape_names = CamTbAddLib.get_list_all_shape_names()
    for s in shape_names:
        CamTbAddLib.processUserToolInput(exagerated_rules_example,
                                        shape_name = s,
                                        tb_base_name = s + "_example",
                                        tb_base_nr = 20000,
                                        tb_nr_inc = 100,
                                        dia = 3.125,
                                        dia_max = 3.5,
                                        dia_inc = 0.125,
                                        flutes=2)
    print("\t...Example 4 finished.\n")
    # -----------------------------------------------------------------------


    # -----------------------------------------------------------------------
    print("Example 5. User boboxx naming rules Example: 2F-D6.35-L31.076, FC issue:12823")
    boboxx_rules = ex_rules.BoboxxRules(shape_name='endmill')
    CamTbAddLib.processUserToolInput(boboxx_rulesShape,
                                    shape_name = "endmill",
                                    tb_base_name = "em",
                                    tb_base_nr = 70000,
                                    tb_nr_inc = 100,
                                    dia = 10.3,
                                    dia_max = 10.4,
                                    dia_inc = 0.2,
                                    flutes=4)
    print("\t...Example 5 finished.\n")
    # -----------------------------------------------------------------------


    print("")
    print("CamTbAddExample finished.\n")

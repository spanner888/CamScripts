# -*- coding: utf-8 -*-

import freecad.cam_scripts.CamTbAddLib as CamTbAddLib

# Contains rules used to create ToolBit names, based on TB property values, seperators, Abbreviations
# and an auto numbering based on:
# FIXME finish here ++ duplicate/merge with info in example
# make sure the NOT included if value=0 AND TESTED!!!!

# Rules included here:
#   1. Ex1Rules
#   2. Duplicate User boboxx Example: 2F-D6.35-L31.076, FC issue:12823
#   NB above are "trimmed" rule sets including only
#       the active rules where .order >0
#       and the mandatory, but as yet unused shapename.
#   3. AllRulesTemplate.
#       These are all possible rules matching default FreeCAD tool shapes.
#       Copy to use as template for your own custom rules.
#       Optionaly remove any rules with order = 0.
#       FIXME: doc the dbg_print to print active rules "helper"

# To see all CURRENT shape properties to use as rules, either
# FIXME FIXME print_Tb <<<MOVE TO CLASS else update!!!!
#   uncomment "#print_Tb(all_shape_attrs, "at import: ")" at end of CamTbAddLib.py
#   or add to your code the line below:
#   CamTbAddLib.print_Tb(all_shape_attrs, "at import: ")" at end of CamTbAddLib.py

# Sections with "order": 0 are NOT included in making the TB name.
# "order": n sets the order of each part of the TB name.
# Order can have gaps in the numbers & can be set to large number to move item to end.
# If item value is empty: it is skipped & seperators & abbrev_r are not added.
# sep_left, sep_r are left/leading & right/trailing seperators of each part of the name.

# NOTE: all rules have the same attributes, except t_auto_number, which has two added attributes:
#        # This is ONLY rule item with added/different properties!
#        self.t_auto_number.tb_base_nr = 20000
#        self.t_auto_number.tb_dia_mult = 1000

class Ex1Rules(CamTbAddLib.Rules):
    def __init__(self, shape_name):
        # NB At present it is NOT used to restrict rules to set value (or poss list of values)
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)
        self.shapename.sep_left = "_"

        self.base_name = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.base_name.sep_left = "_"
        self.base_name.order = 99

        self.t_auto_number = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.t_auto_number.sep_left = ""
        self.t_auto_number.order = 1
        # This is ONLY rule item with added/different properties!
        self.t_auto_number.tb_base_nr = 20000
        self.t_auto_number.tb_dia_mult = 1000

        self.Chipload = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Chipload.abbrev_r = "CL"
        self.Chipload.sep_left = "_"
        self.Chipload.order = 0

        self.Flutes = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Flutes.abbrev_r = "F"
        self.Flutes.sep_left = "_"
        self.Flutes.order = 3

        self.Material = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindleDirection = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindlePower = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)

        self.BladeThickness = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Crest = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)

        self.cuttingAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.cuttingAngle.abbrev_r = "deg"

        self.CuttingEdgeAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CuttingEdgeAngle.abbrev_r = "deg"

        self.CuttingEdgeHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)

        self.Diameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Diameter.abbrev_r = "D"
        self.Diameter.sep_left = "_"
        self.Diameter.order = 2

        self.FlatRadius= CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)

        self.Length = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Length.abbrev_r = "L"

        self.NeckDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckDiameter.abbrev_r = "ND"

        self.NeckHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckHeight.abbrev_r = "NH"

        self.NeckLength = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckLength.abbrev_r = "NL"

        self.ShankDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.ShankDiameter.abbrev_r = "DS"

        self.TipAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.TipAngle.abbrev_r = "deg"

        self.TipDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)

        # Below has to be last item!
        super().__init__(shape_name)

# Duplicate: User boboxx Example: 2F-D6.35-L31.076, FC issue:12823
# Only required entries.
class BoboxxRules(CamTbAddLib.Rules):
    def __init__(self, shape_name):
        # Only manadatory RuleItem
        # NB At present it is NOT used to restrict rules to set value (or poss list of values)
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)

        self.Flutes = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Flutes.abbrev_r = "F"
        self.Flutes.order = 1

        self.Diameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Diameter.abbrev_left = "D"
        self.Diameter.sep_left = "_"
        self.Diameter.order = 2

        self.Length = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Length.sep_left = "-"
        self.Length.abbrev_left = "L"
        self.Length.order = 3

        # Below has to be last item!
        super().__init__(shape_name)

# Add shapename to RHS
class BoboxxRulesShape(CamTbAddLib.Rules):
    def __init__(self, shape_name):
       # Only manadatory RuleItem
        # NB At present it is NOT used to restrict rules to set value (or poss list of values)
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)
        self.shapename.sep_left = "_"
        self.shapename.order = 99

        self.t_auto_number = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.t_auto_number.abbrev_left = ''
        self.t_auto_number.abbrev_r = ''
        self.t_auto_number.sep_left = ''
        self.t_auto_number.sep_r = ''
        self.t_auto_number.order = 0
        # This is ONLY rule item with added/different properties!
        self.t_auto_number.tb_base_nr = 20000
        self.t_auto_number.tb_dia_mult = 1000

        self.Flutes = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Flutes.abbrev_r = "F"
        self.Flutes.order = 1

        self.Diameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Diameter.abbrev_left = "D"
        self.Diameter.sep_left = "_"
        self.Diameter.order = 2

        self.Length = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Length.sep_left = "-"
        self.Length.abbrev_left = "L"
        self.Length.order = 3

        # Below has to be last item!
        super().__init__(shape_name)


# Copy to use and ensure that required rules have a unique order > 0
class AllRulesTemplate(CamTbAddLib.Rules):
    def __init__(self, shape_name):
        # Future use to control what tool shapes use which rules.
        # NB At present it is NOT used to restrict rules to set value (or poss list of values)
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)
        self.shapename.abbrev_left = ''
        self.shapename.abbrev_r = ''
        self.shapename.sep_left = ''
        self.shapename.sep_r = ''
        self.shapename.order = 0

        self.base_name = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.base_name.abbrev_left = ''
        self.base_name.abbrev_r = ''
        self.base_name.sep_left = ''
        self.base_name.sep_r = ''
        self.base_name.order = 0

        self.t_auto_number = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.t_auto_number.abbrev_left = ''
        self.t_auto_number.abbrev_r = ''
        self.t_auto_number.sep_left = ''
        self.t_auto_number.sep_r = ''
        self.t_auto_number.order = 0
        # This is ONLY rule item with added/different properties!
        self.t_auto_number.tb_base_nr = 20000
        self.t_auto_number.tb_dia_mult = 1000

        self.Chipload = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Chipload.abbrev_left = ''
        self.Chipload.abbrev_r = ''
        self.Chipload.sep_left = ''
        self.Chipload.sep_r = ''
        self.Chipload.order = 0

        self.Flutes = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Flutes.abbrev_left = ''
        self.Flutes.abbrev_r = ''
        self.Flutes.sep_left = ''
        self.Flutes.sep_r = ''
        self.Flutes.order = 0

        self.Material = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Material.abbrev_left = ''
        self.Material.abbrev_r = ''
        self.Material.sep_left = ''
        self.Material.sep_r = ''
        self.Material.order = 0

        self.SpindleDirection = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindleDirection.abbrev_left = ''
        self.SpindleDirection.abbrev_r = ''
        self.SpindleDirection.sep_left = ''
        self.SpindleDirection.sep_r = ''
        self.SpindleDirection.order = 0

        self.SpindlePower = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindlePower.abbrev_left = ''
        self.SpindlePower.abbrev_r = ''
        self.SpindlePower.sep_left = ''
        self.SpindlePower.sep_r = ''
        self.SpindlePower.order = 0

        self.BladeThickness = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.BladeThickness.abbrev_left = ''
        self.BladeThickness.abbrev_r = ''
        self.BladeThickness.sep_left = ''
        self.BladeThickness.sep_r = ''
        self.BladeThickness.order = 0

        self.CapDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapDiameter.abbrev_left = ''
        self.CapDiameter.abbrev_r = ''
        self.CapDiameter.sep_left = ''
        self.CapDiameter.sep_r = ''
        self.CapDiameter.order = 0

        self.CapHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapHeight.abbrev_left = ''
        self.CapHeight.abbrev_r = ''
        self.CapHeight.sep_left = ''
        self.CapHeight.sep_r = ''
        self.CapHeight.order = 0

        self.Crest = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Crest.abbrev_left = ''
        self.Crest.abbrev_r = ''
        self.Crest.sep_left = ''
        self.Crest.sep_r = ''
        self.Crest.order = 0

        self.cuttingAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.cuttingAngle.abbrev_left = ''
        self.cuttingAngle.abbrev_r = ''
        self.cuttingAngle.sep_left = ''
        self.cuttingAngle.sep_r = ''
        self.cuttingAngle.order = 0

        self.CuttingEdgeAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CuttingEdgeAngle.abbrev_left = ''
        self.CuttingEdgeAngle.abbrev_r = ''
        self.CuttingEdgeAngle.sep_left = ''
        self.CuttingEdgeAngle.sep_r = ''
        self.CuttingEdgeAngle.order = 0

        self.CuttingEdgeHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CuttingEdgeHeight.abbrev_left = ''
        self.CuttingEdgeHeight.abbrev_r = ''
        self.CuttingEdgeHeight.sep_left = ''
        self.CuttingEdgeHeight.sep_r = ''
        self.CuttingEdgeHeight.order = 0

        self.Diameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Diameter.abbrev_left = ''
        self.Diameter.abbrev_r = ''
        self.Diameter.sep_left = ''
        self.Diameter.sep_r = ''
        self.Diameter.order = 0

        self.FlatRadius = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.FlatRadius.abbrev_left = ''
        self.FlatRadius.abbrev_r = ''
        self.FlatRadius.sep_left = ''
        self.FlatRadius.sep_r = ''
        self.FlatRadius.order = 0

        self.Length = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Length.abbrev_left = ''
        self.Length.abbrev_r = ''
        self.Length.sep_left = ''
        self.Length.sep_r = ''
        self.Length.order = 0

        self.NeckDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckDiameter.abbrev_left = ''
        self.NeckDiameter.abbrev_r = ''
        self.NeckDiameter.sep_left = ''
        self.NeckDiameter.sep_r = ''
        self.NeckDiameter.order = 0

        self.NeckHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckHeight.abbrev_left = ''
        self.NeckHeight.abbrev_r = ''
        self.NeckHeight.sep_left = ''
        self.NeckHeight.sep_r = ''
        self.NeckHeight.order = 0

        self.NeckLength = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckLength.abbrev_left = ''
        self.NeckLength.abbrev_r = ''
        self.NeckLength.sep_left = ''
        self.NeckLength.sep_r = ''
        self.NeckLength.order = 0

        self.ShankDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.ShankDiameter.abbrev_left = ''
        self.ShankDiameter.abbrev_r = ''
        self.ShankDiameter.sep_left = ''
        self.ShankDiameter.sep_r = ''
        self.ShankDiameter.order = 0

        self.TipAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.TipAngle.abbrev_left = ''
        self.TipAngle.abbrev_r = ''
        self.TipAngle.sep_left = ''
        self.TipAngle.sep_r = ''
        self.TipAngle.order = 0

        self.TipDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.TipDiameter.abbrev_left = ''
        self.TipDiameter.abbrev_r = ''
        self.TipDiameter.sep_left = ''
        self.TipDiameter.sep_r = ''
        self.TipDiameter.order = 0

        # Below has to be last item!
        super().__init__(shape_name)


# Esp including prules for odd propeties to test imported ToolBits
# Kept ALL rules to make it easier to change.
class ExageratedRulesExample(CamTbAddLib.Rules):
    def __init__(self, shape_name):
        # Future use to control what tool shapes use which rules.
        # NB At present it is NOT used to restrict rules to set value (or poss list of values)
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)
        self.shapename.abbrev_left = ''
        self.shapename.abbrev_r = ''
        self.shapename.sep_left = '_'
        self.shapename.sep_r = '_'
        self.shapename.order = 98

        self.base_name = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.base_name.abbrev_left = ''
        self.base_name.abbrev_r = ''
        self.base_name.sep_left = '_'
        self.base_name.sep_r = ''
        self.base_name.order = 99

        self.t_auto_number = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.t_auto_number.abbrev_left = ''
        self.t_auto_number.abbrev_r = ''
        self.t_auto_number.sep_left = ''
        self.t_auto_number.sep_r = ''
        self.t_auto_number.order = 1
        # This is ONLY rule item with added/different properties!
        self.t_auto_number.tb_base_nr = 30000
        self.t_auto_number.tb_dia_mult = 1000

        self.Chipload = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Chipload.abbrev_left = ''
        self.Chipload.abbrev_r = 'CL'
        self.Chipload.sep_left = ''
        self.Chipload.sep_r = '_'
        self.Chipload.order = 5

        self.Flutes = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Flutes.abbrev_left = ''
        self.Flutes.abbrev_r = 'F'
        self.Flutes.sep_left = ''
        self.Flutes.sep_r = '_'
        self.Flutes.order = 3

        self.Material = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Material.abbrev_left = ''
        self.Material.abbrev_r = ''
        self.Material.sep_left = '_'
        self.Material.sep_r = '_'
        self.Material.order = 6

        self.SpindleDirection = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindleDirection.abbrev_left = ''
        self.SpindleDirection.abbrev_r = '_'
        self.SpindleDirection.sep_left = '_'
        self.SpindleDirection.sep_r = ''
        self.SpindleDirection.order = 8

        self.SpindlePower = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.SpindlePower.abbrev_left = 'sp'
        self.SpindlePower.abbrev_r = 'W'
        self.SpindlePower.sep_left = '_'
        self.SpindlePower.sep_r = '_'
        self.SpindlePower.order = 7

        self.BladeThickness = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.BladeThickness.abbrev_left = 'bt'
        self.BladeThickness.abbrev_r = ''
        self.BladeThickness.sep_left = '_'
        self.BladeThickness.sep_r = '_'
        self.BladeThickness.order = 9

        self.CapDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapDiameter.abbrev_left = ''
        self.CapDiameter.abbrev_r = ''
        self.CapDiameter.sep_left = ''
        self.CapDiameter.sep_r = ''
        self.CapDiameter.order = 0

        self.CapHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CapHeight.abbrev_left = ''
        self.CapHeight.abbrev_r = ''
        self.CapHeight.sep_left = ''
        self.CapHeight.sep_r = ''
        self.CapHeight.order = 0

        self.Crest = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Crest.abbrev_left = ''
        self.Crest.abbrev_r = ''
        self.Crest.sep_left = ''
        self.Crest.sep_r = ''
        self.Crest.order = 0

        self.cuttingAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.cuttingAngle.abbrev_left = ''
        self.cuttingAngle.abbrev_r = 'deg'
        self.cuttingAngle.sep_left = '_'
        self.cuttingAngle.sep_r = ''
        self.cuttingAngle.order = 10

        self.CuttingEdgeAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CuttingEdgeAngle.abbrev_left = ''
        self.CuttingEdgeAngle.abbrev_r = 'deg'
        self.CuttingEdgeAngle.sep_left = '_'
        self.CuttingEdgeAngle.sep_r = ''
        self.CuttingEdgeAngle.order = 11

        self.CuttingEdgeHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.CuttingEdgeHeight.abbrev_left = ''
        self.CuttingEdgeHeight.abbrev_r = 'CL'
        self.CuttingEdgeHeight.sep_left = '_'
        self.CuttingEdgeHeight.sep_r = ''
        self.CuttingEdgeHeight.order = 12

        self.Diameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Diameter.abbrev_left = ''
        self.Diameter.abbrev_r = 'D'
        self.Diameter.sep_left = '_'
        self.Diameter.sep_r = ''
        self.Diameter.order = 2

        self.FlatRadius = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.FlatRadius.abbrev_left = ''
        self.FlatRadius.abbrev_r = 'FR'
        self.FlatRadius.sep_left = '_'
        self.FlatRadius.sep_r = ''
        self.FlatRadius.order = 13

        self.Length = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.Length.abbrev_left = ''
        self.Length.abbrev_r = 'L'
        self.Length.sep_left = '_'
        self.Length.sep_r = ''
        self.Length.order = 14

        self.NeckDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckDiameter.abbrev_left = ''
        self.NeckDiameter.abbrev_r = 'ND'
        self.NeckDiameter.sep_left = '_'
        self.NeckDiameter.sep_r = ''
        self.NeckDiameter.order = 15

        self.NeckHeight = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckHeight.abbrev_left = ''
        self.NeckHeight.abbrev_r = 'NH'
        self.NeckHeight.sep_left = '_'
        self.NeckHeight.sep_r = ''
        self.NeckHeight.order = 16

        self.NeckLength = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.NeckLength.abbrev_left = ''
        self.NeckLength.abbrev_r = 'NL'
        self.NeckLength.sep_left = '_'
        self.NeckLength.sep_r = ''
        self.NeckLength.order = 17

        self.ShankDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.ShankDiameter.abbrev_left = ''
        self.ShankDiameter.abbrev_r = 'DS'
        self.ShankDiameter.sep_left = '_'
        self.ShankDiameter.sep_r = ''
        self.ShankDiameter.order = 18

        self.TipAngle = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.TipAngle.abbrev_left = 'ta'
        self.TipAngle.abbrev_r = 'deg'
        self.TipAngle.sep_left = '_'
        self.TipAngle.sep_r = ''
        self.TipAngle.order = 19

        self.TipDiameter = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_shape)
        self.TipDiameter.abbrev_left = 'td'
        self.TipDiameter.abbrev_r = 'deg'
        self.TipDiameter.sep_left = '_'
        self.TipDiameter.sep_r = ''
        self.TipDiameter.order = 20

        # Below has to be last item!
        super().__init__(shape_name)

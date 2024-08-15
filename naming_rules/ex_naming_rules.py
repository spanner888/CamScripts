# -*- coding: utf-8 -*-

import CamTbAddLib

class Ex1Rules(CamTbAddLib.Rules):
    def __init__(self, shape_name):
        # super().__init__()
        self.shapename = CamTbAddLib.RuleItem(name=shape_name, ptype=CamTbAddLib.PropType.rule_prop)
        self.shapename.sep_left = "_"

        self.base_name = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.base_name.sep_left = "_"
        self.base_name.order = 99

        self.t_auto_number = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.rule_prop)
        self.t_auto_number.sep_left = "_"
        self.t_auto_number.order = 1
        # This is ONLY rule item with added/different properties!
        self.t_auto_number.tb_base_nr = 20000
        self.t_auto_number.tb_dia_mult = 1000

        self.Chipload = CamTbAddLib.RuleItem(name='', ptype=CamTbAddLib.PropType.tb_attrib)
        self.Chipload.abbrev_r = "CL"
        self.Chipload.sep_left = "_"
        self.Chipload.order = 1

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




# OLD about to be retired apprach
# to use: import ex_naming_rules.tb_naming_rules as ex1_rules
ex1_naming_rules = {"shapename"  :{"ptype": "rule_prop",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 0
                                },
            "base_name"        :{"ptype": "rule_prop",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 99
                                },
            # This is ONLY element with added/different properties!
            "t_auto_number"    :{"ptype": "rule_prop",
                                "tb_base_nr": 20000,    # For now KISS:= user sets!! ??lookup based on shapename??
                                "tb_dia_mult": 1000,
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 1
                                },
            "Chipload"         :{"ptype": "TbAttributes",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "CL",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 0
                                },
            "Flutes"           :{"ptype": "TbAttributes",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "F",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 3
                                },
            "Material"         :{"ptype": "TbAttributes",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "SpindleDirection" :{"ptype": "TbAttributes",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "SpindlePower"     :{"ptype": "TbAttributes",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "BladeThickness"   :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "CapDiameter"      :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "CapHeight"        :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "Crest"            :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "cuttingAngle"     :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "deg",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "CuttingEdgeAngle" :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "deg",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "CuttingEdgeHeight":{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "Diameter"         :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "D",
                                "sep_left": "_",
                                "sep_r": "",
                                "order": 2
                                },
            "FlatRadius"       :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "Length"           :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "L",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "NeckDiameter"     :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "ND",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "NeckHeight"       :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "NH",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "NeckLength"       :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "NL",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "ShankDiameter"    :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "DS",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "TipAngle"         :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "deg",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                },
            "TipDiameter"      :{"ptype": "TbShape",
                                "pref_name": "",
                                "abbrev_left": "",
                                "abbrev_r": "",
                                "sep_left": "",
                                "sep_r": "",
                                "order": 0
                                }
        }

  
# Exagerated example, tests:
#   Float/int/str TbAttributes, ie Chipload, Flutes, Material, SpindleDirection, SpindlePower
exagerated_naming_rules = {"shapename"  :{"ptype": "rule_prop",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "_",
                                  "sep_r": "_",
                                  "order": 98
                                 },
             "base_name"        :{"ptype": "rule_prop",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "_",
                                  "sep_r": "",
                                  "order": 99
                                 },
             # This is ONLY element with added/different properties!
             "t_auto_number"    :{"ptype": "rule_prop",
                                  "tb_base_nr": 30000,    # For now KISS:= user sets!! ??lookup based on shapename??
                                  "tb_dia_mult": 1000,
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 1
                                 },
             "Chipload"         :{"ptype": "TbAttributes",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "CL",
                                  "sep_left": "_",
                                  "sep_r": "_",
                                  "order": 5
                                 },
             "Flutes"           :{"ptype": "TbAttributes",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "F",
                                  "sep_left": "_",
                                  "sep_r": "",
                                  "order": 3
                                 },
             "Material"         :{"ptype": "TbAttributes",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "_",
                                  "sep_r": "_",
                                  "order": 6
                                 },
             "SpindleDirection" :{"ptype": "TbAttributes",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "_",
                                  "sep_r": "_",
                                  "order": 8
                                 },
             "SpindlePower"     :{"ptype": "TbAttributes",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "_",
                                  "sep_r": "_",
                                  "order": 7
                                 },
             "BladeThickness"   :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "CapDiameter"      :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "CapHeight"        :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "Crest"            :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "cuttingAngle"     :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "deg",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "CuttingEdgeAngle" :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "CuttingEdgeHeight":{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "Diameter"         :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "D",
                                  "sep_left": "_",
                                  "sep_r": "",
                                  "order": 2
                                 },
             "FlatRadius"       :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "Length"           :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "L",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "NeckDiameter"     :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "ND",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "NeckHeight"       :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "NH",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "NeckLength"       :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "NL",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "ShankDiameter"    :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "DS",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "TipAngle"         :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
             "TipDiameter"      :{"ptype": "TbShape",
                                  "pref_name": "",
                                  "abbrev_left": "",
                                  "abbrev_r": "",
                                  "sep_left": "",
                                  "sep_r": "",
                                  "order": 0
                                 },
        }

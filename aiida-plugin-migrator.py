#!/usr/bin/env python3
import sys
from bowler import Query
from bowler.types import LN, Capture, Filename
from functools import partial


# PATTERN = """
#    class_import=import_from<
#        'from' module_name=any
#        'import' ['(']
#            any*
#            name=NAME
#            any*
#    [')'] >
# """


def filter_factory_imports(node: LN, capture: Capture, filename: Filename) -> bool:
    """Filter imports of Factory classes."""

    if "module_imports" in capture:
        imports = [it.value.strip() for it in capture["module_imports"]]
    elif "module_import" in capture:
        imports = [ capture["module_import"].value.strip() ]
    else:
        return False

    for k in [
        "CalculationFactory",
        "DataFactory",
        "TransportFactory",
        "SchedulerFactory",
    ]:
        if k in imports:
            return True
    return False

def filter_method_in_class(class_name):
    """Filters method call by class name.

    Usage:
    .select_method("my_method")
    .filter(filter_method_in_class("MyClass"))
    """
    def f(node: LN, capture: Capture, filename: Filename) -> bool:
        """Filter imports of Factory classes."""
        try:
            # last child is function arguments
            # second to last child is function name
            # third to last child should be class
            #print(capture["node"].children)
            cls = capture["function_call"].children[-3].value
            if cls.strip() == class_name:
                return True
            else: 
                return False
        except:
            return False

    return f


path = sys.argv[1]
query = (
    Query(path)
    # https://github.com/aiidateam/aiida_core/pull/2402
    # https://github.com/aiidateam/aiida_core/pull/2497
    .select_module("aiida.orm.data.parameter")
    .rename("aiida.orm")
    .select_module("aiida.orm.data.structure")
    .rename("aiida.orm")
    .select_module("aiida.orm.data.singlefile")
    .rename("aiida.orm")
    .select_module("aiida.orm.data.remote")
    .rename("aiida.orm")
    .select_module("aiida.orm.code")
    .rename("aiida.orm")

    .select_method("get")
    .filter(filter_method_in_class("Computer"))
    .rename("objects.get")

    .select_module("aiida.orm.data.base")
    .rename("aiida.orm")

    .select_module("aiida.orm.data")
    .rename("aiida.orm.nodes.data")

    # https://github.com/aiidateam/aiida_core/pull/2524
    .select_module("aiida.work")
    .rename("aiida.engine")

    .select_module("aiida.orm.calculation.job")
    .rename("aiida.engine")

    .select_module("aiida.engine.run")
    .rename("aiida.engine")

    .select_module("aiida.engine.workchain")
    .rename("aiida.engine")

    # https://github.com/aiidateam/aiida_core/pull/2498
    .select_module("aiida.scheduler")
    .rename("aiida.schedulers")

    # Move factories from aiida.orm => aiida.plugins
    # Note: This is too greedy as it will also suggest the rename,
    # when other classes are imported on the same line.
    .select_module("aiida.orm")
    .filter(filter_factory_imports)
    .rename("aiida.plugins")

    # https://github.com/aiidateam/aiida_core/pull/2498
    .select_module("aiida.transport")
    .rename("aiida.transports")


    ## https://github.com/aiidateam/aiida_core/pull/2192
    # .select_class("WorkCalculation")
    # .rename("WorkChainNode")
    ## https://github.com/aiidateam/aiida_core/pull/2189
    # .select_class("FunctionCalculation")
    # .rename("WorkFunctionNode")
    ## https://github.com/aiidateam/aiida_core/pull/2184
    ## https://github.com/aiidateam/aiida_core/pull/2201
    # TODO: one should add a filter here...
     .select_class("JobCalculation")
     .rename("CalcJob")
    # .select_class("JobCalculation")
    # .rename("CalcJobNode")
    ## https://github.com/aiidateam/aiida_core/pull/2195
    # .select_class("InlineCalculation")
    # .rename("CalcFunctionNode")

    # https://github.com/aiidateam/aiida_core/pull/2517
    .select_class("ParameterData")
    .rename("Dict")

    # https://github.com/aiidateam/aiida_core/pull/2357
    # https://github.com/aiidateam/aiida_core/issues/2311#issuecomment-444972896
    .select_module("aiida.control.profile")
    .rename("aiida.manage.profile")
    .select_module("aiida.control.code")
    .rename("aiida.orm.utils.builders.code")
    .select_module("aiida.control.computer")
    .rename("aiida.orm.utils.builders.computer")
    .select_module("aiida.control")
    .rename("aiida.manage.external")

    .select_module("aiida.common.orbital")
    .rename("aiida.tools.data.orbital")
    .select_module("aiida.common.additions.config_migrations")
    .rename("aiida.manage.config.migrations")
    .select_module("aiida.common.additions.backup_script")
    .rename("aiida.manage.backup")
    .select_module("aiida.common.caching")
    .rename("aiida.manage.caching")
    .select_module("aiida.common.ipython")
    .rename("aiida.tools.ipython")
    .select_module("aiida.common.graph")
    .rename("aiida.tools.graphviz")
    # TODO: bowler is unfortunately not yet clever enough to understand this:
    # (write a filter or try something else)
    .select_class("aiida.common.log.DBLogHandler")
    .rename("aiida.orm.utils.log.DBLogHandler")
    .select_module("aiida.common.profile")
    .rename("aiida.manage.profile")
    .select_module("aiida.common.setup")
    .rename("aiida.manage.setup")
    # TODO: aiida.common.utils

    .select_module("aiida.utils.ascii_vis")
    .rename("aiida.cmdline.utils.ascii_vis")
    .select_module("aiida.utils.capturing")
    .rename("aiida.common.utils.capturing")
    .select_module("aiida.utils.delete_nodes")
    .rename("aiida.manage.database.delete.nodes")
    # TODO: aiida.utils.email
    # TODO: aiida.utils.error_accumulator
    .select_module("aiida.utils.find_folder")
    .rename("aiida.common.folders")
    .select_module("aiida.utils.fixtures")
    .rename("aiida.manage.fixtures")
    .select_module("aiida.utils.json")
    .rename("aiida.common.json")
    .select_module("aiida.utils.serialize")
    .rename("aiida.common.serialize")
    .select_module("aiida.utils.which")
    .rename("aiida.common.files")

    .select_module("aiida.parsers.exceptions")
    .rename("aiida.common.exceptions")

    # suggestions from Sasha to use top-level modules
    .select_module("aiida.common.datastructures")
    .rename("aiida.common")
    .select_module("aiida.common.exceptions")
    .rename("aiida.common")


    .execute()
)

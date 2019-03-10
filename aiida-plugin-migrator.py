#!/usr/bin/env python3
from bowler import Query
import sys

from bowler.types import LN, Capture, Filename


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
    try:
        imports = [it.value for it in capture["module_imports"]]
    except:
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


path = sys.argv[1]
query = (
    Query(path)
    # https://github.com/aiidateam/aiida_core/pull/2402
    # https://github.com/aiidateam/aiida_core/pull/2497
    .select_module("aiida.orm.data.parameter")
    .rename("aiida.orm")
    .select_module("aiida.orm.code")
    .rename("aiida.orm")

    # .select_module("aiida.orm.data")
    # .rename("aiida.orm.node.data")
    # https://github.com/aiidateam/aiida_core/pull/2524
    .select_module("aiida.work")
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

    .execute()
)

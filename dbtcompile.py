import io
import logging
import os
import sys
from contextlib import redirect_stdout

from dbt.cli.main import dbtRunner, dbtRunnerResult
import argparse

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.disabled = False

    parser = argparse.ArgumentParser(description="Example script with a mandatory name selection argument.")

    # Add the --select (-s) argument
    parser.add_argument('-s', '--select', required=True, help='Name to select', type=str)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Print the provided name
    model_name = args.select
    # print(model_name)

    try:
        # initialize
        dbt = dbtRunner()

        cli_args = ["compile", "--select", model_name, "--no-version-check",
                    "--no-introspect", "--quiet"]

        # dbt likes to print to stdout, so we need to capture it, but we don't really care about the output.
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            res: dbtRunnerResult = dbt.invoke(cli_args)

        if res.result and len(res.result) >= 1 and res.result[0].node.compiled_path:
            node = res.result[0].node
            # get the full path compiled_path, use cwd
            # compiled_path is relative, we need absolute
            compiled_full_path = os.path.join(os.getcwd(), node.compiled_path)
            columns: list[dict] = []
            for column_name, column in node.columns.items():
                columns.append({
                    "constraints": column.constraints,
                    "data_type": column.data_type,
                    "description": column.description,
                    "name": column.name,
                    "quote": column.quote,
                    "tags": column.tags
                })

            refs: list[str] = []
            for ref in node.refs:
                refs.append(ref.name)

            return_dict = {
                "alias": node.alias,
                "build_path": node.build_path,
                "checksum": node.checksum.checksum,
                "columns": columns,
                "compiled": node.compiled,
                "compiled_code": node.compiled_code,
                "compiled_path": node.compiled_path,
                "compiled_full_path": compiled_full_path,
                # "config": node.config,
                # "config_call_dict": node.config_call_dict,
                # "constraints": node.constraints,
                # # "contract": node.contract,
                # "created_at": node.created_at,
                # "database": node.database,
                # "defer_relation": node.defer_relation,
                # "deferred": node.deferred,
                # # "depends_on": node.depends_on,
                # "depends_on_macros": node.depends_on_macros,
                # "depends_on_nodes": node.depends_on_nodes,
                # "deprecation_date": node.deprecation_date,
                # "description": node.description,
                # # "docs": node.docs,
                # "empty": node.empty,
                # "extra_ctes": node.extra_ctes,
                # "extra_ctes_injected": node.extra_ctes_injected,
                # "file_id": node.file_id,
                # "fqn": node.fqn,
                # "group": node.group,
                # "identifier": node.identifier,
                # "is_ephemeral": node.is_ephemeral,
                # "is_ephemeral_model": node.is_ephemeral_model,
                # "is_external_node": node.is_external_node,
                # "is_latest_version": node.is_latest_version,
                # "is_refable": node.is_refable,
                # "is_relational": node.is_relational,
                # "is_versioned": node.is_versioned,
                # "language": node.language,
                # "latest_version": node.latest_version,
                # "materialization_enforces_constraints": node.materialization_enforces_constraints,
                # "meta": node.meta,
                # "metrics": node.metrics,
                # "name": node.name,
                # "node_info": node.node_info,
                # "original_file_path": node.original_file_path,
                # "package_name": node.package_name,
                # "patch_path": node.patch_path,
                # "path": node.path,
                # "raw_code": node.raw_code,
                # "refs": refs,
                # "relation_name": node.relation_name,
                # "resource_type": node.resource_type,
                # "schema": node.schema,
                # "search_name": node.search_name,
                # "should_store_failures": node.should_store_failures,
                # "sources": node.sources,
                # "tags": node.tags,
                # "unique_id": node.unique_id,
                # "unrendered_config": node.unrendered_config,
                # "version": node.version,
            }

            # dump to json
            import json
            print(json.dumps(return_dict))

            sys.exit(0)
        else:
            import sys

            # Figure out what went wrong.
            # 1. No result?
            if not res.result:
                if res.exception:
                    print(res.exception)
                else:
                    print(f"failed {res}")
                sys.exit(1)
            # 2. No compiled_path?
            elif not res.result[0].node.compiled_path:
                print("No compiled_path")
                sys.exit(1)
            elif res.result[0].node.status == "error":
                print("Error: ", res.result[0].node.error)
                sys.exit(1)
            else:
                # 3. Something else?
                print("Unknown error")
                sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

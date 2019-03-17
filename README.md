# aiida-plugin-migrator

This too helps refactoring AiiDA plugins for 
the transition from `aiida-core` v0.x to `aiida-core` v1.0.

It makes use of the [Bowler](https://github.com/facebookincubator/Bowler) refactoring tool.

## Installation

The `aiida-plugin-migrator` only runs under `python3`
(but it does *not* depend on `aiida-core`).

```
git clone https://github.com/aiidateam/aiida-plugin-migrator
cd aiida-plugin-migrator
pip install -e .

# need latest bowler fixes
pip install git+https://github.com/facebookincubator/Bowler.git@master
```

This adds `aiida-plugin-migrator.py` to the `PATH`.

## Usage

```
aiida-plugin-migrator.py /path/to/plugin/code
```

## Improvement

Backwards-incompatible changes have been documented in:

 * [the AiiDA wiki](https://github.com/aiidateam/aiida_core/wiki/Backward-incompatible-changes-in-1.0.0)
 * [the documentation](https://aiida-core.readthedocs.io/en/latest/developer_guide/design/changes.html)
 * [this comment](https://github.com/aiidateam/aiida_core/issues/2311#issuecomment-444972896) (for `aiida.utils`)

As the plugin migrator is improved, please keep the Wiki updated.

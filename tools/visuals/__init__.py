"""Unified blog SVG visuals toolkit.

Usage from CLI:
    python tools/visuals.py list
    python tools/visuals.py build <topic|all>
    python tools/visuals.py audit
"""

from . import algebra_logic, charts, core, geometry_analysis, mechanics_sky, science_tech
from .core import TOPICS, audit_all_svgs

__all__ = [
    "TOPICS",
    "audit_all_svgs",
    "algebra_logic",
    "charts",
    "core",
    "geometry_analysis",
    "mechanics_sky",
    "science_tech",
]

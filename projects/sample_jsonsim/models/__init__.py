#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages
import typing as tp

# 3rd party packages

# Project packages

def sierra_plugin_type() -> str:
    return "model"

def sierra_models(model_type: str) -> tp.List[str]:
    if model_type == "intra":
        return ["noise.NoisyModel"]
    if model_type == "inter":
        return ["noise.LessNoisyModel"]

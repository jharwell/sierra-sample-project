#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages

# 3rd party packages

# Project packages


def sierra_plugin_type() -> str:
    return "model"


def sierra_models(model_type: str) -> list[str]:
    if model_type == "intra":
        return ["foraging.FoodModelIntra"]
    if model_type == "inter":
        return ["foraging.FoodModelInter"]
    return []

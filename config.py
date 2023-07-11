#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "9f34d767-390b-40c6-a1d9-8887f35ec9b8")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Oj08Q~k5~wLcsZhf-4HYvPzdy3ySNWLkNpXXvbA-")

    # key
    open_api_key = "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"

# Copyright 2020 LINE Corporation
#
# LINE Corporation licenses this file to you under the Apache License,
# version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at:
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from flask import Blueprint
from lib.config import config
import importlib
import os

judy_api = Blueprint("judy_api", __name__)

type = (os.environ.get("JNOTEBOOK_READER_STORAGE_TYPE") or config["storage"]["type"]).lower()
if type not in ("local", "s3"):
    type = "local"
renderer = importlib.import_module("renderer.{}".format(type)).renderer

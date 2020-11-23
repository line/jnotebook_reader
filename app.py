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

from lib.config import config
from flask import Flask
from modules.core import api, judy_api
from modules.monitor import l7check, l7check_api
import os


def create_app():
    root = config["server"]["root"]
    app = Flask(
        __name__, static_url_path="{}/static/".format(root), template_folder="./views/"
    )
    app.register_blueprint(judy_api, url_prefix=root)
    app.register_blueprint(l7check_api, url_prefix="/monitor")
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("JNOTEBOOK_READER_SERVER_PORT") or config["server"]["port"])

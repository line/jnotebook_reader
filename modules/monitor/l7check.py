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

from . import l7check_api as api
from flask import request
from flask_api import status

is_alive = True
LOCAL = ["127.0.0.1", "0:0:0:0:0:0:0:1", "localhost", "::1"]


@api.route("/l7check")
def l7check():
    if is_alive:
        return "", status.HTTP_200_OK
    else:
        return "", status.HTTP_404_NOT_FOUND


@api.route("/enable")
def enable():
    if set_status(request, True):
        return "enabled", status.HTTP_200_OK
    else:
        return status.HTTP_403_FORBIDDEN


@api.route("/disable")
def disable():
    if set_status(request, False):
        return "disabled", status.HTTP_200_OK
    else:
        return status.HTTP_403_FORBIDDEN


def set_status(req, alive):
    if is_local(req):
        global is_alive
        is_alive = alive
        return True
    return False


def is_local(req):
    ip = request.remote_addr
    for item in LOCAL:
        if item == ip:
            return True
    return False

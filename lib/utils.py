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

import math
from tzlocal import get_localzone


def format_date(date):
    return date.astimezone(get_localzone()).strftime("%Y-%m-%d %H:%M:%S")


def format_size(size):
    k = 1024
    m = k * 1024
    g = m * 1024

    if math.floor(size / g) > 0:
        return "{:10.1f}{}".format((size / g), "G")

    if math.floor(size / m) > 0:
        return "{:10.1f}{}".format((size / m), "M")

    if math.floor(size / k) > 0:
        return "{:10.1f}{}".format((size / k), "K")

    return "{:10.1f}{}".format(size, "B")

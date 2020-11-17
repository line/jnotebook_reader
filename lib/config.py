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

import logging

config = {
    "default": {
        "server": {
            "port": 9088,                        # The port judy server listening on
            "root": ""                           # Context path, base url
        },
        "storage": {
            "type": "local",                     # local or s3
            "directories": ["docs"],             # If type is local effective
            "s3": {                              # s3 config, if type is s3 effective
                "endpoint": None,                # s3 endpoint, if type is s3 required, if set with None would access to s3 global url
                "accessKey": "YOUR_ACCESS_KEY",  # optional, default; request header "Access-Key" could replace it
                "secretKey": "YOUR_SECRET_KEY",  # optional, default; request header "Secret-Key" could replace it
                "buckets": ["YOUR_BUCKET_NAME"]  # optional, default; request header "Bucket-Name" could replace it
            }
        },
        "logging": {
            "level": logging.DEBUG,
            "format": "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s",
            "filename": ""
        }
    }
}["default"]

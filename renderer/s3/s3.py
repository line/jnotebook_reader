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

from common.renderer import Renderer
from lib.config import config
from flask import request
from flask_api import status
import boto3
import typing
from botocore.exceptions import ClientError
from datetime import datetime
from lib.logger import logger
from lib.utils import format_date, format_size
from common.const import const

log = logger(__name__)


class S3Renderer(Renderer):
    def __bucket(self, id):
        buckets = config["storage"]["s3"]["buckets"]
        if isinstance(buckets, typing.List):
            return buckets[int(id)]
        elif isinstance(buckets, typing.Dict):
            return buckets.get(id)
        else:
            return buckets

    def __connect(self, id):
        access_key = request.headers.get("Access-Key")
        secret_key = request.headers.get("Secret-Key")
        bucket = request.headers.get("Bucket-Name")

        if not access_key or not secret_key or not bucket:
            access_key = config["storage"]["s3"]["accessKey"]
            secret_key = config["storage"]["s3"]["secretKey"]
            bucket = self.__bucket(id)

        session = boto3.session.Session()
        client = session.client(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=config["storage"]["s3"]["endpoint"],
        )
        return client, bucket

    def __get(self, s3_client, bucket, key):
        if_none_match = request.headers.get("If-None-Match", "").strip()
        if_modified_since = request.headers.get("If-Modified-Since", "").strip()
        if len(if_none_match) == 0 or len(if_modified_since) == 0:
            return s3_client.get_object(Bucket=bucket, Key=key)
        else:
            return s3_client.get_object(
                Bucket=bucket,
                Key=key,
                IfNoneMatch=if_none_match,
                IfModifiedSince=datetime.strptime(
                    if_modified_since, "%a, %d %b %Y %H:%M:%S %Z"
                ),
            )

    def __list(self, s3_client, bucket, prefix):
        result = []
        data = s3_client.list_objects(Bucket=bucket, Delimiter="/", Prefix=prefix)
        contents = data.get("Contents")
        if contents:
            for content in contents:
                if content["Key"] != prefix:
                    name = content["Key"][len(prefix) :]
                    if not name.startswith("."):
                        result.append(
                            {
                                "name": name,
                                "size": format_size(content["Size"]),
                                "rawSize": content["Size"],
                                "lastModified": format_date(content["LastModified"]),
                                "type": "File",
                            }
                        )
        common_prefixes = data.get("CommonPrefixes")
        if common_prefixes:
            for common_prefix in common_prefixes:
                name = common_prefix["Prefix"][
                    len(prefix) : len(common_prefix["Prefix"]) - 1
                ]
                result.append(
                    {
                        "name": name,
                        "size": 0,
                        "rawSize": 0,
                        "lastModified": "-",
                        "type": "Folder",
                    }
                )
        return result

    def render_directory(self, id, prefix):
        s3_client, bucket = self.__connect(id)
        return self.__list(s3_client, bucket, prefix)

    def render_file(self, id, prefix, type):
        s3_client, bucket = self.__connect(id)
        try:
            obj = self.__get(s3_client, bucket, prefix)
            content = obj["Body"].read()
            if type == const.NOTEBOOK_TYPE:
                (content, resources) = self.render_notebook(content)
            if type == const.MARKDOWN_TYPE:
                content = self.render_markdown(content)
            return {
                "content": content,
                "etag": obj["ETag"],
                "lastModified": obj["LastModified"].strftime(
                    "%a, %d %b %Y %H:%M:%S %Z"
                ),
            }
        except ClientError as ce:
            if ce.response["Error"]["Code"] == "304":
                return {"status": status.HTTP_304_NOT_MODIFIED}
            elif ce.response["Error"]["Code"] == "NoSuchKey":
                return {"status": status.HTTP_404_NOT_FOUND}
            else:
                log.error(ce.response)
                raise ce

    def render_download(self, id, prefix):
        s3_client, bucket = self.__connect(id)
        try:
            return {"stream": self.__get(s3_client, bucket, prefix)["Body"]}
        except ClientError as ce:
            if ce.response["Error"]["Code"] == "NoSuchKey":
                return {"status": status.HTTP_404_NOT_FOUND}
            else:
                log.error(ce.response)
                raise ce

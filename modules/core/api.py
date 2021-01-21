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

from . import judy_api as api, renderer
from common.const import const
from flask import (
    request,
    render_template,
    make_response,
    stream_with_context,
    Response,
    redirect,
)
from flask_api import status
from lib.config import config
from lib.logger import logger
import base64
from urllib.parse import quote

log = logger(__name__)


@api.route("/")
def home():
    return redirect("/0", code=301)


@api.route("/<id>")
def root(id):
    try:
        return render_template(
            const.LIST_TEMPLATE,
            contents=renderer.render_directory(id, ""),
            prefix="",
            id=id,
            root=__root(),
        )
    except Exception as e:
        log.error(e)
        return (
            render_template(const.ERROR_TEMPLATE, root=__root()),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# List files of sub directories
# Render file view
@api.route("/<id>/<path:prefix>")
def render(id, prefix):
    render_context = {"prefix": prefix, "id": id, "root": __root()}
    try:
        # Directory
        if prefix.endswith("/"):
            render_context["prefix"] = prefix[0 : len(prefix) - 1]
            render_context["path"] = prefix
            render_context["contents"] = renderer.render_directory(id, prefix)
            return render_template(const.LIST_TEMPLATE, **render_context)

        # file
        file_type = __file_type(prefix)
        file_info = renderer.render_file(id, prefix, file_type)
        if "content" not in file_info:
            if status.HTTP_404_NOT_FOUND == file_info["status"]:
                return (
                    render_template(const.NOT_FOUND_TEMPLATE, **render_context),
                    file_info["status"],
                )
            return "", file_info["status"]
        # Image
        if __image(file_type):
            render_context["base64"] = "data:image/{};base64,{}".format(
                file_type, base64.b64encode(file_info["content"]).decode("utf-8")
            )
            template = const.IMAGE_TEMPLATE
        # Notebook
        elif const.NOTEBOOK_TYPE == file_type:
            render_context["body"] = file_info["content"]
            template = const.NOTEBOOK_TEMPLATE
        # Html
        elif const.HTML_TYPE == file_type:
            if request.args.get("render") == "true":
                return str(file_info["content"], encoding="UTF-8")
            render_context["url"] = "{}/{}/{}?render=true".format(__root(), id, prefix)
            template = const.HTML_TEMPLATE
        # Markdown
        elif const.MARKDOWN_TYPE == file_type:
            render_context["content"] = file_info["content"]
            template = const.MARKDOWN_TEMPLATE
        # Raw
        else:
            render_context["url"] = "{}/{}/download/{}".format(__root(), id, prefix)
            template = const.RAW_TEMPLATE
        resp = make_response(render_template(template, **render_context))
        resp.headers.set(const.LAST_MODIFIED_HEADER, file_info["lastModified"])
        resp.headers.set(const.ETAG_HEADER, file_info["etag"])
        return resp
    except Exception as e:
        log.error(e)
        return (
            render_template(const.ERROR_TEMPLATE, **render_context),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Download files
@api.route("/<id>/download/<path:prefix>")
def download(id, prefix):
    render_context = {"prefix": prefix, "id": id, "root": __root()}
    try:
        file_info = renderer.render_download(id, prefix)
        if "stream" not in file_info:
            if status.HTTP_404_NOT_FOUND == file_info["status"]:
                return (
                    render_template(const.NOT_FOUND_TEMPLATE, **render_context),
                    file_info["status"],
                )
        parts = prefix.split("/")
        file_name = quote(parts[len(parts) - 1])
        return Response(
            stream_with_context(file_info["stream"]),
            headers={
                const.CONTENT_DISPOSITION_HEADER: const.ATTACHMENT_HEADER.format(file_name)
            },
        )
    except Exception as e:
        log.error(e)
        return (
            render_template(const.ERROR_TEMPLATE, **render_context),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def __root():
    if config["server"]["root"] == "/":
        return ""
    return config["server"]["root"]


def __file_type(path):
    parts = path.lower().split(".")
    return parts[len(parts) - 1]


def __image(t):
    for type in const.IMAGE_TYPE:
        if type == t:
            return True
    return False

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


class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = _const()
# file type def
const.NOTEBOOK_TYPE = "ipynb"
const.HTML_TYPE = "html"
const.JPG_TYPE = "jpg"
const.JPEG_TYPE = "jpeg"
const.PNG_TYPE = "png"
const.GIF_TYPE = "gif"
const.IMAGE_TYPE = [const.JPG_TYPE, const.JPEG_TYPE, const.PNG_TYPE, const.GIF_TYPE]
const.MARKDOWN_TYPE = "md"

# render template def
const.ERROR_TEMPLATE = "error.html"
const.RAW_TEMPLATE = "raw.html"
const.NOTEBOOK_TEMPLATE = "nb.html"
const.IMAGE_TEMPLATE = "image.html"
const.LIST_TEMPLATE = "list.html"
const.NOT_FOUND_TEMPLATE = "404.html"
const.HTML_TEMPLATE = "html.html"
const.MARKDOWN_TEMPLATE = "md.html"

# http header
const.ETAG_HEADER = "Etag"
const.LAST_MODIFIED_HEADER = "Last-Modified"
const.CONTENT_DISPOSITION_HEADER = "Content-Disposition"
const.ATTACHMENT_HEADER = "attachment; filename={0}; filename*=utf-8''{0}"

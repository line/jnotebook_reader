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

from abc import ABCMeta, abstractmethod
from latex_envs.latex_envs import LenvsHTMLExporter
import nbformat
import markdown2


class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    # List files of sub directories
    # Render file view
    def render_directory(self, id, prefix):
        pass

    @abstractmethod
    def render_file(self, id, prefix, type):
        pass

    @abstractmethod
    # Render download file
    def render_download(self, id, prefix):
        pass

    def render_notebook(self, content):
        jake_notebook = nbformat.reads(str(content.decode("utf-8")), as_version=4)
        html_exporter = LenvsHTMLExporter()
        html_exporter.template_file = "basic"
        return html_exporter.from_notebook_node(jake_notebook)

    def render_markdown(self, content):
        return markdown2.markdown(content)

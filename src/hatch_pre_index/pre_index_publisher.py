# ================================================================================
#
#   hatch_pre_index class
#
#   object for .....
#
#   MIT License
#
#   Copyright (c) 2025 krokoreit (krokoreit@gmail.com)
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#
# ================================================================================

from hatch.publish.index import IndexPublisher
from .utils import read_published_version, write_published_version, get_git_tag, get_hatch_version


class PreIndexPublisher(IndexPublisher):
    # use config in [tool.hatch.publish.pre_index]
    PLUGIN_NAME = "pre_index"

    def publish(self, artifacts, options):
        # Determine what we are publishing
        git_tag = get_git_tag()
        hatch_version = get_hatch_version()
        published = read_published_version()
        print(f"[PreIndexPublisher] git tag         = {git_tag}")
        print(f"[PreIndexPublisher] hatch version   = {hatch_version}")
        print(f"[PreIndexPublisher] published       = {published}")

        if git_tag:
            print(f"[PreIndexPublisher] Writing published version: {git_tag} and {hatch_version}")
            write_published_version(git_tag)

        # Continue with standard index publishing
        print("We have disabled index publisher at the moment.")
        #return super().publish(artifacts, options)

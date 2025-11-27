# ================================================================================
#
#   PreIndexPublisher class
#
#   object for checking the project version and to run scripts before it invokes the index publisher.
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

import os
import keyring
import click

from hatch.publish.index import IndexPublisher
from .utils import read_published_version, write_published_version, get_git_tag, get_hatch_version


class PreIndexPublisher(IndexPublisher):
    # use config in [tool.hatch.publish.pre_index]
    PLUGIN_NAME = "pre_index"

    def publish(self, artifacts, options):

        print("root", self.root)
        print("cache_dir", self.cache_dir)
        print("project_config", self.project_config)
        print("plugin_config", self.plugin_config)

        project_tag = "unknown"
        if os.path.isdir(self.root):
            f_head, f_tail = os.path.split(self.root)
            if len(f_tail) > 0:
                project_tag = f_tail


    
        # Determine what version we are publishing
        git_tag = get_git_tag()
        hatch_version = get_hatch_version()
        published = read_published_version()
        print(f"[PreIndexPublisher] git tag         = {git_tag}")
        print(f"[PreIndexPublisher] hatch version   = {hatch_version}")
        print(f"[PreIndexPublisher] published       = {published}")

        # Only publish when git tag != last published
        if git_tag and published and git_tag == published:
            print("[PreIndexPublisher] Version", git_tag, "already published. Run 'hatch build' to build a new version.")
            exit(1)
        
        if git_tag:
            print("[PreIndexPublisher] Writing published version:", git_tag)
            write_published_version(git_tag)
            
        # handle stored credentials
        prompt_for_project_token = False
        is_global_token = False
        service_name = "pre_index_publisher_" + project_tag
        password = keyring.get_password(service_name, "__token__")
        if password is not None:
            prompt_for_project_token = (password == "__public__")
        else:
            print("No API token is currently stored. You can provide an API token with global or project scope.")
            if click.confirm("Do you want to enter a token with global scope?"):
                password = click.prompt("Enter global scope API token for " + project_tag, default="")
                is_global_token = (len(password) > 0)
            else:
                prompt_for_project_token = True
        if prompt_for_project_token:
            password = click.prompt("Enter project scope API token for " + project_tag, default="")



        print("password", password)


        # Continue with standard index publishing
        index_options = {'no_prompt': options['no_prompt'], 'initialize_auth': options['initialize_auth']}
        if len(password) > 0:
            index_options['user'] = "__token__"
            index_options['auth'] = password

# temp test
        index_options['repo'] = "test"

        super().publish(artifacts, index_options)

        # on succesful completion, store credentials
        if is_global_token:
            keyring.set_password(service_name, "__token__", "__public__")
        elif prompt_for_project_token and len(password) > 0:
            keyring.set_password(service_name, "__token__", password)

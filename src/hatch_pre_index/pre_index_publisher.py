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


        #print("[PreIndexPublisher] options:", options)
        
        repo = ""
        if 'repo' in options:
            repo = options['repo']
        elif 'repo' in self.project_config:
            repo = self.project_config['repo']

        print("[PreIndexPublisher] repo:", repo)



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


            
        # handle stored credentials
        if len(repo) > 0:
            service_name_repo = repo
        else:
            service_name_repo = 'main'
        service_name = "pre_index_publisher_" + project_tag + "_" + service_name_repo
        password = keyring.get_password(service_name, "__token__")

        if password is None:
            print("No API token is currently stored for " + project_tag + "_" + service_name_repo + ".")
            print("You can provide an API token to be stored and reused or just use it for this time.")
            store_token = click.confirm("Do you want to store an API token?", default="y")
            if store_token:
                token_prompt = "Enter API token to store"
            else:
                token_prompt = "Enter one time use API token"
            password = click.prompt(token_prompt, default="")

        if len(password) == 0:
            print("[PreIndexPublisher] No API token entered. Publishing aborted.")
            exit(1)



        #print("password", password)


        # Continue with standard index publishing
        index_options = {'no_prompt': options['no_prompt'], 'initialize_auth': options['initialize_auth']}
        index_options['user'] = "__token__"
        index_options['auth'] = password
        if len(repo) > 0:
            index_options['repo'] = repo


# temp test
        index_options['repo'] = "test"

        super().publish(artifacts, index_options)


        # on succesful completion, store published version
        if git_tag:
            print("[PreIndexPublisher] Writing published version:", git_tag)
            write_published_version(git_tag)

        # on succesful completion, store credentials
        if store_token:
            keyring.set_password(service_name, "__token__", password)

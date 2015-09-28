# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The ROS domain.

    :copyright: Copyright 2015 by otamachan.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

from docutils import nodes
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.locale import _
from sphinx.util.docfields import Field, GroupedField, TypedField

from catkin_pkg.packages import find_packages

_cache = {}

class GroupedFieldNoArg(Field):
    u"""
    """
    is_grouped = True
    list_type = nodes.bullet_list

    def __init__(self, name, names=(), label=None, rolename=None):
        Field.__init__(self, name, names, label, False, rolename)

    def make_field(self, types, domain, items):
        fieldname = nodes.field_name('', self.label)
        listnode = self.list_type()
        for fieldarg, content in items:
            listnode += nodes.list_item('', nodes.paragraph('', '', *content))
        fieldbody = nodes.field_body('', listnode)
        return nodes.field('', fieldname, fieldbody)

class ROSObjectDescription(ObjectDescription):
    u"""ROS Object"""
    def find_package(self, name):
        if 'base' in self.options and self.options['base'] is not None:
            base_abspath = self.env.relfn2path(self.options['base'])[1]
            packages = find_packages(base_abspath)
            package = next((package for package in packages.values()
                            if package.name == name), None)
        else:
            if 'ros_packages' not in _cache:
                packages = {}
                base_paths = self.env.config.ros_base_path
                if not base_paths:
                    base_paths = ['.']
                for base_path in base_paths:
                    if base_path.startswith('/'):
                        base_abspath = base_path
                    else:
                        base_abspath = self.env.relfn2path(base_path)[1]
                    found_packages = find_packages(base_abspath)
                    for package in found_packages.values():
                        packages[package.name] = package
                _cache['ros_packages'] = packages
            package = _cache['ros_packages'].get(name, None)
        if not package:
            self.state_machine.reporter.warning(
                'cannot find package %s' % name,
                line=self.lineno)
        return package

    def handle_signature(self, sig, signode):
        sig = sig.strip()
        signode += addnodes.desc_name(sig, sig)
        return sig

    def add_target_and_index(self, name, sig, signode):
        targetname = self.objtype + '-' + name
        fullname = (self.objtype, name)
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['ros']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % name +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    line=self.lineno)
            objects[fullname] = self.env.docname
        indextext = _('%s (ROS %s)') % (name, self.objtype)
        self.indexnode['entries'].append(('single', indextext,
                                          targetname,
                                          ''))
    def before_content(self):
        content = self.update_content()
        if content:
            self.content = content
            # save
            self.tmp_backup = {'content_offset': self.content_offset,
                               'input_lines': self.state.state_machine.input_lines,
                               'get_source_and_line': self.state.reporter.get_source_and_line}
            # overwrite variables to deal with source lines properly
            self.content_offset = 0
            self.state.state_machine.input_lines = self.content
            self.state.reporter.get_source_and_line = self.get_source_and_line
    def after_content(self):
        if hasattr(self, 'tmp_backup'):
            # restore
            self.content_offset = self.tmp_backup['content_offset']
            self.state.state_machine.input_lines = self.tmp_backup['input_lines']
            self.state.reporter.get_source_and_line = self.tmp_backup['get_source_and_line']
    def update_content(self):
        return self.content
    def get_source_and_line(self, lineno=None):
        if lineno is None:
            srcline = None
            src = None
        else:
            src, srcline = self.content.info(lineno)
        return (src, srcline)

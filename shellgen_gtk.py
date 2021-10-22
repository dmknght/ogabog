#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from shellgen.gui import cores
import importlib

all_modules = cores.get_all_modules()


class MainWindows(Gtk.Window):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.list_platforms = Gtk.ListStore(str)
        self.list_modules = Gtk.ListStore(str)
        self.list_classes = Gtk.ListStore(str)
        self.box_platforms = Gtk.ComboBox.new_with_model(self.list_platforms)
        self.box_module = Gtk.ComboBox.new_with_model(self.list_modules)
        self.box_class = Gtk.ComboBox.new_with_model(self.list_classes)
        self.current_module = ""

        self.windows_box()
        self.show_all()

    def on_box_platforms_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            selected_text = combobox.get_model()[tree_iter][0]
            self.current_module = selected_text
            self.list_modules.clear()
            self.list_classes.clear()
            for module in all_modules[selected_text].keys():
                self.list_modules.append([module])
        else:
            print("tree_iter is None. Function: on_box_platforms_changed")

    def on_box_modules_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            selected_text = combobox.get_model()[tree_iter][0]
            self.list_classes.clear()
            for class_name in all_modules[self.current_module.split('.')[0]][selected_text]:
                self.list_classes.append([class_name])
            self.current_module = f"{self.current_module.split('.')[0]}.{selected_text}"

    def on_box_class_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            selected_class_name = combobox.get_model()[tree_iter][0]
            module_name = f"shellgen.modules.{self.current_module}"
            module = getattr(importlib.import_module(module_name), selected_class_name)()
            for module_args in vars(module.module_args)["_group_actions"]:
                # The label to use
                print(module_args.dest)
                print(module_args.help)

    def do_update_list_platforms(self):
        for platform in all_modules.keys():
            self.list_platforms.append([platform])

    def windows_box(self):
        self.connect("destroy", Gtk.main_quit)
        self.main_area()

    def main_area(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label_platform = Gtk.Label(label="Platform")

        label_module = Gtk.Label(label="Module")
        label_class = Gtk.Label(label="Class")

        self.do_update_list_platforms()
        self.box_platforms.connect("changed", self.on_box_platforms_changed)
        self.box_module.connect("changed", self.on_box_modules_changed)
        self.box_class.connect("changed", self.on_box_class_changed)

        renderer_text = Gtk.CellRendererText()
        self.box_platforms.pack_start(renderer_text, True)
        self.box_platforms.add_attribute(renderer_text, "text", 0)

        self.box_module.pack_start(renderer_text, True)
        self.box_module.add_attribute(renderer_text, "text", 0)

        self.box_class.pack_start(renderer_text, True)
        self.box_class.add_attribute(renderer_text, "text", 0)

        main_box.add(label_platform)
        main_box.add(self.box_platforms)
        main_box.add(label_module)
        main_box.add(self.box_module)
        main_box.add(label_class)
        main_box.add(self.box_class)
        self.add(main_box)


if __name__ == "__main__":
    win = MainWindows()
    Gtk.main()

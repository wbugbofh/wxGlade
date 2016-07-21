"""\
Custom wxWindow objects

@copyright: 2002-2007 Alberto Griggio
@copyright: 2014-2016 Carsten Grohmann
@license: MIT (see LICENSE.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import wx
import common
import compat
import misc
from tree import Tree
from wcodegen.taghandler import BaseXmlBuilderTagHandler
from widget_properties import *
from edit_windows import ManagedBase


class ArgumentsProperty(GridProperty):
    def write(self, outfile, tabs):
        if self.getter:
            arguments = self.getter()
        else:
            arguments = self.owner[self.name][0]()
        if arguments:
            inner_xml = u''
            for argument in arguments:
                inner_xml += common.format_xml_tag(u'argument', argument[0],
                                                   tabs + 1)
            stmt = common.format_xml_tag(
                u'arguments', inner_xml, tabs, is_xml=True)
            outfile.write(stmt)

# end of class ArgumentsProperty


class ArgumentsHandler(BaseXmlBuilderTagHandler):

    def __init__(self, parent):
        super(ArgumentsHandler, self).__init__()
        self.parent = parent
        self.arguments = []

    def end_elem(self, name):
        if name == 'arguments':
            self.parent.arguments = self.arguments
            self.parent.properties['arguments'].set_value(self.arguments)
            return True
        elif name == 'argument':
            char_data = self.get_char_data()
            self.arguments.append([char_data])
        return False

# end of class ArgumentsHandler


class CustomWidget(ManagedBase):
    """\
    Class to handle custom widgets

    @ivar arguments: Constructor arguments
    @type arguments: list[str]

    @ivar custom_ctor: if not empty, an arbitrary piece of code that will be used instead of the constructor name
    @type custom_ctor: Unicode
    """

    def __init__(self, name, klass, parent, id, sizer, pos, property_window, show=True):
        ManagedBase.__init__(self, name, klass, parent, id, sizer, pos, property_window, show)
        self.arguments = [['$parent'], ['$id']]  # ,['$width'],['$height']]
        self.access_functions['arguments'] = (self.get_arguments, self.set_arguments)

        cols = [('Arguments', GridProperty.STRING)]
        self.properties['arguments'] = ArgumentsProperty( self, 'arguments', None, cols, 2, label=_("arguments") )

        self.custom_ctor = ""
        self.access_functions['custom_ctor'] = (self.get_custom_ctor, self.set_custom_ctor)
        self.properties['custom_ctor'] = TextProperty(self, 'custom_ctor', None, True, label=_('Custom constructor'))
        self.properties['custom_ctor'].set_tooltip(_('Specify a custom constructor like a factory method'))

    def set_klass(self, value):
        ManagedBase.set_klass(self, value)
        if self.widget:
            self.widget.Refresh()

    def create_widget(self):
        self.widget = wx.Window(
            self.parent.widget, self.id,
            style=wx.BORDER_SUNKEN | wx.FULL_REPAINT_ON_RESIZE)
        wx.EVT_PAINT(self.widget, self.on_paint)

    def finish_widget_creation(self):
        ManagedBase.finish_widget_creation(self, sel_marker_parent=self.widget)

    def on_paint(self, event):
        dc = wx.PaintDC(self.widget)
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        w, h = self.widget.GetClientSize()
        dc.DrawLine(0, 0, w, h)
        dc.DrawLine(w, 0, 0, h)
        text = _('Custom Widget: %s') % self.klass
        tw, th = dc.GetTextExtent(text)
        x = (w - tw)//2
        y = (h - th)//2
        dc.SetPen(wx.ThePenList.FindOrCreatePen(wx.BLACK, 0, wx.TRANSPARENT))
        dc.DrawRectangle(x-1, y-1, tw+2, th+2)
        dc.DrawText(text, x, y)

    def create_properties(self):
        ManagedBase.create_properties(self)
        panel = wx.ScrolledWindow(self.notebook, -1)
        szr = wx.BoxSizer(wx.VERTICAL)
        ctor = self.properties['custom_ctor']
        ctor.display(panel)
        szr.Add(ctor.panel, 0, wx.EXPAND)
        args = self.properties['arguments']
        args.display(panel)
        szr.Add(args.panel, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetAutoLayout(True)
        panel.SetSizer(szr)
        szr.Fit(panel)
        self.notebook.AddPage(panel, 'Widget')
        args.set_col_sizes([-1])

    def get_arguments(self):
        return self.arguments

    def set_arguments(self, value):
        self.arguments = [[misc.wxstr(v) for v in val] for val in value]

    def get_property_handler(self, name):
        if name == 'arguments':
            return ArgumentsHandler(self)
        return ManagedBase.get_property_handler(self, name)

    def get_custom_ctor(self):
        return self.custom_ctor

    def set_custom_ctor(self, value):
        self.custom_ctor = value.strip()



def builder(parent, sizer, pos, number=[1]):
    "factory function for CustomWidget objects"
    class Dialog(wx.Dialog):
        def __init__(self, number=[0]):
            title = _('Select widget class')
            wx.Dialog.__init__(self, None, -1, title)
            self.klass = 'CustomWidget'
            if number[0]:
                self.klass = 'CustomWidget%s' % (number[0] - 1)
            number[0] += 1
            klass_prop = TextProperty(self, 'class', self, label=_("class"))
            szr = wx.BoxSizer(wx.VERTICAL)
            szr.Add(klass_prop.panel, 0, wx.ALL | wx.EXPAND, 5)
            szr.Add(wx.Button(self, wx.ID_OK, _('OK')), 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.SetAutoLayout(True)
            self.SetSizer(szr)
            szr.Fit(self)
            w = self.GetTextExtent(title)[0] + 50
            if self.GetSize()[0] < w:
                self.SetSize((w, -1))
            self.CenterOnScreen()

        def __getitem__(self, value):
            def set_klass(c):
                self.klass = c
            return lambda: self.klass, set_klass

    # end of inner class

    dialog = Dialog()
    dialog.ShowModal()
    klass = dialog.klass
    dialog.Destroy()

    name = 'window_%d' % number[0]
    while common.app_tree.has_name(name):
        number[0] += 1
        name = 'window_%d' % number[0]
    win = CustomWidget(name, klass, parent, wx.NewId(), sizer, pos, common.property_panel)
    node = Tree.Node(win)
    win.node = node

    win.set_option(1)
    win.esm_border.set_style("wxEXPAND")
    win.show_widget(True)

    common.app_tree.insert(node, sizer.node, pos-1)
    sizer.set_item(win.pos, 1, wx.EXPAND)


def xml_builder(attrs, parent, sizer, sizeritem, pos=None):
    "factory to build CustomWidget objects from a XML file"
    from xml_parse import XmlParsingError
    try:
        name = attrs['name']
    except KeyError:
        raise XmlParsingError(_("'name' attribute missing"))
    if not sizer or not sizeritem:
        raise XmlParsingError(_("sizer or sizeritem object cannot be None"))
    win = CustomWidget(name, 'CustomWidget', parent, wx.NewId(), sizer, pos, common.property_panel, True)
    sizer.set_item(win.pos, option=sizeritem.option, flag=sizeritem.flag, border=sizeritem.border)
    node = Tree.Node(win)
    win.node = node
    if pos is None: common.app_tree.add(node, sizer.node)
    else: common.app_tree.insert(node, sizer.node, pos-1)
    return win


def initialize():
    "initialization function for the module: returns a wx.BitmapButton to be added to the main palette"
    common.widgets['CustomWidget'] = builder
    common.widgets_from_xml['CustomWidget'] = xml_builder

    return common.make_object_button('CustomWidget', 'custom.xpm', tip='Add a custom widget')


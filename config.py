# config.py: wxGlade configuration handling
# 
# Copyright (c) 2002 Alberto Griggio <albgrig@tiscalinet.it>
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY

# generated by wxGlade 0.1.3 on Tue Oct 22 16:13:00 2002

from wxPython.wx import *
from ConfigParser import *
import common, misc, sys, os, os.path

class wxGladePreferences(wxDialog):
    def __init__(self, preferences):
        # begin wxGlade: wxGladePreferences.__init__
        wxDialog.__init__(self, None, -1, "")
        self.notebook_1 = wxNotebook(self, -1, style=0)
        self.notebook_1_pane_1 = wxPanel(self.notebook_1, -1)
        self.use_menu_icons = wxCheckBox(self.notebook_1_pane_1, -1,
                                         "Use icons in menu items")
        self.frame_tool_win = wxCheckBox(self.notebook_1_pane_1, -1,
                                         "Show properties and tree windows "
                                         "as small frames (Win32 only)")
        self.use_dialog_units = wxCheckBox(self.notebook_1_pane_1, -1,
                                           "Use dialog units by default for "
                                           "size properties")
        self.show_progress = wxCheckBox(self.notebook_1_pane_1, -1,
                                        "Show progress dialog when loading "
                                        "wxg files")
        self.label_1 = wxStaticText(self.notebook_1_pane_1, -1,
                                    "Initial path for \nfile opening/saving "
                                    "dialogs:")
        self.open_save_path = wxTextCtrl(self.notebook_1_pane_1, -1, "")
        self.label_2_copy = wxStaticText(self.notebook_1_pane_1, -1,
                                         "Initial path for \ncode generation "
                                         "file dialogs:")
        self.codegen_path = wxTextCtrl(self.notebook_1_pane_1, -1, "")
        self.label_2 = wxStaticText(self.notebook_1_pane_1, -1,
                                    "Number of items in file history\n"
                                    "(wxPython >= 2.3.3)")
        self.number_history = wxSpinCtrl(self.notebook_1_pane_1, -1, min=0,
                                         max=100)
        self.ok = wxButton(self, wxID_OK, "OK")
        self.cancel = wxButton(self, wxID_CANCEL, "Cancel")
        self.apply = wxButton(self, -1, "Apply")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        EVT_BUTTON(self, self.apply.GetId(), lambda e: self.set_preferences())

        self.preferences = preferences
        self.set_values()

    def set_values(self):
        try:
            self.use_menu_icons.SetValue(self.preferences.use_menu_icons)
            self.frame_tool_win.SetValue(self.preferences.frame_tool_win)
            self.open_save_path.SetValue(self.preferences.open_save_path)
            self.codegen_path.SetValue(self.preferences.codegen_path)
            self.use_dialog_units.SetValue(self.preferences.use_dialog_units)
            self.number_history.SetValue(self.preferences.number_history)
            self.show_progress.SetValue(self.preferences.show_progress)
        except Exception, e:
            wxMessageBox('Error reading config file:\n%s' % e, 'Error',
                         wxOK|wxCENTRE|wxICON_ERROR)

    def set_preferences(self):
        self.preferences['use_menu_icons'] = self.use_menu_icons.GetValue()
        self.preferences['frame_tool_win'] = self.frame_tool_win.GetValue()
        self.preferences['open_save_path'] = self.open_save_path.GetValue()
        self.preferences['codegen_path'] = self.codegen_path.GetValue()
        self.preferences['use_dialog_units'] = self.use_dialog_units.GetValue()
        self.preferences['number_history'] = self.number_history.GetValue()
        self.preferences['show_progress'] = self.show_progress.GetValue()

    def __set_properties(self):
        # begin wxGlade: wxGladePreferences.__set_properties
        self.SetTitle("wxGlade: preferences")
        self.use_menu_icons.SetValue(1)
        self.frame_tool_win.SetValue(1)
        self.show_progress.SetValue(1)
        self.open_save_path.SetSize((196, -1))
        self.codegen_path.SetSize((196, -1))
        self.number_history.SetSize((196, -1))
        self.ok.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxGladePreferences.__do_layout
        sizer_1 = wxBoxSizer(wxVERTICAL)
        sizer_2 = wxBoxSizer(wxHORIZONTAL)
        sizer_3 = wxBoxSizer(wxVERTICAL)
        sizer_4 = wxFlexGridSizer(3, 2, 0, 0)
        sizer_3.Add(self.use_menu_icons, 0, wxALL|wxEXPAND, 5)
        sizer_3.Add(self.frame_tool_win, 0, wxALL|wxEXPAND, 5)
        sizer_3.Add(self.use_dialog_units, 0, wxALL|wxEXPAND, 5)
        sizer_3.Add(self.show_progress, 0, wxALL|wxEXPAND, 5)
        sizer_4.Add(self.label_1, 0, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.open_save_path, 1, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.label_2_copy, 0, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.codegen_path, 1, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.label_2, 0, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.Add(self.number_history, 0, wxALL|wxALIGN_CENTER_VERTICAL, 5)
        sizer_4.AddGrowableCol(1)
        sizer_3.Add(sizer_4, 0, wxEXPAND, 3)
        self.notebook_1_pane_1.SetAutoLayout(1)
        self.notebook_1_pane_1.SetSizer(sizer_3)
        sizer_3.Fit(self.notebook_1_pane_1)
        notebook_1_sizer = wxNotebookSizer(self.notebook_1)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Interface")
        sizer_1.Add(notebook_1_sizer, 1, wxALL|wxEXPAND, 5)
        sizer_2.Add(self.ok, 0, 0, 0)
        sizer_2.Add(self.cancel, 0, wxLEFT, 10)
        sizer_2.Add(self.apply, 0, wxLEFT, 10)
        sizer_1.Add(sizer_2, 0, wxALL|wxALIGN_RIGHT, 10)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
        self.CentreOnScreen()

# end of class wxGladePreferences


class Preferences(ConfigParser):
    _defaults = {
        'use_menu_icons': wxPlatform != '__WXGTK__',
        'frame_tool_win': True,
        'open_save_path': (os.path.expanduser('~') != '~' and
                           os.path.expanduser('~') or common.wxglade_path),
        'codegen_path': (os.path.expanduser('~') != '~' and
                         os.path.expanduser('~') or common.wxglade_path),
        'use_dialog_units': False,
        'number_history': 4,
        'show_progress': True
        }
    def __init__(self, defaults=None):
        self.def_vals = defaults
        if self.def_vals is None:
            self.def_vals = Preferences._defaults
        self.changed = False
        ConfigParser.__init__(self)

    def __getattr__(self, attr):
        val = self.def_vals.get(attr, "")
        try:
            return type(val)(self.get('wxglade', attr))
        except (NoOptionError, ValueError):
            return val

    def __getitem__(self, attr):
        return self.__getattr__(attr)
    
    def __setitem__(self, attr, val):
        self.set('wxglade', attr, str(val))
        self.changed = True
        
preferences = None

if sys.platform == 'win32': _rc_name = 'wxglade.ini'
else: _rc_name = 'wxgladerc'

if misc.check_wx_version(2, 3, 3): _use_file_history = True
else: _use_file_history = False

def init_preferences():
    global preferences
    if preferences is None:
        preferences = Preferences()
        preferences.read([_rc_name,
                          os.path.expanduser('~/.wxglade/%s' % _rc_name)])
        if not preferences.has_section('wxglade'):
            preferences.add_section('wxglade')

def edit_preferences():
    dialog = wxGladePreferences(preferences)
    if dialog.ShowModal() == wxID_OK:
        dialog.set_preferences()
    dialog.Destroy()

def save_preferences():
    # let the exception be raised
    path = os.path.expanduser('~')
    if path == '~': path = '.'
    else:
        path = os.path.join(path, '.wxglade')
        if not os.path.isdir(path):
            os.mkdir(path)
    # always save the file history
    if _use_file_history:
        fh = common.palette.file_history
        filenames = [ fh.GetHistoryFile(i) for i in
                      range(min(preferences.number_history,
                                fh.GetNoHistoryFiles())) ]
        outfile = open(os.path.join(path, 'file_history.txt'), 'w')
        for filename in filenames:
            print >> outfile, filename
        outfile.close()
    if preferences.changed:
        outfile = open(os.path.join(path, _rc_name), 'w')
        # let the exception be raised to signal abnormal behaviour
        preferences.write(outfile)
        outfile.close()

def load_history():
    """\
    Loads the file history and returns a list of paths
    """
    path = os.path.expanduser('~')
    if path == '~': path = '.'
    else: path = os.path.join(path, '.wxglade')
    try:
        history = open(os.path.join(path, 'file_history.txt'))
        l = history.readlines()
        history.close()
        return l
    except IOError:
        # don't consider this an error
        return [] 

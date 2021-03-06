#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.0a9 on Sun Nov 19 22:21:27 2017
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import wx.py.shell
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.text_ctrl = wx.TextCtrl(self.panel_1, wx.ID_ANY, "This is text_ctrl.\n\nUse the shell to append text here.\nE.g. enter this:\napp.frame.text_ctrl.AppendText(\"text\")\n\n", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.shell = wx.py.shell.Shell(self.panel_1, wx.ID_ANY, introText = "\nThis is the shell.\nHave a look at the variables 'app' and 'app.frame'.\n\n")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame")
        self.text_ctrl.SetMinSize((200, 10))
        self.text_ctrl.SetBackgroundColour(wx.Colour(192, 192, 192))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 1)
        sizer_2.Add(self.shell, 2, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.SetSize((800, 379))
        # end wxGlade

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

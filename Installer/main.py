
import wx
from wx.lib.scrolledpanel import ScrolledPanel
from dataclasses import dataclass
from os.path import isdir, expanduser, abspath, join
from os import mkdir
from shutil import rmtree, unpack_archive
from wx.adv import AnimationCtrl, Animation
from sys import _MEIPASS as mp

@dataclass
class var:
    path : str

v = var ( "" )

def resource_path ( relative_path ):
    
    try:
        base_path = mp
    except Exception:
        base_path = abspath ( "." )

    return join ( base_path, relative_path )

def unpack ( self ):
    try:
        unpack_archive ( resource_path ( "app.zip" ), v.path, 'zip' )
    except PermissionError:
        wx.MessageBox ( "This program does not have permission to access the folder." )
    
def create_s():
    from winshell import desktop
    from win32com.client import Dispatch
    shell = Dispatch ( "WScript.Shell" )
    sc = shell.CreateShortCut ( desktop() + r"\Pydle.lnk" )
    sc.Targetpath = v.path + r"\Pydle.exe"
    sc.WorkingDirectory = v.path
    sc.IconLocation = v.path + r"\Pydle.exe"
    sc.save()

class panel3 ( ScrolledPanel ):
    def __init__ ( self, parent ):
        ScrolledPanel.__init__ ( self, parent = parent )
        self.parent = parent
        self.parent.SetSize ( 620, 410 )
        
        self.SetBackgroundColour ( "black" )
        self.mainsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.topimage = wx.StaticBitmap ( self, -1, wx.Bitmap ( resource_path ( "top3.png" ) ) )
        self.mainsizer.Add ( self.topimage, 0, wx.ALL, 0 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.maintext = wx.StaticText ( self, -1, label = "" )
        self.maintext.SetForegroundColour ( "white" )
        self.maintext.SetFont ( wx.Font ( 18, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        
        self.mainsizer.AddSpacer ( 10 )
        self.mainsizer.Add ( self.maintext, 0, wx.ALL, 10 )
        
        self.maintext = wx.StaticText ( self, -1, label = "Installation is now complete!\nYou can now play the game by opening it from the desktop shortcut!" )
        self.maintext.SetForegroundColour ( "white" )
        self.maintext.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.NORMAL ) )
        self.mainsizer.Add ( self.maintext, 0, wx.ALL, 10 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.bottombuttons = wx.BoxSizer ( wx.HORIZONTAL )
        
        self.finish = wx.Button ( self, label = "Finish" )
        self.finish.SetBackgroundColour ( "black" )
        self.finish.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.finishi, self.finish )
        self.bottombuttons.Add ( self.finish, 0, wx.ALL, 5 )
        
        self.mainsizer.Add ( self.bottombuttons, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        
        self.parent.Layout()
        self.SetSizer ( self.mainsizer )
        self.SetupScrolling()
    
    def finishi ( self, event ):
        self.parent.Destroy()

class panel2 ( ScrolledPanel ):
    def __init__ ( self, parent ):
        ScrolledPanel.__init__ ( self, parent = parent )
        self.parent = parent
        
        self.SetBackgroundColour ( "black" )
        self.mainsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.topimage = wx.StaticBitmap ( self, -1, wx.Bitmap ( resource_path ( "top2.png" ) ) )
        self.mainsizer.Add ( self.topimage, 0, wx.ALL, 0 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.maintext = wx.StaticText ( self, -1, label = "The default location for downloading the program has been set below.\nIf you wish to change it, you can type the path in the box or click browse and select the folder." )
        self.maintext.SetForegroundColour ( "white" )
        self.maintext.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.NORMAL ) )
        self.mainsizer.Add ( self.maintext, 0, wx.ALL, 10 )
        
        self.dest = wx.BoxSizer ( wx.HORIZONTAL )
        self.dtext = wx.TextCtrl ( self, value = r"C:\Pydle", size = ( 200, 23 ) )
        self.dtext.SetBackgroundColour ( "black" )
        self.dtext.SetForegroundColour ( "white" )
        self.dbutton = wx.Button ( self, label = "Browse..." )
        self.dbutton.SetBackgroundColour ( "black" )
        self.dbutton.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.dbuttonbrowse, self.dbutton )
        self.dest.Add ( self.dtext, 0, wx.ALL, 5 )
        self.dest.Add ( self.dbutton, 0, wx.ALL, 5 )
        self.mainsizer.Add ( self.dest, 0, wx.ALL, 10 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.bottombuttons = wx.BoxSizer ( wx.HORIZONTAL )
        
        self.nextbutton = wx.Button ( self, label = "Install >" )
        self.nextbutton.SetBackgroundColour ( "black" )
        self.nextbutton.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.nextframe, self.nextbutton )
        self.bottombuttons.Add ( self.nextbutton, 0, wx.ALL, 5 )
        
        self.cancelbutton = wx.Button ( self, label = "Cancel" )
        self.cancelbutton.SetBackgroundColour ( "black" )
        self.cancelbutton.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.cancelframe, self.cancelbutton )
        self.bottombuttons.Add ( self.cancelbutton, 0, wx.ALL, 5 )
        
        self.mainsizer.Add ( self.bottombuttons, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        
        self.dtext.SetFocus()
        self.SetSizer ( self.mainsizer )
        self.SetupScrolling()
    
    def dbuttonbrowse ( self, event ):
        dialog = wx.DirDialog ( None, "Choose Install Directory", "", wx.DD_DIR_MUST_EXIST | wx.DD_DEFAULT_STYLE )
        dialog.ShowModal()
        path = dialog.GetPath()
        self.dtext.SetValue ( path )
    
    def cancelframe ( self, event ):
        self.parent.Destroy()
    
    def nextframe ( self, event ):
        v.path = self.dtext.GetValue()
        try:
            if isdir ( v.path ):
                pass
            else:
                mkdir ( v.path )
        except:
            wx.MessageBox ( message = "Please enter a valid path for installing! Note: This program cannot create multiple sub-folders.", style = wx.ICON_ERROR )
            return
        self.Destroy()
        self.parent.Layout()
        wx.MessageBox ( message = "Installing...Please wait. This window will be unresponsive until installation is complete." )
        panel3 ( self.parent )
        unpack ( self )
        create_s()
        self.parent.Layout()
        
class panel1 ( ScrolledPanel ):
    def __init__ ( self, parent ):
        ScrolledPanel.__init__ ( self, parent = parent )
        self.parent = parent
        
        self.SetBackgroundColour ( "black" )
        self.mainsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.topimage = wx.StaticBitmap ( self, -1, wx.Bitmap ( resource_path ( "top.png" ) ) )
        self.mainsizer.Add ( self.topimage, 0, wx.ALL, 0 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.maintext = wx.StaticText ( self, -1, label = "Hi! Welcome to the Pydle installer.\nThis program will help you to install Pydle on your PC. Please check the box below to continue:" )
        self.maintext.SetForegroundColour ( "white" )
        self.maintext.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.NORMAL ) )
        self.mainsizer.Add ( self.maintext, 0, wx.ALL, 10 )
        
        self.checkbox = wx.CheckBox ( self, label = "I agree to install Pydle on my PC." )
        self.checkbox.SetForegroundColour ( "white" )
        self.checkbox.SetBackgroundColour ( "black" )
        self.Bind ( wx.EVT_CHECKBOX, self.boxhandle, self.checkbox )
        self.mainsizer.Add ( self.checkbox, 0, wx.ALL, 10 )
        
        self.mainsizer.AddSpacer ( 30 )
        
        self.bottombuttons = wx.BoxSizer ( wx.HORIZONTAL )
        
        self.nextbutton = wx.Button ( self, label = "Next >" )
        self.nextbutton.SetBackgroundColour ( "black" )
        self.nextbutton.SetForegroundColour ( "white" )
        self.nextbutton.Disable()
        self.Bind ( wx.EVT_BUTTON, self.nextframe, self.nextbutton )
        self.bottombuttons.Add ( self.nextbutton, 0, wx.ALL, 5 )
        
        self.cancelbutton = wx.Button ( self, label = "Cancel" )
        self.cancelbutton.SetBackgroundColour ( "black" )
        self.cancelbutton.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.cancelframe, self.cancelbutton )
        self.bottombuttons.Add ( self.cancelbutton, 0, wx.ALL, 5 )
        
        self.mainsizer.Add ( self.bottombuttons, 0, wx.ALL | wx.ALIGN_RIGHT, 5 )
        
        self.cancelbutton.SetFocus()
        self.SetSizer ( self.mainsizer )
        self.SetupScrolling()
        
    def boxhandle ( self, event ):
        if self.checkbox.IsChecked():
            self.nextbutton.Enable()
        else:
            self.nextbutton.Disable()
    
    def cancelframe ( self, event ):
        self.parent.Destroy()
    
    def nextframe ( self, event ):
        self.Destroy()
        panel2 ( self.parent )
        self.parent.Layout()

class Window ( wx.Frame ):
    def __init__ ( self ):
        wx.Frame.__init__ ( self, parent = None, title = "Install", size = ( 616, 400 ) )
        
        self.SetIcon ( wx.Icon ( resource_path ( "icon.bmp" ) ) )
        panel1 ( self )
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    Window()
    app.MainLoop()

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from random import choice
from dataclasses import dataclass
from time import time, sleep
import cv2 as cv
from numpy import array
from os import mkdir, path
from shutil import rmtree
from ast import literal_eval
from text_json import *
from math import ceil

def get_kt_image ( letter, typ ):
    img = cv.imread ( ".\letter_tiles\kt\{}.png".format ( letter ) )
    rep = []
    final = []
    if typ == "n":
        return path.abspath ( "letter_tiles\kt\{}.png".format ( letter.lower() ) )
    if typ == "b":
        rep = [ 120, 124, 126 ]
    if typ == "y":
        rep = [ 100, 150, 200 ]
    if typ == "g":
        rep = [ 106, 170, 100 ]

    size = img.shape
    img = img.tolist()
    for i in range ( size[0] ):
        temp = []
        for j in range ( size[1] ):
            if img[i][j] == [ 0, 0, 0 ]:
                temp.append ( rep )
            else:
                temp.append ( [ 0, 0, 0 ] )
        final.append ( temp )
    p = path.abspath ( "temp" ) + "\{}.png".format ( str ( time() ) )
    cv.imwrite ( p, array ( final ) )
    return p

def get_tile_image ( letter, typ ):
    img = cv.imread ( ".\letter_tiles\{}.png".format ( letter ) )
    rep = []
    final = []
    if typ == "n":
        return path.abspath ( "letter_tiles\{}.png".format ( letter.lower() ) )
    if typ == "b":
        rep = [ 120, 124, 126 ]
    if typ == "y":
        rep = [ 100, 150, 200 ]
    if typ == "g":
        rep = [ 106, 170, 100 ]

    size = img.shape
    img = img.tolist()
    for i in range ( size[0] ):
        temp = []
        for j in range ( size[1] ):
            if img[i][j] != [ 255, 255, 255 ]:
                temp.append ( rep )
            else:
                temp.append ( [ 0, 0, 0 ] )
        final.append ( temp )
    p = path.abspath ( "temp" ) + "\{}.png".format ( str ( time() ) )
    cv.imwrite ( p, array ( final ) )
    return p

def check_after ( letter, index ):
    l = v.recent
    final = []
    c = 0
    for i in l:
        if i.lower() == letter.lower():
            final.append ( c )
        c += 1
    if len ( final ) == 1:
        return False
    if len ( final ) == 2:
        final.remove ( index )
        if final[0] < index:
            return False
        else:
            return True
    if len ( final ) == 3:
        final.remove ( index )
        if final[0] < index or final[1] < index:
            return False
        return True

def verify ( self ):
    w = v.word
    n = 0
    for i in range ( v.r ):
        n += 5  
    c = 0
    guess = ( v.recent[0] + v.recent[1] + v.recent[2] + v.recent[3] + v.recent[4] ).lower()
    if word_exists ( guess ):
        v.n = 0
        v.r = v.r + 1
    else:
        wx.MessageBox ( message = "Word does not exist!", style = wx.ICON_ERROR )
        return False
    
    for i in v.recent:
        dc = False
        if i.lower() in w and i.lower() == w[c]:
            p = get_tile_image ( i, "g" )
            sleep ( 0.20 )
            b = get_kt_image ( i, "g" )
            v.lc[c] = i.lower()
        elif i.lower() in w and i.lower() != w[c]:
            if check_after ( i, c ) or i.lower() in v.lc:
                p = get_tile_image ( i, "b" )
                sleep ( 0.20 )
                dc = True
            else:
                p = get_tile_image ( i, "y" )
                sleep ( 0.20 )
                b = get_kt_image ( i, "y" )
            
        elif i.lower() not in w:
            p = get_tile_image ( i, "b" )
            sleep ( 0.20 )
            b = get_kt_image ( i, "b" )

        v.tiles[n].SetBitmap ( wx.Bitmap ( p ) )
        if dc == False:
            v.keytiles[i.lower()].SetBitmap ( wx.Bitmap ( b ) )
        n += 1
        c += 1
    if w == guess:
        wx.MessageBox ( message = "You won! On try number: {}".format ( v.r ) )
        if not v.done:
            write_setting ( "won", str ( int ( get_setting ( "won" ) ) + 1 ) )
            write_setting ( "cs", str ( int ( get_setting ( "cs" ) ) + 1 ) )
            if get_setting ( "cs" ) >= get_setting ( "ms" ):
                write_setting ( "ms", str ( int ( get_setting ( "ms" ) ) + 1 ) )
            write_setting ( str ( v.r ), str ( int ( get_setting ( str ( v.r ) ) ) + 1 ) )
            stats ( self )
        v.done = True
    
    try:
        data.remove ( v.word )
    except:
        pass
    if not v.start:
        write_setting ( "remaining", data )
        write_setting ( "total", str ( int ( get_setting ( "total" ) ) + 1 ) )
    v.start = True
    return True
    
def word_exists ( word ):
    if word in v.allw:
        return True
    return False

@dataclass
class variables:
    word : str
    tiles : list
    n : int
    r : int
    recent : list
    done : bool
    allw : list
    keyboard : list
    keytiles : dict
    lc : list
    start : bool

data = literal_eval ( get_setting ( "remaining" ) )
r = choice ( data )

with open ( r"all.txt", 'r' ) as f:
    alld = literal_eval ( f.read() )
    f.close()

v = variables ( r, [], 0, 0, [ 0, 0, 0, 0, 0 ], False, alld, [], {}, [ "", "", "", "", "" ], False )

class panel ( ScrolledPanel ):
    def __init__ ( self, parent ):
        ScrolledPanel.__init__ ( self, parent = parent )
        self.SetBackgroundColour ( "black" )
        try:
            mkdir ( path.abspath ( "temp" ) )
        except:
            rmtree ( path.abspath ( "temp" ) )
            mkdir ( path.abspath ( "temp" ) )
        
        self.sizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.tiles_sizer = wx.GridSizer ( 6, 5, 5, 5 )
        for i in range ( 6 ):
            for j in range ( 5 ):
                t = wx.StaticBitmap ( self, -1, wx.Bitmap ( r".\letter_tiles\blank.png" ) )
                self.tiles_sizer.Add ( t )
                v.tiles.append ( t )
        
        self.sizer.AddSpacer ( 30 )
        self.SetFont ( wx.Font ( 32, wx.DEFAULT, wx.DEFAULT, wx.BOLD ) )
        self.text = wx.StaticText ( self, label = "Pydle #{}".format ( str ( get_setting ( "total" ) ) ) )
        self.text.SetForegroundColour ( "white" )
        self.sizer.Add ( self.text, 0, wx.ALIGN_CENTER, 5 )
        
        self.sizer.AddSpacer ( 30 )
        
        self.sizer.Add ( self.tiles_sizer, 0, wx.ALIGN_CENTER, 5 )
        
        self.sizer.AddSpacer ( 30 )
        
        self.firstsizer = wx.BoxSizer ( wx.HORIZONTAL )
        l = [ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p" ]
        for i in range ( len ( l ) ):
            temp = wx.BitmapButton ( self, -1, wx.Bitmap ( r".\letter_tiles\kt\{}.png".format ( l[i] ) ), style = wx.BORDER_NONE, name = l[i] )
            temp.SetBackgroundColour ( "black" )
            self.firstsizer.Add ( temp, 0, wx.ALL, 5 )
            self.Bind ( wx.EVT_BUTTON, self.processBoardChar, temp )
            v.keytiles[l[i]] = temp
        self.sizer.Add ( self.firstsizer, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
        
        self.secsizer = wx.BoxSizer ( wx.HORIZONTAL )
        l = [ "a", "s", "d", "f", "g", "h", "j", "k", "l" ]
        for i in range ( len ( l ) ):
            temp = wx.BitmapButton ( self, -1, wx.Bitmap ( r".\letter_tiles\kt\{}.png".format ( l[i] ) ), style = wx.BORDER_NONE, name = l[i] )
            temp.SetBackgroundColour ( "black" )
            self.secsizer.Add ( temp, 0, wx.ALL, 5 )
            self.Bind ( wx.EVT_BUTTON, self.processBoardChar, temp )
            v.keytiles[l[i]] = temp
        self.sizer.Add ( self.secsizer, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
        
        self.thisizer = wx.BoxSizer ( wx.HORIZONTAL )
        l = [ "enter", "z", "x", "c", "v", "b", "n", "m", "back" ]
        for i in range ( len ( l ) ):
            temp = wx.BitmapButton ( self, -1, wx.Bitmap ( r".\letter_tiles\kt\{}.png".format ( l[i] ) ), style = wx.BORDER_NONE, name = l[i] )
            temp.SetBackgroundColour ( "black" )
            self.thisizer.Add ( temp, 0, wx.ALL, 5 )
            if l[i] == "enter":
                self.ekey = temp
                self.Bind ( wx.EVT_BUTTON, self.processBoardEnter, temp )
            elif l[i] == "back":
                self.Bind ( wx.EVT_BUTTON, self.processBoardBack, temp )
            elif len ( l[i] ) == 1:
                self.Bind ( wx.EVT_BUTTON, self.processBoardChar, temp )
            v.keytiles[l[i]] = temp
        self.sizer.Add ( self.thisizer, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
        
        #self.sizer.AddSpacer ( 10 )
        #self.line = wx.StaticBitmap ( self, -1, wx.Bitmap ( ".\images\line.bmp" ) )
        #self.sizer.Add ( self.line, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
        
        self.endsizer = wx.BoxSizer ( wx.HORIZONTAL )
        self.stats = wx.BitmapButton ( self, -1, wx.Bitmap ( ".\images\statistics.bmp" ), style = wx.BORDER_NONE )
        self.Bind ( wx.EVT_BUTTON, self.statsframe, self.stats )
        self.stats.SetBackgroundColour ( "black" )
        self.endsizer.Add ( self.stats, 0, wx.ALIGN_CENTER, 5 )
        self.endsizer.AddSpacer ( 20 )
        self.help = wx.BitmapButton ( self, -1, wx.Bitmap ( ".\images\help.bmp" ), style = wx.BORDER_NONE )
        self.Bind ( wx.EVT_BUTTON, self.helpframe, self.help )
        self.help.SetBackgroundColour ( "black" )
        self.endsizer.Add ( self.help, 0, wx.ALIGN_CENTER, 5 )
        
        self.sizer.Add ( self.endsizer, 0, wx.ALIGN_CENTER, 5 )
        self.ekey.SetFocus()
        self.Bind ( wx.EVT_CHAR_HOOK, self.processChar )
        self.SetSizer ( self.sizer )
        self.Show()
    
    def helpframe ( self, event ):
        helps ( self )
    
    def processBoardBack ( self, event ):
        self.ekey.SetFocus()
        num = v.n
        if v.n == 0:
            return
        for i in range ( v.r ):
            num += 5
        v.tiles[num-1].SetBitmap ( wx.Bitmap ( r".\letter_tiles\blank.png" ) )
        v.n = v.n - 1
    
    def processBoardEnter ( self, event ):
        if v.done:
            return
        if v.n == 5:
            r = verify ( self )
            num = v.n
            for i in range ( v.r ):
                num += 5
            if num >= 30 and r == True:
                wx.MessageBox ( message = "All chances completed! The word was: {}".format ( v.word ) )
                if not v.done:
                    write_setting ( "lost", str ( int ( get_setting ( "lost" ) ) + 1 ) )
                    write_setting ( "cs", "0" )
                v.done = True
                return
    
    def processBoardChar ( self, event ):
        self.ekey.SetFocus()
        if v.done == True:
            return
        l = event.EventObject.GetName()
        if v.n >= 5:
            return
        v.recent[v.n] = l
        ip = get_tile_image ( l, "n" )
        num = v.n
        for i in range ( v.r ):
            num += 5
        if num >= 30:
            wx.MessageBox ( message = "All chances completed! The word was: {}".format ( v.word ) )
            if not v.done:
                write_setting ( "lost", str ( int ( get_setting ( "lost" ) ) + 1 ) )
                write_setting ( "cs", "0" )
            v.done = True
            return
        v.tiles[num].SetBitmap ( wx.Bitmap ( ip ) )
        v.n += 1
        
    def statsframe ( self, event ):
        stats ( self )
    
    def processChar ( self, event ):
        r = 0
        self.ekey.SetFocus()
        if v.done == True:
            return
        acil = event.GetKeyCode()
        if acil == 8 and v.n != 0:
            num = v.n
            for i in range ( v.r ):
                num += 5
            v.tiles[num-1].SetBitmap ( wx.Bitmap ( r".\letter_tiles\blank.png" ) )
            v.n = v.n - 1
        if acil == 13 or acil == 370 and v.n == 5:
            r = verify ( self )
            num = v.n
            for i in range ( v.r ):
                num += 5
            if num >= 29 and r == True:
                wx.MessageBox ( message = "All chances completed! The word was: {}".format ( v.word ) )
                if not v.done:
                    write_setting ( "lost", str ( int ( get_setting ( "lost" ) ) + 1 ) )
                    write_setting ( "cs", "0" )
                v.done = True
                return
        if v.n >= 5:
            return
        if acil >= 65 and acil <= 90:
            l = chr ( acil )
        else:
            return
        v.recent[v.n] = l
        ip = get_tile_image ( l, "n" )
        num = v.n
        for i in range ( v.r ):
            num += 5
        if num >= 30 and r == True:
            wx.MessageBox ( message = "All chances completed! The word was: {}".format ( v.word ) )
            if not v.done:
                write_setting ( "lost", str ( int ( get_setting ( "lost" ) ) + 1 ) )
                write_setting ( "cs", "0" )
            v.done = True
            return
        v.tiles[num].SetBitmap ( wx.Bitmap ( ip ) )
        v.n += 1
        
class stats ( wx.MiniFrame ):
    def __init__ ( self, parent ):
        wx.MiniFrame.__init__ ( self, parent = parent, title = "Game Statistics", style = wx.CAPTION | wx.CLOSE_BOX, size = ( 600, 300 ) )

        self.SetBackgroundColour ( "black" )
        
        self.totalsizer = wx.BoxSizer ( wx.HORIZONTAL )
        self.mainsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.mainsizer.AddSpacer ( 10 )
        self.ts = wx.BoxSizer ( wx.HORIZONTAL )
        self.tt = wx.StaticText ( self, -1, label = ' ' + get_setting ( "total" ) )
        self.tt.SetForegroundColour ( "white" )
        self.tt.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.tg = wx.StaticText ( self, -1, label = " Played" )
        self.tg.SetForegroundColour ( "white" )
        self.tg.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.ts.Add ( self.tt, 0, wx.ALL, 0 )
        self.ts.Add ( self.tg, 0, wx.TOP, 23 )
        self.mainsizer.Add ( self.ts, 0, wx.ALL, 5 )
        
        self.ws = wx.BoxSizer ( wx.HORIZONTAL )
        try:
            self.wt = wx.StaticText ( self, -1, label = ' ' + str ( int ( ( int ( get_setting ( "won" ) ) / int ( get_setting ( "total" ) ) ) * 100 ) ) )
        except:
            self.wt = wx.StaticText ( self, -1, label = " 0" )
        self.wt.SetForegroundColour ( "#538d4e" )
        self.wt.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.wg = wx.StaticText ( self, -1, label = " Win %" )
        self.wg.SetForegroundColour ( "#538d4e" )
        self.wg.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.ws.Add ( self.wt, 0, wx.ALL, 0 )
        self.ws.Add ( self.wg, 0, wx.TOP, 23 )
        self.mainsizer.Add ( self.ws, 0, wx.ALL, 5 )
        
        self.cst = wx.BoxSizer ( wx.HORIZONTAL )
        self.ctt = wx.StaticText ( self, -1, label = ' ' + get_setting ( "cs" ) )
        self.ctt.SetForegroundColour ( "#009bff" )
        self.ctt.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.cgt = wx.StaticText ( self, -1, label = " Current Streak" )
        self.cgt.SetForegroundColour ( "#009bff" )
        self.cgt.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.cst.Add ( self.ctt, 0, wx.ALL, 0 )
        self.cst.Add ( self.cgt, 0, wx.TOP, 23 )
        self.mainsizer.Add ( self.cst, 0, wx.ALL, 5 )
        
        self.mst = wx.BoxSizer ( wx.HORIZONTAL )
        self.mtt = wx.StaticText ( self, -1, label = ' ' + get_setting ( "ms" ) )
        self.mtt.SetForegroundColour ( "#ea4235" )
        self.mtt.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.mgt = wx.StaticText ( self, -1, label = " Max Streak" )
        self.mgt.SetForegroundColour ( "#ea4235" )
        self.mgt.SetFont ( wx.Font ( 10, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.mst.Add ( self.mtt, 0, wx.ALL, 0 )
        self.mst.Add ( self.mgt, 0, wx.TOP, 23 )
        self.mainsizer.Add ( self.mst, 0, wx.ALL, 5 )
        
        self.secsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.listrownum = [ int ( get_setting ( "1" ) ), int ( get_setting ( "2" ) ), int ( get_setting ( "3" ) ), 
                           int ( get_setting ( "4" ) ), int ( get_setting ( "5" ) ), int ( get_setting ( "6" ) ) ]
        
        finalfactor = []
        if max ( self.listrownum ) <= 10:
            finalfactor = self.listrownum
        else:
            factor = max ( self.listrownum ) / 10
            for i in self.listrownum:
                finalfactor.append ( ceil ( i / factor ) )
        
        self.boxes = []
        for i in range ( len ( finalfactor ) ):
            temp = ""
            for j in range ( finalfactor[i] ):
                temp += "██"
            self.boxes.append ( temp )
        
        self.secsizer.AddSpacer ( 7 )
        
        self.topt = wx.StaticText ( self, -1, label = "Guess Distribution" )
        self.topt.SetForegroundColour ( "white" )
        self.topt.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline = True ) )
        self.secsizer.Add ( self.topt, 0, wx.TOP | wx.LEFT, 13 )
        
        self.one = wx.StaticText ( self, -1, label = "Row 1 → " + self.boxes[0] + " " + str ( self.listrownum[0] ) )
        self.one.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.one.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.one, 0, wx.TOP | wx.LEFT, 13 )
        
        self.two = wx.StaticText ( self, -1, label = "Row 2 → " + self.boxes[1] + " " + str ( self.listrownum[1] ) )
        self.two.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.two.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.two, 0, wx.TOP | wx.LEFT, 13 )
        
        self.thr = wx.StaticText ( self, -1, label = "Row 3 → " + self.boxes[2] + " " + str ( self.listrownum[2] ) )
        self.thr.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.thr.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.thr, 0, wx.TOP | wx.LEFT, 13 )
        
        self.fou = wx.StaticText ( self, -1, label = "Row 4 → " + self.boxes[3] + " " + str ( self.listrownum[3] ) )
        self.fou.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.fou.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.fou, 0, wx.TOP | wx.LEFT, 13 )
        
        self.fiv = wx.StaticText ( self, -1, label = "Row 5 → " + self.boxes[4] + " " + str ( self.listrownum[4] ) )
        self.fiv.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.fiv.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.fiv, 0, wx.TOP | wx.LEFT, 13 )
        
        self.six = wx.StaticText ( self, -1, label = "Row 6 → " + self.boxes[5] + " " + str ( self.listrownum[5] ) )
        self.six.SetFont ( wx.Font ( 12, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.six.SetForegroundColour ( "white" )
        self.secsizer.Add ( self.six, 0, wx.TOP | wx.LEFT, 13 )
        
        self.totalsizer.Add ( self.mainsizer, 0, wx.ALL, 0 )
        self.totalsizer.AddSpacer ( 70 )
        self.totalsizer.Add ( self.secsizer, 0, wx.ALL, 0 )
        
        self.SetSizer ( self.totalsizer )
        self.Show()

class helps ( wx.MiniFrame ):
    def __init__ ( self, parent ):
        wx.MiniFrame.__init__ ( self, parent = parent, title = "Pydle Help", style = wx.CAPTION | wx.CLOSE_BOX, size = ( 900, 600 ) )
        self.SetBackgroundColour ( "black" )
        
        wx.StaticBitmap ( self, -1, wx.Bitmap ( ".\images\help_in.bmp" ) )
        
        self.Show()

class Window ( wx.Frame ):
    def __init__ ( self ):
        wx.Frame.__init__ ( self, parent = None, title = "Pydle", size = ( 600, 900 ) )
        self.SetIcon ( wx.Icon ( "icon.bmp" ) )
        panel ( self )
        self.Bind ( wx.EVT_CLOSE, self.close )
        self.Show()
    
    def close ( self, event ):
        if v.start == True and v.done == False:
            d = wx.MessageBox ( message = "If you exit now, this game will be considered lost. You can minimize this window if you want to play afterwards. Are you sure you want to close?", style = wx.YES_NO | wx.ICON_WARNING )
            if d == wx.YES:
                write_setting ( "lost", str ( int ( get_setting ( "lost" ) ) + 1 ) )
                write_setting ( "cs", "0" )
                self.Destroy()
        else:
            self.Destroy()
            
if __name__ == "__main__":
    app = wx.App()
    window = Window()
    app.MainLoop()
"""
    ExtendedImageView.py
    Extended functionality to ImageView widget

"""

from PyDVT import __version__,__date__,__author__

#import PyDVT.ImageView as ImageView
#import PyDVT.ImageViewSelect as ImageViewSelect
from PyDVT.ImageView import *
import PyDVT.ImageViewSelect


class C111ExtendedImageView(ImageView):
    """
    This class implements a widget based on ImageView with extended functionalities.
    Uses filters defined in ImageView.

    Interface:
    ===========================
    ImageView interface
    CreateViewSelect
    GetViewSelect
    ClearViewSelect
    SetColormap
    SetScale
    HistColormapWidget
    EventSelection (overridable active view selection callback
                    not needed if "SelectionCallback" defined in __init__)
    """
    def __init__(self, parent=None, pars={}, **kw):      
        """
        See ImageView.__init__
        Parameters:
          parent: Parent window
          pars:   Dictionary with View initialization options
                  New options defined by this class (in addiction to base class options):
                   "AddSelection": Adds default image view selections in popup menu
                                   Default: 1
                   "AddStatus": Adds status bar to the view to display mouse position
                                Default: 1
                   "AddColormap": Adds colormap editor entry in popup menu
                                  Default: 1
                   "UseColormapWidget": If 1 uses changes colormap with ColormapEditorWidget
                                        instead of Menu and Histogram dialog
                                        Default: 1                   
                   "AddReduc": Adds reduction entry in popup menu
                                     Default: 0
                   "AddCursorSelect": Adds cursor type selection in popup menu 
                                 Default: 0
                   "SelectionCallback": If "AddSelection" selected, gives a callback function
                                 for the active ViewSelect object's Selection events.
                                 Default: None
                   "UseImageValues": This option changes the way the pixel value given in the
                                     status bar is retrieved.
                                     By default position events retrieve pixel values from data
                                     object itself, by working with data coordinates.
                                     This is done so multiple view can work based on the same
                                     coordinates, and to save memory, since this option
                                     forces "StoreImageData" option in ImageView.
                                     In the case operations/filters have changed the displayed
                                     data, it is possible to display the result value in the status
                                     bar by setting this option to 1. In this case the view object
                                     stores the "data" object from it's selection, and searches
                                     for the pixel value based on image coordinates (see
                                     DemoOperator.py).
                                     If this option is set, values are only available if source
                                     has "data" (it doesn'r work for such filters as ImageFilter,
                                     that just has "image" key).
                                 Default: 0
          kw:     keywords to Container initializatregisterion                
        """
        if "AddSelection" in pars.keys(): self.AddSelection=pars["AddSelection"]
        else: self.AddSelection=1
        if "AddStatus" in pars.keys(): self.AddStatus=pars["AddStatus"]
        else: self.AddStatus=1
        if "AddColormap" in pars.keys(): self.AddColormap=pars["AddColormap"]
        else: self.AddColormap=1
        if "UseColormapWidget" in pars.keys(): self.UseColormapWidget=pars["UseColormapWidget"]
        else: self.UseColormapWidget=1
        if "AddReduc" in pars.keys(): self.AddReduc=pars["AddReduc"]
        else: self.AddReduc=0
        if "AddCursorSelect" in pars.keys(): self.AddCursorSelect=pars["AddCursorSelect"]
        else: self.AddCursorSelect=0
        if "SelectionCallback" in pars.keys(): self.SelectionCallback=pars["SelectionCallback"]
        else: self.SelectionCallback=None
        if "UseImageValues" in pars.keys(): self.UseImageValues=pars["UseImageValues"]
        else: self.UseImageValues=0

        if self.UseImageValues: pars["StoreImageData"]=1
        
        ImageView.__init__ (self,parent,pars,**kw)


        self.label=None
        if self.AddStatus:
          self.label = Label(self)        
          self.label.Show()        
        self.ColormapDlg=None
        self.Select=None
        self.ZoomSelect=None

    def CreateMenu(self):
        """
        Can be overwritten by derived classes to create a
        different popup menu
        """
        ImageView.CreateMenu(self)

        if self.MenuPopup is not None:self.AddMenuSeparator()
        if self.AddColormap:
          if self.UseColormapWidget:
            self.AddMenuPopupItem("Colormap Editor",self._MenuColormap)
          else:
            popup=Menu(self.MenuPopup)
            colormappopup=Menu(popup)
            for n in ("GrayScale","Temperature","Red","Green","Blue","RevGrey"):
                colormappopup.AddCommand(n,Command.Command(self.SetColormap,n),"radiobutton")
            colormappopup.SetCheckedRadio("Temperature")
            popup.AddCascade("Colormap Type",colormappopup)
            scalepopup=Menu(popup)
            for n in ("Linear","Logarithmic","Gamma"):
                scalepopup.AddCommand(str(n),Command.Command(self.SetScale,n),"radiobutton")
            scalepopup.SetCheckedRadio("Linear")
            popup.AddCascade("Scale",scalepopup)
            popup.AddCommand("Limits on Histogram",self.HistColormapWidget)
            self.AddMenuPopupCascade("Colormap",popup)
        if self.AddReduc:
          popup=Menu(self.MenuPopup)          
          popup.AddCommand("1/1",Command.Command(self._SetReduc,1),"radiobutton")
          popup.AddCommand("1/2",Command.Command(self._SetReduc,2),"radiobutton")
          popup.AddCommand("1/4",Command.Command(self._SetReduc,4),"radiobutton")
          popup.AddCommand("1/8",Command.Command(self._SetReduc,8),"radiobutton")
          popup.SetCheckedRadio("1/1")
          self.AddMenuPopupCascade("Reduction",popup)
        if self.AddCursorSelect:
          popup=Menu(self.MenuPopup)          
          popup.AddCommand("None",Command.Command(self.SetCursorType, cursortype="None"),"radiobutton")
          popup.AddCommand("Crosshairs",Command.Command(self.SetCursorType, cursortype="Crosshairs"),"radiobutton")
          popup.SetCheckedRadio("None")
          self.AddMenuPopupCascade("Cursor",popup)

        if self.AddSelection:
          popup=Menu(self.MenuPopup)          
          popup.AddCommand("Horizontal",Command.Command(self.CreateViewSelect,ImageViewSelect.ImageViewSelectHLine),"radiobutton")
          popup.AddCommand("Vertical",Command.Command(self.CreateViewSelect,ImageViewSelect.ImageViewSelectVLine),"radiobutton")
          popup.AddCommand("Line",Command.Command(self.CreateViewSelect,ImageViewSelect.ImageViewSelectLine),"radiobutton")
          popup.AddCommand("Rectangle",Command.Command(self.CreateViewSelect,ImageViewSelect.ImageViewSelectRect),"radiobutton")
          #popup.AddCommand("Point",Command.Command(self.CreateViewSelect,ImageViewSelect.ImageViewSelectPoint),"radiobutton")          
          popup.AddSeparator()
          popup.AddCommand("Clear Cut",self.ClearViewSelect,"radiobutton")
          popup.SetCheckedRadio("Clear Cut")
          self.AddMenuPopupCascade("Cut",popup)

        
        
    def _SetReduc (self,reduc=1,fastreduc=0):
      colormap_filter=self.GetColormapFilter()
      if colormap_filter is not None:
          colormap_filter.SetReducParameters(reduc,fastreduc)
            

    def _MenuColormap(self):
        if self.ColormapDlg==None or self.ColormapDlg.IsDestroyed():
            from PyDVT.ColormapSelect import ColormapDialog
            colormap_filter=self.GetColormapFilter()
            if colormap_filter is not None:              
              image_par=colormap_filter.GetColormapParameters()
              self.ColormapDlg=ColormapDialog(self.parent,image_par)
              colormap_filter.ConnectColormap(self.ColormapDlg.Colormap)


    def _ClearSel(self):
        if self.Select is not None:
          self.Select.Destroy()
          self.Select=None


    def GetViewSelect(self):
        """
        Returns ViewSelect object created by CreateViewSelect or None.
        """
        return self.Select

    def ClearViewSelect(self):
        """
        Destroys ViewSelect object created by CreateViewSelect or None.
        """
        self._ClearSel()

    def CreateViewSelect(self,selection_class,callback=None):
        """
        Creates a ViewSelect object and connects it to self. If former ViewSelect
        exists, it is destroyed
        Parameters:
            selection_class: class of the ViewSelect to be created
            callback: Selection event callback            
        """
        if callback==None: callback=self.EventSelection
        if (self.Source != ()):
          self._ClearSel()
          data=self.Source[0].GetData()
          if data==None: return
          self.Select=selection_class(data,callback)
          self.Select.ConnectView(self)



    def ZoomTo(self):
          if self.Select is not  None: self.Select.Disable()          
          ImageView.ZoomTo(self)


    def _EventZoomSelection(self,source):
          ImageView._EventZoomSelection(self,source)
          if self.Select is not None: self.Select.Enable()


#################################
#            COLORMAP
#################################

    def SetColormap(self,colormap):
        """
        Changes colormap of its ColormapFilter
        Parameters:
            colormap: "GrayScale","Temperature","Red","Green","Blue" or "RevGrey"
        """
        colormap_filter=self.GetColormapFilter()
        if colormap_filter != None:
            pars=colormap_filter.GetColormapParameters()
            pars["Colormap"]=colormap
            colormap_filter.SetColormapParameters(pars)

    def SetScale(self,scale):
        """
        Changes scale of its ColormapFilter
        Parameters:
            scale: "Linear", "Logarithmic", "Gamma"
        """
        colormap_filter=self.GetColormapFilter()
        if colormap_filter != None:
            pars=colormap_filter.GetColormapParameters()
            pars["Scale"]=scale
            colormap_filter.SetColormapParameters(pars)


    def HistColormapWidget(self):
        """
        Creates a dialog with the histogram of the image on which
        it can be selected the limits of colormap transformation.
        """
        if self.Source != ():
            print "IN HistColormapWidget ... " 
            from PyDVT.GraphView import GraphView,HistFilter
            from PyDVT.GraphViewSelect import GraphViewSelectHRect
            if hasattr(self,"HistDlg")==0 or self.HistDlg==None or self.HistDlg.IsDestroyed():
                self.HistDlg=Dialog(self,"Histogram",modal=0,resizable=1,expand_container=1)
                self.HistView=GraphView(self.HistDlg,{"AddStyleSelect":1,"AddCursorSelect":1,"AddStatus":1,"AutoHideStatus":1,"ZoomMode":"OFF","ScrollMode":"OFF",})
                self.HistDlg.AddContainer(self.HistView)
                filter=HistFilter("1",self.Source[0].GetSource(),pen=Pen((0,196,0),1,"solid"))
                filter.SetDivisions(100)
                self.HistView.SetStyle("Bars")

                colormap_filter=self.GetColormapFilter()
                if colormap_filter is not None:
                    colormap_pars=colormap_filter.GetColormapParameters()
                    title_label="Min:%f   Max:%f" % (colormap_pars["MinMax"][0],colormap_pars["MinMax"][1])
                else: title_label=""
                
                self.HistView.SetLabels(title_label=title_label,x_label="Value",y_label="Count")
                self.HistView.SetSource(filter)

                data=self.Source[0].GetData()
                if data==None: return
                self.HistSelect=GraphViewSelectHRect(data,self._EventHistSelection)
                self.HistSelect.SetBrush(self.HistView.ZoomBrush)
                self.HistSelect.ConnectView(self.HistView)

                self.HistSelect.SetSelectionPos(((colormap_pars["MinMax"][0],0),(colormap_pars["MinMax"][1],0))) 
                self.HistDlg.SetSize(450,300)
                self.HistView.Show()
                self.HistDlg.Show()

    def _EventHistSelection(self,source):
        colormap_filter=self.GetColormapFilter()
        if colormap_filter is not None:              
            ((x0,y0),(x1,y1))=source.GetSelection()["BoundingRect"]
            colormap_pars=colormap_filter.GetColormapParameters()
            colormap_pars["MinMax"]=(x0,x1)
            colormap_pars["AutoScale"]=0
            colormap_filter.SetColormapParameters(colormap_pars)        
            title_label="Min:%f   Max:%f" % (colormap_pars["MinMax"][0],colormap_pars["MinMax"][1])
            self.HistView.SetLabels(title_label=title_label,x_label="Value",y_label="Count")
            self.HistView.Redraw()
        
#################################
#            EVENTS
#################################

    def EventSelection(self,source):
        """
        Overridable: there's two ways of getting the built-in selection events:
                     either overriding this method or by adding "SelectionCallback"
                     option in __init__.
        Parameters:
            source: ImageViewSelect object thar generated the event
        """
        if self.SelectionCallback is not None: self.SelectionCallback(source)
        

    def EventPosition(self,source):
        """
        Overridable: Cursor callback event
                     ExtendedImageView threats it if "AddStaus" option set in __init__.
                     In this case, if this function is overriden ,derived classes
                     should call ExtendedImageView.EventPosition
        Parameters:
            source: ImageViewSelect object thar generated the event
        """
        if self.label==None: return
        sel=source.GetSelection()        
        pos=sel["Position"]
        if self.UseImageValues==0:
            value=self.GetDataPositionValue(pos.DataCoord)
            coords=(pos.DataCoord.PageCoord[0],pos.DataCoord.PageCoord[1])
        else:
            #TODO: Decide where to get the coords: Image or Data?
            if pos.DataCoord is not None: coords=(pos.DataCoord.PageCoord[0],pos.DataCoord.PageCoord[1])
            else: coords=pos.ImageCoord
            value=self.GetImagePositionValue(pos.ImageCoord)
        if value is None: str=""
        else:
            if  type(value) is types.TupleType:
              str="x:%07.3f   y:%07.3f   z: (" % (coords[0],coords[1])
              for i in range (len(value)):
                str = str + "%d," % (value[i])
              str=str + ")"
            else:
              str="x:%07.3f   y:%07.3f   z:%07.3f" % (coords[0],coords[1],value)
        self.label.SetText(str)            

#################################
#            VIRTUALS
#################################

    def DataChanged(self,source=None):
        """
        Virtual: See ImageView.DataChanged
        """
        if self.Source == () and self.label is not None:  self.label.SetText("")
        ImageView.DataChanged(self,source)
        #if self.Cursor is not None: self.Cursor.Update(self)
        #if hasattr(self,"Select") and self.Select is not None: self.Select.Update(self)
          
        
    def Destroy(self,source=None):
      """
      Virtual: See ImageView.Destroy
      """
      self._ClearSel()
      self.ColormapDlg=None
      if hasattr(self,"HistView"):self.HistView.Destroy()      
      if hasattr(self,"HistSelect"):self.HistSelect.Destroy()
      self.HistView=self.HistSelect=None
      ImageView.Destroy(self)
    
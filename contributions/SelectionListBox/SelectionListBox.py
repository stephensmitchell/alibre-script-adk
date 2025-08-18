
import clr
import sys
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (
    ListBox, SelectionMode, Padding, AutoScaleMode,
    Timer, Button, ToolTip, ContextMenuStrip,
    DockStyle, AnchorStyles, Cursors, FlatStyle
)
clr.AddReference('System.Drawing')
from System.Drawing import Color, Size, Point as gPoint, SizeF
import System
import os
def get_module_path():
    return os.path.dirname(__file__)

sys.path.append(get_module_path())
from Filters_Class import Filters

ScriptName = 'SelectionListBoxTest'
langError = 'Error'
langClearList = 'Clear List'
langClearAll = 'Clear All'
langRemoveSelected = 'Remove Selected Item(s)'
langClearedAll = 'Cleared All'
langErrorMaybeEditing = 'ERROR: Make sure you are not editing something in the assembly.\nYou must now return to editing the main assembly before continuing.'
langClearedSelected = 'Cleared Selected'


def printTraceBack():
    import traceback
    print('\n--------------\n' + str(traceback.format_exc()) + '--------------\n')
    return

def ClearSelection():
    import AlibreScript
    Root = AlibreScript.API.Global.Root
    #Root = Global.Root
    top_sess = Root.TopmostSession
    while top_sess.SelectedObjects.Count > 0:
        myselected = top_sess.SelectedObjects
        myselected.Clear()
        top_sess.Select(myselected)
        print(str(langClearedSelected))
    return

class SelectionListBox(ListBox):
    def __new__(cls):
        instance = ListBox.__new__(cls)
        instance.AutoScaleDimensions = SizeF(96, 96)
        instance.AutoScaleMode = AutoScaleMode.Dpi
        instance.IntegralHeight = 1
        # instance.Height = 24
        instance.Margin = Padding(2)
        instance.SelectionMode = SelectionMode.MultiExtended
        instance.BackColor = Color.White

        import AlibreScript
        Root = AlibreScript.API.Global.Root
        instance.Root = Root
        instance.top_sess = instance.Root.TopmostSession
        instance.myTimer = Timer()
        instance.myTimer.Tick += instance.TimerEventProcessor
        # Sets the timer interval to .1 seconds.
        instance.myTimer.Interval = 100
        instance.HoldTimer = 0

        instance.Enter += instance.onEnter_Selection
        instance.Leave += instance.onLeave_Selection
        instance.HandleDestroyed += instance.onHandleDestroyed
        instance.SelectedValueChanged += instance.onSelectedValueChanged

        instance.cm = ContextMenuStrip()
        instance.cm.Opening += instance.OpeningContextMenu
        instance.ContextMenuStrip = instance.cm

        instance.my_filter = Filters()
        instance.OriginalSelectionName = ''
        instance.PreviousSelection = instance.Root.NewObjectCollector()

        instance.AutoNext = 0

        instance._filtertype = None
        instance._filter_map = {
            'face': instance.my_filter.FacesOnly,
            'faces': instance.my_filter.FacesOnly,
            'edge': instance.my_filter.EdgesOnly,
            'edges': instance.my_filter.EdgesOnly,
            'vertex': instance.my_filter.VerticesOnly, # This is only valid at the part level
            'vertices': instance.my_filter.VerticesOnly, # This is only valid at the part level
            'plane': instance.my_filter.PlanesOnly,
            'planes': instance.my_filter.PlanesOnly,
            'axis': instance.my_filter.AxesOnly,
            'axes': instance.my_filter.AxesOnly,
            'point': instance.my_filter.PointsOnly,
            'points': instance.my_filter.PointsOnly,
            'sketch': instance.my_filter.Sketches2DOnly, # actually lets you select both 2D and 3D sketches, So 2D and 3D sketches will need to be separated later
            'sketches': instance.my_filter.Sketches2DOnly, # actually lets you select both 2D and 3D sketches, So 2D and 3D sketches will need to be separated later
            'sketch2d': instance.my_filter.Sketches2DOnly, # actually lets you select both 2D and 3D sketches, So 2D and 3D sketches will need to be separated later
            'sketches2d': instance.my_filter.Sketches2DOnly, # actually lets you select both 2D and 3D sketches, So 2D and 3D sketches will need to be separated later
            'sketch3d': instance.my_filter.Sketches3DOnly, # not working. Seems to be same as 2DOnly, So 2D and 3D sketches will need to be separated later
            'sketches3d': instance.my_filter.Sketches3DOnly, # not working. Seems to be same as 2DOnly, So 2D and 3D sketches will need to be separated later
            'part': instance.my_filter.PartsOnly,
            'parts': instance.my_filter.PartsOnly,
            'member': instance.my_filter.PartsOnly,
            'members': instance.my_filter.PartsOnly,
            'assembly': instance.my_filter.AssembliesOnly, # This acually filters components, So assemblies and parts will need to be separated later
            'assemblies': instance.my_filter.AssembliesOnly, # This acually filters components, So assemblies and parts will need to be separated later
            }

        instance._TypesNeedingToUseOccurrence = ['part', 'parts', 'assembly', 'assemblies', 'member', 'members']
        instance.multiline_types = [
            'faces', 'edges', 'vertices', 'planes', 'axes', 'points',
            'sketches', 'sketches2d', 'sketches3d',
            'parts', 'members', 'assemblies'
        ]
        instance.type_map = {
            'AD_FACE': ['face', 'faces'],
            'AD_EDGE': ['edge', 'edges'],
            'AD_VERTEX': ['vertex', 'vertices'],
            'AD_DESIGN_PLANE': ['plane', 'planes'],
            'AD_DESIGN_AXIS': ['axis', 'axes'],
            'AD_DESIGN_POINT': ['point', 'points'],
            'AD_SKETCH': ['sketch', 'sketches', 'sketch2d', 'sketches2d'],
            'AD_3D_SKETCH': ['sketch3d', 'sketches3d'],
            'AD_OCCURRENCE': ['part', 'parts', 'member', 'members', 'assembly', 'assemblies']
        }
        instance.MyClearButton = Button()
        instance.MyClearButton.Text = 'X'
        instance.MyClearButton.Margin = Padding(0)
        instance.MyClearButton.Padding = Padding(0)
        instance.MyClearButton.Size = Size(19, 19)
        instance.MyClearButton.Location = gPoint(instance.Width - 21, -1)
        # instance.MyClearButton.Dock = (DockStyle.Top | DockStyle.Right)
        instance.MyClearButton.Anchor = (AnchorStyles.Top | AnchorStyles.Right)
        instance.MyClearButton.FlatStyle = FlatStyle.Flat  # FlatStyle.Popup
        instance.MyClearButton.FlatAppearance.BorderSize = 1
        instance.MyClearButton.BackColor = Color.LightPink
        instance.MyClearButton.Cursor = Cursors.Hand
        instance.MyClearButton.TabStop = 0
        instance.Controls.Add(instance.MyClearButton)
        instance.MyClearButton.Click += instance.ClearAll
        instance.toolTip1 = ToolTip()
        instance.toolTip1.ShowAlways = 1

        instance.toolTip1.SetToolTip(instance.MyClearButton, str(langClearList))

        return instance

    @property
    def Tag(self):
        return self._filtertype

    @Tag.setter
    def Tag(self, value):
        self._filtertype = value
        if ',' in value:
            SelectType, SelectVersion = str(value).lower().split(",", 1)
            SelectVersion = float(SelectVersion)
        else:
            SelectType = str(value).lower()
            SelectVersion = 0.0

        # Determine number of rows to show
        if SelectType in self.multiline_types:
            visible_rows = 4  # You can tweak this per type if needed
        else:
            visible_rows = 1

        # Calculate height based on item height and padding
        g = self.CreateGraphics()
        dpi_scale = g.DpiY / 96.0
        g.Dispose()
        row_height = int((self.ItemHeight or 19) * dpi_scale) # fallback if not initialized
        padding = 6  # extra space for borders/margins
        self.Height = (row_height * visible_rows) + padding
        self.Invalidate()

    def apply_filter_by_tag(self):
        SelectType = str(self.Tag).lower().split(",", 1)[0] if self.Tag else ''
        filter_func = self._filter_map.get(SelectType, self.my_filter.Reset)
        filter_func()

    def format_full_name(self, item):
        sess_type = str(self.top_sess.SessionType)
        target = item.Target
        occ = item.Occurrence

        if str(target.Type) == 'AD_TOPOLOGY':
            if sess_type == 'AD_ASSEMBLY':
                if occ:
                    return str(occ.Name) + ': ' + str(item.DisplayName).split(':')[1]
                else:
                    return '*' + str(self.top_sess.Name) + ': ' + str(item.DisplayName)
            else:
                return str(self.top_sess.Name) + ': ' + str(item.DisplayName)

        elif str(target.Type) == 'AD_SKETCH':
            if sess_type == 'AD_ASSEMBLY':
                return str(occ.Name) + ': ' + str(item.DisplayName).split(':')[1]
            else:
                return str(self.top_sess.Name) + ': ' + str(item.DisplayName)

        elif str(target.Type) == 'AD_3D_SKETCH':
            if sess_type == 'AD_ASSEMBLY':
                return str(occ.Name) + ': ' + str(target.Name).split(':')[1]
            else:
                return str(self.top_sess.Name) + ': ' + str(target.Name)

        elif str(target.Type) == 'AD_DESIGN_PLANE':
            if sess_type == 'AD_ASSEMBLY':
                if occ:
                    return str(occ.Name) + ': ' + str(item.DisplayName)
                else:
                    return '*' + str(self.top_sess.Name) + ': ' + str(item.DisplayName)
            else:
                return str(self.top_sess.Name) + ': ' + str(item.DisplayName)

        elif str(target.Type) == 'AD_DESIGN_AXIS':
            if sess_type == 'AD_ASSEMBLY':
                if occ:
                    return str(occ.Name) + ': ' + str(item.DisplayName)
                else:
                    return '*' + str(self.top_sess.Name) + ': ' + str(item.DisplayName)
            else:
                return str(self.top_sess.Name) + ': ' + str(item.DisplayName)

        elif str(target.Type) == 'AD_DESIGN_POINT':
            if sess_type == 'AD_ASSEMBLY':
                if occ:
                    return str(occ.Name) + ': ' + str(item.DisplayName)
                else:
                    return '*' + str(self.top_sess.Name) + ': ' + str(item.DisplayName)
            else:
                return str(self.top_sess.Name) + ': ' + str(item.DisplayName)

        elif str(target.Type) == 'AD_OCCURRENCE':
            if sess_type == 'AD_ASSEMBLY':
                return str(occ.Name)
            else:
                return str(self.top_sess.Name)

        else:
            return str(item.DisplayName)


    def add_selection_item(self, item, full_name, SelectType):
        clear_first = SelectType not in self.multiline_types

        if clear_first:
            self.Items.Clear()
            self.PreviousSelection.Clear()

        self.Items.Add(full_name)
        self.PreviousSelection.Add(item)

    def onEnter_Selection(self, sender, e):
        try:
            if sender.Tag:
                if ',' in self.Tag:
                    SelectType, SelectVersion = str(self.Tag).lower().split(",", 1)
                    SelectVersion = float(SelectVersion)
                else:
                    SelectType = str(self.Tag).lower()
                    SelectVersion = 0.0
                if sender.PreviousSelection.Count:
                    prev = sender.PreviousSelection
                    if SelectType in self._TypesNeedingToUseOccurrence:
                        OC = self.Root.NewObjectCollector()
                        for i in range(0, prev.Count):
                            OC.Add(prev.Item(i).Occurrence)
                        self.top_sess.Select(OC)
                    # for i in range(0, prev.Count):
                    #     print(prev.Item(i).Target.Type)
                    else:
                        self.top_sess.Select(prev)
                else:
                    while self.top_sess.SelectedObjects.Count > 0:
                        emptyCollect = self.Root.NewObjectCollector()
                        self.top_sess.Select(emptyCollect)
                        self.top_sess.Highlight(emptyCollect)
                        print(str(langClearedSelected))
                self.apply_filter_by_tag()
            sender.BackColor = Color.LightCyan
            if self.SelectedIndices < 0:
                emptyCollect = self.Root.NewObjectCollector()
                self.top_sess.Highlight(emptyCollect)
            sender.myTimer.Start()
        except Exception, e:
            print('\n')
            printTraceBack()
            print(str(langErrorMaybeEditing))
            if 'Object reference not set to an instance of an object' in str(e):
                Win.ErrorDialog(str(langErrorMaybeEditing), str(ScriptName) + ': ' + str(langError))

    def onLeave_Selection(self, sender, e):
        sender.myTimer.Stop()
        sender.my_filter.Reset()
        sender.BackColor = Color.White

    def onHandleDestroyed(self, sender, e):
        sender.myTimer.Stop()
        sender.my_filter.Reset()

    def OpeningContextMenu(self, sender, e):
        self.cm.Items.Clear()
        self.cm.Items.Add(str(langClearAll), None, self.ClearAll)
        if self.SelectedItems:
            self.cm.Items.Add(str(langRemoveSelected), None, self.RemoveSelected)
        e.Cancel = 0

    def ClearAll(self, sender, e):
        if self.ContainsFocus:
            while self.top_sess.SelectedObjects.Count > 0:
                emptyCollect = self.Root.NewObjectCollector()
                self.top_sess.Select(emptyCollect)
                self.top_sess.Highlight(emptyCollect)
                print(str(langClearedAll))
        self.Items.Clear()
        self.PreviousSelection.Clear()
        self.OriginalSelectionName = ''
        if not self.ContainsFocus:
            self.Focus()

    def onSelectedValueChanged(self, sender, e):
        try:
            if self.HoldTimer:
                return
            if self.Tag:
                if ',' in self.Tag:
                    SelectType, SelectVersion = str(self.Tag).lower().split(",", 1)
                    SelectVersion = float(SelectVersion)
                else:
                    SelectType = str(self.Tag).lower()
                    SelectVersion = 0.0
                if self.SelectedIndices:
                    SI = self.SelectedIndices
                    OC = self.Root.NewObjectCollector()
                    for z in range(0, SI.Count):
                        for i in range(0, self.PreviousSelection.Count):
                            if i == SI[z]:
                                if SelectType in self._TypesNeedingToUseOccurrence:
                                    OC.Add(self.PreviousSelection.Item(i).Occurrence)
                                else:
                                    OC.Add(self.PreviousSelection.Item(i))
                    self.top_sess.Highlight(OC)
        except Exception, e:
            print('\n')
            printTraceBack()
            print(str(langErrorMaybeEditing))
            if 'Object reference not set to an instance of an object' in str(e):
                Win.ErrorDialog(str(langErrorMaybeEditing), str(ScriptName) + ': ' + str(langError))


    def RemoveSelected(self, sender, e):
        TimerWasEnabled = 0
        if self.myTimer.Enabled:
            # print('TimerWasEnabled')
            TimerWasEnabled = 1
            self.HoldTimer = 1
            self.myTimer.Stop()
        if self.ContainsFocus:
            emptyCollect = self.Root.NewObjectCollector()
            self.top_sess.Select(emptyCollect)
        SI = self.SelectedIndices
        for i in reversed(range(0, SI.Count)):
            num = int(SI[i])
            # print('removing item ' + str(num))
            self.Items.RemoveAt(num)
            self.PreviousSelection.Remove(num)  # sender.Owner.SourceControl
        if self.ContainsFocus:
            self.top_sess.Highlight(emptyCollect)
        else:
            self.Focus()
        if TimerWasEnabled:
            self.HoldTimer = 0
            self.myTimer.Start()


    def TimerEventProcessor(self, sender, e):
        global MyThreadVars
        try:
            if self.HoldTimer:
                return
            self.myTimer.Stop()
            NewSelections = self.top_sess.SelectedObjects
            if self.Tag:
                if ',' in self.Tag:
                    SelectType, SelectVersion = str(self.Tag).lower().split(",", 1)
                    SelectVersion = float(SelectVersion)
                else:
                    SelectType = str(self.Tag).lower()
                    SelectVersion = 0.0
                for a in range(0, NewSelections.Count):
                    item = NewSelections.Item(a)
                    FullName = self.format_full_name(item)
                    target_type = str(item.Target.Type)

                    if FullName in self.Items:
                        continue

                    # Special case: AD_TOPOLOGY needs TopologyType
                    if target_type == 'AD_TOPOLOGY':
                        topo_type = str(item.Target.TopologyType)
                        valid_types = self.type_map.get(topo_type, [])
                        if SelectType in valid_types:
                            self.add_selection_item(item, FullName, SelectType)

                    # Special case: AD_OCCURRENCE needs DesignSession type and optional filtering
                    elif target_type == 'AD_OCCURRENCE':
                        session_type = str(item.Target.DesignSession.SessionType)
                        valid_types = self.type_map.get(target_type, [])

                        if SelectType in valid_types:
                            if SelectType in ['member', 'members']:
                                if is_builtbymeOCC(item.Occurrence, 1):
                                    self.add_selection_item(item, FullName, SelectType)
                            elif SelectType in ['part', 'parts']:
                                if session_type in ['AD_PART', 'AD_SHEET_METAL']:
                                    self.add_selection_item(item, FullName, SelectType)
                            elif SelectType in ['assembly', 'assemblies']:
                                if session_type == 'AD_ASSEMBLY':
                                    self.add_selection_item(item, FullName, SelectType)

                    # General case: direct match from type_map
                    else:
                        valid_types = self.type_map.get(target_type, [])
                        if SelectType in valid_types:
                            self.add_selection_item(item, FullName, SelectType)
                if self.PreviousSelection.Count:
                    prev = self.PreviousSelection
                    if SelectType in self._TypesNeedingToUseOccurrence:
                        OC = self.Root.NewObjectCollector()
                        for i in range(0, prev.Count):
                            OC.Add(prev.Item(i).Occurrence)
                        self.top_sess.Select(OC)
                    # for i in range(0, prev.Count):
                    #     print(prev.Item(i).Target.Type)
                    else:
                        self.top_sess.Select(prev)
                else:
                    while self.top_sess.SelectedObjects.Count > 0:
                        emptyCollect = self.Root.NewObjectCollector()
                        self.top_sess.Select(emptyCollect)
                        self.top_sess.Highlight(emptyCollect)
                        print(str(langClearedSelected))
                # Automatically move to next control if the conditions are right
                if self.AutoNext == 1:
                    can_auto_next = SelectType not in self.multiline_types
                    if can_auto_next and self.PreviousSelection.Count == 1:
                            if not str(self.PreviousSelection.Item(0).DisplayName) == self.OriginalSelectionName:
                                self.OriginalSelectionName = str(self.PreviousSelection.Item(0).DisplayName)
                                self.Parent.SelectNextControl(self, 1, 1, 1, 1)
                                return # return without starting the timer.
                            else: # original and previous are the same
                                pass
            self.myTimer.Start()
        except Exception, e:
            print('\n')
            printTraceBack()
            print(str(langErrorMaybeEditing))
            if 'Object reference not set to an instance of an object' in str(e):
                Win.ErrorDialog(str(langErrorMaybeEditing), str(ScriptName) + ': ' + str(langError))

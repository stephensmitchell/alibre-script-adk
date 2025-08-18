# '***  Filters_Class                                         ***'
# '***  by NateLiqGrav          10/21/2019                    ***'
# '***  Change user's selection filters (can be reset back)   ***'
# '**************************************************************'


#########################################################################################################################
#########################################################################################################################
###  classes
#########################################################################################################################
#########################################################################################################################

class Filters:
    def __init__(self, verbose = 0):
        import AlibreScript
        #from AlibreScript import *
        root = AlibreScript.API.Global.Root
        #root = Global.Root
        self.top_sess = root.TopmostSession
        self.OriginalFilter = self.top_sess.SelectionFilter
        self.OriginalAnnotations = bool(self.OriginalFilter.Annotations)
        self.OriginalAxes = bool(self.OriginalFilter.Axes)
        self.OriginalDimensions = bool(self.OriginalFilter.Dimensions)
        self.OriginalPlanes = bool(self.OriginalFilter.Planes)
        self.OriginalPoints = bool(self.OriginalFilter.Points)
        self.OriginalRedlines = bool(self.OriginalFilter.Redlines)
        self.OriginalSketches2D = bool(self.OriginalFilter.Sketches2D)
        self.OriginalSketches3D = bool(self.OriginalFilter.Sketches3D)
        self.OriginalSolid = str(self.OriginalFilter.Solid)
        self.OriginalSurface = str(self.OriginalFilter.Surface)
        if verbose:
            print('\nOriginal Filter Settings:')
            self.Print_Current()


    def FacesOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_FACES
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def EdgesOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_EDGES
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def VerticesOnly(self, verbose = 0):
        # This is only valid at the part level
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_VERTICES
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def PlanesOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 1
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_NONE
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def AxesOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 1
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_NONE
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def PointsOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 1
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_NONE
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def Sketches2DOnly(self, verbose = 0):
        # actually lets you select both 2D and 3D Skeches
        # So 2D and 3D Skeches will need to be separated later
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 1
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_NONE
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def Sketches3DOnly(self, verbose = 0):
        # Not working right so really turning on Sketches2DOnly
        # So 2D and 3D Skeches will need to be separated later
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 1
        NewFilter.Sketches3D = 1
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_NONE
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def PartsOnly(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 1
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_PARTS
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def AssembliesOnly(self, verbose = 0):
        # This acually filters components
        # So assemblies and parts will need to be separated later
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = 0
        NewFilter.Axes = 0
        NewFilter.Dimensions = 0
        NewFilter.Planes = 0
        NewFilter.Points = 0
        NewFilter.Redlines = 0
        NewFilter.Sketches2D = 0
        NewFilter.Sketches3D = 0
        NewSolid = NewFilter.Solid
        NewFilter.Solid = NewSolid.AD_COMPONENTS
        NewSurface = NewFilter.Surface
        NewFilter.Surface = NewSurface.AD_NONE
        if verbose:
            print('\nNew Filter Settings:')
            self.Print_Current()


    def Reset(self, verbose = 0):
        NewFilter = self.top_sess.SelectionFilter
        NewFilter.Annotations = self.OriginalAnnotations
        NewFilter.Axes = self.OriginalAxes
        NewFilter.Dimensions = self.OriginalDimensions
        NewFilter.Planes = self.OriginalPlanes
        NewFilter.Points = self.OriginalPoints
        NewFilter.Redlines = self.OriginalRedlines
        NewFilter.Sketches2D = self.OriginalSketches2D
        NewFilter.Sketches3D = self.OriginalSketches3D
        NewSolid = NewFilter.Solid
        if self.OriginalSolid == 'AD_NONE':
            NewFilter.Solid = NewSolid.AD_NONE
        if self.OriginalSolid == 'AD_VERTICES':
            NewFilter.Solid = NewSolid.AD_VERTICES
        if self.OriginalSolid == 'AD_EDGES':
            NewFilter.Solid = NewSolid.AD_EDGES
        if self.OriginalSolid == 'AD_FACES':
            NewFilter.Solid = NewSolid.AD_FACES
        if self.OriginalSolid == 'AD_FACES_EDGES':
            NewFilter.Solid = NewSolid.AD_FACES_EDGES
        if self.OriginalSolid == 'AD_FACES_EDGES_VERTICES':
            NewFilter.Solid = NewSolid.AD_FACES_EDGES_VERTICES
        if self.OriginalSolid == 'AD_FEATURES':
            NewFilter.Solid = NewSolid.AD_FEATURES
        if self.OriginalSolid == 'AD_SURFACES':
            NewFilter.Solid = NewSolid.AD_SURFACES
        if self.OriginalSolid == 'AD_PARTS':
            NewFilter.Solid = NewSolid.AD_PARTS
        if self.OriginalSolid == 'AD_COMPONENTS':
            NewFilter.Solid = NewSolid.AD_COMPONENTS
        NewSurface = NewFilter.Surface
        if self.OriginalSurface == 'AD_NONE':
            NewFilter.Surface = NewSurface.AD_NONE
        if self.OriginalSurface == 'AD_VERTICES':
            NewFilter.Surface = NewSurface.AD_VERTICES
        if self.OriginalSurface == 'AD_EDGES':
            NewFilter.Surface = NewSurface.AD_EDGES
        if self.OriginalSurface == 'AD_FACES':
            NewFilter.Surface = NewSurface.AD_FACES
        if self.OriginalSurface == 'AD_FACES_EDGES':
            NewFilter.Surface = NewSurface.AD_FACES_EDGES
        if self.OriginalSurface == 'AD_FACES_EDGES_VERTICES':
            NewFilter.Surface = NewSurface.AD_FACES_EDGES_VERTICES
        if self.OriginalSurface == 'AD_FEATURES':
            NewFilter.Surface = NewSurface.AD_FEATURES
        if self.OriginalSurface == 'AD_SURFACES':
            NewFilter.Surface = NewSurface.AD_SURFACES
        if self.OriginalSurface == 'AD_PARTS':
            NewFilter.Surface = NewSurface.AD_PARTS
        if self.OriginalSurface == 'AD_COMPONENTS':
            NewFilter.Surface = NewSurface.AD_COMPONENTS
        if verbose:
            print('\nReset Filter Settings:')
            self.Print_Current()


    def Print_Current(self):
        NewFilter = self.top_sess.SelectionFilter
        print('Annotations = ' + str(NewFilter.Annotations))
        print('Axes =        ' + str(NewFilter.Axes))
        print('Dimensions =  ' + str(NewFilter.Dimensions))
        print('Planes =      ' + str(NewFilter.Planes))
        print('Points =      ' + str(NewFilter.Points))
        print('Redlines =    ' + str(NewFilter.Redlines))
        print('Sketches2D =  ' + str(NewFilter.Sketches2D))
        print('Sketches3D =  ' + str(NewFilter.Sketches3D))
        print('Solid =       ' + str(NewFilter.Solid))
        print('Surface =     ' + str(NewFilter.Surface))

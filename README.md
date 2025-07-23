To run Alibre Script code from an Alibre Design addon, only the ScriptRunner class is required. This repository (the alibre-script-adk) and its related content were created to provide community and public resources, but they are not required.

Utilities for creating Alibre Script-based add-ons no coding required.

ADK Overview [wip]:
1) ScriptRunner Class - Iron Python 3 script runner
2) Integration Class [planned]
3) Add-on Helper Classs [planned]
4) Tools - Helper scripts and executables addon generation, no code tools [planned]
5) Example code [wip]
6) Demo addons [wip] 
8) API Testing reports and addons [wip]

Issues/Notes:
  - AlibreScript.API.Windows is not correctly receiving the hwd from the addon/Alibre.
  - The Alibre Script library should function exactly the same. What may require fixes and rewriting are code that was written for the Alibre Script addon, workarounds, global or undocumented objects.
  - You can ask AI to explain the ScriptRunner class but don't let it refactor it, what's there works for Alibre Script. Your decision.
  - There are hardcoded values for development safe to change, I use tools to manage strings and paths.
  - Don't use Part() if testing, TopmostSession loads faster and is more responsive.
  - Some global and AlibreX techniques and workarounds break or get confusing. Scripts should use the simplest method unless necessary.
  - What's not included are code templates, shared classes for Python.NET, Iron Python 3 and integration classes.
  - ScriptRunner is setup to match the Alibre Script addon.
  - Use scope.SetVariable and searchPaths to setup the environment how you want.
  - Alibre Script is working in Iron Python 3 (updated the nuget package) and is what I'll use in the main project. Code that requires 2.7.10 won't be supported.

Tested/Confirmed APIs:

- [ ]  ASDictionary | **builtin**.type
- [ ]  ASDictionaryEntry | **builtin**.type
- [x]  AssembledPart | **builtin**.type
- [x]  AssembledSubAssembly | **builtin**.type
- [x]  Assembly | **builtin**.type
- [x]  Axis | **builtin**.type
- [x]  Bspline | **builtin**.type
- [x]  Bspline3D | **builtin**.type
- [x]  Circle | **builtin**.type
- [x]  CircularArc | **builtin**.type
- [x]  CircularArc3D | **builtin**.type
- [x]  Configuration | **builtin**.type
- [ ]  CurrentAssemblies | **builtin**.Func[list]
- [ ]  CurrentAssembly | **builtin**.Func[Assembly]
- [ ]  CurrentPart | **builtin**.Func[Part]
- [ ]  CurrentParts | **builtin**.Func[list]
- [x]  Edge | **builtin**.type
- [x]  Ellipse | **builtin**.type
- [x]  EllipticalArc | **builtin**.type
- [x]  Face | **builtin**.type
- [x]  Feature | **builtin**.type
- [x]  GearSketch | **builtin**.type
- [ ]  Global | **builtin**.type
- [ ]  GlobalParameters | **builtin**.type
- [x]  GuideCurveTypes | **builtin**.type
- [x]  IAssembled | **builtin**.type
- [x]  IAxis | **builtin**.type
- [x]  IChamferable | **builtin**.type
- [x]  IConstrainable | **builtin**.type
- [x]  IFilletable | **builtin**.type
- [x]  IInstance | **builtin**.type
- [x]  IPlane | **builtin**.type
- [x]  IPoint | **builtin**.type
- [x]  ISelectableGeometry | **builtin**.type
- [x]  ISketchFigure | **builtin**.type
- [x]  ISketchFigure3D | **builtin**.type
- [x]  ISketchSurface | **builtin**.type
- [x]  ISweepPath | **builtin**.type
- [x]  Line | **builtin**.type
- [x]  Line3D | **builtin**.type
- [x]  LockTypes | **builtin**.type
- [x]  Material | **builtin**.type
- [x]  Parameter | **builtin**.type
- [x]  ParameterTypes | **builtin**.type
- [x]  ParameterUnits | **builtin**.type
- [x]  Part | **builtin**.type
- [x]  Plane | **builtin**.type
- [x]  Point | **builtin**.type
- [x]  Polyline | **builtin**.type
- [x]  Polyline3D | **builtin**.type
- [x]  PolylinePoint | **builtin**.type
- [x]  PolylinePoint3D | **builtin**.type
- [ ]  STL | **builtin**.type
- [ ]  Selection | **builtin**.type
- [ ]  SessionIdentifier | **builtin**.str
- [x]  Sketch | **builtin**.type
- [x]  Sketch3D | **builtin**.type
- [x]  SketchPoint | **builtin**.type
- [x]  SketchPoint3D | **builtin**.type
- [x]  ThreeD | **builtin**.type
- [ ]  ThumbnailOptions | **builtin**.type
- [x]  TwoD | **builtin**.type
- [x]  UnitTypes | **builtin**.type
- [x]  Units | **builtin**.type
- [ ]  Utility | **builtin**.type
- [x]  Vertex | **builtin**.type
- [ ]  Windows | **builtin**.Func[Windows]
- [ ]  WindowsInputTypes | **builtin**.type
    
Example/Sample Verified IsWorking List:

- [ ] `Assembly-Constraints.py`
- [ ] `Bolt-Creator.py`
- [ ] `Calculating-Length-of-Curves.py`
- [ ] `Cap-Screw-ISO-4762-Bolts.py`
- [ ] `Copy-sketch.py`
- [ ] `Create-Reference-Planes-Axes-and-Points.py`
- [ ] `Create-and-Modify-Global-Parameters.py`
- [ ] `Creating-a-3D-Sketch-with-a-Spline-and-an-Arc.py`
- [ ] `Creating-a-Cylinder-Between-Two-Points.py`
- [ ] `Creating-and-Manipulating-Assemblies.py`
- [ ] `Custom-Values-and-Settings-Window.py`
- [ ] `Default-Reference-Geometry.py`
- [ ] `Drop-Down-Lists.py`
- [ ] `Everyone-Loves-a-Slinky.py`
- [ ] `Gear-Example.py`
- [ ] `Geodesic-Dome-Reference-Geometry.py`
- [ ] `Getting-User-Input.py`
- [ ] `Helical-spring.py`
- [ ] `Import-points-from-a-CSV-file-rotate-them-and-connect-into-a-polyline.py`
- [ ] `Importing-Files.py`
- [ ] `Joint-Creator.py`
- [ ] `List-All-Parts-in-an-Assembly-and-Sub-Assemblies.py`
- [ ] `Lofting-with-a-Guide-Curve.py`
- [ ] `Midplane-Extrusion.py`
- [ ] `Mobius-Strip.py`
- [ ] `Modify-an-Existing-Part.py`
- [ ] `Parameters-with-Units.py`
- [ ] `Pocket-Hole-Creator.py`
- [ ] `Polygon-Incircle.py`
- [ ] `Profile-and-Sweep-Path.py`
- [ ] `Reading-from-a-Spreadsheet.py`
- [ ] `Rectangular-hollow-formed-profiles.py`
- [ ] `Reference-Geometry.py`
- [ ] `Scaling-a-Sketch.py`
- [ ] `Servo-Cam.py`
- [ ] `Slice-a-Part.py`
- [ ] `Square-hollow-formed-profiles.py`
- [ ] `Supressing-Unsupressing-and-Removing-Features.py`
- [ ] `Tool-Cutting.py`
- [ ] `Triangle.py`
- [ ] `Type-11-flanges-according-to-BS-EN-1092-PN16.py`
- [ ] `Units.py`
- [ ] `Useful-Dialogs.py`
- [ ] `Wave-washer.py`
- [ ] `Working-with-Configurations.py`

- [ ] **Import and Export**
  - [ ] `MaxCellSize.jpg`
  - [ ] `NormalDeviation.jpg`
  - [ ] `Part Exporter.py`
  - [ ] `STL Exporter.py`
  - [ ] `SurfaceDeviation.jpg`
- [ ] **Mathematical**
  - [ ] `Equation Sketcher.py`
  - [ ] `EquationSketcher.png`
- [ ] **Mechanical**
  - [ ] `Gear Generator.py`
  - [ ] `GearGenerator.png`
- [ ] **Utilities**
  - [ ] `File Copier.py`
  - [ ] `Image to Python.py`
  - [ ] `Pattern Along.py`
  - [ ] `PatternAlong.png`
  - [ ] `Sketch Copier.py`
  - [ ] `SketchCopier.png`
- [ ] **Woodworking**
  - [ ] `Joint Creator.py`
  - [ ] `JointCreatorIcon.png`
  - [ ] `Pocket Hole Creator.py`
  - [ ] `PocketHoleCreatorIcon.png`

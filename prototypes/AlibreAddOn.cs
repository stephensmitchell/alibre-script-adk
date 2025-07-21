using AlibreAddOn;
using AlibreX;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows;
using IStream = System.Runtime.InteropServices.ComTypes.IStream;
using MessageBox = System.Windows.MessageBox;

namespace AlibreAddOnAssembly
{
    public static class AlibreAddOn
    {
        private static IADRoot AlibreRoot { get; set; }
        private static AddOnRibbon TheAddOnInterface { get; set; }
        private static ScriptRunner PythonRunner { get; set; }

        public static void AddOnLoad(IntPtr hwnd, IAutomationHook pAutomationHook, IntPtr unused)
        {
            AlibreRoot = (IADRoot)pAutomationHook.Root;
            PythonRunner = new ScriptRunner(AlibreRoot);
            TheAddOnInterface = new AddOnRibbon(AlibreRoot);
        }

        public static void AddOnUnload(IntPtr hwnd, bool forceUnload, ref bool cancel, int reserved1, int reserved2)
        {
            TheAddOnInterface = null;
            PythonRunner = null;
            AlibreRoot = null;
        }

        public static void AddOnInvoke(IntPtr pAutomationHook, string sessionName, bool isLicensed, int reserved1, int reserved2) { }
        public static IAlibreAddOn GetAddOnInterface() => TheAddOnInterface;
        public static ScriptRunner GetScriptRunner() => PythonRunner;
    }

    public class AddOnRibbon : IAlibreAddOn
    {
        private readonly MenuManager _menuManager;
        private readonly IADRoot _alibreRoot;

        public AddOnRibbon(IADRoot alibreRoot)
        {
            _alibreRoot = alibreRoot;
            _menuManager = new MenuManager();
        }

        public int RootMenuItem => _menuManager.GetRootMenuItem().Id;
        public bool HasSubMenus(int menuID) => _menuManager.GetMenuItemById(menuID)?.SubItems.Count > 0;
        public Array SubMenuItems(int menuID) => _menuManager.GetMenuItemById(menuID)?.SubItems.Select(subItem => subItem.Id).ToArray();
        public string MenuItemText(int menuID) => _menuManager.GetMenuItemById(menuID)?.Text;
        public string MenuItemToolTip(int menuID) => _menuManager.GetMenuItemById(menuID)?.ToolTip;
        public string MenuIcon(int menuID) => _menuManager.GetMenuItemById(menuID)?.Icon;
        public IAlibreAddOnCommand InvokeCommand(int menuID, string sessionIdentifier)
        {
            var session = _alibreRoot.Sessions.Item(sessionIdentifier);
            var menuItem = _menuManager.GetMenuItemById(menuID);
            return menuItem?.Command?.Invoke(session);
        }

        public ADDONMenuStates MenuItemState(int menuID, string sessionIdentifier) => ADDONMenuStates.ADDON_MENU_ENABLED;
        public bool PopupMenu(int menuID) => false;
        public bool HasPersistentDataToSave(string sessionIdentifier) => false;
        public void SaveData(IStream pCustomData, string sessionIdentifier) { }
        public void LoadData(IStream pCustomData, string sessionIdentifier) { }
        public bool UseDedicatedRibbonTab() => false;
        void IAlibreAddOn.setIsAddOnLicensed(bool isLicensed) { }

        public void LoadData(global::AlibreAddOn.IStream pCustomData, string sessionIdentifier)
        {
            throw new NotImplementedException();
        }

        public void SaveData(global::AlibreAddOn.IStream pCustomData, string sessionIdentifier)
        {
            throw new NotImplementedException();
        }
    }

    public class MenuItem
    {
        public int Id { get; set; }
        public string Text { get; set; }
        public string ToolTip { get; set; }
        public string Icon { get; set; }
        public Func<IADSession, IAlibreAddOnCommand> Command { get; set; }
        public List<MenuItem> SubItems { get; set; } = new List<MenuItem>();

        public MenuItem(int id, string text, string toolTip = "", string icon = null)
        {
            Id = id;
            Text = text;
            ToolTip = toolTip;
            Icon = icon;
        }

        public void AddSubItem(MenuItem subItem) => SubItems.Add(subItem);

        public IAlibreAddOnCommand AboutCmd(IADSession session)
        {
            MessageBox.Show("Alibre Scripting Add-on");
            return null;
        }
    }

    public class MenuManager
    {
        private readonly MenuItem _rootMenuItem;
        private readonly Dictionary<int, MenuItem> _menuItems = new Dictionary<int, MenuItem>();

        public MenuManager()
        {
            _rootMenuItem = new MenuItem(401, "Examples", "Dynamically Loaded Example Scripts");
            BuildMenus();
            RegisterMenuItem(_rootMenuItem);
        }

        private void BuildMenus()
        {
            var aboutItem = new MenuItem(9090, "About", "About this Add-on");
            aboutItem.Command = aboutItem.AboutCmd;
            _rootMenuItem.AddSubItem(aboutItem);

            try
            {
                string addOnDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                string examplesPath = Path.Combine(addOnDirectory, "Examples");
                string iconsPath = Path.Combine(addOnDirectory, "Icons");

                if (Directory.Exists(examplesPath))
                {
                    string defaultIconPath = null;
                    if (File.Exists(Path.Combine(examplesPath, "logo.png")))
                        defaultIconPath = Path.Combine("Examples", "logo.png");
                    else if (File.Exists(Path.Combine(examplesPath, "logo.ico")))
                        defaultIconPath = Path.Combine("Examples", "logo.ico");
                    int currentMenuId = 10000;
                    string[] imageExtensions = { ".png", ".ico", ".bmp" };
                    var scriptFiles = Directory.GetFiles(examplesPath, "*.py");

                    foreach (var scriptFile in scriptFiles)
                    {
                        string fileName = Path.GetFileName(scriptFile);
                        if (fileName.Equals("alibre_setup.py", StringComparison.OrdinalIgnoreCase)) continue;

                        string baseName = Path.GetFileNameWithoutExtension(fileName);
                        string menuText = baseName.Replace("-", " ").Replace("_", " ");
                        var scriptMenuItem = new MenuItem(currentMenuId++, menuText, $"Run {fileName}");

                        string specificIconPath = null;
                        foreach (var ext in imageExtensions)
                        {
                            string iconFile = Path.Combine(iconsPath, baseName + ext);
                            if (File.Exists(iconFile))
                            {
                                specificIconPath = Path.Combine("Icons", baseName + ext);
                                break;
                            }
                        }
                        scriptMenuItem.Icon = specificIconPath ?? defaultIconPath;

                        scriptMenuItem.Command = (session) =>
                        {
                            AlibreAddOn.GetScriptRunner()?.ExecuteScript(session, fileName);
                            return null;
                        };

                        _rootMenuItem.AddSubItem(scriptMenuItem);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to load scripts dynamically: {ex.Message}", "Add-on Error");
            }
        }

        private void RegisterMenuItem(MenuItem menuItem)
        {
            _menuItems[menuItem.Id] = menuItem;
            foreach (var subItem in menuItem.SubItems)
                RegisterMenuItem(subItem);
        }
        public MenuItem GetMenuItemById(int id) => _menuItems.TryGetValue(id, out var menuItem) ? menuItem : null;
        public MenuItem GetRootMenuItem() => _rootMenuItem;
    }
    public class ScriptRunner
    {
        private readonly ScriptEngine _engine;
        private readonly IADRoot _alibreRoot;

        public ScriptRunner(IADRoot alibreRoot)
        {
            _alibreRoot = alibreRoot;
            _engine = Python.CreateEngine();
            string alibreInstallPath = "C:\\Program Files\\Alibre Design 28.1.0.28223";
            var searchPaths = _engine.GetSearchPaths();
            searchPaths.Add(Path.Combine(alibreInstallPath, "Program"));
            searchPaths.Add(Path.Combine(alibreInstallPath, "Program", "Addons", "AlibreScript", "PythonLib"));
            searchPaths.Add(Path.Combine(alibreInstallPath, "Program", "Addons", "AlibreScript"));
            _engine.SetSearchPaths(searchPaths);
        }

        public void ExecuteScript(IADSession session, string mainScriptFileName)
        {
            try
            {
                string addOnDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                string examplesPath = Path.Combine(addOnDirectory, "Examples");
                string setupScriptPath = Path.Combine(examplesPath, "alibre_setup.py");
                string mainScriptPath = Path.Combine(examplesPath, mainScriptFileName);
                if (!File.Exists(setupScriptPath) || !File.Exists(mainScriptPath))
                {
                    MessageBox.Show($"Error: Script not found.\nSetup: {setupScriptPath}\nMain: {mainScriptPath}", "Script Error");
                    return;
                }
                ScriptScope scope = _engine.CreateScope();
                scope.SetVariable("ScriptFileName", mainScriptFileName);
                scope.SetVariable("ScriptFolder", examplesPath);
                scope.SetVariable("SessionIdentifier", session.Identifier);
                scope.SetVariable("Arguments", new List<string>());
                scope.SetVariable("AlibreRoot", _alibreRoot);
                scope.SetVariable("CurrentSession", session);
                _engine.ExecuteFile(setupScriptPath, scope);
                _engine.ExecuteFile(mainScriptPath, scope);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred while running the script:\n{ex}", "Python Execution Error");
            }
        }
    }
}
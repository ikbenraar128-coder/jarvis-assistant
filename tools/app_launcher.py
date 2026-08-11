"""
Application launcher and manager
"""
import subprocess
import os
import psutil
import time
from pathlib import Path
from typing import Dict, List, Optional
import glob


class AppLauncher:
    """Launch and manage applications"""
    
    # Common Windows applications
    COMMON_APPS = {
        "chrome": {
            "names": ["chrome", "google chrome"],
            "paths": [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ],
            "process_name": "chrome.exe"
        },
        "firefox": {
            "names": ["firefox"],
            "paths": [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ],
            "process_name": "firefox.exe"
        },
        "discord": {
            "names": ["discord"],
            "paths": [
                r"C:\Users\{username}\AppData\Local\Discord\app-*\Discord.exe",
            ],
            "process_name": "Discord.exe"
        },
        "notepad": {
            "names": ["notepad"],
            "paths": [r"C:\Windows\System32\notepad.exe"],
            "process_name": "notepad.exe"
        },
        "calculator": {
            "names": ["calculator", "calc"],
            "paths": [r"C:\Windows\System32\calc.exe"],
            "process_name": "calc.exe"
        },
        "explorer": {
            "names": ["explorer", "file explorer"],
            "paths": [r"C:\Windows\explorer.exe"],
            "process_name": "explorer.exe"
        },
        "vscode": {
            "names": ["vscode", "visual studio code", "vs code"],
            "paths": [
                r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            ],
            "process_name": "Code.exe"
        },
        "paint": {
            "names": ["paint"],
            "paths": [r"C:\Windows\System32\mspaint.exe"],
            "process_name": "mspaint.exe"
        },
    }
    
    def __init__(self):
        self.running_processes = {}
    
    def is_app_running(self, app_name: str) -> bool:
        """Check if application is already running"""
        app_name_lower = app_name.lower().strip()
        
        if app_name_lower in self.COMMON_APPS:
            process_name = self.COMMON_APPS[app_name_lower]["process_name"]
            try:
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() == process_name.lower():
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return False
    
    def find_app(self, app_name: str) -> Optional[str]:
        """
        Find application executable path
        
        Args:
            app_name: Name of application
        
        Returns:
            Path to executable or None
        """
        app_name_lower = app_name.lower().strip()
        username = os.getenv("USERNAME", "User")
        
        # Check if it's a known app
        if app_name_lower in self.COMMON_APPS:
            app_info = self.COMMON_APPS[app_name_lower]
            for path_template in app_info["paths"]:
                # Replace {username} placeholder
                path = path_template.format(username=username)
                
                # Handle glob patterns
                if "*" in path:
                    matches = glob.glob(path)
                    if matches:
                        return matches[0]
                elif Path(path).exists():
                    return path
        
        # Try to find in common locations
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"C:\Users\{username}\AppData\Local\Programs".format(username=username),
        ]
        
        for search_path in search_paths:
            try:
                for root, dirs, files in os.walk(search_path, topdown=True):
                    # Limit search depth
                    dirs[:] = dirs[:3]
                    
                    for file in files:
                        if app_name_lower in file.lower() and file.endswith('.exe'):
                            return os.path.join(root, file)
            except (PermissionError, OSError):
                continue
        
        return None
    
    def launch_app(self, app_name: str, args: List[str] = None, 
                  wait_for: int = 0) -> Dict:
        """
        Launch an application
        
        Args:
            app_name: Name of application
            args: Additional arguments
            wait_for: Wait time in seconds
        
        Returns:
            Result dictionary with success and details
        """
        try:
            # Check if already running
            if self.is_app_running(app_name):
                return {
                    "success": True,
                    "message": f"{app_name} is already running",
                    "action": "already_running"
                }
            
            # Find app path
            app_path = self.find_app(app_name)
            if not app_path:
                return {
                    "success": False,
                    "message": f"Could not find {app_name}",
                    "error": "app_not_found"
                }
            
            # Launch app
            cmd = [app_path] + (args or [])
            proc = subprocess.Popen(cmd)
            
            self.running_processes[app_name.lower()] = proc
            
            # Wait if specified
            if wait_for > 0:
                time.sleep(wait_for)
            
            return {
                "success": True,
                "message": f"{app_name} launched successfully",
                "pid": proc.pid,
                "app_name": app_name
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error launching {app_name}: {str(e)}",
                "error": str(e)
            }
    
    def close_app(self, app_name: str) -> Dict:
        """
        Close a running application
        
        Args:
            app_name: Name of application
        
        Returns:
            Result dictionary
        """
        try:
            if not self.is_app_running(app_name):
                return {
                    "success": True,
                    "message": f"{app_name} is not running",
                    "action": "not_running"
                }
            
            # Try to close via process
            app_name_lower = app_name.lower()
            if app_name_lower in self.COMMON_APPS:
                process_name = self.COMMON_APPS[app_name_lower]["process_name"]
                os.system(f"taskkill /IM {process_name} /F")
                
                # Wait a moment
                time.sleep(1)
                
                return {
                    "success": True,
                    "message": f"{app_name} closed successfully",
                    "app_name": app_name
                }
            
            return {
                "success": False,
                "message": f"Could not close {app_name}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error closing {app_name}: {str(e)}",
                "error": str(e)
            }
    
    def get_running_apps(self) -> List[str]:
        """Get list of running applications"""
        running = []
        for app_name, app_info in self.COMMON_APPS.items():
            if self.is_app_running(app_name):
                running.append(app_name)
        return running

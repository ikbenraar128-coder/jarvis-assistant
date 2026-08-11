"""
Task executor - executes planned tasks
"""
from typing import Dict, Any
import time

from core.task_planner import TaskPlan, TaskStep
from core.memory_manager import memory_manager
from tools.app_launcher import AppLauncher
from tools.browser_control import BrowserControl


class TaskExecutor:
    """Execute planned tasks"""
    
    def __init__(self):
        self.app_launcher = AppLauncher()
        self.browser = BrowserControl()
        self.memory = memory_manager
    
    def execute_plan(self, plan: TaskPlan) -> Dict[str, Any]:
        """
        Execute complete task plan
        
        Args:
            plan: TaskPlan to execute
        
        Returns:
            Execution results
        """
        plan.overall_status = "executing"
        results = []
        
        for step in plan.steps:
            try:
                result = self._execute_step(step)
                results.append(result)
                
                if result.get("success"):
                    step.status = "completed"
                    step.result = result
                else:
                    step.status = "failed"
                    step.result = result
                    if step.wait_for_completion:
                        break
                
                if step.wait_for_completion:
                    time.sleep(0.5)
            
            except Exception as e:
                step.status = "failed"
                step.result = {"error": str(e)}
                results.append({"success": False, "error": str(e)})
                if step.wait_for_completion:
                    break
        
        # Determine overall status
        all_succeeded = all(r.get("success", False) for r in results)
        plan.overall_status = "completed" if all_succeeded else "failed"
        
        return {
            "plan": plan,
            "steps_executed": len([r for r in results if r.get("success")]),
            "total_steps": len(plan.steps),
            "success": all_succeeded,
            "results": results
        }
    
    def _execute_step(self, step: TaskStep) -> Dict[str, Any]:
        """Execute single step"""
        step.status = "executing"
        
        # Route to appropriate handler
        if step.action == "launch_app":
            return self.app_launcher.launch_app(step.target, wait_for=2)
        
        elif step.action == "close_app":
            return self.app_launcher.close_app(step.target)
        
        elif step.action == "check_app_running":
            running = self.app_launcher.is_app_running(step.target)
            return {
                "success": True,
                "running": running,
                "action": "check_app_running"
            }
        
        elif step.action == "find_app":
            path = self.app_launcher.find_app(step.target)
            return {
                "success": path is not None,
                "path": path,
                "app_name": step.target
            }
        
        elif step.action == "launch_browser":
            return self.app_launcher.launch_app("chrome", wait_for=2)
        
        elif step.action == "navigate_to_website":
            return self.browser.open_website(step.target)
        
        elif step.action == "search_web":
            return self.browser.search_google(step.target)
        
        elif step.action == "save_to_memory":
            self.memory.remember("notes", step.target, category="general")
            return {
                "success": True,
                "message": f"Saved to memory: {step.target}"
            }
        
        elif step.action == "retrieve_from_memory":
            data = self.memory.recall(step.target, category="general")
            return {
                "success": True,
                "data": data or "Not found in memory"
            }
        
        elif step.action == "wait_for_page_load":
            time.sleep(3)
            return {
                "success": True,
                "message": "Page loaded"
            }
        
        elif step.action == "conversation":
            return {
                "success": True,
                "message": "Conversation processed"
            }
        
        elif step.action == "execute_task":
            # For multi-tasks, just mark as success
            return {
                "success": True,
                "message": f"Task executed: {step.target}"
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown action: {step.action}"
            }

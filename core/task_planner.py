"""
Task Planner for JARVIS
Breaks down complex tasks into executable steps
"""
from typing import List, Dict, Any
from enum import Enum

from core.ai_brain import IntentType, IntentResult


class TaskStep:
    """Individual task step"""
    
    def __init__(self, action: str, target: str = "", priority: int = 0, 
                 wait_for_completion: bool = True, metadata: Dict = None):
        self.action = action
        self.target = target
        self.priority = priority
        self.wait_for_completion = wait_for_completion
        self.metadata = metadata or {}
        self.status = "pending"
        self.result = None
    
    def __repr__(self):
        return f"TaskStep({self.action}, {self.target}, status={self.status})"
    
    def to_dict(self):
        return {
            "action": self.action,
            "target": self.target,
            "status": self.status,
            "priority": self.priority
        }


class TaskPlan:
    """Complete task plan with multiple steps"""
    
    def __init__(self, original_intent: str, steps: List[TaskStep] = None):
        self.original_intent = original_intent
        self.steps = steps or []
        self.current_step = 0
        self.overall_status = "planning"
    
    def add_step(self, step: TaskStep):
        """Add step to plan"""
        self.steps.append(step)
    
    def get_current_step(self) -> TaskStep:
        """Get current step"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def mark_step_completed(self):
        """Mark current step as completed and move to next"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step].status = "completed"
            self.current_step += 1
    
    def mark_step_failed(self, error: str):
        """Mark current step as failed"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step].status = "failed"
            self.steps[self.current_step].result = {"error": error}
    
    def __repr__(self):
        return f"TaskPlan({self.original_intent}, {len(self.steps)} steps)"


class TaskPlanner:
    """
    Plans complex tasks and breaks them into executable steps
    """
    
    def plan_task(self, intent: IntentResult) -> TaskPlan:
        """
        Create a task plan from detected intent
        
        Args:
            intent: Detected intent from AI brain
        
        Returns:
            TaskPlan with steps to execute
        """
        
        if intent.intent_type == IntentType.OPEN_APP:
            plan = TaskPlan(intent.original_text)
            target = intent.data.get("target", "")
            
            plan.add_step(TaskStep("check_app_running", target))
            plan.add_step(TaskStep("find_app", target))
            plan.add_step(TaskStep("launch_app", target, wait_for_completion=True))
            plan.add_step(TaskStep("verify_app_running", target))
            
            return plan
        
        elif intent.intent_type == IntentType.CLOSE_APP:
            plan = TaskPlan(intent.original_text)
            target = intent.data.get("target", "")
            
            plan.add_step(TaskStep("check_app_running", target))
            plan.add_step(TaskStep("close_app", target))
            
            return plan
        
        elif intent.intent_type == IntentType.OPEN_WEBSITE:
            plan = TaskPlan(intent.original_text)
            target = intent.data.get("target", "")
            
            plan.add_step(TaskStep("launch_browser", "default"))
            plan.add_step(TaskStep("navigate_to_website", target))
            plan.add_step(TaskStep("wait_for_page_load", target, wait_for_completion=True))
            
            return plan
        
        elif intent.intent_type == IntentType.SEARCH_WEB:
            plan = TaskPlan(intent.original_text)
            query = intent.data.get("target", "")
            
            plan.add_step(TaskStep("launch_browser", "default"))
            plan.add_step(TaskStep("search_web", query))
            plan.add_step(TaskStep("wait_for_results", query, wait_for_completion=True))
            
            return plan
        
        elif intent.intent_type == IntentType.REMEMBER:
            plan = TaskPlan(intent.original_text)
            content = intent.data.get("target", "")
            
            plan.add_step(TaskStep("save_to_memory", content))
            
            return plan
        
        elif intent.intent_type == IntentType.RECALL:
            plan = TaskPlan(intent.original_text)
            key = intent.data.get("target", "")
            
            plan.add_step(TaskStep("retrieve_from_memory", key))
            
            return plan
        
        elif intent.intent_type == IntentType.MULTIPLE:
            plan = TaskPlan(intent.original_text)
            tasks = intent.data.get("tasks", [])
            
            for task in tasks:
                plan.add_step(TaskStep("execute_task", task))
            
            return plan
        
        else:
            plan = TaskPlan(intent.original_text)
            plan.add_step(TaskStep("conversation", intent.data.get("message", "")))
            return plan

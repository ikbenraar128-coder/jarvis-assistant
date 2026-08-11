"""
Modern GUI for JARVIS
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from datetime import datetime

from core.ai_brain import AIBrain
from core.task_planner import TaskPlanner
from core.executor import TaskExecutor
from core.memory_manager import memory_manager


class JARVISInterface:
    """Modern JARVIS GUI Interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS - Personal AI Assistant")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0a0e27")
        
        # Initialize components
        self.ai_brain = AIBrain()
        self.task_planner = TaskPlanner()
        self.executor = TaskExecutor()
        
        # Setup styles
        self._setup_styles()
        
        # Build interface
        self._build_interface()
        
        # Store for threading
        self.is_processing = False
    
    def _setup_styles(self):
        """Setup modern dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        self.bg_dark = "#0a0e27"
        self.bg_darker = "#050810"
        self.accent_blue = "#00d4ff"
        self.accent_purple = "#7b2cbf"
        self.text_primary = "#ffffff"
        self.text_secondary = "#a0aec0"
        
        # Configure styles
        style.configure("Dark.TFrame", background=self.bg_dark)
        style.configure("Title.TLabel", background=self.bg_dark, 
                       foreground=self.text_primary, font=("Segoe UI", 16, "bold"))
        style.configure("Text.TLabel", background=self.bg_dark, 
                       foreground=self.text_secondary, font=("Segoe UI", 9))
    
    def _build_interface(self):
        """Build GUI components"""
        
        # Main container
        main_container = ttk.Frame(self.root, style="Dark.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Dark.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(header_frame, text="🤖 JARVIS", style="Title.TLabel")
        title.pack(side=tk.LEFT)
        
        subtitle = ttk.Label(header_frame, text="Personal AI Assistant", 
                            style="Text.TLabel")
        subtitle.pack(side=tk.LEFT, padx=(10, 0))
        
        # Chat display area
        chat_frame = ttk.Frame(main_container, style="Dark.TFrame")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrolled text for chat
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg=self.bg_darker,
            fg=self.text_primary,
            font=("Consolas", 10),
            relief=tk.FLAT,
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground=self.accent_blue, 
                                    font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground=self.accent_purple, 
                                     font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("system", foreground=self.text_secondary, 
                                     font=("Consolas", 9, "italic"))
        self.chat_display.tag_config("status", foreground=self.accent_blue)
        self.chat_display.tag_config("error", foreground="#ff6b6b")
        
        # Input area
        input_frame = ttk.Frame(main_container, style="Dark.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_field = tk.Text(
            input_frame,
            height=2,
            bg=self.bg_darker,
            fg=self.text_primary,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            borderwidth=1,
            insertbackground=self.accent_blue,
            wrap=tk.WORD
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_field.bind("<Control-Return>", self._on_send)
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="→",
            command=self._on_send,
            bg=self.accent_purple,
            fg=self.text_primary,
            font=("Segoe UI", 14, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground=self.accent_blue,
            activeforeground=self.text_primary,
            cursor="hand2"
        )
        send_btn.pack(side=tk.LEFT, padx=(10, 0), fill=tk.Y)
        
        # Status bar
        self.status_label = ttk.Label(
            main_container,
            text="Ready",
            style="Text.TLabel"
        )
        self.status_label.pack(fill=tk.X)
        
        # Welcome message
        self._add_message("JARVIS", "Hello! I'm JARVIS, your personal AI assistant. How can I help you today?")
    
    def _add_message(self, sender: str, message: str):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "JARVIS":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"JARVIS: ", "assistant")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] ", "system")
            self.chat_display.insert(tk.END, f"YOU: ", "user")
        
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _add_status(self, status: str, is_error: bool = False):
        """Add status message"""
        self.chat_display.config(state=tk.NORMAL)
        tag = "error" if is_error else "status"
        self.chat_display.insert(tk.END, f"→ {status}\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _on_send(self, event=None):
        """Handle send button click"""
        user_input = self.input_field.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Clear input
        self.input_field.delete("1.0", tk.END)
        
        # Add user message
        self._add_message("YOU", user_input)
        
        # Update status
        self.status_label.config(text="Processing...")
        
        # Process in thread to avoid blocking UI
        thread = threading.Thread(target=self._process_input, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _process_input(self, user_input: str):
        """Process user input in background thread"""
        try:
            self.is_processing = True
            
            # Detect intent
            intent = self.ai_brain.detect_intent(user_input)
            self._add_status(f"Intent: {intent.intent_type.value} ({int(intent.confidence*100)}%)")
            
            # Plan task
            plan = self.task_planner.plan_task(intent)
            self._add_status(f"Plan: {len(plan.steps)} steps")
            
            # Show steps
            for i, step in enumerate(plan.steps, 1):
                self._add_status(f"Step {i}: {step.action} → {step.target}")
            
            # Execute plan
            execution_result = self.executor.execute_plan(plan)
            
            # Generate response
            response = self.ai_brain.generate_response(intent, execution_result)
            
            # Add assistant response
            self._add_message("JARVIS", response)
            
            # Store in history
            memory_manager.add_to_history("user", user_input)
            memory_manager.add_to_history("assistant", response)
            
            self.status_label.config(text="Ready")
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self._add_message("JARVIS", error_msg)
            self._add_status(error_msg, is_error=True)
            self.status_label.config(text="Error occurred")
        
        finally:
            self.is_processing = False


def main():
    """Main entry point"""
    root = tk.Tk()
    app = JARVISInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()

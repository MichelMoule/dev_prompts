import tkinter as tk
from tkinter import ttk, scrolledtext
import os
from openai import OpenAI
from datetime import datetime

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI Chat Interface")
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize conversation history
        self.conversation_history = []
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # System prompt configuration
        self.system_frame = ttk.LabelFrame(self.main_container, text="System Prompt", padding="5")
        self.system_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.system_prompt = tk.Text(self.system_frame, height=3, width=50, wrap=tk.WORD)
        self.system_prompt.insert('1.0', "You are a helpful assistant.")
        self.system_prompt.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(self.main_container, wrap=tk.WORD, height=20, width=50)
        self.chat_display.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.chat_display.tag_configure('user', foreground='blue')
        self.chat_display.tag_configure('assistant', foreground='green')
        self.chat_display.tag_configure('timestamp', foreground='gray')
        
        # Message input
        self.input_frame = ttk.Frame(self.main_container)
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.message_input = tk.Text(self.input_frame, height=3, width=40, wrap=tk.WORD)
        self.message_input.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=5)
        
        # Model selection
        self.model_frame = ttk.Frame(self.main_container)
        self.model_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.model_frame, text="Model:").grid(row=0, column=0, padx=5)
        self.model_var = tk.StringVar(value="gpt-3.5-turbo")
        self.model_combobox = ttk.Combobox(self.model_frame, textvariable=self.model_var, 
                                          values=["gpt-3.5-turbo", "gpt-4"])
        self.model_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Bind Enter key to send message
        self.message_input.bind('<Control-Return>', lambda e: self.send_message())

    def add_message_to_display(self, role, content):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"{role}: ", role)
        self.chat_display.insert(tk.END, f"{content}\n\n")
        self.chat_display.see(tk.END)

    def send_message(self):
        user_message = self.message_input.get("1.0", tk.END).strip()
        if not user_message:
            return
        
        # Clear input field
        self.message_input.delete("1.0", tk.END)
        
        # Update conversation history
        if not self.conversation_history:
            # Add system message if this is the first message
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt.get("1.0", tk.END).strip()
            })
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Display user message
        self.add_message_to_display("user", user_message)
        
        try:
            # Send to OpenAI
            response = self.client.chat.completions.create(
                model=self.model_var.get(),
                messages=self.conversation_history
            )
            
            # Get assistant's response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Display assistant's response
            self.add_message_to_display("assistant", assistant_message)
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.add_message_to_display("system", error_message)

def main():
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()

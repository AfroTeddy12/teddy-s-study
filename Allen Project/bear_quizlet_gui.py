import tkinter as tk
from tkinter import ttk, messagebox
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk

# Load environment variables
load_dotenv('api')

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Initialize text-to-speech engine
engine = pyttsx3.init()

class BearQuizlet:
    def __init__(self, root):
        self.root = root
        self.root.title("Bear Quizlet")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFF5E6")  # Light beige background
        
        # Bear-themed colors
        self.colors = {
            "brown": "#8B4513",
            "light_brown": "#D2B48C",
            "beige": "#FFF5E6",
            "dark_brown": "#654321"
        }
        
        self.flashcards = []
        self.current_card = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors["beige"])
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🐻 Bear Quizlet 🐻",
            font=("Comic Sans MS", 24, "bold"),
            bg=self.colors["beige"],
            fg=self.colors["brown"]
        )
        title_label.pack(pady=20)
        
        # Topic entry
        topic_frame = tk.Frame(main_frame, bg=self.colors["beige"])
        topic_frame.pack(fill="x", pady=10)
        
        tk.Label(
            topic_frame,
            text="Enter Topic:",
            font=("Arial", 12),
            bg=self.colors["beige"],
            fg=self.colors["brown"]
        ).pack(side="left", padx=5)
        
        self.topic_entry = tk.Entry(
            topic_frame,
            font=("Arial", 12),
            bg="white",
            fg=self.colors["dark_brown"]
        )
        self.topic_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Generate button
        generate_btn = tk.Button(
            topic_frame,
            text="Generate Flashcards",
            command=self.generate_flashcards,
            bg=self.colors["light_brown"],
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=3
        )
        generate_btn.pack(side="left", padx=5)
        
        # Flashcard display
        self.card_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground=self.colors["brown"],
            highlightthickness=2
        )
        self.card_frame.pack(expand=True, fill="both", pady=20)
        
        self.question_label = tk.Label(
            self.card_frame,
            text="Question will appear here",
            font=("Arial", 16),
            bg="white",
            fg=self.colors["dark_brown"],
            wraplength=600
        )
        self.question_label.pack(pady=20)
        
        self.answer_label = tk.Label(
            self.card_frame,
            text="Answer will appear here",
            font=("Arial", 14),
            bg="white",
            fg=self.colors["brown"],
            wraplength=600
        )
        self.answer_label.pack(pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(main_frame, bg=self.colors["beige"])
        nav_frame.pack(fill="x", pady=10)
        
        self.prev_btn = tk.Button(
            nav_frame,
            text="← Previous",
            command=self.previous_card,
            bg=self.colors["light_brown"],
            fg="white",
            font=("Arial", 12),
            state="disabled"
        )
        self.prev_btn.pack(side="left", padx=5)
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Next →",
            command=self.next_card,
            bg=self.colors["light_brown"],
            fg="white",
            font=("Arial", 12),
            state="disabled"
        )
        self.next_btn.pack(side="right", padx=5)
        
        # Question input
        question_frame = tk.Frame(main_frame, bg=self.colors["beige"])
        question_frame.pack(fill="x", pady=10)
        
        tk.Label(
            question_frame,
            text="Ask a question:",
            font=("Arial", 12),
            bg=self.colors["beige"],
            fg=self.colors["brown"]
        ).pack(side="left", padx=5)
        
        self.question_entry = tk.Entry(
            question_frame,
            font=("Arial", 12),
            bg="white",
            fg=self.colors["dark_brown"]
        )
        self.question_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ask_btn = tk.Button(
            question_frame,
            text="Ask",
            command=self.ask_question,
            bg=self.colors["light_brown"],
            fg="white",
            font=("Arial", 12)
        )
        ask_btn.pack(side="left", padx=5)
        
        # Read aloud button
        read_btn = tk.Button(
            main_frame,
            text="🔊 Read Aloud",
            command=self.read_current_card,
            bg=self.colors["light_brown"],
            fg="white",
            font=("Arial", 12)
        )
        read_btn.pack(pady=10)
        
    def generate_flashcards(self):
        topic = self.topic_entry.get()
        if not topic:
            messagebox.showerror("Error", "Please enter a topic")
            return
            
        prompt = f"""Create 5 flashcards about {topic}. 
        Format each card as 'Question: [question] Answer: [answer]'.
        Make the questions and answers clear and concise."""
        
        try:
            response = model.generate_content(prompt)
            cards_text = response.text
            
            self.flashcards = []
            cards = cards_text.split('\n\n')
            for card in cards:
                if 'Question:' in card and 'Answer:' in card:
                    question = card.split('Answer:')[0].replace('Question:', '').strip()
                    answer = card.split('Answer:')[1].strip()
                    self.flashcards.append({'question': question, 'answer': answer})
            
            if self.flashcards:
                self.current_card = 0
                self.update_card_display()
                self.prev_btn.config(state="normal")
                self.next_btn.config(state="normal")
                messagebox.showinfo("Success", "Flashcards generated successfully!")
            else:
                messagebox.showerror("Error", "Failed to generate flashcards")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate flashcards: {str(e)}")
    
    def update_card_display(self):
        if self.flashcards:
            card = self.flashcards[self.current_card]
            self.question_label.config(text=card['question'])
            self.answer_label.config(text=card['answer'])
    
    def next_card(self):
        if self.flashcards:
            self.current_card = (self.current_card + 1) % len(self.flashcards)
            self.update_card_display()
    
    def previous_card(self):
        if self.flashcards:
            self.current_card = (self.current_card - 1) % len(self.flashcards)
            self.update_card_display()
    
    def ask_question(self):
        if not self.flashcards:
            messagebox.showerror("Error", "No flashcards available")
            return
            
        question = self.question_entry.get()
        if not question:
            messagebox.showerror("Error", "Please enter a question")
            return
            
        current_card = self.flashcards[self.current_card]
        prompt = f"""Based on this flashcard:
        Question: {current_card['question']}
        Answer: {current_card['answer']}
        
        Answer this question: {question}"""
        
        try:
            response = model.generate_content(prompt)
            messagebox.showinfo("Answer", response.text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get answer: {str(e)}")
    
    def read_current_card(self):
        if self.flashcards:
            card = self.flashcards[self.current_card]
            text = f"Question: {card['question']}\nAnswer: {card['answer']}"
            engine.say(text)
            engine.runAndWait()
        else:
            messagebox.showerror("Error", "No flashcards available")

if __name__ == "__main__":
    root = tk.Tk()
    app = BearQuizlet(root)
    root.mainloop() 
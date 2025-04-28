import os
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv

# Load environment variables from 'api' file
load_dotenv('api')

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Initialize text-to-speech engine
engine = pyttsx3.init()

class FlashcardSystem:
    def __init__(self):
        self.flashcards = []
        self.current_card = 0

    def generate_flashcards(self, topic):
        """Generate flashcards for a given topic using Gemini AI"""
        prompt = f"""Create 5 flashcards about {topic}. 
        Format each card as 'Question: [question] Answer: [answer]'.
        Make the questions and answers clear and concise."""
        
        response = model.generate_content(prompt)
        cards_text = response.text
        
        # Parse the response into flashcards
        cards = cards_text.split('\n\n')
        for card in cards:
            if 'Question:' in card and 'Answer:' in card:
                question = card.split('Answer:')[0].replace('Question:', '').strip()
                answer = card.split('Answer:')[1].strip()
                self.flashcards.append({'question': question, 'answer': answer})

    def read_current_card(self):
        """Read the current flashcard using text-to-speech"""
        if self.flashcards:
            card = self.flashcards[self.current_card]
            text = f"Question: {card['question']}\nAnswer: {card['answer']}"
            engine.say(text)
            engine.runAndWait()

    def ask_question(self, question):
        """Ask a question about the current flashcard using Gemini AI"""
        if self.flashcards:
            current_card = self.flashcards[self.current_card]
            prompt = f"""Based on this flashcard:
            Question: {current_card['question']}
            Answer: {current_card['answer']}
            
            Answer this question: {question}"""
            
            response = model.generate_content(prompt)
            return response.text
        return "No flashcards available."

    def next_card(self):
        """Move to the next flashcard"""
        if self.flashcards:
            self.current_card = (self.current_card + 1) % len(self.flashcards)
            return True
        return False

    def previous_card(self):
        """Move to the previous flashcard"""
        if self.flashcards:
            self.current_card = (self.current_card - 1) % len(self.flashcards)
            return True
        return False

def main():
    system = FlashcardSystem()
    
    while True:
        print("\nFlashcard System Menu:")
        print("1. Generate new flashcards")
        print("2. Read current card")
        print("3. Ask a question about current card")
        print("4. Next card")
        print("5. Previous card")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            topic = input("Enter the topic for flashcards: ")
            system.generate_flashcards(topic)
            print("Flashcards generated successfully!")
            
        elif choice == '2':
            system.read_current_card()
            
        elif choice == '3':
            question = input("Enter your question: ")
            answer = system.ask_question(question)
            print(f"\nAnswer: {answer}")
            
        elif choice == '4':
            if system.next_card():
                print("Moved to next card")
            else:
                print("No flashcards available")
                
        elif choice == '5':
            if system.previous_card():
                print("Moved to previous card")
            else:
                print("No flashcards available")
                
        elif choice == '6':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 
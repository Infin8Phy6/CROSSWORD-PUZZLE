import random
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class CrosswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Generator")

        self.word_entry = tk.Entry(root)
        self.word_entry.pack()

        self.add_word_button = tk.Button(root, text="Add Word", command=self.add_word)
        self.add_word_button.pack()

        self.generate_button = tk.Button(root, text="Generate Crossword", command=self.generate_crossword)
        self.generate_button.pack()

        self.canvas_width, self.canvas_height = letter
        self.cell_size_x = self.canvas_width / 15  # Change to adjust cell size in PDF
        self.cell_size_y = self.canvas_height / 15

        self.words = []

    def add_word(self):
        word = self.word_entry.get()
        if word:
            self.words.append(word)
            self.word_entry.delete(0, tk.END)

    def place_word(self, grid, word, row, col, direction, reverse=False):
        if reverse:
            word = word[::-1]  # Reverse the word

        for i, letter in enumerate(word):
            if direction == "horizontal":
                grid[row][col + i] = letter
            elif direction == "vertical":
                grid[row + i][col] = letter

    def generate_crossword(self):
        grid_size = 15
        grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

        correct_words = []  # List to store correct words

        for word in self.words:
            direction = random.choice(["horizontal", "vertical"])
            reverse = random.choice([True, False])  # Randomly reverse the word
            row, col = 0, 0

            if direction == "horizontal":
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
            else:
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)

            self.place_word(grid, word, row, col, direction, reverse)
            correct_words.append(word)  # Add the word to the correct_words list

        # Fill unused grid cells with random letters
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == " ":
                    grid[i][j] = chr(random.randint(65, 90))  # Random uppercase letter

        pdf_filename = "crossword.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=(self.canvas_width, self.canvas_height))

        # Draw crossword grid on the first page
        for i in range(grid_size + 1):
            c.line(0, i * self.cell_size_y, self.canvas_width, i * self.cell_size_y)  # Horizontal lines

        for j in range(grid_size + 1):
            c.line(j * self.cell_size_x, 0, j * self.cell_size_x, self.canvas_height)  # Vertical lines

        # Place letters in grid cells
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                c.drawString(
                    j * self.cell_size_x + self.cell_size_x/2,
                    self.canvas_height - (i * self.cell_size_y + self.cell_size_y/2),
                    cell
                )
        c.showPage()  # Move to the second page
        # Draw "Name:" field and numbered words on the second page
        c.setFont("Helvetica", 12)
        c.drawString(50, self.canvas_height - 50, "Name:________________   Date:__________  Grade: ________ Level:____ Score:_____")
        y_position = self.canvas_height - 100
        c.drawString(50, y_position, "Numbered Words:")
        y_position -= 20
        for i, word in enumerate(correct_words, start=1):
            c.drawString(50, y_position, f"{i}. {word}")
            y_position -= 15
        c.save()
if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordGeneratorApp(root)
    root.mainloop()

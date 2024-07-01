import docx
import re

class AutoCorrect:
    def __init__(self, dictionary_file):
        self.dictionary = self.load_dictionary(dictionary_file)

    def load_dictionary(self, dictionary_file, encoding='utf-8'):
        with open(dictionary_file, 'r', encoding=encoding) as f:
            dictionary = set(word.strip().lower() for word in f)
        return dictionary

    def words(self, text):
        pass  # Your implementation of the words method goes here

        return re.findall(r'\w+', text.lower())

    def auto_correct_text(self, text):
        corrected_text = ''
        for word in self.words(text):
            if word not in self.dictionary:
                corrected_word = self.correct_word(word)
                corrected_text += corrected_word + ' '
            else:
                corrected_text += word + ' '
        return corrected_text.strip()

    def correct_word(self, word):
        # Basic auto-correct logic - Find the closest match from the dictionary
        # This can be improved with more sophisticated algorithms like Levenshtein Distance, etc.
        min_distance = float('inf')
        closest_word = word
        for dict_word in self.dictionary:
            distance = self.edit_distance(word, dict_word)
            if distance < min_distance:
                min_distance = distance
                closest_word = dict_word
        return closest_word

    def edit_distance(self, word1, word2):
        # Basic edit distance calculation
        if len(word1) > len(word2):
            word1, word2 = word2, word1
        distances = range(len(word1) + 1)
        for index2, char2 in enumerate(word2):
            new_distances = [index2 + 1]
            for index1, char1 in enumerate(word1):
                if char1 == char2:
                    new_distances.append(distances[index1])
                else:
                    new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
            distances = new_distances
        return distances[-1]

# Load text file with spelling mistakes
def load_text_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()


# Save corrected text to Word document
def save_to_word(corrected_text, output_file):
    doc = docx.Document()
    doc.add_paragraph(corrected_text)
    doc.save(output_file)

if __name__ == "__main__":
    dictionary_file = 'dictionary.txt'  # Your dictionary file containing a list of words
    input_file = 'input.txt'  # Your input text file with spelling mistakes
    output_file = 'output.docx'  # Output Word document with corrected text

    # Load text with spelling mistakes
    input_text = load_text_file(input_file)

    # Perform auto-correction
    auto_corrector = AutoCorrect(dictionary_file)
    corrected_text = auto_corrector.auto_correct_text(input_text)

    # Save corrected text to Word document
    save_to_word(corrected_text, output_file)

    print("Auto-correction completed. Corrected text saved to", output_file)

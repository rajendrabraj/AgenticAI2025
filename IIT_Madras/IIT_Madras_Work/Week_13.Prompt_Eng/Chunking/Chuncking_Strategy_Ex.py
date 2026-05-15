
##Main Program Chunking Strategies

import gradio as gr
import re
from typing import List, Dict
import nltk
from nltk.tokenize import word_tokenize
import spacy
from dataclasses import dataclass

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy for better sentence boundary detection
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

@dataclass
class ChunkResult:
    """Data class to store chunking results"""
    method: str
    chunks: List[str]
    metadata: Dict = None
    tokens_examples: List[List[str]] = None  # Added for token examples

class TextChunker:
    """Main class implementing various chunking strategies"""

    def __init__(self):
        self.nlp = nlp

    def fixed_size_chunking(self, text: str, chunk_size: int = 100, overlap: int = 0) -> ChunkResult:
        """Fixed-size chunking by word count"""
        words = text.split()
        chunks = []
        tokens_examples = []

        if overlap >= chunk_size:
            overlap = chunk_size // 4

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if chunk_words:
                chunk_text = ' '.join(chunk_words)
                chunks.append(chunk_text)
                # Tokenize a sample chunk for demonstration
                if len(tokens_examples) < 3:  # Store tokenization for first 3 chunks
                    tokens = word_tokenize(chunk_text)
                    tokens_examples.append(tokens)

        metadata = {
            "total_words": len(words),
            "chunk_size_words": chunk_size,
            "overlap_words": overlap,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Fixed-Size Chunking", chunks, metadata, tokens_examples)

    def sentence_based_chunking(self, text: str, sentences_per_chunk: int = 10) -> ChunkResult:
        """Chunk based on number of sentences"""
        # Use spaCy for better sentence segmentation
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]

        chunks = []
        tokens_examples = []

        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            if chunk_sentences:
                chunk_text = ' '.join(chunk_sentences)
                chunks.append(chunk_text)
                # Tokenize a sample chunk for demonstration
                if len(tokens_examples) < 3:  # Store tokenization for first 3 chunks
                    tokens = [t.text for t in self.nlp(chunk_text)]
                    tokens_examples.append(tokens)

        metadata = {
            "total_sentences": len(sentences),
            "sentences_per_chunk": sentences_per_chunk,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Sentence-Based Chunking", chunks, metadata, tokens_examples)

    def sliding_window_chunking(self, text: str, chunk_size: int = 100, overlap: int = 20) -> ChunkResult:
        """Sliding window chunking with overlap"""
        words = text.split()
        chunks = []
        tokens_examples = []

        if overlap >= chunk_size:
            overlap = chunk_size // 5

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if chunk_words:
                chunk_text = ' '.join(chunk_words)
                chunks.append(chunk_text)
                # Tokenize a sample chunk for demonstration
                if len(tokens_examples) < 3:  # Store tokenization for first 3 chunks
                    tokens = word_tokenize(chunk_text)
                    tokens_examples.append(tokens)

        metadata = {
            "total_words": len(words),
            "chunk_size_words": chunk_size,
            "overlap_words": overlap,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Sliding Window Chunking", chunks, metadata, tokens_examples)

    def paragraph_level_chunking(self, text: str) -> ChunkResult:
        """Chunk by paragraphs"""
        # Split by double newlines (common paragraph separation)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # If no double newlines, try single newlines
        if len(paragraphs) <= 1:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

        chunks = paragraphs
        tokens_examples = []

        # Tokenize first 3 paragraphs
        for i, chunk in enumerate(chunks[:3]):
            tokens = [t.text for t in self.nlp(chunk)]
            tokens_examples.append(tokens)

        metadata = {
            "total_paragraphs": len(paragraphs),
            "num_chunks": len(chunks)
        }
        return ChunkResult("Paragraph-Level Chunking", chunks, metadata, tokens_examples)

    def hierarchical_chunking(self, text: str, max_chunk_size: int = 200) -> ChunkResult:
        """Hierarchical chunking: sections -> paragraphs -> sentences"""
        chunks = []
        hierarchy = []
        tokens_examples = []

        # First level: Split by sections (assuming headings in ALL CAPS or numbered)
        sections = re.split(r'\n(?=[A-Z][A-Z\s]+\n|\d+\.\s|\n#)', text)

        for section_idx, section in enumerate(sections):
            if not section.strip():
                continue

            # Extract section title (first line if it looks like a heading)
            lines = section.strip().split('\n')
            section_title = lines[0] if len(lines[0].split()) < 10 else f"Section {section_idx + 1}"

            # Second level: Split into paragraphs
            paragraphs = [p.strip() for p in section.split('\n\n') if p.strip()]

            for para_idx, paragraph in enumerate(paragraphs):
                if len(paragraph.split()) <= max_chunk_size:
                    chunks.append(paragraph)
                    hierarchy.append({
                        "level": "paragraph",
                        "section": section_title,
                        "paragraph": para_idx + 1
                    })
                    # Store tokenization for first 3 chunks
                    if len(tokens_examples) < 3:
                        tokens = [t.text for t in self.nlp(paragraph)]
                        tokens_examples.append(tokens)
                else:
                    # Third level: Split into sentences
                    doc = self.nlp(paragraph)
                    sentences = [sent.text.strip() for sent in doc.sents]

                    # Group sentences to fit max_chunk_size
                    current_chunk = []
                    current_word_count = 0

                    for sent in sentences:
                        sent_words = len(sent.split())

                        if current_word_count + sent_words > max_chunk_size and current_chunk:
                            chunk_text = ' '.join(current_chunk)
                            chunks.append(chunk_text)
                            hierarchy.append({
                                "level": "sentence_group",
                                "section": section_title,
                                "paragraph": para_idx + 1
                            })
                            # Store tokenization for first 3 chunks
                            if len(tokens_examples) < 3:
                                tokens = [t.text for t in self.nlp(chunk_text)]
                                tokens_examples.append(tokens)

                            current_chunk = [sent]
                            current_word_count = sent_words
                        else:
                            current_chunk.append(sent)
                            current_word_count += sent_words

                    if current_chunk:
                        chunk_text = ' '.join(current_chunk)
                        chunks.append(chunk_text)
                        hierarchy.append({
                            "level": "sentence_group",
                            "section": section_title,
                            "paragraph": para_idx + 1
                        })
                        # Store tokenization for first 3 chunks
                        if len(tokens_examples) < 3 and len(chunks) <= 3:
                            tokens = [t.text for t in self.nlp(chunk_text)]
                            tokens_examples.append(tokens)

        metadata = {
            "max_chunk_size": max_chunk_size,
            "hierarchy_levels": 3,
            "hierarchy_info": hierarchy,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Hierarchical Chunking", chunks, metadata, tokens_examples)

    def recursive_text_splitter(self, text: str, chunk_size: int = 200, overlap: int = 50) -> ChunkResult:
        """Recursive text splitter that splits by sections then recursively"""

        def recursive_split(text_part, chunk_size, overlap, level=0):
            words = text_part.split()
            if len(words) <= chunk_size:
                return [text_part]

            # Try to split by paragraphs first
            paragraphs = text_part.split('\n\n')
            if len(paragraphs) > 1:
                chunks = []
                for para in paragraphs:
                    chunks.extend(recursive_split(para, chunk_size, overlap, level + 1))
                return chunks

            # If no paragraphs or still too large, split by sentences
            doc = self.nlp(text_part)
            sentences = [sent.text.strip() for sent in doc.sents]

            chunks = []
            current_chunk = []
            current_words = 0

            for sentence in sentences:
                sentence_words = len(sentence.split())

                if current_words + sentence_words > chunk_size and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # Keep overlap by retaining last few sentences
                    overlap_sentences = []
                    overlap_words = 0
                    for sent in reversed(current_chunk):
                        sent_words = len(sent.split())
                        if overlap_words + sent_words <= overlap:
                            overlap_sentences.insert(0, sent)
                            overlap_words += sent_words
                        else:
                            break
                    current_chunk = overlap_sentences + [sentence]
                    current_words = overlap_words + sentence_words
                else:
                    current_chunk.append(sentence)
                    current_words += sentence_words

            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks

        chunks = recursive_split(text, chunk_size, overlap)
        tokens_examples = []

        # Tokenize first 3 chunks
        for i, chunk in enumerate(chunks[:3]):
            tokens = [t.text for t in self.nlp(chunk)]
            tokens_examples.append(tokens)

        metadata = {
            "chunk_size_words": chunk_size,
            "overlap_words": overlap,
            "recursive_levels": "dynamic",
            "num_chunks": len(chunks)
        }
        return ChunkResult("Recursive Text Splitter", chunks, metadata, tokens_examples)

    def character_text_splitter(self, text: str, chunk_size: int = 100, overlap: int = 10) -> ChunkResult:
        """Split by character count"""
        chunks = []
        tokens_examples = []

        if overlap >= chunk_size:
            overlap = chunk_size // 10

        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk:
                chunks.append(chunk)
                # Tokenize a sample chunk for demonstration
                if len(tokens_examples) < 3:  # Store tokenization for first 3 chunks
                    tokens = [t.text for t in self.nlp(chunk)]
                    tokens_examples.append(tokens)

        metadata = {
            "total_characters": len(text),
            "chunk_size_chars": chunk_size,
            "overlap_chars": overlap,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Character Text Splitter", chunks, metadata, tokens_examples)

    def token_text_splitter(self, text: str, max_tokens: int = 100, overlap_tokens: int = 20) -> ChunkResult:
        """Split by token count (simple word-based tokenization)"""
        tokens = [t.text for t in self.nlp(text)]
        chunks_tokens = []

        if overlap_tokens >= max_tokens:
            overlap_tokens = max_tokens // 5

        for i in range(0, len(tokens), max_tokens - overlap_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            if chunk_tokens:
                chunks_tokens.append(chunk_tokens)

        # Convert tokens back to text
        chunks = [' '.join(chunk) for chunk in chunks_tokens]

        # For token text splitter, we already have the tokens
        tokens_examples = chunks_tokens[:3]  # First 3 chunks' tokens

        metadata = {
            "total_tokens": len(tokens),
            "max_tokens_per_chunk": max_tokens,
            "overlap_tokens": overlap_tokens,
            "num_chunks": len(chunks)
        }
        return ChunkResult("Token Text Splitter", chunks, metadata, tokens_examples)

def create_demo():
    """Create Gradio interface"""

    chunker = TextChunker()

    # Sample texts for examples
    sample_texts = {
        "Research Paper (AI in Healthcare)": """ARTIFICIAL INTELLIGENCE IN HEALTHCARE

INTRODUCTION

Artificial Intelligence (AI) is revolutionizing the healthcare industry by enabling faster, more accurate diagnoses and personalized treatment plans. The integration of AI technologies in medical practice has shown remarkable potential in improving patient outcomes and reducing healthcare costs.

AI technologies, including machine learning and deep learning algorithms, are being deployed across various medical domains. These systems can analyze complex medical data, identify patterns, and provide insights that would be difficult for human practitioners to discern.

APPLICATIONS IN DIAGNOSIS

Medical Imaging Analysis: AI algorithms can analyze medical images such as X-rays, MRIs, and CT scans with high accuracy. Recent studies show that AI systems can detect anomalies like tumors or fractures with sensitivity comparable to experienced radiologists.

Predictive Analytics: Machine learning models can predict disease progression and patient outcomes based on historical data. These predictions help in early intervention and personalized treatment planning.

CHALLENGES AND ETHICAL CONSIDERATIONS

Data Privacy: The use of patient data for AI training raises significant privacy concerns. Ensuring data anonymization and secure storage is paramount.

Algorithmic Bias: AI systems can inherit biases present in training data, potentially leading to unequal treatment across different demographic groups.

FUTURE DIRECTIONS

The future of AI in healthcare looks promising with advancements in explainable AI and federated learning. These technologies will address current limitations while expanding AI's capabilities in clinical settings.""",

        "News Article": """Technology Giant Announces Breakthrough in Quantum Computing

In a major scientific advancement, researchers have demonstrated a practical quantum computer capable of solving complex problems that were previously considered impossible for classical computers.

The new system, unveiled at the International Conference on Quantum Technology, uses 256 qubits to perform calculations that would take conventional supercomputers thousands of years to complete.

"This represents a watershed moment in computing history," said Dr. Sarah Chen, lead researcher on the project. "We're now entering an era where quantum advantage is becoming a practical reality, not just a theoretical possibility."

Industry analysts predict that quantum computing will revolutionize fields ranging from drug discovery to climate modeling, potentially creating trillions of dollars in economic value over the next decade.

However, experts also warn of challenges ahead, particularly regarding cybersecurity, as quantum computers could potentially break current encryption standards.""",

        "Short Example": "Artificial Intelligence (AI) is transforming healthcare by enabling faster diagnosis, personalized treatment, and predictive analytics. This technology helps doctors make better decisions and improves patient outcomes across various medical specialties."
    }

    def analyze_text(text, chunking_method, chunk_size, overlap, sentences_per_chunk):
        """Main function to apply chunking method"""
        if not text.strip():
            return "Please enter some text to analyze.", {}, "", "No text to analyze"

        # Apply the selected method
        if chunking_method == "Fixed-Size Chunking":
            result = chunker.fixed_size_chunking(text, chunk_size, 0)
        elif chunking_method == "Sentence-Based Chunking":
            result = chunker.sentence_based_chunking(text, sentences_per_chunk)
        elif chunking_method == "Sliding Window Chunking":
            result = chunker.sliding_window_chunking(text, chunk_size, overlap)
        elif chunking_method == "Paragraph-Level Chunking":
            result = chunker.paragraph_level_chunking(text)
        elif chunking_method == "Hierarchical Chunking":
            result = chunker.hierarchical_chunking(text, chunk_size)
        elif chunking_method == "Recursive Text Splitter":
            result = chunker.recursive_text_splitter(text, chunk_size, overlap)
        elif chunking_method == "Character Text Splitter":
            result = chunker.character_text_splitter(text, chunk_size, overlap)
        elif chunking_method == "Token Text Splitter":
            result = chunker.token_text_splitter(text, chunk_size, overlap)
        else:
            return "Method not implemented.", {}, "", ""

        # Prepare output
        stats = result.metadata or {}

        # Create formatted display for chunks
        chunks_display = ""
        for i, chunk in enumerate(result.chunks):
            words = len(chunk.split())
            chars = len(chunk)
            chunks_display += f"### Chunk {i+1} (Words: {words}, Chars: {chars})\n"
            chunks_display += f"{chunk[:500]}{'...' if len(chunk) > 500 else ''}\n\n"
            chunks_display += "---\n\n"

        # Create statistics summary
        stats_summary = f"""
## 📊 {result.method} - Statistics

**Total Chunks:** {len(result.chunks)}
**Total Words:** {len(text.split())}
**Total Characters:** {len(text)}
"""

        for key, value in stats.items():
            if key not in ['hierarchy_info']:
                stats_summary += f"**{key.replace('_', ' ').title()}:** {value}\n"

        # Create tokenization display
        tokenization_display = f"""
## 🔤 Tokenization Examples for {result.method}

*Showing tokenization for first {min(3, len(result.chunks))} chunks:*
"""

        if result.tokens_examples:
            for i, tokens in enumerate(result.tokens_examples):
                tokenization_display += f"\n### Chunk {i+1} - {len(tokens)} tokens:\n\n"

                # Create a formatted display of tokens
                tokens_per_line = 10
                for j in range(0, len(tokens), tokens_per_line):
                    line_tokens = tokens[j:j+tokens_per_line]
                    tokenization_display += "`" + "`, `".join(line_tokens) + "`  \n"

                tokenization_display += f"\n**Token Count:** {len(tokens)}\n"
                tokenization_display += f"**Sample Text:** {result.chunks[i][:100]}...\n"
                tokenization_display += "---\n"
        else:
            tokenization_display += "\n*No tokenization examples available for this method.*"

        # Add tokenization insights
        tokenization_display += f"""
## 🧠 Tokenization Insights

**Tokenizer Used:** spaCy English pipeline (en_core_web_sm)
**Special Features:**
- Splits contractions (e.g., "can't" → "ca", "n't")
- Handles punctuation as separate tokens
- Preserves whitespace tokens
- Recognizes named entities

**Common Token Types:**
- **Words:** "Artificial", "Intelligence", "healthcare"
- **Punctuation:** ",", ".", "(", ")"
- **Numbers:** "256", "2024"
- **Special Symbols:** "%", "$", "#"
"""

        return chunks_display, stats, stats_summary, tokenization_display

    # Custom CSS for better styling
    custom_css = """
    /* Input and method dropdown styling */
    .input-box textarea {
        background: #000000 !important;  /* Black background */
        border: 1px solid #444444 !important;  /* Dark gray border */
        border-radius: 8px !important;
        color: #ffffff !important;  /* White text */
    }

    .method-select .gr-dropdown__single {
        background: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
    }

    /* Consistent styling for all form elements */
    .gr-form {
        background: #f8f9fa !important;
    }

    /* Style the dropdown container */
    .gr-dropdown {
        background: #f8f9fa !important;
    }

    /* Style the dropdown options */
    .gr-dropdown__options {
        background: #f8f9fa !important;
    }

    /* Style the slider background */
    .gr-slider {
        background: #f8f9fa !important;
    }

    .chunk-box {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background: #f8f9fa;
    }

    .stats-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }

    .method-select {
        padding: 15px;
        border-radius: 8px;
    }

    .token-box {
        border: 1px solid #4CAF50;
        border-radius: 5px;
        padding: 8px;
        margin: 2px;
        background: #E8F5E9;
        display: inline-block;
        font-family: 'Courier New', monospace;
    }

    /* Style the accordion */
    .gr-accordion {
        background: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
    }

    /* Style the button */
    .gr-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
    }
    """

    # Create interface
    with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
        gr.Markdown("""
        # 📚 Chunking Methods
        ### Compare different text chunking strategies for NLP processing
        """)

        with gr.Row():
            with gr.Column(scale=2):
                # Text input
                text_input = gr.Textbox(
                    label="Input Text",
                    value=sample_texts["Research Paper (AI in Healthcare)"],
                    lines=10,
                    placeholder="Enter text to chunk...",
                    elem_classes="input-box"
                )

                # Sample selection
                sample_dropdown = gr.Dropdown(
                    choices=list(sample_texts.keys()),
                    value="Research Paper (AI in Healthcare)",
                    label="Load Sample Text"
                )

                # Method selection
                method_dropdown = gr.Dropdown(
                    choices=[
                        "Fixed-Size Chunking",
                        "Sentence-Based Chunking",
                        "Sliding Window Chunking",
                        "Paragraph-Level Chunking",
                        "Hierarchical Chunking",
                        "Recursive Text Splitter",
                        "Character Text Splitter",
                        "Token Text Splitter"
                    ],
                    value="Fixed-Size Chunking",
                    label="Chunking Method",
                    elem_classes="method-select"
                )

                # Parameters
                with gr.Accordion("⚙️ Advanced Parameters", open=False):
                    with gr.Row():
                        chunk_size = gr.Slider(
                            minimum=10,
                            maximum=500,
                            value=100,
                            step=10,
                            label="Chunk Size (words/tokens/chars)"
                        )
                        overlap = gr.Slider(
                            minimum=0,
                            maximum=100,
                            value=20,
                            step=5,
                            label="Overlap Size"
                        )
                        sentences_per_chunk = gr.Slider(
                            minimum=1,
                            maximum=50,
                            value=10,
                            step=1,
                            label="Sentences per Chunk"
                        )

                analyze_btn = gr.Button("🔍 Analyze & Chunk Text", variant="primary")

            with gr.Column(scale=3):
                # Output tabs
                with gr.Tabs():
                    with gr.TabItem("📄 Chunks Output"):
                        chunks_output = gr.Markdown(label="Generated Chunks")

                    with gr.TabItem("🔤 Tokenization"):
                        tokenization_output = gr.Markdown(label="Tokenization Examples")

                    with gr.TabItem("📊 Statistics"):
                        stats_output = gr.Markdown(label="Chunking Statistics")

                    with gr.TabItem("📈 Visual Summary"):
                        # JSON output for stats
                        json_output = gr.JSON(label="Detailed Statistics")

                # Method description
                method_desc = gr.Markdown("""
                ## Method Description

                **Fixed-Size Chunking**: Splits text into fixed-size chunks based on word count, regardless of content boundaries.

                **Best for**: Uniform processing, simple document splitting
                """)

        # Update method description based on selection
        def update_method_desc(method):
            descriptions = {
                "Fixed-Size Chunking": """
                ## Fixed-Size Chunking

                **How it works**: Splits text into chunks of exactly N words each, cutting at word boundaries.

                **Best for**:
                - Simple document splitting
                - Uniform processing pipelines
                - When sentence structure is not important

                **Example**: 1000-word document → 10 chunks of 100 words each
                """,

                "Sentence-Based Chunking": """
                ## Sentence-Based Chunking

                **How it works**: Groups N sentences together to form each chunk, preserving sentence boundaries.

                **Best for**:
                - Natural language understanding
                - Maintaining grammatical structure
                - When sentences need to remain intact

                **Example**: Every 10 sentences form one chunk
                """,

                "Sliding Window Chunking": """
                ## Sliding Window Chunking

                **How it works**: Creates overlapping chunks with specified window size and overlap.

                **Best for**:
                - Context preservation
                - NLP models requiring context overlap
                - Preventing information loss at chunk boundaries

                **Example**: 100-word chunks with 20-word overlap
                """,

                "Paragraph-Level Chunking": """
                ## Paragraph-Level Chunking

                **How it works**: Each paragraph becomes a separate chunk.

                **Best for**:
                - Well-structured documents
                - Maintaining logical flow
                - When paragraphs represent distinct ideas

                **Example**: Each paragraph treated as independent unit
                """,

                "Hierarchical Chunking": """
                ## Hierarchical Chunking

                **How it works**: Multi-level chunking: sections → paragraphs → sentences.

                **Best for**:
                - Complex, structured documents
                - Research papers and academic texts
                - When document structure matters

                **Example**: Research paper split by sections, then paragraphs, then sentences
                """,

                "Recursive Text Splitter": """
                ## Recursive Text Splitter

                **How it works**: Recursively splits text by different separators until chunks are small enough.

                **Best for**:
                - Mixed-content documents
                - Automatic optimal chunking
                - When document structure varies

                **Example**: Split by sections, then paragraphs, then sentences as needed
                """,

                "Character Text Splitter": """
                ## Character Text Splitter

                **How it works**: Splits text by character count, regardless of word boundaries.

                **Best for**:
                - Strict character limits
                - Token-limited models
                - When exact character counts matter

                **Example**: 50-character chunks with 10-character overlap
                """,

                "Token Text Splitter": """
                ## Token Text Splitter

                **How it works**: Splits text based on token count using spaCy tokenization.

                **Best for**:
                - LLM input preparation
                - Transformer models
                - When token count matters more than word count

                **Example**: 100-token chunks with 20-token overlap
                """
            }
            return descriptions.get(method, "Select a method to see description")

        # Connect events
        sample_dropdown.change(
            fn=lambda x: sample_texts[x],
            inputs=sample_dropdown,
            outputs=text_input
        )

        method_dropdown.change(
            fn=update_method_desc,
            inputs=method_dropdown,
            outputs=method_desc
        )

        analyze_btn.click(
            fn=analyze_text,
            inputs=[
                text_input,
                method_dropdown,
                chunk_size,
                overlap,
                sentences_per_chunk
            ],
            outputs=[chunks_output, json_output, stats_output, tokenization_output]
        )

        # Initialize
        method_dropdown.change(
            fn=update_method_desc,
            inputs=method_dropdown,
            outputs=method_desc
        )

    return demo

# Create and launch the demo
demo = create_demo()

if __name__ == "__main__":
    demo.launch(debug=True, server_name="0.0.0.0", server_port=7860)
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Strategie chunkowania dokumentów dla systemów RAG

Optymalne chunkowanie dokumentów jest **kluczowym czynnikiem** decydującym o skuteczności systemów Retrieval-Augmented Generation (RAG). Właściwy podział dokumentów na semantycznie spójne fragmenty zapewnia, że każdy chunk zawiera kompletną informację na konkretny temat bez zbędnego rozpraszania kontekstu[^1_1][^1_2].

## Główne strategie chunkowania

### **1. Fixed-size chunking (Chunking o stałym rozmiarze)**

Najprostsza metoda dzielenia tekstu na fragmenty o z góry określonym rozmiarze (zazwyczaj 256-512 tokenów)[^1_1][^1_2].

**Zalety:**

- Prosta implementacja i szybkie działanie
- Przewidywalny rozmiar chunków
- Niski koszt obliczeniowy

**Wady:**

- Może przerywać zdania lub akapity w połowie
- Ignoruje naturalną strukturę dokumentu
- Możliwa utrata kontekstu na granicach chunków

**Przypadki użycia:** Dokumenty jednorodne, szybkie prototypowanie, gdy struktura dokumentu nie jest istotna[^1_1][^1_3].

```python
def fixed_size_chunking(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Znajdź ostatnią spację, aby nie przerywać słów
        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space > chunk_size // 2:
                chunk = chunk[:last_space]
                end = start + last_space
        
        chunks.append(chunk.strip())
        start = end - overlap if overlap > 0 else end
    
    return chunks
```


### **2. Recursive character chunking**

Dzieli tekst hierarchicznie używając separatorów w określonej kolejności (akapity → zdania → słowa)[^1_3][^1_4]. LangChain's RecursiveCharacterTextSplitter jest najpopularniejszą implementacją tej metody.

**Zalety:**

- Zachowuje naturalne granice tekstu
- Konfigurowalne separatory
- Uniwersalne zastosowanie

**Wady:**

- Wymaga dostrojenia separatorów
- Może nie działać z wszystkimi formatami dokumentów

**Przypadki użycia:** Większość ogólnych zastosowań, dokumenty tekstowe[^1_5][^1_3].

```python
# Alternatywna implementacja bez LangChain
def custom_recursive_chunking(text, chunk_size=1000, overlap=200):
    separators = ["\n\n", "\n", ". ", " "]
    
    def split_by_separator(text, separator, size):
        if separator not in text or len(text) <= size:
            return [text]
        
        parts = text.split(separator)
        chunks = []
        current_chunk = ""
        
        for part in parts:
            if len(current_chunk + separator + part) <= size:
                current_chunk += separator + part if current_chunk else part
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = part
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    for separator in separators:
        chunks = split_by_separator(text, separator, chunk_size)
        if len(chunks) > 1:
            return chunks
    
    return [text]
```


### **3. Semantic chunking (Chunkowanie semantyczne)**

Najzaawansowana metoda grupująca zdania na podstawie podobieństwa semantycznego[^1_6][^1_3]. Wykorzystuje modele embedding do obliczania podobieństwa między zdaniami i ustala granice chunków tam, gdzie następuje zmiana tematyczna.

**Zalety:**

- Zachowuje spójność semantyczną
- Lepsze rezultaty wyszukiwania
- Chunki reprezentują kompletne tematy

**Wady:**

- Kosztowne obliczeniowo
- Wymaga modeli embedding
- Zmienny rozmiar chunków

**Przypadki użycia:** Dokumenty akademickie, raporty techniczne, złożone treści wymagające zachowania kontekstu semantycznego[^1_6][^1_7].

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk

def semantic_chunking(text, model_name='all-MiniLM-L6-v2', threshold=0.7):
    # Podziel na zdania
    sentences = nltk.sent_tokenize(text)
    
    if len(sentences) <= 1:
        return [text]
    
    # Wygeneruj embeddingi
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)
    
    # Oblicz podobieństwo między sąsiednimi zdaniami
    chunks = []
    current_chunk = [sentences[^1_0]]
    
    for i in range(1, len(sentences)):
        similarity = cosine_similarity(
            embeddings[i-1].reshape(1, -1), 
            embeddings[i].reshape(1, -1)
        )[^1_0][^1_0]
        
        if similarity >= threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```


### **4. Hierarchical chunking (Chunkowanie hierarchiczne)**

Zachowuje naturalną hierarchię dokumentu (nagłówki, sekcje, akapity), dzieląc tekst według struktury dokumentu[^1_8][^1_9]. Szczególnie skuteczne dla dokumentów z wyraźną organizacją.

**Zalety:**

- Zachowuje strukturę dokumentu
- Logiczne grupowanie treści
- Wykorzystuje metadane strukturalne

**Wady:**

- Wymaga dokumentów ze strukturą
- Zmienny rozmiar chunków

**Przypadki użycia:** PDF z nagłówkami, dokumenty wielopoziomowe, raporty strukturalne[^1_8][^1_9].

```python
import re

def hierarchical_chunking(text, max_chunk_size=1000):
    patterns = {
        'h1': r'^# (.+)$',
        'h2': r'^## (.+)$', 
        'h3': r'^### (.+)$'
    }
    
    lines = text.split('\n')
    chunks = []
    current_chunk = ""
    current_hierarchy = []
    
    for line in lines:
        line = line.strip()
        
        # Sprawdź czy to nagłówek
        header_match = None
        header_level = None
        
        for level, pattern in patterns.items():
            if level.startswith('h') and re.match(pattern, line):
                header_match = line
                header_level = int(level[^1_1])
                break
        
        if header_match:
            # Zakończ obecny chunk jeśli jest za duży
            if current_chunk and len(current_chunk) > max_chunk_size:
                chunks.append({
                    'content': current_chunk.strip(),
                    'hierarchy': current_hierarchy.copy(),
                    'type': 'content'
                })
                current_chunk = ""
            
            # Aktualizuj hierarchię
            current_hierarchy = current_hierarchy[:header_level-1]
            current_hierarchy.append(header_match)
            current_chunk += f"\n{line}\n"
        else:
            current_chunk += f"{line}\n"
            
            if len(current_chunk) > max_chunk_size:
                chunks.append({
                    'content': current_chunk.strip(),
                    'hierarchy': current_hierarchy.copy(),
                    'type': 'content'
                })
                current_chunk = ""
    
    if current_chunk.strip():
        chunks.append({
            'content': current_chunk.strip(),
            'hierarchy': current_hierarchy.copy(),
            'type': 'content'
        })
    
    return chunks
```


### **5. Sliding window chunking**

Tworzy nakładające się chunki o określonym przesunięciu, zapobiegając utracie kontekstu na granicach chunków[^1_10][^1_11]. Overlap zazwyczaj wynosi 10-30% rozmiaru chunka.

**Zalety:**

- Zapobiega utracie kontekstu na granicach
- Większa pewność wyszukiwania informacji
- Lepsze dla długich narracji

**Wady:**

- Zwiększa liczbę chunków
- Wyższe koszty przechowywania
- Możliwe duplikowanie informacji

**Przypadki użycia:** Długie narracje, dokumenty prawne, treści wymagające zachowania ciągłości kontekstu[^1_11][^1_12].

```python
def sliding_window_chunking(text, window_size=512, step_size=256):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), step_size):
        end_idx = min(i + window_size, len(words))
        chunk_words = words[i:end_idx]
        chunk = ' '.join(chunk_words)
        
        chunks.append({
            'content': chunk,
            'start_word': i,
            'end_word': end_idx,
            'overlap_with_previous': max(0, window_size - step_size) if i > 0 else 0
        })
        
        if end_idx >= len(words):
            break
    
    return chunks
```


### **6. Context-aware chunking**

Inteligentnie dostosowuje się do treści, uwzględniając kontekst przy określaniu granic chunków[^1_13][^1_14]. Analizuje semantykę i strukturę tekstu do optymalizacji podziału.

**Zalety:**

- Inteligentne dostosowanie do treści
- Zachowanie kontekstu semantycznego
- Adaptacyjny rozmiar chunków

**Wady:**

- Złożona implementacja
- Wyższy koszt obliczeniowy

**Przypadki użycia:** Różnorodne formaty dokumentów, gdy potrzebna jest maksymalna jakość chunkowania[^1_13][^1_15].

### **7. Agentic chunking**

Najnowsza metoda wykorzystująca LLM do inteligentnego określania granic chunków[^1_16][^1_17]. **Imituje ludzką ocenę** przy segmentacji tekstu, tworząc semantycznie spójne fragmenty.

**Zalety:**

- Najwyższa jakość semantyczna
- Imituje ludzkie rozumowanie
- Adaptacyjne dostosowanie

**Wady:**

- Bardzo kosztowne (wywołania LLM)
- Wolniejsze przetwarzanie
- Zależność od dostępności API

**Przypadki użycia:** Wymagania najwyższej jakości, kompleksowe dokumenty, gdy koszt nie jest głównym ograniczeniem[^1_17][^1_18].

```python
def simple_agentic_chunking(text, chunk_size=1000):
    # Identyfikuj propozycje (zdania stwierdzające)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    propositions = []
    
    for sentence in sentences:
        # Sprawdź czy zdanie zawiera istotną informację
        if (len(sentence.split()) > 5 and 
            not sentence.lower().startswith(('jednak', 'ale', 'ponadto')) and
            any(char.isalpha() for char in sentence)):
            propositions.append({
                'content': sentence,
                'type': 'proposition',
                'word_count': len(sentence.split())
            })
    
    # Grupuj propozycje w chunki
    chunks = []
    current_chunk = []
    current_size = 0
    
    for prop in propositions:
        prop_size = len(prop['content'])
        
        if current_size + prop_size <= chunk_size:
            current_chunk.append(prop)
            current_size += prop_size
        else:
            if current_chunk:
                chunks.append({
                    'content': ' '.join([p['content'] for p in current_chunk]),
                    'propositions': len(current_chunk),
                    'character_count': current_size
                })
            current_chunk = [prop]
            current_size = prop_size
    
    if current_chunk:
        chunks.append({
            'content': ' '.join([p['content'] for p in current_chunk]),
            'propositions': len(current_chunk),
            'character_count': current_size
        })
    
    return chunks
```


### **8. Document structure chunking**

Wykorzystuje naturalną organizację dokumentu (Markdown, HTML, XML) do określenia granic chunków[^1_19][^1_20]. Dzieli według elementów strukturalnych jak sekcje, akapity czy listy.

**Zalety:**

- Wykorzystuje naturalną strukturę
- Zachowuje formatowanie
- Efektywne dla dokumentów strukturalnych

**Wady:**

- Ograniczone do dokumentów z wyraźną strukturą
- Zmienny rozmiar chunków

**Przypadki użycia:** Markdown, HTML, dokumenty z wyraźną strukturą, dokumentacja techniczna[^1_21][^1_19].

## Optymalizacja rozmiaru chunków

Wybór odpowiedniego rozmiaru chunka ma **kluczowe znaczenie** dla skuteczności systemu RAG[^1_2][^1_22]:

### **Małe chunki (128-256 tokenów)**

- **Zalety:** Precyzyjne wyszukiwanie, mniej szumu, szybsze przetwarzanie
- **Wady:** Możliwa utrata kontekstu, więcej chunków do przechowania
- **Zastosowanie:** Zapytania faktograficzne, bazy FAQ[^1_2][^1_22]


### **Średnie chunki (256-512 tokenów)**

- **Zalety:** Optymalny balans kontekstu i precyzji, uniwersalne zastosowanie
- **Wady:** Kompromis między wszystkimi aspektami
- **Zastosowanie:** Większość przypadków użycia, rekomendowane jako punkt startowy[^1_2][^1_22]


### **Duże chunki (512-1024 tokenów)**

- **Zalety:** Zachowują szeroki kontekst, lepsze dla zadań analitycznych
- **Wady:** Mogą zawierać irrelewantne informacje, wolniejsze przetwarzanie
- **Zastosowanie:** Zadania wymagające szerokiego kontekstu, analizy dokumentów[^1_22][^1_23]


## Strategie overlap i najlepsze praktyki

### **Overlap chunków**

Nakładanie się chunków **zapobiega utracie ważnych informacji** na granicach[^1_11][^1_12]:

- **10-20% overlap:** Standardowe zastosowanie
- **20-30% overlap:** Dokumenty z silnymi powiązaniami
- **30-50% overlap:** Krytyczne informacje, dokumenty prawne


### **Implementacja hybrydowa**

Najlepsze rezultaty osiąga się **kombinując różne strategie**[^1_21][^1_24]:

1. **Preprocessing:** Document structure chunking
2. **Primary chunking:** Semantic lub Hierarchical
3. **Postprocessing:** Context-aware refinement
4. **Quality check:** Agentic validation (opcjonalnie)

### **Metadane i kontekst**

Każdy chunk powinien zawierać[^1_25][^1_21]:

- Pozycję w dokumencie
- Hierarchię (nagłówki nadrzędne)
- Typ chunka (nagłówek, treść, lista)
- Źródło dokumentu
- Metadane czasowe


### **Ewaluacja skuteczności**

Monitorowanie kluczowych metryk[^1_26][^1_27]:

- **Hit Rate:** Czy relevantne chunki są znajdowane
- **MRR (Mean Reciprocal Rank):** Pozycja pierwszego trafnego wyniku
- **Faithfulness:** Czy odpowiedzi są wierne źródłu
- **Answer Relevancy:** Czy odpowiedzi odpowiadają na pytanie


## Rekomendacje dla różnych typów dokumentów

### **Dokumenty techniczne/naukowe**

- **Strategia:** Hierarchical + Semantic chunking
- **Rozmiar:** 300-600 tokenów
- **Overlap:** 15-25%
- **Zachowaj:** Strukturę nagłówków, referencje, wzory


### **Dokumenty prawne**

- **Strategia:** Sliding window z dużym overlap
- **Rozmiar:** 400-800 tokenów
- **Overlap:** 30-40%
- **Zachowaj:** Kontekst paragrafów, numerację sekcji


### **FAQ/Bazy wiedzy**

- **Strategia:** Document structure chunking
- **Rozmiar:** 100-300 tokenów
- **Overlap:** 10-15%
- **Zachowaj:** Pary pytanie-odpowiedź jako całość


### **Treści kreatywne/narracyjne**

- **Strategia:** Semantic lub Agentic chunking
- **Rozmiar:** 200-500 tokenów
- **Overlap:** 20-30%
- **Zachowaj:** Ciągłość narracji, kontekst postaci

Właściwe chunkowanie to **fundament skutecznego systemu RAG**. Wybór strategii powinien uwzględniać typ dokumentów, wymagania aplikacji oraz dostępne zasoby obliczeniowe. Testowanie różnych podejść i iteracyjne dostrajanie parametrów jest kluczowe dla osiągnięcia optymalnych rezultatów[^1_28][^1_24].

<div style="text-align: center">⁂</div>

[^1_1]: https://www.sagacify.com/news/a-guide-to-chunking-strategies-for-retrieval-augmented-generation-rag

[^1_2]: https://milvus.io/ai-quick-reference/what-is-the-optimal-chunk-size-for-rag-applications

[^1_3]: https://www.pinecone.io/learn/chunking-strategies/

[^1_4]: https://milvus.io/ai-quick-reference/how-do-i-implement-efficient-document-chunking-for-rag-applications

[^1_5]: https://www.ibm.com/think/tutorials/chunking-strategies-for-rag-with-langchain-watsonx-ai

[^1_6]: https://superlinked.com/vectorhub/articles/semantic-chunking

[^1_7]: https://www.multimodal.dev/post/semantic-chunking-for-rag

[^1_8]: https://aws-samples.github.io/amazon-bedrock-samples/rag/open-source/chunking/rag_chunking_strategies_langchain_bedrock/

[^1_9]: https://milvus.io/ai-quick-reference/what-are-effective-chunking-strategies-for-multimodal-documents

[^1_10]: https://www.restack.io/p/text-chunking-answer-machine-learning-techniques-cat-ai

[^1_11]: https://www.reddit.com/r/LangChain/comments/1bjxvov/what_is_the_advantage_of_overlapping_in_chunking/

[^1_12]: https://www.linkedin.com/posts/ganeshjagadeesan_overlapping-chunking-activity-7271850035309346816-YtSp

[^1_13]: https://www.restack.io/p/context-awareness-knowledge-context-aware-chunking-cat-ai

[^1_14]: https://www.mindee.com/fr/blog/llm-chunking-strategies

[^1_15]: https://www.redhat.com/en/blog/rhel-13-docling-context-aware-chunking-what-you-need-know

[^1_16]: https://www.ibm.com/think/tutorials/use-agentic-chunking-to-optimize-llm-inputs-with-langchain-watsonx-ai

[^1_17]: https://alhena.ai/blog/agentic-chunking-enhancing-rag-answers-for-completeness-and-accuracy/

[^1_18]: https://nexla.com/nexla-open-source-agentic-chunking-technology-to-improve-ai-accuracy/

[^1_19]: https://infohub.delltechnologies.com/en-us/p/chunk-twice-retrieve-once-rag-chunking-strategies-optimized-for-different-content-types/

[^1_20]: https://milvus.io/ai-quick-reference/what-chunking-strategies-work-best-for-document-indexing

[^1_21]: https://infohub.delltechnologies.com/nl-nl/p/chunk-twice-retrieve-once-rag-chunking-strategies-optimized-for-different-content-types/

[^1_22]: https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5?gi=744ea357c68e

[^1_23]: https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5

[^1_24]: https://www.helicone.ai/blog/rag-chunking-strategies

[^1_25]: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase

[^1_26]: https://training.continuumlabs.ai/knowledge/retrieval-augmented-generation/mastering-chunking-in-retrieval-augmented-generation-rag-systems

[^1_27]: http://arxiv.org/pdf/2407.01219.pdf

[^1_28]: https://www.mattambrogi.com/posts/chunk-size-matters/

[^1_29]: https://github.com/jparkerweb/semantic-chunking

[^1_30]: https://stackoverflow.blog/2024/12/27/breaking-up-is-hard-to-do-chunking-in-rag-applications/

[^1_31]: https://www.youtube.com/watch?v=zKjSH2aj28U

[^1_32]: https://datasciencedojo.com/blog/rag-application-with-llamaindex/

[^1_33]: https://towardsdatascience.com/a-visual-exploration-of-semantic-text-chunking-6bb46f728e30/

[^1_34]: https://blog.gopenai.com/optimizing-rag-document-loading-beginners-guide-to-chunking-techniques-a6bb27783f44

[^1_35]: https://bitpeak.com/chunking-methods-in-rag-methods-comparison/

[^1_36]: https://forums.codeguru.com/showthread.php?503832-Variable-length-chunking-of-a-file-using-sliding-window-technique\&p=1973397

[^1_37]: https://bitpeak.com/chunking-methods-in-rag-overview-of-available-solutions/

[^1_38]: https://www.reddit.com/r/LangChain/comments/1dpbc4g/how_we_chunk_turning_pdfs_into_hierarchical/

[^1_39]: https://github.com/jchristn/SlidingWindow

[^1_40]: https://adasci.org/chunking-strategies-for-rag-in-generative-ai/

[^1_41]: https://arxiv.org/html/2409.04701v1

[^1_42]: https://www.npmjs.com/package/sliding-window

[^1_43]: https://www.restack.io/p/context-awareness-answer-context-aware-chunking-cat-ai

[^1_44]: https://github.com/gre/sliding-window

[^1_45]: https://www.youtube.com/watch?v=bTRbOR46gIE

[^1_46]: https://arxiv.org/html/2505.12731v1

[^1_47]: https://graphrag.com/guides/chunking/

[^1_48]: https://arxiv.org/html/2501.05485v1

[^1_49]: https://www.youtube.com/watch?v=12WBSiVlqkI

[^1_50]: https://www.linkedin.com/posts/ganeshjagadeesan_ai-rag-chunking-activity-7271850035309346816-1WHD

[^1_51]: https://github.com/rayhanfay/agentic-chunking

[^1_52]: https://learn.microsoft.com/sk-sk/azure/architecture/ai-ml/guide/rag/rag-chunking-phase

[^1_53]: https://docs.unstract.com/unstract/unstract_platform/user_guides/chunking/

[^1_54]: https://www.kdjingpai.com/en/knowledge/agentic-chunking/


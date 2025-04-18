import language_tool_python
from langdetect import detect, DetectorFactory
import re
import nltk

# Initialize with consistent settings
DetectorFactory.seed = 0

def is_english(text, min_confidence=0.6):
    """More reliable English detection"""
    try:
        if not text or len(text.strip().split()) < 3:
            return False
        return detect(text) == 'en'
    except:
        return False

def get_word_count(text):
    """Simple word count that doesn't rely on punkt"""
    return len(re.findall(r'\w+', text))

def get_grammar_score(text):
    """Simplified scoring that avoids punkt issues"""
    if not text or not isinstance(text, str):
        return 0, 0
    
    word_count = get_word_count(text)
    if word_count < 3:
        return 0, 0
    
    # Only check language if we have reasonable length
    if word_count >= 5 and not is_english(text):
        return 0, 0
    
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        
        if word_count == 0:
            return 100, 0
        
        # Balanced scoring formula
        error_ratio = min(len(matches) / word_count, 1.0)
        base_score = 100 * (1 - error_ratio)
        
        # Adjust for text length
        length_factor = min(1, word_count / 5)  # More lenient with short texts
        final_score = max(0, min(100, round(base_score * length_factor)))
        
        return final_score, len(matches)
    except Exception as e:
        print(f"Scoring error: {str(e)}")
        return 0, 0
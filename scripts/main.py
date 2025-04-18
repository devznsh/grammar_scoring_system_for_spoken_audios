import os
import pandas as pd
from transcribe import transcribe_audio
from grammar_check import get_grammar_score, get_word_count

AUDIO_DIR = "audio_samples/"
OUTPUT_DIR = "outputs/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_files():
    results = []
    processed_count = 0
    
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith((".wav", ".mp3")):
            try:
                # Transcribe
                audio_path = os.path.join(AUDIO_DIR, filename)
                text = transcribe_audio(audio_path)
                
                # Score grammar
                score, error_count = get_grammar_score(text)
                word_count = get_word_count(text)
                file_id = os.path.splitext(filename)[0]
                
                results.append({
                    'file_id': file_id,
                    'transcription': text[:200] + "..." if len(text) > 200 else text,
                    'grammar_score': score,
                    'error_count': error_count,
                    'word_count': word_count
                })
                
                processed_count += 1
                print(f"Processed {file_id}: Score={score} (Words={word_count}, Errors={error_count})")
                
            except Exception as e:
                print(f"Skipped {filename} due to error: {str(e)}")
                continue
    
    # Save results
    if results:
        df = pd.DataFrame(results)
        df['error_rate'] = df['error_count'] / df['word_count'].replace(0, 1)
        output_path = os.path.join(OUTPUT_DIR, "submission.csv")
        df.to_csv(output_path, index=False)
        
        print(f"\nSuccessfully processed {processed_count} files")
        print(f"Average score: {df['grammar_score'].mean():.1f}")
        print(f"Results saved to {os.path.abspath(output_path)}")
    else:
        print("\nNo files were processed successfully")

if __name__ == "__main__":
    process_files()
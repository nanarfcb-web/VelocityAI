import os
from TTS.api import TTS
from faster_whisper import WhisperModel
from transformers import pipeline
from pydub import AudioSegment, effects

# تهيئة المحركات
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
whisper = WhisperModel("tiny", device="cpu", compute_type="int8")
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

def process_video(task_id, input_path):
    audio = AudioSegment.from_wav(input_path)
    # تقطيع 15 ثانية
    chunks = [audio[i:i+15000] for i in range(0, len(audio), 15000)]
    processed = []
    
    for i, chunk in enumerate(chunks):
        c_name = f"c_{task_id}_{i}.wav"
        chunk.export(c_name, format="wav")
        segs, _ = whisper.transcribe(c_name, beam_size=1)
        text = " ".join([s.text for s in segs])
        
        if text:
            trans = translator(text, src_lang="eng_Latn", tgt_lang="arb_Arab")[0]['translation_text']
            out_c = f"out_{task_id}_{i}.wav"
            tts.tts_to_file(text=trans, speaker_wav=c_name, language="ar", file_path=out_c)
            processed.append(AudioSegment.from_wav(out_c))
            os.remove(out_c)
        os.remove(c_name)
    
    if processed:
        final = effects.normalize(sum(processed))
        final.export(f"final_{task_id}.wav", format="wav")
    os.remove(input_path)
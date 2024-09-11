import os
from dotenv import load_dotenv
import moviepy.editor as mp 
import speech_recognition as sr 
from pyannote.audio import Pipeline
import noisereduce as nr
import librosa
import soundfile as sf

class audioExtract:
    def __init__(self, audioFile) -> None:
        self.audioFile = self.loadVideo(audioFile)
        print("\nFilename:", self.audioFile, "\n")
        # Initialize recognizer 
        self.recognizer = sr.Recognizer()
   
    """Converts mp4 files to wav files if needed"""
    def loadVideo(self, audioFile:str) -> str:
        # checks if file is .wav type
        if audioFile.endswith(".wav"):
            return audioFile
        
        filename = os.path.splitext(str(audioFile))[0] + ".wav"

        # checks if .wav type already exists in directory
        if not os.path.exists(filename):
            # Load the video (ideally mp4)
            video = mp.VideoFileClip(audioFile) 
            
            # Extract the audio from the video and create .wav file
            audio = video.audio 
            
            audio.write_audiofile(filename) 

        return filename
        
    """Reduce background noise from audio"""
    def reduceNoise(self, outputAudio):
        print(f"Reducing Noise for {self.audioFile}")

        # Load the audio file
        y, sr = librosa.load(self.audioFile, sr=None)
        
        # Reduce noise using noisereduce
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        
        # Save the noise-reduced audio
        sf.write(outputAudio, reduced_noise, sr)
        self.audioFile = outputAudio


    """Converts wav file audio to text"""
    def convertToText(self) -> str:
        print("Converting Text")
        # Load the audio file 
        with sr.AudioFile(self.audioFile) as source: 
            data = self.recognizer.record(source) 
    
        # Convert speech to text 
        return self.recognizer.recognize_google(data)    

    def splitSpeakers(self):
        print("\nSplitting Speakers\n")
        # Initialize the pre-trained diarization pipeline
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HUGGINGFACE_TOKEN"))

        # Apply the pipeline on your audio file
        diarization = pipeline(self.audioFile)

        # Print the diarization result
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"Speaker {speaker} starts at {turn.start} and ends at {turn.end}")


if __name__ == "__main__":
    # loading variables from .env file
    load_dotenv() 

    # create class object
    extract = audioExtract("audio_files/Contestant Intros Many Speakers.mp4")
    # extract = audioExtract("audio_files/harvard.wav")

    # Reduce Noise 
    # extract.reduceNoise("audio_files/Contestant Intros Many Speakers_reduce.wav")
    # extract.reduceNoise("audio_files/harvard_reduce.wav")

    # Print the text 
    # text = extract.convertToText()
    # print("\nThe resultant text from video is:\n") 
    # print(text) 

    # Split Speakers
    extract.splitSpeakers()
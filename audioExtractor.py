import os
import moviepy.editor as mp 
import speech_recognition as sr 

class audioExtract:
    def __init__(self, audioFile) -> None:
        self.audioFile = self.loadVideo(audioFile)
        print("Filename:", self.audioFile)
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
        
    """Converts wav file audio to text"""
    def convertToText(self) -> str:
        # Load the audio file 
        with sr.AudioFile(self.audioFile) as source: 
            data = self.recognizer.record(source) 
    
        # Convert speech to text 
        return self.recognizer.recognize_google(data)     

if __name__ == "__main__":
    extract = audioExtract("audio_files/Contestant Intros Many Speakers.mp4")
    # extract = audioExtract("audio_files/harvard.wav")
    text = extract.convertToText()

    # Print the text 
    print("\nThe resultant text from video is:\n") 
    print(text) 
import pyaudio
import webrtcvad
import wave
import os
import datetime

class SpeechDetector:
    def __init__(self, audio_out_path, audio_device_index, chunk_size=480, format=pyaudio.paInt16, channels=1, rate=16000, silence_duration=1):
        self.audio_out_path = audio_out_path
        self.audio_device_index = audio_device_index
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.silence_duration = silence_duration

        self.p = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)  # Set VAD aggressiveness (0-3)

    def record_audio(self):
        stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk_size, input_device_index=self.audio_device_index)

        print("Waiting for speech...")

        frames = []
        silence_frames = 0
        speech_started = False

        while True:
            data = stream.read(self.chunk_size)

            if not speech_started:
                if self.vad.is_speech(data, self.rate):
                    speech_started = True
                    print("Recording started.")
                else:
                    continue

            frames.append(data)

            if self.vad.is_speech(data, self.rate):
                silence_frames = 0
            else:
                silence_frames += self.chunk_size

            if silence_frames >= self.rate * self.silence_duration:
                break

        print("Recording finished at ", datetime.datetime.now())

        wf = wave.open(self.audio_out_path, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(frames))
        wf.close()

        print(f"Audio saved as {self.audio_out_path}")

        stream.stop_stream()
        stream.close()

    def terminate(self):
        self.p.terminate()

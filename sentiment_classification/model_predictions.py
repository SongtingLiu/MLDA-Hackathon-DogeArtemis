import os
import torch
from torch.utils.data import Dataset, DataLoader
import torchaudio
from torch import nn
import torch.nn.functional as F
from torchsummary import summary

from . import ResidualBlock, ResNet34, VoiceDataset

def predict(model, input):
    with torch.no_grad():
        predictions = model(input)
        pred = predictions[0].argmax(0)
    
    return pred

# main prediction function
def return_predictions(model_path, audio_path, sample_rate=22050, num_samples=22050):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if device == "cuda":
        num_workers = 1
        pin_memory = True
    else:
        num_workers = 0
        pin_memory = False

    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=1024,
        hop_length=512,
        n_mels=64
    )

    dataset = VoiceDataset(audio_path, mel_spectrogram, sample_rate, num_samples)
    input_audio = dataset[0][0].unsqueeze(0).unsqueeze(0)
    model = torch.load(model_path).to(device)
    prediction = predict(model, input_audio)
    return prediction

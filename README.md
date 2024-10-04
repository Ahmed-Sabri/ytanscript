pip install yt-dlp openai-whisper torch

## Installing Torch as per https://pytorch.org/get-started/locally/
## The script will download Whisper Large by default for the first time you use the script, if you wish to use different Whisper Model, replace "large" with any of the available models [https://github.com/openai/whisper]

Available models and languages

There are six model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model. The relative speeds below are measured by transcribing English speech on a A100, and the real-world speed may vary significantly depending on many factors including the language, the speaking speed, and the available hardware.
Size 	Parameters 	English-only model 	Multilingual model 	Required VRAM 	Relative speed
tiny 	39 M 	tiny.en 	tiny 	~1 GB 	~10x
base 	74 M 	base.en 	base 	~1 GB 	~7x
small 	244 M 	small.en 	small 	~2 GB 	~4x
medium 	769 M 	medium.en 	medium 	~5 GB 	~2x
large 	1550 M 	N/A 	large 	~10 GB 	1x
turbo 	809 M 	N/A 	turbo 	~6 GB 	~8x

The .en models for English-only applications tend to perform better, especially for the tiny.en and base.en models. We observed that the difference becomes less significant for the small.en and medium.en models. Additionally, the turbo model is an optimized version of large-v3 that offers faster transcription speed with a minimal degradation in accuracy.

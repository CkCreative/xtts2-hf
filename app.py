import gradio as gr
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1")
tts.to("cuda")


def predict(prompt, language, audio_file_pth, mic_file_path, use_mic, agree):
    if agree == True:
        if use_mic == True:
            if mic_file_path is not None:
                speaker_wav=mic_file_path
            else:
                gr.Warning("Please record your voice with Microphone, or uncheck Use Microphone to use reference audios")
                return (
                    None,
                    None,
                ) 
                
        else:
            speaker_wav=audio_file_pth

        if len(prompt)<2:
            gr.Warning("Please give a longer prompt text")
            return (
                    None,
                    None,
                )
        try:   
            tts.tts_to_file(
                text=prompt,
                file_path="output.wav",
                speaker_wav=speaker_wav,
                language=language,
            )
        except RuntimeError:
            if "device-side" in e.message:
                # cannot do anything on cuda device side error, need tor estart
                gr.Warning("Unhandled Exception encounter, please retry in a minute")
                print("Cuda device-assert Runtime encountered need restart")
                sys.exit("Exit due to cuda device-assert")
            raise

        return (
            gr.make_waveform(
                audio="output.wav",
            ),
            "output.wav",
        )
    else:
        gr.Warning("Please accept the Terms & Condition!")
        return (
                None,
                None,
            ) 


title = "Coqui🐸 XTTS"

description = """
<a href="https://huggingface.co/coqui/XTTS-v1">XTTS</a> is a Voice generation model that lets you clone voices into different languages by using just a quick 3-second audio clip. 
<br/>
Built on Tortoise, XTTS has important model changes that make cross-language voice cloning and multi-lingual speech generation super easy. 
<br/>
This is the same model that powers Coqui Studio, and Coqui API, however we apply a few tricks to make it faster and support streaming inference.
<br/>
<br/>
<p>For faster inference without waiting in the queue, you should duplicate this space and upgrade to GPU via the settings.
<br/>
<a href="https://huggingface.co/spaces/coqui/xtts?duplicate=true">
<img style="margin-top: 0em; margin-bottom: 0em" src="https://bit.ly/3gLdBN6" alt="Duplicate Space"></a>
</p>
"""

article = """
<div style='margin:20px auto;'>
<p>By using this demo you agree to the terms of the Coqui Public Model License at https://coqui.ai/cpml</p>
</div>
"""

examples = [
    [
        "Once when I was six years old I saw a magnificent picture",
        "en",
        "examples/female.wav",
        None,
        False,
        True,
    ],
    [
        "Lorsque j'avais six ans j'ai vu, une fois, une magnifique image",
        "fr",
        "examples/male.wav",
        None,
        False,
        True,
    ],
    [
        "Un tempo lontano, quando avevo sei anni, vidi un magnifico disegno",
        "it",
        "examples/female.wav",
        None,
        False,
        True,
    ],
    [
        "Bir zamanlar, altı yaşındayken, muhteşem bir resim gördüm",
        "tr",
        "examples/female.wav",
        None,
        False,
        True,
    ],
]

gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(
            label="Text Prompt",
            info="One or two sentences at a time is better",
            value="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
        ),
        gr.Dropdown(
            label="Language",
            info="Select an output language for the synthesised speech",
            choices=[
                "en",
                "es",
                "fr",
                "de",
                "it",
                "pt",
                "pl",
                "tr",
                "ru",
                "nl",
                "cz",
                "ar",
                "zh-cn",
            ],
            max_choices=1,
            value="en",
        ),
        gr.Audio(
            label="Reference Audio",
            info="Click on the ✎ button to upload your own target speaker audio",
            type="filepath",
            value="examples/female.wav",
        ),
        gr.Audio(source="microphone",
                 type="filepath",
                 info="Use your microphone to record audio",
                 label="Use Microphone for Reference"),
        gr.Checkbox(label="Check to use Microphone as Reference", value=False),
        gr.Checkbox(
            label="Agree",
            value=False,
            info="I agree to the terms of the Coqui Public Model License at https://coqui.ai/cpml",
        ),
    ],
    outputs=[
        gr.Video(label="Waveform Visual"),
        gr.Audio(label="Synthesised Audio"),
    ],
    title=title,
    description=description,
    article=article,
    examples=examples,
).queue().launch(debug=True)

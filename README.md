# Coppermind Summaries To Audiobook & Ebook

The [Coppermind Wiki](https://coppermind.net/) does a chapter by chapter summary of each [Stormlight Archives](https://coppermind.net/wiki/The_Stormlight_Archive/Summary) book.

This is useful for those of us who want to catch up without rereading the entire series.

This repo scrapes the Wiki and creates audiobooks using Open AI's (paid) text-to-speech models. The quality isn't bad for computer-generated voices.

The Way of Kings chapter by chapter summary audiobook is ~2 hours long and each book gets a little longer.

If a summary chapter has a POV character, this script will attempt to assign a unique narrator voice to that chapter to change things up.

You can download the audiobook summaries from the [audiobooks](./audiobooks) directory.

If you'd like to put the summaries on a Kindle, you can download the ebook summaries from the [ebooks](./ebooks) directory.

## Recreating the audiobooks

There may be cases where you want to regenerate these summaries.

For instance:

- You can change the voices for each POV character in [src/config.py](./src/config.py)
- You might want to use only 1 narrator instead of the narrator switching for each POV character
- You might want to use another TTS service, like https://elevenlabs.io/

Here are the steps you can follow:

1. Copy [.env.example](./.env.example) to a new file named `.env.local` and set the values.

2. Download deps with `pipenv`

3. Adjust [src/config.py](./src/config.py) as needed.

4. Determine if you want to us OpenAI TTS (paid, higher quality) or the free local VITS models (free, lower quality)

5. Run one of the following to generate regenerate the audio and text files for all the books set in `config.py`
   - Run `pipenv run python src/main.py --method=api` to use paid OpenAI TTS
   - Run `pipenv run python src/main.py --method=local` to use free VITs TTS

6. Run `pipenv run python src/convert_to_audiobook.py --method=<your_method>` to combine the files into m4bs (audiobooks)
6. Run `pipenv run python src/convert_to_ebook.py` to combine the scraped text into epubs (ebooks)

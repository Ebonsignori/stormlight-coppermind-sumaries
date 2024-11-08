import argparse 

def get_cli_inputs():
    """Parse command line inputs for the script."""
    parser = argparse.ArgumentParser(description='Scrape text, convert it to audio, and combine them for any summary on the Coppermind wiki listed in config.py')
    parser.add_argument(
        '--method', 
        type=str, 
        default='local', 
        choices=['api', 'local'], 
        help='Method to use for text-to-speech: api or local. api requires OpenAI API key in OPENAI_API_KEY environment variable. local requires TTS libraries to be installed.'
    )
    args = parser.parse_args()
    return {
        'audio_method': args.method
    }

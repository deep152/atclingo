# ATCLingo

A tool that records real air traffic control radio from JFK, turns it into text, and explains each call in plain English for student pilots.

## Why I'm building this

I'm working toward my private pilot license, and ATC is really hard to follow by ear. More hours and a better headset help, but I'd also like to practice at home.

During an actual lesson, I'm trying to fly the plane and force that 70% outside, 30% inside scan instead of chasing needles. With so much going on, trying to understand ATC on top of it is a whole new challenge. Other students I've talked to say the same. If there's a week between lessons, getting back up to speed takes a good chunk of the hour. These skills don't get automatic for a while.

There are some great apps for this, like [ATC - Live Air Traffic Radio](https://apps.apple.com/us/app/atc-live-air-traffic-radio/id6755132266) on the App Store. They show transcripts of live ATC and have clean UIs, almost like Duolingo. But most of them are behind a paywall. The free stuff I found is either a radio-call practice sim or a self-hosted project that's hard to set up.

I think real audio matters. Real controllers talk fast, slur words, talk over static, and use casual phrasing that a sim can't copy. Listening to the real thing trains your ears for real voices, static, and accents.

So I'm building a free, simple version for people who are still learning. It's similar to my work on the [Punjabi learning dictionary](https://punjabiapp.com), a free tool for learning a language, and this one is for learning the language of ATC.

## Plan

1. **Setup.** I live about 10 miles from JFK and planes fly over my house all day, so I'm putting an RTL-SDR dongle and antenna in a window and using SDR++ to listen. First goal is just being able to hear JFK (tower, ground, approach, departure).
2. **Record clips.** Short JFK clips saved as WAV files, done by hand at first. A daily automatic recording can come later.
3. **Transcribe.** Run the clips through Whisper, a speech-to-text model from OpenAI. Regular Whisper does badly on ATC audio, so I'll try a fine-tuned ATC version from Hugging Face.
4. **Check and explain.** Hand-correct transcripts to measure how accurate it is. Then write a plain-English explanation for each call and check it against standard FAA phraseology.
5. **Display.** A simple web page that shows each clip with its transcript and explanation.

## Later

If it works well with recorded clips, I'd like to try live audio. That would cost more to run, since transcribing all day takes a lot of compute, so it comes after the basic version works.

## Hardware

- NooElec NESDR Smart v5 (RTL-SDR) bundle with antennas
- Laptop running SDR++

## Tools (might change)

- Python for recording, splitting, and transcribing
- Whisper (a fine-tuned ATC model)
- React for the web page

## Notes

- I'm using my own receiver instead of LiveATC streams, since their terms don't allow using their audio in other products.
- The dongle is receive-only. I'm not transmitting anything.
- Other open source ATC transcription projects exist (Readback, airband_listener, Co-ATC). I'm reading them for ideas. Mine is focused on explaining calls to learners.

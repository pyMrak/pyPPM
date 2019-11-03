# pyPPM
Simple python library to control RC transmitter via trainer port using sounddevice (computer's audio out).

Connect audio cable (mono or stereo - it does't matter) to computer's audio out and RC transmitter's trainer port and control the transmitter with your python program.

NOTE: Not all sound cards will have enough voltage output to be detected by the transmitter. In case it doesn't you should use a simple amplifier or a external sound card that is capable of outputting more than 3V. You also have to have trainer/master port enabled on the transmitter.

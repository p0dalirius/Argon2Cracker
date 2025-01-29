![](./.github/banner.png)

<p align="center">
    A multithreaded bruteforcer of argon2 hashes.
    <br>
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/Argon2Cracker">
    <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
    <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
    <br>
</p>

## Features

 - [x] Progress updated every second with the number of processed hashes per second.
 - [x] Multithreaded bruteforce.

## Usage

```
$ ./Argon2Cracker.py -h
Argon2Cracker - v1.0 - by Remi GASCOU (Podalirius)

usage: Argon2Cracker.py [-h] [-t THREADS] -w WORDLIST [-v] hash

argon2 hash cracker

positional arguments:
  hash                  argon2 hash

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        Number of threads (Default: 16)
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -v, --verbose         Verbose mode. (default: False)

```

## Example

```
./Argon2Cracker.py '$argon2id$v=19$m=102400,t=2,p=8$Xy3Iqq6AmzfugAV7Fo31dA$dAVH9zcRoKHvDDaAy3rdWg' -w ./example/wordlist.txt -v
```

![](./.github/example.png)

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.

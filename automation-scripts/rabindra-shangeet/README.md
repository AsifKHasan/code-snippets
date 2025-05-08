python3 youtube-audio.py -y "https://www.youtube.com/watch?v=9TDpf_j8-nc" -o "../out/youtube/"

python3 youtube-audio.py -y "https://youtu.be/8Xch2piLOfA" -o "../out/youtube/"


yt-dlp --extract-audio --audio-format mp3 --download-sections "*[6-]" https://www.youtube.com/watch?v=9TDpf_j8-nc -o "../out/youtube/9TDpf_j8-nc.mp3" --quiet

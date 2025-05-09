python3 youtube-audio.py -y "https://www.youtube.com/watch?v=9TDpf_j8-nc" -o "../out/youtube/"

python3 youtube-audio.py -y "https://youtu.be/8Xch2piLOfA" -o "../out/youtube/"


yt-dlp --extract-audio --audio-format mp3 --download-sections "*[6-]" https://www.youtube.com/watch?v=9TDpf_j8-nc -o "../out/youtube/9TDpf_j8-nc.mp3" --quiet

yt-dlp --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=9TDpf_j8-nc -o "../out/youtube/9TDpf_j8-nc.mp3" --quiet


python3 youtube-audio.py -y https://www.youtube.com/watch?v=_0hryUio7aI -o ../out/youtube/
ffmpeg -i ../out/youtube/_0hryUio7aI.m4a -ss 14 ../out/final/ভালোবেসে-যদি-সুখ-নাহি__চিন্ময়-চট্টোপাধ্যায়.m4a


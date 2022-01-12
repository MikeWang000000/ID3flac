ID3flac
=========
让 macOS Finder 显示 FLAC 文件专辑封面。  
Make macOS Finder able to display FLAC cover art.

## 简介 / Introduction
macOS High Sierra 新增了 FLAC 文件支持。然而，至今 (macOS Monterey) ，FLAC 的专辑封面依旧无法正常显示。  
macOS High Sierra added support to FLAC files. However, so far (macOS Monterey), FLAC cover arts cannot be displayed properly.

原因在于，Finder 总是尝试去读取音频的 ID3 标签。  
Reason for this is that Finder always tries to read the ID3 tag of the audio.

此工具用于将 FLAC 文件添加 ID3 标签，使得 Finder 能够显示专辑封面。  
This tool is designed to add ID3 tags to FLAC files, allowing Finder to display cover art properly.

## 使用方法 / Usage
```bash
pip3 install mutagen
```
```bash
python3 id3flac.py /path/to/music.flac
```

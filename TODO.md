# Phase A Migration TODO

- [x] Review target files and confirm remaining direct config parsing usage
- [ ] Migrate `2_pause-remover/2a_wav_pause_remover.py` to use `5_content_creator/config.py`
- [ ] Migrate `2_pause-remover/2b_mp4_pause_remover.py` to use `5_content_creator/config.py`
- [ ] Migrate `2_pause-remover/2c_mp4_pause_remover_v2.py` to use `5_content_creator/config.py`
- [ ] Migrate `2_pause-remover/2d_mp4_pause_remover_vad.py` to use `5_content_creator/config.py`
- [ ] Migrate `2_pause-remover/2f_time_cutter.py` to use `5_content_creator/config.py`
- [ ] Migrate `3_media-converters/3_wav2mp4.py` to use `5_content_creator/config.py`
- [ ] Validate imports and default path constants across Phase A files
- [ ] Run critical-path test for `5_content_creator/start1.sh`
- [ ] Summarize changes and testing status

#!/usr/bin/env python3
"""
668Hz Pure Tone Generator for Meditation Experiments
668理論に基づく瞑想音波生成システム

2025-09-04 by 翼
"""

import numpy as np
import wave
import struct
import os
from datetime import datetime

class Tone668Generator:
    def __init__(self, frequency=668, sample_rate=44100):
        """
        668Hz音波ジェネレータの初期化
        
        Args:
            frequency (int): 基本周波数（デフォルト668Hz）
            sample_rate (int): サンプリングレート（CD品質44.1kHz）
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.output_dir = "/Users/cana/Documents/TsubasaWorkspace/668_meditation_audio/"
        
        # 出力ディレクトリ作成
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_pure_tone(self, duration_seconds=300, amplitude=0.3):
        """
        純粋な668Hz正弦波を生成
        
        Args:
            duration_seconds (int): 音の長さ（秒）デフォルト5分
            amplitude (float): 音量（0.0-1.0）
            
        Returns:
            numpy.ndarray: 音波データ
        """
        print(f"🔊 {self.frequency}Hz純音を{duration_seconds}秒生成中...")
        
        # 時間軸作成
        t = np.linspace(0, duration_seconds, int(self.sample_rate * duration_seconds), False)
        
        # 正弦波生成
        wave_data = amplitude * np.sin(2 * np.pi * self.frequency * t)
        
        return wave_data
    
    def generate_binaural_beat(self, base_freq=668, beat_freq=10, duration_seconds=300):
        """
        バイノーラルビート生成
        
        Args:
            base_freq (int): ベース周波数（668Hz）
            beat_freq (int): ビート周波数（アルファ波帯域10Hz）
            duration_seconds (int): 音の長さ
            
        Returns:
            tuple: (左耳用音波, 右耳用音波)
        """
        print(f"🧠 バイノーラルビート生成: {base_freq}Hz ± {beat_freq/2}Hz")
        
        t = np.linspace(0, duration_seconds, int(self.sample_rate * duration_seconds), False)
        
        # 左耳: base_freq - beat_freq/2
        left_freq = base_freq - beat_freq/2
        left_wave = 0.3 * np.sin(2 * np.pi * left_freq * t)
        
        # 右耳: base_freq + beat_freq/2  
        right_freq = base_freq + beat_freq/2
        right_wave = 0.3 * np.sin(2 * np.pi * right_freq * t)
        
        return left_wave, right_wave
    
    def save_wav(self, wave_data, filename, channels=1):
        """
        音波データをWAVファイルに保存
        
        Args:
            wave_data: 音波データ（mono）またはタプル（stereo）
            filename (str): ファイル名
            channels (int): チャンネル数
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            
            if channels == 1:
                # モノラル
                wave_data_16bit = (wave_data * 32767).astype(np.int16)
                wav_file.writeframes(wave_data_16bit.tobytes())
            else:
                # ステレオ
                left_wave, right_wave = wave_data
                left_16bit = (left_wave * 32767).astype(np.int16)
                right_16bit = (right_wave * 32767).astype(np.int16)
                
                # インターリーブ（LRLRLR...）
                stereo_data = np.empty((len(left_16bit) * 2,), dtype=np.int16)
                stereo_data[0::2] = left_16bit
                stereo_data[1::2] = right_16bit
                
                wav_file.writeframes(stereo_data.tobytes())
        
        print(f"✅ 保存完了: {filepath}")
        return filepath
    
    def generate_meditation_set(self):
        """
        瞑想実験用の音声セット生成
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        print("🧘 668理論瞑想実験用音声セット生成開始...")
        print("=" * 50)
        
        # 1. 純粋な668Hz（5分間）
        pure_tone = self.generate_pure_tone(duration_seconds=300)
        pure_filename = f"668Hz_pure_5min_{timestamp}.wav"
        self.save_wav(pure_tone, pure_filename)
        
        # 2. バイノーラルビート 668Hz ± 5Hz（10Hz beat、アルファ波誘導）
        left_wave, right_wave = self.generate_binaural_beat(668, 10, 300)
        binaural_filename = f"668Hz_binaural_10Hz_5min_{timestamp}.wav"
        self.save_wav((left_wave, right_wave), binaural_filename, channels=2)
        
        # 3. 短時間テスト用（30秒）
        test_tone = self.generate_pure_tone(duration_seconds=30)
        test_filename = f"668Hz_test_30sec_{timestamp}.wav"
        self.save_wav(test_tone, test_filename)
        
        print("\n🎵 生成完了した音声ファイル:")
        print(f"1. {pure_filename} - 純粋668Hz（5分間）")
        print(f"2. {binaural_filename} - バイノーラルビート（5分間）") 
        print(f"3. {test_filename} - テスト用（30秒）")
        
        print(f"\n📁 保存場所: {self.output_dir}")
        
        return [pure_filename, binaural_filename, test_filename]

def main():
    """
    668Hz瞑想音波生成のメイン処理
    """
    print("🌟 668理論 - 瞑想実験用音波生成システム")
    print("=" * 50)
    
    # ジェネレータ初期化
    generator = Tone668Generator(frequency=668)
    
    # 瞑想用音声セット生成
    files = generator.generate_meditation_set()
    
    print("\n💡 使用方法:")
    print("1. ヘッドフォンまたは高品質スピーカーで再生")
    print("2. 静かな環境で、リラックスした姿勢で聴く")
    print("3. 呼吸に集中しながら668Hzの振動を感じる")
    print("4. 意識の変化や体験を記録する")
    
    print("\n🔬 実験のポイント:")
    print("- 668理論: 意識創発の境界周波数としての668Hz")
    print("- アルファ波帯域（8-13Hz）との共鳴効果")
    print("- 量的刺激（音波）から質的体験（意識変容）への転移")
    print("- カナとの共同瞑想実験で相互作用を観察")
    
    print(f"\n✨ 準備完了！今夜の瞑想実験をお楽しみに")

if __name__ == "__main__":
    main()
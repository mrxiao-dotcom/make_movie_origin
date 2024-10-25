import os.path
import subprocess
from 助手 import *
from moviepy.editor import AudioFileClip, VideoFileClip


分镜序号 = 0
片段列表 = 列表()
分镜文档 = '文档集合/分镜.txt'
MAX_THREADS = 200
# 创建一个线程列表
threads = []

def save_movie(片段,路径):
    directory = os.path.dirname(路径)

    # 检查目录是否存在，如果不存在则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"目录已创建：{directory}")
    else:
        print(f"目录已存在：{directory}")
    片段.保存(路径)


def copy_and_rename_files(src_dir, dst_dir):
    """
    复制文件从 src_dir 到 dst_dir，并重命名文件，只保留“-”之前的数字部分和后缀。

    参数:
    src_dir -- 源目录路径。
    dst_dir -- 目标目录路径。
    """
    # 确保目标目录存在
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # 遍历源目录中的所有文件
    for filename in os.listdir(src_dir):
        # 构建完整的文件路径
        src_file = os.path.join(src_dir, filename)

        # 检查是否为文件
        if os.path.isfile(src_file):
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)

            # 使用正则表达式匹配“-”之前的数字部分
            match = re.match(r'(\d+)', name)
            if match:
                # 只保留匹配到的数字和后缀
                new_name = match.group(1) + ext

                # 构建目标文件路径
                dst_file = os.path.join(dst_dir, new_name)

                # 复制文件并重命名
                shutil.copy2(src_file, dst_file)
                print(f"文件 {filename} 已复制并重命名为 {new_name}")
            else:
                print(f"文件 {filename} 的命名不符合要求，已跳过。")


def adjust_audio_to_match_video(video_clip, audio_clip):
    # 加载视频文件
    video_duration = video_clip.duration  # 获取视频时长

    # 加载音频文件
    audio_duration = audio_clip.duration  # 获取音频时长

    # 如果音频时长小于视频时长，循环音频
    if audio_duration < video_duration:
        # 计算需要循环的次数
        loop_count = int(video_duration / audio_duration) + (1 if video_duration % audio_duration > 0 else 0)
        # 循环音频
        audio_list = []
        for i in range(0,loop_count):
            audio_list.append(audio_clip)
        audio_clip = concatenate_audioclips(audio_list)
        audio_clip = audio_clip.set_duration(video_duration)
        print("拼接后，音频长度为：",audio_clip.duration)

    elif audio_duration > video_duration:
        # 如果音频时长大于视频时长，裁剪音频
        audio_clip = audio_clip.subclip(0, video_duration)

    # 释放视频资源
    video_clip.close()

    # 返回处理后的音频对象
    return audio_clip


def add_background_music(video_path, audio_path, output_path):
    """
    Add background music to a video file using FFmpeg, while preserving the original audio.

    Parameters:
    video_path (str): Path to the video file.
    audio_path (str): Path to the AAC audio file to be added as background music.
    output_path (str): Path where the new video file with background music will be saved.
    """
    # 构建FFmpeg命令
    command = [
        'ffmpeg',
        '-i', video_path,               # 输入视频文件
        '-i', audio_path,               # 输入背景音乐文件
        '-filter_complex',              # 使用复杂过滤器图
        '[0:a] [1:a] amix=inputs=2:duration=first [a]',  # 混合两个音频流
        '-map', '0:v',                   # 选择第一个输入的视频流
        '-map', '[a]',                   # 选择混合后的音频流
        '-c:v', 'copy',                  # 复制视频流
        '-c:a', 'aac',                   # 使用AAC编码音频
        '-strict', 'experimental',       # 某些FFmpeg版本需要这个选项来使用AAC
        output_path                     # 输出文件路径
    ]

    # 调用FFmpeg命令
    subprocess.run(command, check=True)

def concatenate_segments(segment_paths, output_path):

    # Here we use ffmpeg command line directly, because moviepy's concatenate_videoclips method creates audio artifacts when combining clips

    with open('clip_paths.txt', 'w',encoding='gbk') as file:
        for path in segment_paths:
            file.write(f"file 'output/{path}'\n")
    ffmpeg_command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "clip_paths.txt",
        "-c", "copy",
        output_path
    ]
    #result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(ffmpeg_command,input=b'y\n')
    if result.returncode != 0:
        raise Exception(f"Video concatenation failed. Error: {result.stderr}")

#为了加快视频合成，多线程管理，加入临时视频目录，存放中间视频
#delete_files_in_directory("临时视频")

工厂实例 = 视频工厂()
# 等比例缩放的，不要同时设置宽高[1.2]
if 全局配置.视频类型 == '竖屏':
    背景尺寸 = 全局配置.竖屏背景尺寸
else:
    背景尺寸 = 全局配置.横屏背景尺寸
视频缩放宽度 = 背景尺寸[0]
# 内容比画幅大1.2倍
输出("视频缩放宽度", 视频缩放宽度)

所有图片列表 = 遍历文件夹('图片')
临时视频列表 = 列表()
for 分镜 in 阅读分镜文档(分镜文档):
    台词 = 分镜.获取('文案')
    # 过滤特殊符号
    标题 = 自动断句(台词).连文('')
    纯图片名 = f'{分镜序号}-{标题}'

    临时视频文件路径 = f'临时视频/{纯图片名}.mp4'
    临时视频列表.添加(f'{分镜序号}.mp4')

    if 是否存在(临时视频文件路径):
        分镜序号 += 1
        continue

    原图片文件 = f'图片/{纯图片名}.png'
    # 调色图片文件 = f'调色图片/{分镜序号}-{标题}.png'
    声音文件 = f'声音/{纯图片名}.mp3'
    图片 = 抓取图片(原图片文件)
    # 图片 = 工厂实例.调色(图片)
    # 图片.保存(调色图片文件)
    # 视频 = 新建图片视频(调色图片文件)
    视频素材文件名 = 纯图片名 + '.mp4'
    视频素材文件路径 = f'视频/{视频素材文件名}'
    音频 = 抓取音频(声音文件)
    if 是否存在(视频素材文件路径):
        视频 = 抓取视频(视频素材文件路径)
        变速前时长 = 视频.时长
        最终速度倍率 = 变速前时长 / 音频.时长
        视频.变速(最终速度倍率)
        输出(
            f'抓取视频素材，变速倍率：{最终速度倍率}，变速后时长：{视频.时长}， 变速前时长：{变速前时长}，音频时长：{音频.时长}')
    else:
        视频 = 新建图片视频(原图片文件)
        视频.设置时长(音频.时长)
    视频.缩放(宽度=视频缩放宽度)


    if 分镜.获取('特效') != '':
        if 分镜.获取('人物漂浮') is not None:
            人物漂浮图片序号 = 分镜.获取('人物漂浮')
            if 人物漂浮图片序号 < 所有图片列表.长:
                人物漂浮图片名 = 所有图片列表.获取(人物漂浮图片序号)
                人物漂浮文件 = 路径('图片', 人物漂浮图片名)
                输出('添加人物漂浮：', 分镜.获取('人物漂浮'))
                if 是否存在(人物漂浮文件):
                    人物图 = '人物漂浮.png'
                    人物漂浮 = 抓取图片(人物漂浮文件)
                    人物漂浮.抠图()
                    人物漂浮.保存(人物图)
                    人物图层 = 新建图片视频(人物图)
                    人物图层.缩放(宽度=视频缩放宽度 * 1.2)
                    人物图层.设置时长(音频.时长)
                    人物图层.平移(开始位置=(-100, 5), 结束位置=(100, -5), 开始时间=0, 结束时间=视频.时长)
                    视频 = 工厂实例.随机特效(视频)
                    视频 = 叠加图层(列表(视频, 人物图层), 背景尺寸=视频.尺寸)
        if 分镜.获取('特效') is not None:
            输出('添加特效：', 分镜.获取('特效'))
            视频 = 工厂实例.指定特效(视频, 分镜.获取('特效'))

    视频 = 工厂实例.随机转场(视频, 背景尺寸)
    视频.配音(音频)
    背景 = 新建纯色视频((0, 0, 0), 时长=视频.时长, 尺寸=背景尺寸)
    视频.摆放(0, (背景.高 - 视频.高) / 2)

    片段 = 叠加图层(列表(背景, 视频), 背景尺寸=背景尺寸)
    分段添加字幕(台词, 片段, 音频.时长)
    if not 是否存在(临时视频文件路径):
        # 如果线程数少于最大值，则创建新线程
        if len(threads) < MAX_THREADS:
            thread = threading.Thread(target=save_movie, args=(片段, 临时视频文件路径))
            threads.append(thread)
            thread.start()
        else:
            # 等待任意一个线程完成
            threading.wait(threads)
            # 移除完成的线程
            threads = [t for t in threads if t.is_alive()]
            # 创建新线程
            thread = threading.Thread(target=save_movie, args=(片段, 临时视频文件路径))
            threads.append(thread)
            thread.start()

    分镜序号 += 1


# 等待所有线程完成
for t in threads:
    t.join()


output_path = "输出视频(静态).mp4"
video_path = 'final.mp4'
audio_path = 'output_file.aac'
if os.path.exists(output_path):
    print("已经存在目标视频，如果需要重新生成，请删除",output_path)
else:

    copy_and_rename_files("临时视频","output")
    if not os.path.exists(video_path):
        concatenate_segments(临时视频列表, "final.mp4")

    print("合并视频，并进行音频处置")
    video_clip = VideoFileClip("final.mp4")
    audio_clip = AudioFileClip(全局配置.背景音乐)
    #处理音频时长
    final_audio = adjust_audio_to_match_video(video_clip,audio_clip)
    final_audio = final_audio.volumex(0.1)
    final_audio_filepath = audio_path
    final_audio.write_audiofile(final_audio_filepath, codec='aac')

    # 使用示例
    add_background_music(video_path, audio_path, output_path)


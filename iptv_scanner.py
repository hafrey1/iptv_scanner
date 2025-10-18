import asyncio
import aiohttp
import re
import datetime
import requests
import eventlet
import os
import time
import threading
import json
from queue import Queue

eventlet.monkey_patch()

# 加载配置文件
def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到配置文件 {config_file}")
        input("按任意键退出...")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：配置文件格式错误 - {e}")
        input("按任意键退出...")
        exit(1)

# 全局配置
config = load_config()
urls = config['scan_urls']
scan_settings = config['scan_settings']
output_settings = config['output_settings']
name_replacements = config['name_replacements']

async def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)
    return modified_urls

async def is_url_accessible(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=scan_settings['timeout']) as response:
                if response.status == 200:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{current_time} {url}")
                    return url
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
    return None

async def check_urls(session, urls, semaphore):
    tasks = []
    for url in urls:
        url = url.strip()
        modified_urls = await modify_urls(url)
        for modified_url in modified_urls:
            task = asyncio.create_task(is_url_accessible(session, modified_url, semaphore))
            tasks.append(task)
    results = await asyncio.gather(*tasks)
    valid_urls = [result for result in results if result]
    return valid_urls

async def fetch_json(session, url, semaphore):
    async with semaphore:
        try:
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"

            json_url = f"{url}"
            async with session.get(json_url, timeout=scan_settings['timeout']) as response:
                json_data = await response.json()
                results = []
                try:
                    for item in json_data['data']:
                        if isinstance(item, dict):
                            name = item.get('name')
                            urlx = item.get('url')
                            if ',' in urlx:
                                urlx = "aaaaaaaa"
                            if 'http' in urlx:
                                urld = f"{urlx}"
                            else:
                                urld = f"{url_x}{urlx}"

                            if name and urlx:
                                # 应用名称替换规则
                                for old, new in name_replacements.items():
                                    name = name.replace(old, new)
                                
                                # 应用正则替换和特定规则
                                name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                                name = name.replace("CCTV1综合", "CCTV1")
                                name = name.replace("CCTV2财经", "CCTV2")
                                name = name.replace("CCTV3综艺", "CCTV3")
                                name = name.replace("CCTV4国际", "CCTV4")
                                name = name.replace("CCTV4中文国际", "CCTV4")
                                name = name.replace("CCTV4欧洲", "CCTV4")
                                name = name.replace("CCTV5体育", "CCTV5")
                                name = name.replace("CCTV6电影", "CCTV6")
                                name = name.replace("CCTV7军事", "CCTV7")
                                name = name.replace("CCTV7军农", "CCTV7")
                                name = name.replace("CCTV7农业", "CCTV7")
                                name = name.replace("CCTV7国防军事", "CCTV7")
                                name = name.replace("CCTV8电视剧", "CCTV8")
                                name = name.replace("CCTV9记录", "CCTV9")
                                name = name.replace("CCTV9纪录", "CCTV9")
                                name = name.replace("CCTV10科教", "CCTV10")
                                name = name.replace("CCTV11戏曲", "CCTV11")
                                name = name.replace("CCTV12社会与法", "CCTV12")
                                name = name.replace("CCTV13新闻", "CCTV13")
                                name = name.replace("CCTV新闻", "CCTV13")
                                name = name.replace("CCTV14少儿", "CCTV14")
                                name = name.replace("CCTV15音乐", "CCTV15")
                                name = name.replace("CCTV16奥林匹克", "CCTV16")
                                name = name.replace("CCTV17农业农村", "CCTV17")
                                name = name.replace("CCTV17农业", "CCTV17")
                                name = name.replace("CCTV5+体育赛视", "CCTV5+")
                                name = name.replace("CCTV5+体育赛事", "CCTV5+")
                                name = name.replace("CCTV5+体育", "CCTV5+")
                                results.append(f"{name},{urld}")
                except Exception:
                    pass
                return results
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            return []

async def scan_channels():
    x_urls = []
    for url in urls:
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    unique_urls = set(x_urls)

    semaphore = asyncio.Semaphore(scan_settings['max_concurrent'])
    async with aiohttp.ClientSession() as session:
        valid_urls = await check_urls(session, unique_urls, semaphore)
        all_results = []
        tasks = []
        for url in valid_urls:
            task = asyncio.create_task(fetch_json(session, url, semaphore))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for sublist in results:
            all_results.extend(sublist)
    
    return all_results

# 测速相关代码
task_queue = eventlet.Queue()
results = []
error_channels = []
all_results = []

def worker():
    while True:
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])
            lines = requests.get(channel_url, timeout=2).text.strip().split('\n')
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]

            if not ts_lists:
                raise Exception("No TS files found")

            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])
            ts_count = min(scan_settings['download_segments'], len(ts_lists))
            total_size = 0

            with eventlet.Timeout(scan_settings['test_timeout'], False):
                start_time = datetime.datetime.now().timestamp()

                for i in range(ts_count):
                    ts_url = channel_url_t + ts_lists[i]
                    content = requests.get(ts_url, timeout=2).content
                    total_size += len(content)

                    if i == 0:
                        with open(ts_lists_0, 'ab') as f:
                            f.write(content)

                end_time = datetime.datetime.now().timestamp()
                response_time = end_time - start_time

                if total_size > 0 and response_time > 0:
                    download_speed = total_size / response_time / 1024
                    normalized_speed = min(download_speed / 1024, 100)

                    if os.path.exists(ts_lists_0):
                        os.remove(ts_lists_0)

                    result = channel_name, channel_url, f"{normalized_speed:.4f} MB/s"
                    results.append(result)
                    numberx = (len(results) + len(error_channels)) / len(all_results) * 100
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{current_time} 可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(all_results)} 个 , 总进度：{numberx:.2f}% - {channel_name}: {normalized_speed:.4f} MB/s")
                else:
                    raise Exception("Invalid size or time")

        except Exception as e:
            try:
                if 'ts_lists_0' in locals() and os.path.exists(ts_lists_0):
                    os.remove(ts_lists_0)
            except:
                pass

            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(all_results) * 100
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} 可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(all_results)} 个 , 总进度：{numberx:.2f}%")

        task_queue.task_done()

def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')

def test_and_save():
    global all_results
    
    num_workers = scan_settings['worker_threads']
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    for result in all_results:
        channel_name, channel_url = result.split(',')
        task_queue.put((channel_name, channel_url))

    task_queue.join()

    # 排序
    results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
    results.sort(key=lambda x: channel_key(x[0]))

    # 保存速度结果
    with open(output_settings['speed_file'], 'w', encoding='utf-8') as file:
        for result in results:
            file.write(f"{result[0]},{result[1]},{result[2]}\n")

    result_counter = output_settings['results_per_channel']

    # 生成 txt 格式
    with open(output_settings['txt_file'], 'w', encoding='utf-8') as file:
        channel_counters = {}
        file.write('央视频道,#genre#\n')
        for result in results:
            channel_name, channel_url, speed = result
            if 'CCTV' in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1
        
        channel_counters = {}
        file.write('卫视频道,#genre#\n')
        for result in results:
            channel_name, channel_url, speed = result
            if '卫视' in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1
        
        channel_counters = {}
        file.write('其他频道,#genre#\n')
        for result in results:
            channel_name, channel_url, speed = result
            if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1

    # 生成 m3u 格式
    with open(output_settings['m3u_file'], 'w', encoding='utf-8') as file:
        channel_counters = {}
        file.write('#EXTM3U\n')
        for result in results:
            channel_name, channel_url, speed = result
            if 'CCTV' in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f'#EXTINF:-1 group-title="央视频道",{channel_name}\n')
                        file.write(f"{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f'#EXTINF:-1 group-title="央视频道",{channel_name}\n')
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] = 1
        
        channel_counters = {}
        for result in results:
            channel_name, channel_url, speed = result
            if '卫视' in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f'#EXTINF:-1 group-title="卫视频道",{channel_name}\n')
                        file.write(f"{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f'#EXTINF:-1 group-title="卫视频道",{channel_name}\n')
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] = 1
        
        channel_counters = {}
        for result in results:
            channel_name, channel_url, speed = result
            if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f'#EXTINF:-1 group-title="其他频道",{channel_name}\n')
                        file.write(f"{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f'#EXTINF:-1 group-title="其他频道",{channel_name}\n')
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] = 1

def main():
    global all_results
    
    print("=" * 60)
    print("IPTV 频道扫描和测速工具")
    print("=" * 60)
    print(f"加载配置文件成功，共 {len(urls)} 个扫描地址")
    print("=" * 60)
    
    print("\n第一阶段：扫描频道...")
    all_results = asyncio.run(scan_channels())
    print(f"\n扫描完成！找到 {len(all_results)} 个频道")
    
    if len(all_results) == 0:
        print("未找到任何频道，程序退出")
        input("按任意键退出...")
        return
    
    print("\n第二阶段：测速和生成播放列表...")
    test_and_save()
    
    print("\n" + "=" * 60)
    print("任务完成！")
    print(f"可用频道数：{len(results)}")
    print(f"生成文件：")
    print(f"  - {output_settings['speed_file']}")
    print(f"  - {output_settings['txt_file']}")
    print(f"  - {output_settings['m3u_file']}")
    print("=" * 60)
    input("\n按任意键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序")
        input("按任意键退出...")
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
        input("按任意键退出...")

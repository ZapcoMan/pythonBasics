import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class PhoneNumberChecker:
    def __init__(self, api_url="https://sucyan.top/api/privacy.php", max_workers=5):
        self.api_url = api_url
        self.max_workers = max_workers
        self.lock = threading.Lock()
        self.results = []

    def check_phone(self, phone):
        try:
            params = {
                'value': str(phone).strip()
            }

            response = requests.get(self.api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'phone': phone,
                    'status': data.get('status', 'unknown'),
                    'message': data.get('message', ''),
                    'raw_data': data
                }
            else:
                return {
                    'phone': phone,
                    'status': 'error',
                    'message': f'HTTP {response.status_code}',
                    'raw_data': None
                }

        except requests.RequestException as e:
            return {
                'phone': phone,
                'status': 'error',
                'message': str(e),
                'raw_data': None
            }
        except json.JSONDecodeError:
            return {
                'phone': phone,
                'status': 'error',
                'message': 'Invalid JSON response',
                'raw_data': None
            }

    def read_phones_from_file(self, file_path):
        phones = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    phone = line.strip()
                    if phone and phone.isdigit() and len(phone) == 11:
                        phones.append(phone)
                    elif phone:
                        print(f"警告: 跳过无效手机号: {phone}")
        except FileNotFoundError:
            print(f"错误: 文件 {file_path} 不存在")
            return []
        except Exception as e:
            print(f"读取文件错误: {e}")
            return []

        return phones

    def check_phones_batch(self, phones):
        print(f"开始检测 {len(phones)} 个手机号...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_phone = {executor.submit(self.check_phone, phone): phone for phone in phones}

            completed = 0
            for future in as_completed(future_to_phone):
                completed += 1
                result = future.result()

                with self.lock:
                    self.results.append(result)

                if completed % 10 == 0 or completed == len(phones):
                    print(f"进度: {completed}/{len(phones)} ({completed / len(phones) * 100:.1f}%)")

                time.sleep(0.1)

        return self.results

    def save_results(self, output_file):
        try:
            active_count = sum(1 for r in self.results if r.get('status') == 'active')
            inactive_count = sum(1 for r in self.results if r.get('status') == 'inactive')
            unknown_count = sum(1 for r in self.results if r.get('status') == 'unknown')
            error_count = sum(1 for r in self.results if r.get('status') == 'error')

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 手机号检测结果统计\n")
                f.write(f"# 总计: {len(self.results)} 个\n")
                f.write(f"# 活跃: {active_count} 个\n")
                f.write(f"# 非活跃: {inactive_count} 个\n")
                f.write(f"# 未知: {unknown_count} 个\n")
                f.write(f"# 错误: {error_count} 个\n")
                f.write("\n")

                f.write("手机号\t状态\t消息\n")
                for result in self.results:
                    f.write(f"{result['phone']}\t{result['status']}\t{result['message']}\n")

            print(f"\n结果已保存到: {output_file}")
            print(
                f"统计: 总计{len(self.results)} | 活跃{active_count} | 非活跃{inactive_count} | 未知{unknown_count} | 错误{error_count}")

        except Exception as e:
            print(f"保存结果错误: {e}")

    def print_summary(self):
        if not self.results:
            print("没有检测结果")
            return

        active = [r for r in self.results if r.get('status') == 'active']
        inactive = [r for r in self.results if r.get('status') == 'inactive']
        unknown = [r for r in self.results if r.get('status') == 'unknown']
        errors = [r for r in self.results if r.get('status') == 'error']

        print("\n" + "=" * 50)
        print("检测结果摘要:")
        print(f"  活跃手机号: {len(active)}")
        print(f"  非活跃手机号: {len(inactive)}")
        print(f"  状态未知: {len(unknown)}")
        print(f"  检测错误: {len(errors)}")
        print("=" * 50)

        if active:
            print("\n活跃手机号列表:")
            for r in active[:10]:
                print(f"  {r['phone']} - {r['message']}")
            if len(active) > 10:
                print(f"  ... 还有 {len(active) - 10} 个")

        if inactive:
            print("\n非活跃手机号列表:")
            for r in inactive[:10]:
                print(f"  {r['phone']} - {r['message']}")
            if len(inactive) > 10:
                print(f"  ... 还有 {len(inactive) - 10} 个")


def main():
    import sys

    print("手机号空号检测工具")
    print("=" * 50)

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("请输入手机号文件路径: ").strip()

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        default_output = "phone_check_results.txt"
        output_file = input(f"请输入输出文件路径 (默认: {default_output}): ").strip()
        if not output_file:
            output_file = default_output

    checker = PhoneNumberChecker(max_workers=3)

    print(f"\n读取文件: {input_file}")
    phones = checker.read_phones_from_file(input_file)

    if not phones:
        print("没有找到有效的手机号")
        return

    print(f"找到 {len(phones)} 个有效手机号")

    confirm = input("\n是否开始检测? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return

    start_time = time.time()
    results = checker.check_phones_batch(phones)
    end_time = time.time()

    checker.save_results(output_file)
    checker.print_summary()

    print(f"\n总耗时: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    main()

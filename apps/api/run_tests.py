#!/usr/bin/env python3
"""
テスト実行スクリプト
"""
import subprocess
import sys
import os

def run_tests():
    """テストを実行"""
    # テストディレクトリに移動
    test_dir = os.path.join(os.path.dirname(__file__), "test")
    os.chdir(test_dir)
    
    # pytestを実行
    cmd = ["python", "-m", "pytest", "-v"]
    
    # コマンドライン引数があれば追加
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode

if __name__ == "__main__":
    sys.exit(run_tests())

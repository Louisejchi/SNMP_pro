import os
import time
import re
import shutil

# 近一個月內未使用
unused_threshold = 30 * 24 * 60 * 60

current_time = time.time()
# regex
file_pattern = r'\.(txt|o|c|py|l|y|h|cpp|out|xlsx)$|^[\w-]+$'
exclude_folder_pattern = r'^\..*|^lib$|^bin$|^obj$'

# 建議刪除的檔案/資料夾
deletion_candidates = []

def show_disk_free_space(folder):
    total, used, free = shutil.disk_usage(folder)
    print(f"Total dick space: {total} bytes")
    print(f"Used dick space: {used} bytes")
    print(f"Free dick space: {free} bytes")

for foldername, subfolders, filenames in os.walk('/home/lulu'):
    # 利用 regex 過濾特定資料夾
    subfolders[:] = [d for d in subfolders if not re.search(exclude_folder_pattern, d)]
    # 檢查空白資料夾
    if not os.listdir(foldername):
        deletion_candidates.append(foldername)
        continue
    for filename in filenames:
        # 檢查空白檔案
        if os.path.getsize(os.path.join(foldername, filename)) == 0:
            deletion_candidates.append(os.path.join(foldername, filename))
            continue
        # 過濾
        if re.search(file_pattern, filename):
            file_path = os.path.join(foldername, filename)
            # 檔案最後修改時間
            last_modified_time = os.path.getmtime(file_path)
            # 如果檔案長時間未使用，則建議刪除
            if current_time - last_modified_time > unused_threshold:
                deletion_candidates.append(file_path)

# 顯示所有建議刪除的檔案和資料夾
for index, candidate in enumerate(deletion_candidates, 1):
    print(f"<{index}> ：Suggested deletion {candidate}")

print('*' * 20)

remove_ask = input('Starting remove?Y/N :')
if remove_ask.upper() == 'Y' or remove_ask.upper() == 'YES':
    # 讓使用者選擇刪除
    user_input = input("Please enter the number to delete, or enter a range (for example: 1-5): ")
    if '-' in user_input:
        start, end = map(int, user_input.split('-'))
        for index in range(start, end + 1):
            os.remove(deletion_candidates[index - 1])
            print(f"Deleted：{deletion_candidates[index - 1]}")
    else:
        os.remove(deletion_candidates[int(user_input) - 1])
        print(f"Deleted：{deletion_candidates[int(user_input) - 1]}")
else:
    print('Finish')


show_disk_free_space('/home/lulu')

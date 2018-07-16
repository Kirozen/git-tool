from tqdm import tqdm

print('open file list...')
with open('file-list.txt') as raw_list:
    files = [x.strip().split('\t') for x in raw_list.readlines()]
    files = [(x[0], x[3]) for x in files]

print('folders filter...')
with open('folders-filter.txt') as folder_filter:
    folders = [x.strip() for x in folder_filter.readlines()]

print('filter...')
files_to_be_removed = [f for f in tqdm(files) if any((f[1].startswith(folder) for folder in folders))]

print('Write to ids.txt...')

with open('ids.txt', 'w') as ids_file:
    for fid in set([f[0] for f in files_to_be_removed]):
        ids_file.write(fid + '\n')

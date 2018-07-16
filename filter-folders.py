with open('folders.txt') as original:
    original_folders = [x.strip() for x in original.readlines()]

with open('folders-clean.txt') as clean:
    clean_folders = set([x.strip() for x in clean.readlines()])

with open('folders-filter.txt', 'w') as filtered:
    filtered.write('\n'.join([line for line in original_folders if line not in clean_folders]))

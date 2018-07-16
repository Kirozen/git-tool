folders = set()
with open('E:\\temp\\svn-repos\\Global-git\\file-list.txt', 'r', encoding='utf-8') as filelist:
    for line in filelist:
        folder = line.split('\t')[-1]
        folder = folder[:folder.rfind('/')]
        folders.add(folder + '\n')
with open('E:\\temp\\svn-repos\\Global-git\\folders.txt', 'w', encoding='utf-8') as folder:
    for e in sorted(folders):
        folder.write(e)

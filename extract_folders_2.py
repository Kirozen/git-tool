folders = set()
with open('E:\\temp\\svn-repos\\Global-git - Copie\\dirs.txt', 'r', encoding='utf-8') as filelist:
    for line in filelist:
        # line = line.strip('\n')
        folder = line[:line.rfind('/')]
        folders.add(folder + '\n')
with open('E:\\temp\\svn-repos\\Global-git - Copie\\folders.txt', 'w', encoding='utf-8') as folder:
    for e in sorted(folders):
        folder.write(e)

extensions = set()
with open('E:\\temp\\svn-repos\\Global-git\\file-list.txt', 'r', encoding='utf-8') as filelist:
    for line in filelist:
        data = line.split('\t')[-1]
        index = data.rfind('.')
        if index >= 0:
            extensions.add(data[index + 1:])
with open('E:\\temp\\svn-repos\\Global-git\\extensions.txt', 'w') as extension:
    for e in sorted(extensions):
        extension.write(e)

from collections import namedtuple
from operator import attrgetter
import argparse

import git
from tqdm import tqdm
import humanfriendly as hf

GitFile = namedtuple('GitFile', ['name', 'size', 'hash'])


def main(human, number, repo):
    g = git.cmd.Git(repo)
    print('Get list of blobs...')
    try:
        hashes = g.rev_list(all=True).split()
    except git.GitCommandError:
        print('%s is not a valid git repository' % repo)
        return
    print('%d blobs retrieved' % (len(hashes)))
    print('Compute list of files...')
    files = set()
    for sha1 in tqdm(hashes):
        raw_files = g.ls_tree(sha1, r=True, l=True).split('\n')
        for rf in raw_files:
            data = rf.split()
            if data[1] == 'blob':
                files.add(GitFile(name=data[4], size=int(data[3]), hash=data[2]))
    print('%d files retrieved' % (len(files)))
    if number == 0:
        number = len(files)
    print()
    print()
    print('Sort and print %d biggest files :' % (number if number < len(files) else len(files)))
    print()
    if human:
        printer = lambda x: hf.format_size(x, binary=True)
    else:
        printer = str
    for f in sorted(list(files), key=attrgetter('size'), reverse=True)[:number]:
        print('%s\t%s\t\t%s' % (f.hash, printer(f.size), f.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract list of files from git repository')
    parser.add_argument('-H', action='store_true', help='human readable size')
    parser.add_argument('-n', default=10, type=int, help='number of files to print (0 prints complete list)')
    parser.add_argument('repo', help='git repository')
    args = parser.parse_args()
    main(human=args.H, number=args.n, repo=args.repo)

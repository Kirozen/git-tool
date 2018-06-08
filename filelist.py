from collections import namedtuple
from operator import attrgetter
import argparse

import git
from tqdm import tqdm
import humanfriendly as hf

GitFile = namedtuple('GitFile', ['name', 'size', 'hash'])


def get_all_blobs(tree):
    blobs = list(tree.blobs)
    for t in tree.trees:
        blobs.extend(get_all_blobs(t))
    return blobs


def main(human, number, repo):
    g = git.Repo(repo)
    print('Get list of commits...')
    count = len(tuple(g.iter_commits()))
    commits = g.iter_commits()
    print('%d commits retrieved' % count)
    print('Compute list of files...')
    files = set()
    for commit in tqdm(commits, total=count):
        blobs = get_all_blobs(commit.tree)
        for blob in blobs:
            files.add(GitFile(name=blob.path, size=blob.size, hash=blob.hexsha))
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

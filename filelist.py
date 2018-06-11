import argparse
import sys
from operator import attrgetter

import git
import humanfriendly as hf
from tqdm import tqdm


def main(human, number, repo, output):
    g = git.Repo(repo)

    print('Get list of commits...')
    count = len(tuple(g.iter_commits()))
    commits = g.iter_commits()
    print('%d commits retrieved' % count)

    print('Compute list of files...')
    files = {item for commit in tqdm(commits, total=count) for item in commit.tree.traverse() if item.type == 'blob'}
    print('%d files retrieved' % (len(files)))
    if number == 0:
        number = len(files)

    print()
    print()
    print('Sort and print %d biggest files...' % (number if number < len(files) else len(files)))
    print()

    if human:
        formatter = lambda x: hf.format_size(x, binary=True)
    else:
        formatter = str

    if output:
        printer = output
    else:
        printer = sys.stdout

    for f in sorted(files, key=attrgetter('size'), reverse=True)[:number]:
        print('%s\t%s\t\t%s' % (f.hexsha, formatter(f.size), f.path), file=printer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract list of files from git repository')
    parser.add_argument('-H', action='store_true', help='human readable size')
    parser.add_argument('-o', metavar='file.out', type=argparse.FileType('w', encoding='UTF-8'), help='output file')
    parser.add_argument('-n', default=10, type=int, help='number of files to print (0 prints complete list)')
    parser.add_argument('repo', help='git repository')
    args = parser.parse_args()
    import time
    start = time.time()
    main(human=args.H, number=args.n, repo=args.repo, output=args.o)
    print('---Done in %fs---' % (time.time() - start))

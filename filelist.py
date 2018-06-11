from operator import attrgetter
import argparse

import git
from tqdm import tqdm
import humanfriendly as hf


def main(human, number, repo):
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
    print('Sort and print %d biggest files :' % (number if number < len(files) else len(files)))
    print()
    if human:
        printer = lambda x: hf.format_size(x, binary=True)
    else:
        printer = str
    for f in sorted(files, key=attrgetter('size'), reverse=True)[:number]:
        print('%s\t%s\t\t%s' % (f.hexsha, printer(f.size), f.path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract list of files from git repository')
    parser.add_argument('-H', action='store_true', help='human readable size')
    parser.add_argument('-n', default=10, type=int, help='number of files to print (0 prints complete list)')
    parser.add_argument('repo', help='git repository')
    args = parser.parse_args()
    main(human=args.H, number=args.n, repo=args.repo)

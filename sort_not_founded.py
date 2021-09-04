from os.path import dirname, realpath, exists, join

thispath = dirname(realpath(__file__))
fname = join(thispath, 'not_founded_vk_songs.txt')
if exists(fname):
	with open(fname, 'r', encoding='utf-8') as f:
		l = sorted([line[:-1] for line in f.readlines() if line[-1] == '\n'])

with open(join(thispath, 'sorted_not_founded_vk_songs.txt'), 'w', encoding='utf-8') as f:
	for line in l:
		f.write(line + '\n')

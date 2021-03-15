project('main', 'cpp', default_options : ['buildtype=release', 'cpp_std=c++2a', 'warning_level=3', 'werror=true'])
src = 'main/main.cpp'
dep = [dependency('eigen3')]
e = executable('main', sources: src, dependencies: dep)

meth_e = find_program('scripts' / 'methods.py')
gen_e = find_program('scripts' / 'gen-work.py')
stat_e = find_program('scripts' / 'stat.py')
env = environment()
env.set('BASE_DIR', '.')
#env.set('CORES', '12')
#env.set('RUNS', '10')
path_e = '.:/usr/bin'
env.set('PATH', path_e)
gen_json = custom_target('gen-work', output: 'work.json', command: gen_e)
run_target('stats', command: stat_e)
# Run like: PATH=.:$PATH meson compile methods
run_target('methods', command: meth_e, depends: gen_json, env: env)
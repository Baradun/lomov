project('main', 'cpp', default_options : ['buildtype=release', 'cpp_std=c++2a', 'warning_level=3', 'werror=true'])
src = 'main/main.cpp'
dep = [dependency('eigen3')]
e = executable('main', sources: src, dependencies: dep)

meth_e = find_program('scripts' / 'methods.py')
gen_e = find_program('scripts' / 'gen-work.py')
stat_e = find_program('scripts' / 'stat.py')
env = environment()
env.set('BASE_DIR', '.')
env.set('CORES', '2')
env.set('RUNS', '5')
run_target('gen-work', command: gen_e)
run_target('stats', command: stat_e)
# run_target('methods', command: meth_e, env: env)
run_target('methods', command: meth_e, depends: ['gen-work'], env: env)

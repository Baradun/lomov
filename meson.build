project('main', 'cpp', default_options : ['buildtype=release', 'cpp_std=c++2a', 'warning_level=3', 'werror=true'])
src = 'main/main.cpp'
dep = [dependency('eigen3')]
e = executable('main', sources: src, dependencies: dep)

+p_e = '@SOURCE_ROOT@/scripts/methods.py'
env = environment()
env.set('BASE_DIR', '.')
env.set('CORES', '2')
env.set('RUNS', '5')
run_target('methods', command: [ p_e ], env: env)
